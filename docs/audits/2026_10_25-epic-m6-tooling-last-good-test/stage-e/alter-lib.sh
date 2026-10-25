# alter-lib.sh -- shared by the stage-e alteration recipes (T15, #662, the
# coordinator's 06:05 ruling): each recipe changes a throwaway clone of the
# tree (never committed, removed after its run), and fails closed when a
# change does not apply. Usage from a recipe: . "$(dirname "$0")/alter-lib.sh"
set -eu
C="${1:?usage: alter-<bug>.sh <throwaway clone>}"
R="${C}/projects/ROCKNIX/packages"
# change <file> <ERE the line must match, exactly once> <sed expression> [ERE that must match after]
# Without the fourth, the matched line must be gone; an insertion names what it inserted.
change() {
    local f="$1" re="$2" ex="$3" after="${4:-}" n
    n=$(grep -c -E -- "${re}" "${f}" || true)
    [ "${n}" -eq 1 ] || { echo "alter: ${f#${C}/}: '${re}' matched ${n} lines, not 1" >&2; exit 2; }
    echo "  ${f#${C}/}:$(grep -n -E -- "${re}" "${f}" | cut -d: -f1): ${ex}"
    sed -i -E "${ex}" "${f}"
    if [ -n "${after}" ]; then grep -q -E -- "${after}" "${f}"; else ! grep -q -E -- "${re}" "${f}"; fi \
        || { echo "alter: ${f#${C}/}: the change did not apply" >&2; exit 2; }
}
# drop_fn <file> <ERE of the function's first line>: the function, through its closing '}' at column 0
drop_fn() {
    local f="$1" re="$2" n
    n=$(grep -c -E -- "${re}" "${f}" || true)
    [ "${n}" -eq 1 ] || { echo "alter: ${f#${C}/}: function '${re}' found ${n} times" >&2; exit 2; }
    echo "  ${f#${C}/}:$(grep -n -E -- "${re}" "${f}" | cut -d: -f1): removed the function ${re}"
    # The pattern through the environment: awk -v would process its backslashes.
    RE="${re}" awk '$0 ~ ENVIRON["RE"] {skip = 1} skip && /^}/ {skip = 0; next} !skip' "${f}" > "${f}.t15" && mv "${f}.t15" "${f}"
    ! grep -q -E -- "${re}" "${f}"
}
