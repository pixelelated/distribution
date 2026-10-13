#!/usr/bin/env python3
"""Source/literal inspection only. Does not import or execute cloud_oauth or JS."""
import ast
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import platform
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PATH = "projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def page_parts(raw):
    tree = ast.parse(raw)
    literals = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
                if isinstance(n, ast.Assign) and len(n.targets) == 1
                and getattr(n.targets[0], "id", "") in ("STYLE", "REMOTE_PAGE")}
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == "phone_page")
    loop = next(n for n in ast.walk(function) if isinstance(n, ast.For))
    translations = ast.literal_eval(loop.iter)
    # Only additional literal translation pairs may change this function.
    loop.iter = ast.Tuple(elts=[], ctx=ast.Load())
    unchanged = [ast.dump(n, include_attributes=False) for n in tree.body
                 if not (isinstance(n, ast.Assign) and len(n.targets) == 1
                         and getattr(n.targets[0], "id", "") in literals)]
    return literals, translations, unchanged


def script(template):
    return template.split("<script>", 1)[1].split("</script>", 1)[0]


def messages(js):
    data = js.split("var phoneMessages = ", 1)[1].split("[phoneLanguage];", 1)[0]
    # This dictionary is literal string data, not general JavaScript.
    return json.loads(re.sub(r'(?m)^(\s*)([a-zA-Z]+):', r'\1"\2":',
                            re.sub(r', ([a-zA-Z]+):', r', "\1":', data)))


def between(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.elements = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])

    def handle_data(self, data):
        self.text.append(data)


def main():
    binding = json.loads((HERE / "source.json").read_text())
    baseline = subprocess.run(["git", "show", binding["base_commit"] + ":" + PATH],
                              cwd=ROOT, capture_output=True, check=True).stdout
    candidate = (ROOT / PATH).read_bytes()
    assert sha(baseline) == binding["base_sha256"]
    assert sha(candidate) == binding["candidate_sha256"]
    before, old_pairs, old_other = page_parts(baseline)
    after, pairs, other = page_parts(candidate)
    assert old_other == other, "non-literal Python behavior changed"
    assert all(pair in pairs for pair in old_pairs), "prior translations changed"
    style_delta = ("/* Let the short French key symbols leave room for Vider and Voir/Cacher. */\n"
                   "html[lang=fr] .keys button{flex-basis:auto}\n")
    assert after["STYLE"].replace(style_delta, "", 1) == before["STYLE"]
    old_js, js = script(before["REMOTE_PAGE"]), script(after["REMOTE_PAGE"])
    old_messages, new_messages = messages(old_js), messages(js)
    for lang in ("en", "fr"):
        assert all(new_messages[lang][key] == value for key, value in old_messages[lang].items())
        assert set(new_messages[lang]) - set(old_messages[lang]) == {
            "show", "hide", "droppedMaskedOne", "droppedMaskedMany",
            "droppedVisibleOne", "droppedVisibleMany"}
        for key in ("droppedMaskedOne", "droppedMaskedMany"):
            assert "{characters}" not in new_messages[lang][key]
        assert "{count}" in new_messages[lang]["droppedMaskedMany"]
    assert new_messages["en"]["show"] == "Show" and new_messages["en"]["hide"] == "Hide"
    # Literal EN warning equivalence, including singular and plural punctuation.
    for count in (1, 2, 20):
        key = "One" if count == 1 else "Many"
        masked = new_messages["en"]["droppedMasked" + key].replace("{count}", str(count))
        visible = new_messages["en"]["droppedVisible" + key].replace("{characters}", "é")
        suffix = ("it was" if count == 1 else "they were") + " left out."
        assert masked == ("The handheld can't type " + (
            "one of the characters you entered" if count == 1 else
            str(count) + " of the characters you entered") + ", so " + suffix)
        assert visible == "The handheld can't type é, so " + suffix
    old_warn = between(old_js, "  function warnSay() {", "  function typable() {")
    new_warn = between(js, "  function warnSay() {", "  function typable() {")
    expected_warn = '''
    if (!dropped.length) { warn.hidden = true; return; }
    var many = dropped.length > 1;
    warn.textContent = box.type === "password"
      ? (many ? phoneMessages.droppedMaskedMany.replace("{count}", dropped.length)
          : phoneMessages.droppedMaskedOne)
      : (many ? phoneMessages.droppedVisibleMany : phoneMessages.droppedVisibleOne)
          .replace("{characters}", dropped.join(" "));
    warn.hidden = false;
  }
'''
    assert new_warn == expected_warn, "masking branch changed"
    normalized = js.replace(between(js, "var phoneMessages = ", "[phoneLanguage];"),
                            between(old_js, "var phoneMessages = ", "[phoneLanguage];"), 1)
    normalized = normalized.replace(new_warn, old_warn, 1).replace(
        'show.textContent = hidden ? phoneMessages.hide : phoneMessages.show;',
        'show.textContent = hidden ? "Hide" : "Show";', 1)
    assert normalized == old_js, "queue/pointer/probe or other JS changed"
    old_markup = before["REMOTE_PAGE"].split("<script>", 1)[0]
    new_markup = after["REMOTE_PAGE"].split("<script>", 1)[0]
    # The English HTML changes consist only of accessible labels.
    added_labels = ("Text to type on your handheld", "Backspace", "Enter",
                    "Left arrow", "Up arrow", "Down arrow", "Right arrow")
    plain = new_markup
    for label in added_labels:
        assert plain.count(' aria-label="' + label + '"') == 1
        plain = plain.replace(' aria-label="' + label + '"', "", 1)
    assert plain == old_markup
    syntax = []
    for lang in ("en", "fr"):
        template = after["REMOTE_PAGE"]
        if lang == "fr":
            for first, second in pairs:
                assert first in template, "translation selector missing: " + first
                template = template.replace(first, second)
        # Static literal substitution, not a call/import of phone_page.
        rendered = template % dict(style=after["STYLE"],
                                   name=html.escape('Type here "Show" <&>'), pin="1234")
        markup = Markup()
        markup.feed(rendered.split("<script>", 1)[0])
        assert len(markup.ids) == len(set(markup.ids))
        assert set(re.findall(r'getElementById\("([^"]+)"\)', js)) <= set(markup.ids)
        assert '<html lang=' + lang + '>' in rendered
        assert 'Type here &quot;Show&quot; &lt;&amp;&gt;' in rendered
        if lang == "fr":
            labels = {a["data-key"]: a for tag, a in markup.elements if "data-key" in a}
            assert labels["backspace"]["aria-label"] == "Effacer un caractère"
            assert labels["enter"]["aria-label"] == "Entrée"
            for direction in ("left", "up", "down", "right"):
                assert labels[direction]["aria-label"].startswith("Flèche ")
            assert "id=show>Voir" in rendered and "id=clear>Vider" in rendered
            assert 'placeholder="Saisissez ici"' in rendered
            assert "<h2>Pointeur</h2>" in rendered and "sans chiffrement" in rendered
        result = subprocess.run(["node", "--check"], input=script(rendered), text=True,
                                capture_output=True)
        assert result.returncode == 0, result.stderr
        syntax.append({"language": lang, "command": "node --check < literal script",
                       "exit": result.returncode, "stderr": result.stderr})
    for path in HERE.glob("*.py"):
        ast.parse(path.read_bytes(), filename=str(path))
    cases = json.loads((HERE / "locale-cases.json").read_text())
    assert cases["runtime"] == "UNRUN"
    print(json.dumps({"evidence": "STATIC ONLY", "python": platform.python_version(),
                      "source_sha256": sha(candidate), "python_ast": "PASS",
                      "non_page_python_ast_equal": True, "english_visible_copy_equal": True,
                      "prior_locale_and_status_messages_equal": True,
                      "js_equal_except_message_literals_warning_and_toggle_text": True,
                      "masked_branch_has_no_character_interpolation": True,
                      "style_delta": "French key-row flex-basis only",
                      "javascript_syntax": syntax,
                      "locale_cases_json": "parsed; not executed",
                      "browser_regressions_frames_vm": "UNRUN"}, indent=2))


if __name__ == "__main__":
    main()
