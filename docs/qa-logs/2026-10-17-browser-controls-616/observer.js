// SPDX-License-Identifier: GPL-2.0
(() => {
    // Isolated WebKit script world: no page globals, field values, or URLs.
    const q = {ticks: 0, last: 0, max: 0};
    let previous = performance.now();
    const started = previous;
    const timer = setInterval(() => {
        const now = performance.now();
        if (now - started >= 360000) { clearInterval(timer); return; }
        q.last = now - previous;
        q.max = Math.max(q.max, q.last);
        q.ticks++;
        previous = now;
    }, 250);
    globalThis.__qa616Sample = () => {
        let visible = 0, hittable = 0, checked = 0;
        for (const field of document.querySelectorAll('input')) {
            if (++checked > 128) break;
            if (!['text', 'email', 'password', 'tel', 'search', 'url'].includes(field.type)
                || field.disabled || field.readOnly) continue;
            const r = field.getBoundingClientRect();
            const s = getComputedStyle(field);
            const left = Math.max(0, r.left), right = Math.min(innerWidth, r.right);
            const top = Math.max(0, r.top), bottom = Math.min(innerHeight, r.bottom);
            if (right - left < 2 || bottom - top < 2 || s.visibility !== 'visible'
                || s.display === 'none' || Number(s.opacity) === 0) continue;
            visible++;
            const hit = document.elementFromPoint((left + right) / 2, (top + bottom) / 2);
            if (hit === field) hittable++;
        }
        return {
            ready: document.readyState === 'complete' ? 2 : document.readyState === 'interactive' ? 1 : 0,
            foreground: document.visibilityState === 'visible' ? 1 : 0,
            width: innerWidth, height: innerHeight, scale: devicePixelRatio,
            visible, hittable, checked,
            ticks: q.ticks, last_gap_ms: q.last, max_gap_ms: q.max
        };
    };
})();
