#!/usr/bin/env python3
"""Static-only attribution: AST/literal inspection, hashes, node --check; no page execution."""
import ast
import hashlib
import html
import json
import platform
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PATH = "projects/ROCKNIX/packages/network/rclone/sources/cloud_oauth"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def literals(tree):
    return {node.targets[0].id: ast.literal_eval(node.value)
            for node in tree.body if isinstance(node, ast.Assign)
            and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id in ("REMOTE_PAGE", "STYLE")}


def untouched(tree):
    def changed(node):
        if isinstance(node, ast.Import) and [a.name for a in node.names] == ["html"]:
            return True
        if isinstance(node, ast.FunctionDef) and node.name == "phone_page":
            return True
        return (isinstance(node, ast.Assign) and len(node.targets) == 1
                and getattr(node.targets[0], "id", "") in ("STYLE", "REMOTE_PAGE"))
    return [ast.dump(node, include_attributes=False) for node in tree.body if not changed(node)]


def input_block(template):
    return template.split("  // One request at a time, in order.", 1)[1].split(
        "  // This page is scanned before the window exists", 1)[0]


def main():
    binding = json.loads((HERE / "source.json").read_text())
    candidate = (ROOT / PATH).read_bytes()
    base_run = subprocess.run(["git", "show", binding["base_commit"] + ":" + PATH],
                              cwd=ROOT, capture_output=True, check=True)
    base = base_run.stdout
    assert sha(base) == binding["base_sha256"]
    assert sha(candidate) == binding["candidate_sha256"]
    base_ast, candidate_ast = ast.parse(base), ast.parse(candidate)
    assert untouched(base_ast) == untouched(candidate_ast), "broker/security changed"
    before, after = literals(base_ast), literals(candidate_ast)
    assert input_block(before["REMOTE_PAGE"]) == input_block(after["REMOTE_PAGE"])
    gate = 'var opened = open && !ready;\n        ready = open;\n        if (opened) { sent = ""; deliver(box.value); }'
    assert gate in before["REMOTE_PAGE"] and gate in after["REMOTE_PAGE"]
    page_clear = 'if (page !== null) { box.value = ""; sent = ""; }'
    assert page_clear in before["REMOTE_PAGE"] and page_clear in after["REMOTE_PAGE"]
    assert sha(input_block(after["REMOTE_PAGE"]).encode()) == binding["unchanged_input_block_sha256"]
    for path in HERE.glob("*.py"):
        ast.parse(path.read_bytes(), filename=str(path))

    function = next(n for n in candidate_ast.body if isinstance(n, ast.FunctionDef)
                    and n.name == "phone_page")
    loop = next(n for n in ast.walk(function) if isinstance(n, ast.For))
    translations = ast.literal_eval(loop.iter)  # literal data; no cloud_oauth import/eval
    syntax = []
    for language in ("en", "fr"):
        page = after["REMOTE_PAGE"]
        if language == "fr":
            for before_text, after_text in translations:
                page = page.replace(before_text, after_text)
        page = page % {"style": after["STYLE"],
                       "name": html.escape('Synthetic "name" <text> &'), "pin": "1234"}
        assert '<html lang=' + language + '>' in page
        script = page.split("<script>", 1)[1].split("</script>", 1)[0]
        ids = re.findall(r'\bid=(?:"([^"]+)"|([^\s>]+))', page)
        ids = [a or b for a, b in ids]
        assert len(ids) == len(set(ids)), "duplicate element ID"
        assert set(re.findall(r'getElementById\("([^\"]+)"\)', script)) <= set(ids)
        functions = set(re.findall(r"^\s*function\s+(\w+)\s*\(", script, re.M))
        variables = set(re.findall(r"\bvar\s+(\w+)", script))
        assert not functions & variables, "function/var shadowing"
        result = subprocess.run(["node", "--check"], input=script, text=True, capture_output=True)
        syntax.append({"language": language, "command": "node --check < extracted-script",
                       "exit": result.returncode, "stderr": result.stderr})
        assert result.returncode == 0, result.stderr
    node_version = subprocess.run(["node", "--version"], text=True, capture_output=True, check=True)
    fixture_ast = ast.parse((HERE / "browser_fixture.py").read_bytes())
    mock = next(ast.literal_eval(n.value) for n in fixture_ast.body if isinstance(n, ast.Assign)
                and getattr(n.targets[0], "id", "") == "MOCK")
    mock_check = subprocess.run(["node", "--check"], input=mock, text=True, capture_output=True)
    assert mock_check.returncode == 0, mock_check.stderr
    print(json.dumps({"evidence": "STATIC ONLY", "python": platform.python_version(),
                      "node": node_version.stdout.strip(), "git_show_exit": base_run.returncode,
                      "base_sha256": sha(base), "candidate_sha256": sha(candidate),
                      "unchanged_non_page_ast": True, "unchanged_input_block": True,
                      "readiness_and_navigation_clear_preserved": True,
                      "python_ast": "PASS", "javascript_syntax": syntax,
                      "fixture_mock_syntax": {"command": "node --check < MOCK literal",
                                              "exit": mock_check.returncode,
                                              "stderr": mock_check.stderr},
                      "browser_fixture": "UNRUN", "vm": "UNRUN"}, indent=2))


if __name__ == "__main__":
    main()
