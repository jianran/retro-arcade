/* Level 6 — Hot Air Balloon 🎈
 * Hold ←/→ to steer around storm clouds as you rise. Wind gusts push you
 * sideways (telegraphed 1s ahead). Hitting a cloud stalls you briefly.
 * Reach the summit to win.
 */
(function () {
  'use strict';
  const GT = window.GT;

  let bx = 480;            // balloon x
  let alt = 0;             // 0..100 altitude
  let invuln = 0;
  let flashT = 0;
  let obstacles = [];      // {alt, gx, hit}
  let nextAlt = 35;
  let gusts = [];          // {t0, dir, dur, str}
  let nextGust = 5;
  let clouds = [];         // parallax {x, y, s, v}

  GT.registerLevel({
    name: 'Hot Air Balloon',
    icon: '🎈',
    accent: '#7fe08a',
    tagline: 'Steer your balloon up through the stormy sky!',
    instructions: [
      'Hold ← and → to steer left and right',
      'Wind gusts push you sideways — watch for the warning arrows',
      'Hitting a storm cloud stalls you and knocks you down a little',
      'Reach the summit flag to win',
    ],
    timeLimit: 55,

    enter: function (g) {
      bx = 480;
      alt = 0;
      invuln = 0;
      flashT = 0;
      obstacles = [];
      nextAlt = 35;
      gusts = [];
      nextGust = 5;
      clouds = [];
      for (let i = 0; i < 9; i++) {
        clouds.push({
          x: Math.random() * 960,
          y: Math.random() * 640,
          s: 0.5 + Math.random(),
          v: 10 + Math.random() * 12,
        });
      }
      g.setObjective('Reach the summit!');
    },

    update: function (g, dt) {
      let vx = 0;
      if (GT.input.held('arrowleft')) vx -= 220;
      if (GT.input.held('arrowright')) vx += 220;
      let wind = Math.sin(g.t * 0.5) * 40;

      if (g.t > nextGust) {
        gusts.push({ t0: g.t + 1.0, dir: Math.random() < 0.5 ? -1 : 1, dur: 1.8, str: 190 });
        nextGust = g.t + 5 + Math.random() * 1.5;
      }
      for (const gu of gusts) {
        if (g.t >= gu.t0 && g.t < gu.t0 + gu.dur) wind += gu.dir * gu.str;
      }
      gusts = gusts.filter(function (gu) { return g.t < gu.t0 + gu.dur + 1; });

      bx = Math.max(55, Math.min(905, bx + (vx + wind) * dt));
      alt += 3.0 * dt;
      invuln = Math.max(0, invuln - dt);
      flashT = Math.max(0, flashT - dt);

      while (nextAlt < alt + 140) {
        obstacles.push({ alt: nextAlt, gx: 160 + Math.random() * 640, hit: false });
        nextAlt += 30 + Math.random() * 8;
      }

      for (const ob of obstacles) {
        if (ob.hit) continue;
        if (Math.abs(ob.alt - alt) < 16) {
          const gapL = ob.gx - 55;
          const gapR = ob.gx + 55;
          if (bx - 32 < gapL || bx + 32 > gapR) {
            ob.hit = true;
            if (invuln <= 0) {
              alt -= 12;
              invuln = 1.5;
              flashT = 0.6;
              g.sfx.buzz();
            }
          }
        }
      }
      obstacles = obstacles.filter(function (ob) { return ob.alt > alt - 60; });

      for (const cl of clouds) {
        cl.y += cl.v * dt;
        if (cl.y > 690) { cl.y = -60; cl.x = Math.random() * 960; }
      }

      if (alt >= 100) {
        g.setObjective('Summit!');
        g.win();
      }
    },

    draw: function (g, c) {
      // sky
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#4a9fe0', '#bfe3ff']);
      c.fillRect(0, 0, 960, 640);
      GT.gfx.glow(c, 120, 90, 55, 'rgba(255,240,180,0.95)');
      GT.gfx.emoji(c, '☀️', 120, 90, 52);

      // parallax clouds
      for (const cl of clouds) {
        c.fillStyle = 'rgba(255,255,255,0.75)';
        c.beginPath();
        c.ellipse(cl.x, cl.y, 60 * cl.s, 22 * cl.s, 0, 0, Math.PI * 2);
        c.ellipse(cl.x + 40 * cl.s, cl.y - 10 * cl.s, 40 * cl.s, 18 * cl.s, 0, 0, Math.PI * 2);
        c.fill();
      }

      // storm cloud obstacles
      const by = 560 - alt * 5;
      for (const ob of obstacles) {
        const oy = 560 - ob.alt * 5;
        if (oy < -140 || oy > 760) continue;
        c.fillStyle = '#46556e';
        if (ob.gx - 70 > 0) {
          c.beginPath();
          c.roundRect(0, oy - 45, ob.gx - 70, 90, 20);
          c.fill();
        }
        c.beginPath();
        c.roundRect(ob.gx + 70, oy - 45, 960 - ob.gx - 70, 90, 20);
        c.fill();
        // lightning inside clouds
        c.strokeStyle = 'rgba(255,240,140,0.55)';
        c.lineWidth = 2;
        for (let i = 0; i < 2; i++) {
          const lx = (i === 0 ? ob.gx - 110 : ob.gx + 140);
          if (lx < 20 || lx > 940) continue;
          c.beginPath();
          c.moveTo(lx, oy - 22);
          c.lineTo(lx - 8, oy + 2);
          c.lineTo(lx + 4, oy + 2);
          c.lineTo(lx - 6, oy + 22);
          c.stroke();
        }
      }

      // summit flag
      c.strokeStyle = '#8a5a2b';
      c.lineWidth = 4;
      c.beginPath();
      c.moveTo(890, 120);
      c.lineTo(890, 56);
      c.stroke();
      GT.gfx.emoji(c, '🏁', 918, 62, 32);

      // altitude meter
      c.fillStyle = 'rgba(255,255,255,0.25)';
      c.beginPath();
      c.roundRect(928, 70, 14, 490, 7);
      c.fill();
      c.fillStyle = '#ffd75a';
      c.beginPath();
      c.roundRect(928, 560 - alt * 4.9, 14, Math.max(12, alt * 4.9), 7);
      c.fill();

      // gust warning arrows
      for (const gu of gusts) {
        if (g.t >= gu.t0 - 1 && g.t < gu.t0) {
          const ax = gu.dir > 0 ? bx + 110 : bx - 110;
          GT.gfx.glow(c, ax, by - 70, 36, 'rgba(255,215,90,0.5)');
          GT.gfx.text(c, gu.dir > 0 ? '⇒' : '⇐', ax, by - 70, {
            size: 52, color: '#ffd75a', stroke: '#0a0f1a', lineWidth: 5,
          });
        }
      }

      // balloon (blinks while invulnerable after a hit)
      if (invuln > 0 && Math.sin(g.t * 30) > 0) c.globalAlpha = 0.45;
      if (flashT > 0) GT.gfx.glow(c, bx, by - 30, 60, 'rgba(255,120,120,0.5)');
      GT.gfx.emoji(c, '🎈', bx, by - 30, 64);
      c.globalAlpha = 1;
      // basket + ropes
      c.strokeStyle = '#8a5a2b';
      c.lineWidth = 2;
      c.beginPath();
      c.moveTo(bx - 16, by - 8);
      c.lineTo(bx - 14, by + 12);
      c.moveTo(bx + 16, by - 8);
      c.lineTo(bx + 14, by + 12);
      c.stroke();
      c.fillStyle = '#a8743c';
      c.beginPath();
      c.roundRect(bx - 22, by + 12, 44, 26, 6);
      c.fill();
    },
  });
})();
