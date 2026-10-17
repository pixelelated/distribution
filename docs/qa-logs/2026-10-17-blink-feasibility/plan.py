#!/usr/bin/env python3
"""Print a source-bound runtime proposal. Does not launch or allocate anything."""
import argparse
import json
import pathlib


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary',type=pathlib.Path,required=True)
    parser.add_argument('--owner',type=pathlib.Path,required=True)
    parser.add_argument('--port',type=int,required=True)
    parser.add_argument('--uid',type=int,required=True)
    args=parser.parse_args()
    if not args.owner.is_absolute() or not args.binary.is_absolute():
        parser.error('binary and fresh owned output root must be absolute')
    if not 1024<=args.port<=65535 or args.uid<=0:
        parser.error('loopback unprivileged port and non-root guest UID required')
    base=[str(args.binary),'--ozone-platform=wayland','--use-alloy-style','--force-device-scale-factor=1']
    print(json.dumps({
        'status':'PROPOSAL_ONLY_UNRUN',
        'guest_uid':args.uid,
        'external_network':'disabled for synthetic fixture; loopback only',
        'browser_argv':base+['--qa-port='+str(args.port),'--qa-root-cache='+str(args.owner/'context01'),'--url=http://127.0.0.1:'+str(args.port)+'/'],
        'second_fresh_context':'context02, same loopback server; require priorCookie=false and priorStorage=false',
        'separate_report_argv':[base+['--qa-internal-report','--qa-root-cache='+str(args.owner/name),'--url=chrome://'+kind+'/'] for kind,name in [('gpu','gpu-report'),('sandbox','sandbox-report')]],
        'source_check':'Hash patched files against probe-inputs.json and executable before launch.',
        'required_external_controls':['fresh admission and durable watcher','unchanged normal ES handoff','independent 180 second deadline and memory pressure guard','owned process identities and descendants','sandbox/namespace proof before loading fixture','explicit guest-only Wayland/render-node access for unprivileged UID','reviewed framebuffer and process/DRM evidence','normal exit and all-child reaping','retire owned SDK/guest disks/profile after compact export'],
        'not_implemented':['guest admission/lifecycle allocation','privilege/Wayland access setup','provider auth allowlist','native on-screen keyboard','phone field/page records','broker integration','real OAuth callbacks','performance analysis'],
    },indent=2))


if __name__ == '__main__':
    main()
