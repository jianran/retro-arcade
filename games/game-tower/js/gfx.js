/* GameTower — shared canvas draw helpers. */
(function () {
  'use strict';
  const GT = window.GT;

  const EMOJI_FONT = '"Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif';
  const TEXT_FONT = '"Trebuchet MS","Segoe UI",sans-serif';

  GT.gfx = {
    emoji: function (c, ch, x, y, px) {
      c.font = px + 'px ' + EMOJI_FONT;
      c.textAlign = 'center';
      c.textBaseline = 'middle';
      c.fillText(ch, x, y);
    },

    text: function (c, s, x, y, o) {
      o = o || {};
      c.font = (o.size || 20) + 'px ' + (o.family || TEXT_FONT);
      c.fillStyle = o.color || '#e9edf7';
      c.textAlign = o.align || 'center';
      c.textBaseline = o.baseline || 'middle';
      if (o.stroke) {
        c.strokeStyle = o.stroke;
        c.lineWidth = o.lineWidth || 3;
        c.strokeText(s, x, y);
      }
      c.fillText(s, x, y);
    },

    bar: function (c, x, y, w, h, pct, color, bg) {
      pct = Math.max(0, Math.min(1, pct));
      const r = h / 2;
      const x0 = x - r, y0 = y - h / 2;
      const W = w + 2 * r;
      if (bg) {
        c.fillStyle = bg;
        c.beginPath();
        c.roundRect(x0, y0, W, h, r);
        c.fill();
      }
      if (pct > 0.01) {
        c.fillStyle = color || '#52d8c4';
        c.beginPath();
        c.roundRect(x0, y0, Math.max(W * pct, r * 2), h, r);
        c.fill();
      }
    },

    // radial glow; color must be an rgba()/hsla() string (it carries its own alpha)
    glow: function (c, x, y, r, color) {
      const g = c.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, color);
      g.addColorStop(1, 'rgba(0,0,0,0)');
      c.fillStyle = g;
      c.beginPath();
      c.arc(x, y, r, 0, Math.PI * 2);
      c.fill();
    },

    // linear gradient fill helper: grad(c, 0, 0, 0, h, ['#111', '#222'])
    grad: function (c, x0, y0, x1, y1, stops) {
      const g = c.createLinearGradient(x0, y0, x1, y1);
      for (let i = 0; i < stops.length; i++) g.addColorStop(i / (stops.length - 1), stops[i]);
      return g;
    },

    // scatter of twinkling stars; starList = [{x, y, s, ph}]
    stars: function (c, starList, t) {
      for (let i = 0; i < starList.length; i++) {
        const s = starList[i];
        const a = 0.35 + 0.65 * Math.abs(Math.sin(t * 1.4 + s.ph));
        c.fillStyle = 'rgba(255,255,255,' + a.toFixed(3) + ')';
        c.beginPath();
        c.arc(s.x, s.y, s.s, 0, Math.PI * 2);
        c.fill();
      }
    },
  };
})();
