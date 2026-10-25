import ast, os, re, sys
tool, src = sys.argv[1], sys.argv[2]
scripts = sorted(f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f)) and "." not in f)
consts = [n.value for n in ast.walk(ast.parse(open(tool).read())) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
hits = sorted({s for c in consts for s in scripts if re.search(rf"(^|[\s;|&(`]){re.escape(s)}(\s|$|[;|&)`])", c)})
print(f"{len(scripts)} device scripts under the rclone sources, {len(consts)} string constants; invoked: {hits or 'none'}")
