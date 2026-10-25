/* Level 7 — Berry Basket 🍓
 * Catch falling strawberries in your basket, dodge the bombs.
 * 14 berries wins; 3 bombs ends the level.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const NEED_BERRIES = 14;
  const MAX_BOMBS = 3;

  let items = [];        // {kind, x, y, vy, drift, hit}
  let basketX = 480;
  let berries = 0;
  let bombs = 0;
  let spawnT = 1.5;
  let shakeT = 0;
  let squish = [];       // {x, y, t}

  GT.registerLevel({
    name: 'Berry Basket',
    icon: '🍓',
    accent: '#ff8fb2',
    tagline: 'Catch the falling berries — but watch out for bombs!',
    instructions: [
      'Hold ← and → to move the basket',
      'Catch strawberries, dodge the bombs',
      '14 berries wins — 3 bombs and it\'s over!',
    ],
    timeLimit: 50,

    enter: function (g) {
      items = [];
      basketX = 480;
      berries = 0;
      bombs = 0;
      spawnT = 1.5;
      shakeT = 0;
      squish = [];
      g.setObjective('Berries: 0/' + NEED_BERRIES + '   Bombs: 0/' + MAX_BOMBS);
    },

    update: function (g, dt) {
      const dir = (GT.input.held('arrowleft') ? -1 : 0) + (GT.input.held('arrowright') ? 1 : 0);
      basketX = Math.max(80, Math.min(880, basketX + dir * 340 * dt));

      spawnT -= dt;
      const interval = Math.max(0.9, 1.5 - g.t * (0.6 / 45)); // ramps up
      if (spawnT <= 0) {
        items.push({
          kind: Math.random() < 0.30 ? 'bomb' : 'berry',
          x: 90 + Math.random() * 780,
          y: -30,
          vy: 165 + Math.random() * 45,
          drift: (Math.random() - 0.5) * 40,
          hit: false,
        });
        spawnT = interval;
      }

      for (const it of items) {
        it.y += it.vy * dt;
        it.x += it.drift * dt;
        if (it.y > 480 && it.y < 575 && Math.abs(it.x - basketX) < 72) {
          it.hit = true;
          if (it.kind === 'berry') {
            berries++;
            g.sfx.catchSound();
            squish.push({ x: it.x, y: it.y, t: 0 });
            g.setObjective('Berries: ' + berries + '/' + NEED_BERRIES +
              '   Bombs: ' + bombs + '/' + MAX_BOMBS);
            if (berries >= NEED_BERRIES) {
              g.setObjective('Basket full!');
              g.win();
              return;
            }
          } else {
            bombs++;
            shakeT = 0.5;
            g.sfx.buzz();
            g.setObjective('Berries: ' + berries + '/' + NEED_BERRIES +
              '   Bombs: ' + bombs + '/' + MAX_BOMBS);
            if (bombs >= MAX_BOMBS) {
              g.fail('Too many bombs!');
              return;
            }
          }
        }
      }
      items = items.filter(function (it) { return !it.hit && it.y < 660; });

      shakeT = Math.max(0, shakeT - dt);
      for (let i = squish.length - 1; i >= 0; i--) {
        squish[i].t += dt;
        if (squish[i].t > 0.4) squish.splice(i, 1);
      }
    },

    draw: function (g, c) {
      c.save();
      if (shakeT > 0) {
        c.translate(Math.sin(g.t * 90) * 7 * shakeT, Math.cos(g.t * 77) * 7 * shakeT);
      }

      // orchard
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#ffd9a0', '#ffb37a']);
      c.fillRect(0, 0, 960, 640);
      // canopy
      c.fillStyle = '#3f8f4f';
      for (let i = 0; i < 6; i++) {
        c.beginPath();
        c.ellipse(60 + i * 170, -20, 130, 90, 0, 0, Math.PI * 2);
        c.fill();
      }
      // ground
      c.fillStyle = '#8a5a3c';
      c.fillRect(0, 545, 960, 95);

      // basket
      GT.gfx.emoji(c, '🧺', basketX, 518, 52);

      // items
      for (const it of items) {
        if (it.kind === 'bomb') {
          GT.gfx.glow(c, it.x, it.y, 30, 'rgba(255,90,90,0.45)');
          GT.gfx.emoji(c, '💣', it.x, it.y, 40);
        } else {
          GT.gfx.emoji(c, '🍓', it.x, it.y, 40);
        }
      }

      // berry squish particles
      for (const s of squish) {
        const p = s.t / 0.4;
        c.strokeStyle = 'rgba(255,60,90,' + (1 - p).toFixed(2) + ')';
        c.lineWidth = 3;
        for (let i = 0; i < 5; i++) {
          const a = i * 1.26;
          c.beginPath();
          c.arc(s.x + Math.cos(a) * p * 46, s.y + Math.sin(a) * p * 30, 4, 0, Math.PI * 2);
          c.stroke();
        }
      }

      // counters
      GT.gfx.emoji(c, '🍓', 60, 50, 30);
      GT.gfx.text(c, berries + '/' + NEED_BERRIES, 100, 50, { size: 20, align: 'left' });
      GT.gfx.emoji(c, '💣', 850, 50, 30);
      GT.gfx.text(c, (MAX_BOMBS - bombs) + ' left', 892, 50, { size: 18, align: 'left' });

      c.restore();
    },
  });
})();
