/* Level 18 — Whack-a-Meteor ☄️
 * Meteors pop out of four craters. Press the number key (1-4) of the crater
 * to whack it before it disappears. 22 whacks wins.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const CRATERS = [200, 400, 600, 800];
  const NEED = 22;

  let meteors = [null, null, null, null]; // {t, dur} per crater or null
  let hits = 0;
  let spawnT = 0.8;
  let lastPos = -1;
  let whackFx = [];    // {x, t, good}
  let whiffT = 0;

  GT.registerLevel({
    name: 'Whack-a-Meteor',
    icon: '☄️',
    accent: '#ff8fb2',
    tagline: 'Whack the meteors before they vanish!',
    instructions: [
      'Meteors pop out of four craters, left to right',
      'Press 1, 2, 3 or 4 to whack the matching crater',
      'They pop up faster as you go — 22 whacks wins',
    ],
    timeLimit: 60,

    enter: function (g) {
      meteors = [null, null, null, null];
      hits = 0;
      spawnT = 0.8;
      lastPos = -1;
      whackFx = [];
      whiffT = 0;
      g.setObjective('Whacked: 0/' + NEED);
    },

    onKey: function (g, code) {
      if (code !== '1' && code !== '2' && code !== '3' && code !== '4') return;
      const i = parseInt(code, 10) - 1;
      if (meteors[i]) {
        meteors[i] = null;
        hits++;
        whackFx.push({ x: CRATERS[i], t: 0, good: true });
        g.sfx.catchSound();
        g.setObjective('Whacked: ' + hits + '/' + NEED);
        if (hits >= NEED) {
          g.setObjective('All meteors whacked!');
          g.win();
          return;
        }
      } else {
        whiffT = 0.4;
        whackFx.push({ x: CRATERS[i], t: 0, good: false });
        g.sfx.buzz();
      }
    },

    update: function (g, dt) {
      whiffT = Math.max(0, whiffT - dt);
      spawnT -= dt;
      const interval = Math.max(0.75, 1.2 - g.t * (0.45 / 60));
      if (spawnT <= 0) {
        let pos = Math.floor(Math.random() * 4);
        if (pos === lastPos) pos = (pos + 1 + Math.floor(Math.random() * 3)) % 4;
        lastPos = pos;
        if (!meteors[pos]) {
          meteors[pos] = { t: 0, dur: Math.max(0.55, 1.0 - g.t * (0.45 / 60)) };
        }
        spawnT = interval;
      }
      for (let i = 0; i < 4; i++) {
        if (meteors[i]) {
          meteors[i].t += dt;
          if (meteors[i].t > meteors[i].dur) meteors[i] = null;
        }
      }
      for (let i = whackFx.length - 1; i >= 0; i--) {
        whackFx[i].t += dt;
        if (whackFx[i].t > 0.35) whackFx.splice(i, 1);
      }
    },

    draw: function (g, c) {
      // moon surface
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#20284a', '#0c1024']);
      c.fillRect(0, 0, 960, 640);
      // earth in the sky
      GT.gfx.glow(c, 120, 100, 60, 'rgba(127,200,255,0.8)');
      c.fillStyle = '#4a9fe0';
      c.beginPath();
      c.arc(120, 100, 34, 0, Math.PI * 2);
      c.fill();
      c.fillStyle = '#7fe08a';
      c.beginPath();
      c.ellipse(108, 92, 14, 8, 0.4, 0, Math.PI * 2);
      c.ellipse(132, 108, 10, 6, -0.3, 0, Math.PI * 2);
      c.fill();
      // stars
      const stars = [];
      for (let i = 0; i < 40; i++) {
        stars.push({ x: (i * 149) % 960, y: (i * 67) % 300, s: 1.4, ph: i });
      }
      GT.gfx.stars(c, stars, g.t);
      // ground
      c.fillStyle = '#3a3648';
      c.fillRect(0, 400, 960, 240);

      // craters
      for (let i = 0; i < 4; i++) {
        const x = CRATERS[i];
        c.fillStyle = '#2a2735';
        c.beginPath();
        c.ellipse(x, 430, 74, 26, 0, 0, Math.PI * 2);
        c.fill();
        c.strokeStyle = 'rgba(255,255,255,0.15)';
        c.lineWidth = 3;
        c.beginPath();
        c.ellipse(x, 430, 74, 26, 0, 0, Math.PI * 2);
        c.stroke();
        GT.gfx.text(c, String(i + 1), x, 434, { size: 20, color: 'rgba(255,255,255,0.4)' });
      }

      // meteors
      for (let i = 0; i < 4; i++) {
        const m = meteors[i];
        if (!m) continue;
        const x = CRATERS[i];
        const p = m.t / m.dur;
        const rise = Math.sin(Math.min(1, p) * Math.PI);
        const my = 400 - rise * 90;
        const urgency = p > 0.7;
        GT.gfx.glow(c, x, my, 40, urgency ? 'rgba(255,90,90,0.6)' : 'rgba(255,180,80,0.5)');
        GT.gfx.emoji(c, '☄️', x, my, 52);
        // remaining-time ring
        c.strokeStyle = urgency ? '#ff5d73' : '#ffb454';
        c.lineWidth = 5;
        c.beginPath();
        c.arc(x, 442, 66, -Math.PI / 2, -Math.PI / 2 + (1 - p) * Math.PI * 2);
        c.stroke();
      }

      // whack effects
      for (const fx of whackFx) {
        const p = fx.t / 0.35;
        if (fx.good) {
          c.strokeStyle = 'rgba(255,215,90,' + (1 - p).toFixed(2) + ')';
          c.lineWidth = 5;
          for (let k = 0; k < 6; k++) {
            const a = k * 1.05;
            c.beginPath();
            c.arc(fx.x + Math.cos(a) * p * 50, 410 + Math.sin(a) * p * 30, 3, 0, Math.PI * 2);
            c.stroke();
          }
        } else {
          GT.gfx.text(c, 'WHIFF!', fx.x, 350 - p * 20, {
            size: 22, color: 'rgba(255,255,255,' + (1 - p).toFixed(2) + ')',
          });
        }
      }

      // score
      GT.gfx.emoji(c, '☄️', 60, 60, 28);
      GT.gfx.text(c, hits + '/' + NEED, 104, 60, { size: 20, align: 'left' });
    },
  });
})();
