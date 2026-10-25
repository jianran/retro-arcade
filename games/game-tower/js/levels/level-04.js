/* Level 4 — Firefly Hunt ✨ (mouse level)
 * Click where you want the net to swing. The net takes 0.25s to arrive, so
 * aim slightly ahead of the drifting fireflies. Catch all 9.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const N_FLIES = 9;
  const CATCH_R = 45;

  let flies = [];     // {cx, cy, ph, ph2, caught}
  let net = null;     // {sx, sy, tx, ty} while swinging
  let netT = 0;
  let netX = 830;
  let netY = 90;
  let catches = 0;

  GT.registerLevel({
    name: 'Firefly Hunt',
    icon: '✨',
    accent: '#c9a0ff',
    tagline: 'Click to swing your net and catch the drifting fireflies!',
    instructions: [
      'Click anywhere — your net swings there in an instant',
      'The net takes a moment to travel, so aim where the firefly is heading',
      'Catch all 9 fireflies in your jar',
    ],
    timeLimit: 45,

    enter: function (g) {
      flies = [];
      for (let i = 0; i < N_FLIES; i++) {
        flies.push({
          cx: 140 + Math.random() * 680,
          cy: 140 + Math.random() * 330,
          ph: Math.random() * 6.28,
          ph2: Math.random() * 6.28,
          caught: false,
        });
      }
      net = null;
      netT = 0;
      netX = 830;
      netY = 90;
      catches = 0;
      g.setObjective('Fireflies: 0/' + N_FLIES);
    },

    onClick: function (g, x, y) {
      if (net) return; // one swing at a time
      net = { sx: netX, sy: netY, tx: x, ty: y };
      netT = 0;
      g.sfx.whoosh();
    },

    update: function (g, dt) {
      if (net) {
        netT += dt / 0.25;
        const p = Math.min(1, netT);
        netX = net.sx + (net.tx - net.sx) * p;
        netY = net.sy + (net.ty - net.sy) * p;
        if (p >= 1) {
          let got = false;
          for (const f of flies) {
            if (f.caught) continue;
            const fx = f.cx + Math.sin(g.t * 0.7 + f.ph) * 105;
            const fy = f.cy + Math.sin(g.t * 0.9 + f.ph2) * 60;
            if (Math.hypot(fx - netX, fy - netY) < CATCH_R) {
              f.caught = true;
              got = true;
            }
          }
          if (got) {
            catches = flies.filter(function (f) { return f.caught; }).length;
            g.sfx.catchSound();
            g.setObjective('Fireflies: ' + catches + '/' + N_FLIES);
            if (catches >= N_FLIES) g.win();
          } else {
            g.sfx.blip();
          }
          net = null;
        }
      }
    },

    draw: function (g, c) {
      // moonlit garden
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#1a1440', '#0d0a22']);
      c.fillRect(0, 0, 960, 640);
      GT.gfx.glow(c, 110, 80, 50, 'rgba(255,250,220,0.9)');
      GT.gfx.emoji(c, '🌙', 110, 80, 42);

      // grass silhouettes
      c.fillStyle = '#0b1f18';
      c.beginPath();
      c.moveTo(0, 640);
      for (let x = 0; x <= 960; x += 20) {
        c.lineTo(x, 520 + Math.sin(x * 0.05) * 18);
      }
      c.lineTo(960, 640);
      c.closePath();
      c.fill();
      // flowers
      for (let i = 0; i < 9; i++) {
        GT.gfx.emoji(c, '🌸', 40 + i * 115, 560 + (i % 3) * 26, 22);
      }

      // fireflies
      for (const f of flies) {
        if (f.caught) continue;
        const fx = f.cx + Math.sin(g.t * 0.7 + f.ph) * 105;
        const fy = f.cy + Math.sin(g.t * 0.9 + f.ph2) * 60;
        const pulse = 0.35 + 0.5 * Math.abs(Math.sin(g.t * 2.6 + f.ph));
        GT.gfx.glow(c, fx, fy, 34, 'rgba(255,232,110,' + pulse.toFixed(2) + ')');
        GT.gfx.emoji(c, '✨', fx, fy, 22);
      }

      // net (rim + handle)
      const handleAngle = 0.9;
      c.strokeStyle = '#c9a0ff';
      c.lineWidth = 3;
      c.beginPath();
      c.arc(netX, netY, 46, 0, Math.PI * 2);
      c.stroke();
      c.globalAlpha = 0.4;
      for (let i = -40; i <= 40; i += 20) {
        c.beginPath();
        c.moveTo(netX - 46, netY + i);
        c.lineTo(netX + 46, netY + i);
        c.stroke();
      }
      c.globalAlpha = 1;
      c.lineWidth = 5;
      c.beginPath();
      c.moveTo(netX + Math.cos(handleAngle) * 46, netY + Math.sin(handleAngle) * 46);
      c.lineTo(netX + Math.cos(handleAngle) * 100, netY + Math.sin(handleAngle) * 100);
      c.stroke();

      // jar top-right
      c.strokeStyle = 'rgba(255,255,255,0.5)';
      c.lineWidth = 3;
      c.beginPath();
      c.roundRect(780, 60, 100, 100, 12);
      c.stroke();
      c.beginPath();
      c.roundRect(795, 46, 70, 18, 8);
      c.stroke();
      GT.gfx.text(c, catches + '/' + N_FLIES, 830, 186, { size: 18, color: '#c9a0ff' });
      // caught fireflies glow in the jar
      for (let i = 0; i < catches; i++) {
        GT.gfx.glow(c, 795 + (i % 4) * 26, 80 + Math.floor(i / 4) * 40, 12,
          'rgba(255,232,110,0.8)');
      }
    },
  });
})();
