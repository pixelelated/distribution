#!/bin/bash
# #1502 before the build: the round's patched raofflineproxy-ctl bound over
# the image's on guest a (a bind mount, gone at the next reboot), then the
# three states from the shell. Prints each case's stamp; the image's ctl is
# the control (run first, same states).
set -uo pipefail
KEY=/tmp/rocknix-vm-pair/qa-key
SSHO=(-F /dev/null -p 10022 -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
SCPO=(-F /dev/null -P 10022 -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -o ConnectTimeout=10)
S() { timeout 300 ssh -n "${SSHO[@]}" root@127.0.0.1 ". /etc/profile >/dev/null 2>&1; $*"; }
CTL=/workspace/repos/rocknix.worktrees/m7-rc-round-20261125/projects/ROCKNIX/packages/network/raofflineproxy/sources/raofflineproxy-ctl
F=/workspace/tmp/rocknix-session/1501/fixture
S 'mkdir -p /storage/m7-qa-1501' && scp -q "${SCPO[@]}" "$F/standin.py" "$F/ra-refusal-guest.sh" "$CTL" root@127.0.0.1:/storage/m7-qa-1501/ < /dev/null || exit 2
G() { S "bash /storage/m7-qa-1501/ra-refusal-guest.sh $*"; }
stamp() { S 'sed -n "s/.*why=\([A-Z_]*\).*/\1/p" /storage/.config/raofflineproxy/last-scan'; }
for which in image patched; do
    if [ "$which" = patched ]; then
        S 'chmod 755 /storage/m7-qa-1501/raofflineproxy-ctl && mount --bind /storage/m7-qa-1501/raofflineproxy-ctl /usr/bin/raofflineproxy-ctl && sha256sum /usr/bin/raofflineproxy-ctl | cut -c1-16'
    fi
    for c in token-401 token-503 password-401; do
        mode=${c%-*} st=${c#*-}
        G account "$mode" >/dev/null; G standin "$st" >/dev/null || { echo "$which $c: no stand-in"; continue; }
        S 'rm -f /storage/.config/raofflineproxy/last-scan'; G scan >/dev/null
        echo "$which scan $c: $(stamp)"
    done
    # The top-up's recently played pass with a refused sign-in, both ways
    # an account can be held. The interval mark is cleared so it runs.
    for mode in password token; do
        G account "$mode" >/dev/null; G standin 401 >/dev/null
        S 'rm -f /storage/.config/raofflineproxy/last-topup-attempt /storage/.config/raofflineproxy/last-scan; raofflineproxy-ctl topup >/dev/null 2>&1; echo "rc=$?"' >/dev/null
        echo "$which topup $mode-401: $(stamp) | $(S 'grep -E "topup (recently|done)" /storage/.config/raofflineproxy/scan.log | tail -2 | tr "\n" " "')"
    done
done
S 'umount /usr/bin/raofflineproxy-ctl; sha256sum /usr/bin/raofflineproxy-ctl | cut -c1-16'
G release
