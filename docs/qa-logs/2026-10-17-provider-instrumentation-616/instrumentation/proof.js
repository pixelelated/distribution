// SPDX-License-Identifier: GPL-2.0
(() => {
    // This code runs in a dedicated isolated world. It neither reads field
    // values nor changes focus, content, page behavior, or provider resources.
    const doc = Math.round(performance.timeOrigin * 1000);
    const send = value => window.webkit.messageHandlers.qa616Proof.postMessage(value);
    const host = location.hostname.toLowerCase();
    const provider = host === '127.0.0.1' || host === 'localhost' ? 1
        : host === 'dropbox.com' || host.endsWith('.dropbox.com') ? 2
        : host === 'accounts.google.com' ? 3
        : ['login.microsoftonline.com', 'login.live.com', 'onedrive.live.com'].includes(host) ? 4 : 0;
    let sentBinding = false, attempts = 0, inputs = 0;
    const bind = () => {
        if (sentBinding) return;
        if (!(innerWidth > 0 && innerHeight > 0 && devicePixelRatio > 0)) {
            if (++attempts < 100) setTimeout(bind, 50);
            else { sentBinding = true; send({kind: 3, doc, reason: 1}); }
            return;
        }
        sentBinding = true;
        send({kind: 1, doc, provider, ua: navigator.userAgent,
              width: innerWidth, height: innerHeight, scale: devicePixelRatio});
    };
    const schedule = () => requestAnimationFrame(bind);
    if (document.readyState === 'loading')
        document.addEventListener('DOMContentLoaded', schedule, {once: true});
    else schedule();

    document.addEventListener('input', event => {
        if (inputs >= 8) return;
        const target = event.target;
        if (!(target instanceof HTMLInputElement)) return;
        // Password fields and other controls never enter the probe.
        if (!['text', 'email'].includes(target.type)) return;
        const sequence = ++inputs;
        const started = performance.now();
        let eligible = !target.matches(':disabled') && !target.readOnly && target.isConnected;
        let ancestor = target, depth = 0;
        while (ancestor && depth++ < 32) {
            const style = getComputedStyle(ancestor);
            if (style.display === 'none' || style.visibility !== 'visible' || Number(style.opacity) === 0)
                eligible = false;
            ancestor = ancestor.parentElement;
        }
        if (ancestor) eligible = false; // Cannot prove deeper ancestry visible.
        const r = target.getBoundingClientRect();
        const left = Math.max(0, r.left), right = Math.min(innerWidth, r.right);
        const top = Math.max(0, r.top), bottom = Math.min(innerHeight, r.bottom);
        eligible = eligible && right - left >= 2 && bottom - top >= 2
            && document.elementFromPoint((left + right) / 2, (top + bottom) / 2) === target;
        const focused = document.activeElement === target;
        const trusted = event.isTrusted;
        requestAnimationFrame(() => requestAnimationFrame(() => {
            send({kind: 2, doc, sequence, trusted: trusted ? 1 : 0,
                  eligible: eligible ? 1 : 0, focused: focused ? 1 : 0,
                  render_delta_ms: performance.now() - started});
        }));
    }, true);
})();
