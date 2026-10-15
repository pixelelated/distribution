#!/usr/bin/env python3
"""UNRUN #571 fixture. Requires a coordinator runtime lease and installed Playwright.

No broker import, listener, device, account, or provider. Browser requests are
denied except the synthetic document; fetch and polling time are deterministic.
"""
import argparse
import ast
import hashlib
import html
import importlib.metadata
import json
import platform
from pathlib import Path

HERE = Path('/workspace/repos/rocknix.worktrees/m7-player-setup/docs/qa-logs/2026-10-13-phone-locale-source')
ROOT = HERE.parents[2]
SOURCE = ROOT / "projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth"
ORIGIN = "http://phone.invalid/1234"
NAME = 'Synthetic Keyboard for Checking connection & "quoted" <text> ' * 4

MOCK = r"""
(() => {
  const qa = window.qa = {pending: [], timers: [], posts: [], unexpected: [], hold: []};
  window.setTimeout = (fn, ms) => {
    if (ms !== 2000) throw new Error("unexpected timer " + ms);
    qa.timers.push(fn); return qa.timers.length;
  };
  window.fetch = (url, options = {}) => {
    if (url === "/1234?probe=1" && !options.method) {
      return new Promise((resolve, reject) => qa.pending.push({resolve, reject}));
    }
    if (url === "/1234" && options.method === "POST") {
      const body = new URLSearchParams(options.body);
      if (body.get("pin") !== "1234") throw new Error("wrong synthetic PIN");
      qa.posts.push(options.body);
      if (qa.holdPosts) return new Promise(resolve => qa.hold.push(resolve));
      return Promise.resolve(new Response(null, {status: 204}));
    }
    qa.unexpected.push(String(url));
    return Promise.reject(new Error("network denied"));
  };
  qa.answer = ({text, status, fail}) => {
    if (qa.pending.length !== 1) throw new Error("expected one pending probe");
    const p = qa.pending.shift();
    if (fail) p.reject(new Error("synthetic unreachable"));
    else p.resolve(new Response(text, {status}));
  };
  qa.tick = () => {
    if (qa.timers.length !== 1) throw new Error("expected one poll timer");
    qa.timers.shift()();
  };
  qa.flush = async () => { for (let i = 0; i < 100; ++i) await Promise.resolve(); };
})();
"""


def render(language):
    """Run only the exact phone_page function with literal templates and fake locale.

    This is deferred runtime, never importing cloud_oauth or its broker globals.
    """
    raw = SOURCE.read_bytes()
    binding = json.loads((HERE / "source.json").read_text())
    assert hashlib.sha256(raw).hexdigest() == binding["candidate_sha256"]
    tree = ast.parse(raw)
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            name = getattr(node.targets[0], "id", "")
            if name in ("STYLE", "REMOTE_PAGE"):
                constants[name] = ast.literal_eval(node.value)
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == "phone_page")
    env = dict(constants, html=html, signin_language=lambda: language)
    exec(compile(ast.Module(body=[function], type_ignores=[]),
                 "source-bound-phone_page", "exec"), env)
    return env["phone_page"](NAME, "1234")


def run_case(browser, language, width, output):
    from playwright.sync_api import expect

    context = browser.new_context(viewport={"width": width, "height": 800},
                                  has_touch=True, service_workers="block", offline=True)
    unexpected = []
    document = render(language)

    def deny_or_document(route):
        request = route.request
        if request.url == ORIGIN and request.method == "GET" and request.is_navigation_request():
            route.fulfill(status=200, content_type="text/html; charset=utf-8", body=document)
        else:
            unexpected.append(request.url)
            route.abort("blockedbyclient")

    context.route("**/*", deny_or_document)
    context.add_init_script(MOCK)
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_default_timeout(5000)
    try:
        page.goto(ORIGIN)
        page.wait_for_function("qa.pending.length === 1")
        expect(page.locator("html")).to_have_attribute("lang", language)
        assert page.locator("h1").text_content().endswith(NAME)
        assert page.locator("h1").get_attribute("title").endswith(NAME)
        assert page.locator("h1").evaluate("e => e.scrollWidth > e.clientWidth")
        assert page.locator("h1").evaluate("e => getComputedStyle(e).textOverflow") == "ellipsis"
        expect(page.locator("#state")).to_have_attribute("aria-controls", "status-panel")
        expect(page.locator("#status-live")).to_have_attribute("role", "status")
        box = page.locator("#kb")
        box.focus()
        selectors = [".phone-header", "#kb", ".keys", "#pad"]

        def geometry():
            return {sel: page.locator(sel).first.bounding_box() for sel in selectors}

        baseline = geometry()
        baseline_height = page.evaluate("document.documentElement.scrollHeight")

        def stable(focus=True):
            assert geometry() == baseline
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            assert page.evaluate("document.documentElement.scrollHeight") == baseline_height
            if focus:
                expect(box).to_be_focused()

        def flush():
            page.evaluate("qa.flush()")

        def answer(text="", status=200, fail=False):
            if not page.evaluate("qa.pending.length"):
                page.evaluate("qa.tick()")
            page.evaluate("x => qa.answer(x)", dict(text=text, status=status, fail=fail))
            page.wait_for_function("qa.timers.length === 1")
            flush()

        def state(kind, glyph):
            expect(page.locator("#state")).to_have_attribute("data-kind", kind)
            expect(page.locator("#status-glyph")).to_have_text(glyph)
            assert page.locator("#state").get_attribute("aria-label")
            assert page.locator("#status-live").text_content()
            stable()

        def frame(label):
            page.screenshot(path=str(output / f"{language}-{width}-{label}.png"), full_page=True)

        answer("waiting")
        state("disconnected", "×")
        frame("waiting")
        box.fill("before")
        flush()
        assert page.evaluate("qa.posts") == []
        answer("loading a1")
        state("connected", "✓")
        frame("loading")
        assert page.evaluate("qa.posts") == []
        answer("open a1")
        state("connected", "✓")
        assert page.evaluate("qa.posts") == ["type=before&pin=1234"]
        frame("ready")
        announcement = page.locator("#status-live").text_content()
        page.evaluate("""() => {
          qa.liveChanges = 0;
          new MutationObserver(() => ++qa.liveChanges).observe(
            document.getElementById('status-live'), {childList:true, characterData:true, subtree:true});
        }""")
        answer("open a1")
        assert page.locator("#status-live").text_content() == announcement
        assert page.evaluate("qa.liveChanges") == 0
        assert page.evaluate("qa.posts.length") == 1

        # Same-token loading and new-token navigation both stay connected.
        answer("loading a1")
        state("connected", "✓")
        expect(box).to_have_value("before")
        answer("loading b2")
        expect(box).to_have_value("")
        box.fill("next")
        flush()
        assert page.evaluate("qa.posts.length") == 1
        page.evaluate("qa.tick()")  # delayed response: still connected, field not ready
        box.fill("next page")
        flush()
        state("connected", "✓")
        assert page.evaluate("qa.posts.length") == 1
        answer("open b2")
        assert page.evaluate("qa.posts[1]") == "type=next%20page&pin=1234"
        state("connected", "✓")

        # Transport failure / HTTP failure / unrelated 200 never masquerade as open.
        answer(fail=True)
        state("warning", "!")
        frame("warning")
        answer(status=503)
        answer("<html>PIN required</html>")
        answer(fail=True)
        state("warning", "!")
        answer(fail=True)
        state("disconnected", "×")
        expect(page.locator("#status-panel")).to_be_visible()
        assert "Wi-Fi" in page.locator("#status-message").text_content()
        frame("unreachable")
        page.locator("#status-hide").click()
        expect(page.locator("#state")).to_be_focused()
        box.focus()
        answer(fail=True)
        expect(page.locator("#status-panel")).to_be_hidden()
        before_recovery = page.evaluate("qa.posts")
        answer("open b2")
        state("connected", "✓")
        assert page.evaluate("qa.posts") == before_recovery  # no probe-triggered replay
        frame("recovered")

        # Exercise disclosure by keyboard and Escape without moving any controls.
        page.locator("#state").focus()
        page.keyboard.press("Enter")
        expect(page.locator("#status-panel")).to_be_visible()
        page.locator("#status-hide").focus()
        page.keyboard.press("Escape")
        expect(page.locator("#status-panel")).to_be_hidden()
        expect(page.locator("#state")).to_be_focused()
        box.focus()
        stable()

        # A held movement request cannot be overtaken by a tap or named key.
        offset = page.evaluate("qa.posts.length")
        page.evaluate("""() => {
          qa.holdPosts = true;
          const pad = document.getElementById('pad');
          pad.dispatchEvent(new MouseEvent('mousedown', {clientX:10,clientY:10,cancelable:true}));
          window.dispatchEvent(new MouseEvent('mousemove', {clientX:30,clientY:20,cancelable:true}));
          window.dispatchEvent(new MouseEvent('mouseup', {clientX:30,clientY:20,cancelable:true}));
        }""")
        flush()
        assert page.evaluate("qa.posts.slice(-1)") == ["move=20,10&pin=1234"]
        page.evaluate("""() => {
          const pad = document.getElementById('pad');
          for (const type of ['touchstart', 'touchend']) {
            const e = new Event(type, {cancelable:true});
            Object.defineProperty(e, 'touches', {value: type === 'touchstart' ? [{clientX:10,clientY:10}] : []});
            pad.dispatchEvent(e);
          }
          document.querySelector('[data-key=tab]').click();
        }""")
        flush()
        assert page.evaluate("qa.posts.length") == offset + 1
        page.evaluate("""() => {
          qa.holdPosts = false;
          qa.hold.splice(0).forEach(resolve => resolve(new Response(null, {status:204})));
        }""")
        flush()
        assert page.evaluate("n => qa.posts.slice(n)", offset) == [
            "move=20,10&pin=1234", "click=1&pin=1234", "key=tab&pin=1234"]

        # New-source French copy, masked warnings and button geometry.
        expect(box).to_have_attribute("placeholder", "Saisissez ici" if language == "fr" else "Type here")
        expect(box).to_have_attribute("aria-label", "Texte à saisir sur votre console" if language == "fr" else "Text to type on your handheld")
        def fit():
            checks = page.locator(".keys").first.locator("button").evaluate_all("""els => els.map(e => {
              const r = document.createRange(); r.selectNodeContents(e);
              const t = r.getBoundingClientRect(), b = e.getBoundingClientRect();
              return {text:e.textContent, fits:t.left >= b.left && t.right <= b.right && t.top >= b.top && t.bottom <= b.bottom};
            })""")
            assert all(c['fits'] for c in checks), checks
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            return checks
        fit(); frame("locale-masked")
        box.fill("Aéà"); flush()
        offset_local = page.evaluate("qa.posts.length")
        expected = ("La console ne peut pas saisir 2 des caractères entrés. Ils ont été ignorés." if language == "fr" else "The handheld can't type 2 of the characters you entered, so they were left out.")
        expect(page.locator("#warn")).to_have_text(expected)
        frame("locale-warning-masked")
        page.locator("#show").click(); fit()
        expect(page.locator("#show")).to_have_text("Cacher" if language == "fr" else "Hide")
        assert "é à" in page.locator("#warn").text_content()
        frame("locale-warning-revealed")
        page.locator("#show").click(); fit()
        expect(page.locator("#show")).to_have_text("Voir" if language == "fr" else "Show")
        expect(page.locator("#warn")).to_have_text(expected)
        assert page.evaluate("qa.posts.length") == offset_local
        frame("locale-warning-rehidden")
        page.locator("#clear").click()

        # Existing masking, editing, and explicit Close confirmation stay operative.
        box.fill("aé")
        flush()
        expect(box).to_have_value("a")
        expect(box).to_have_attribute("type", "password")
        expect(page.locator("#warn")).to_have_text("La console ne peut pas saisir un des caractères entrés. Il a été ignoré." if language == "fr" else "The handheld can't type one of the characters you entered, so it was left out.")
        page.locator("#show").click()
        expect(box).to_have_attribute("type", "text")
        assert "é" in page.locator("#warn").text_content()
        page.locator("#show").click()
        page.locator("#clear").click()
        expect(box).to_have_value("")
        close_offset = page.evaluate("qa.posts.length")
        page.locator("#leave-ask").click()
        expect(page.locator("#leave-confirm")).to_be_visible()
        page.locator("#leave-keep").click()
        assert page.evaluate("qa.posts.length") == close_offset
        page.locator("#leave-ask").click()
        page.locator("#leave-close").click()
        flush()
        assert page.evaluate("qa.posts.slice(-1)") == ["key=escape&pin=1234"]
        page.evaluate("scrollTo(0, 0)")
        box.focus()
        answer("waiting")
        state("disconnected", "×")
        expect(page.locator("#status-panel")).to_be_visible()
        frame("ended")
        assert page.evaluate("phoneStatusKey") == "ended"
        box.fill("new attempt")
        flush()
        assert page.evaluate("qa.posts.slice(-1)") == ["key=escape&pin=1234"]

        # Script death stays visible even when the next probe succeeds.
        page.evaluate("window.onerror('synthetic script error')")
        state("warning", "!")
        frame("script-error")
        answer("open c3")
        state("warning", "!")
        assert "synthetic script error" in page.locator("#status-message").text_content()
        assert not errors, errors
        assert not unexpected, unexpected
        assert page.evaluate("qa.unexpected") == []
        return {"language": language, "width": width, "result": "PASS", "frames": 12}
    finally:
        context.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="new synthetic evidence directory; must not already exist")
    parser.add_argument("--browser", choices=("chromium", "webkit"), default="chromium")
    parser.add_argument("--executable-path", type=Path,
                        help="explicit already-installed browser binary; never download implicitly")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    report = {"status": "RUNNING", "python": platform.python_version(),
              "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "cases": []}
    try:
        report["playwright"] = importlib.metadata.version("playwright")
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            launch_args = {}
            if args.executable_path:
                executable = args.executable_path.resolve(strict=True)
                launch_args["executable_path"] = str(executable)
                report["executable"] = {"path": str(executable), "sha256": hashlib.sha256(executable.read_bytes()).hexdigest()}
            browser = getattr(pw, args.browser).launch(**launch_args)
            try:
                report["browser"] = {"name": args.browser, "version": browser.version}
                for language in ("en", "fr"):
                    for width in (320, 768):
                        report["cases"].append(run_case(browser, language, width, args.output))
            finally:
                browser.close()
        report["status"] = "PASS"
    except BaseException as error:
        report["status"] = "FAIL"
        report["error"] = repr(error)
        raise
    finally:
        (args.output / "result.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
