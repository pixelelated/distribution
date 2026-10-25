"""Shared by T13's stage-E positive drivers (#660). Each driver is run as

    python3 -I -B stage-e/pos<bug>/drive.py <path to the tool> unfixed|fixed

against the tool at 8a2518fa44 (unfixed) or at the stream's tip (fixed). It
observes which behaviour the tool has, writes only under $TMPDIR, and prints
one verdict line last:

    pos<bug>: unfixed-expectation-met | fixed-expectation-met | UNEXPECTED <what>

and exits 0 when the expectation it was given is met, 1 otherwise."""
import importlib.machinery
import importlib.util
import os
import sys
import tempfile


def args():
    if len(sys.argv) < 3 or sys.argv[2] not in ("unfixed", "fixed"):
        sys.exit(f"usage: {sys.argv[0]} <path to the tool> unfixed|fixed")
    return os.path.abspath(sys.argv[1]), sys.argv[2]


def load(tool):
    """The tool as a module; its `if __name__ == '__main__'` does not run."""
    loader = importlib.machinery.SourceFileLoader("tool_under_test", tool)
    spec = importlib.util.spec_from_loader("tool_under_test", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def scratch(name):
    """A fresh directory under $TMPDIR (never elsewhere)."""
    base = os.environ.get("TMPDIR")
    if not base:
        sys.exit("TMPDIR is not set; these drivers write only under it")
    return tempfile.mkdtemp(prefix=f"t13-{name}-", dir=base)


def verdict(name, expect, observed, detail):
    """observed is 'unfixed' or 'fixed': the behaviour the run saw."""
    if observed == expect:
        print(f"{name}: {expect}-expectation-met ({detail})")
        sys.exit(0)
    print(f"{name}: UNEXPECTED expected the {expect} behaviour, saw the {observed} one ({detail})")
    sys.exit(1)
