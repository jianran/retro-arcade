/* Level 12 — Laundry Line 🧺
 * Items slide along the sort line (up to 3 at once, fast!). Press the key
 * (1/2/3) of the matching bin while an item crosses the sort zone.
 * Sort 20 items to win.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const BINS = [
    { key: '1', color: '#ff5d73', label: 'RED', x: 250, emoji: '👕' },
    { key: '2', color: '#7fe08a', label: 'GREEN', x: 480, emoji: '👖' },
    { key: '3', color: '#7fc8ff', label: 'BLUE', x: 710, emoji: '🧦' },
  ];
  const ZONE_X = 430;
  const ZONE_HALF = 56;
  const NEED = 20;
  const SPEED = 380;

  let items = [];        // {bin, x, anim} — anim: {toX, toY, t} flying to a bin
  let spawnT = 0.3;
  let sorted = 0;
  let errT = 0;

  GT.registerLevel({
    name: 'Laundry Line',
    icon: '🧺',
    accent: '#c9a0ff',
    tagline: 'Sort the laundry into the right bins before it passes!',
    instructions: [
      'Items slide along the line: red shirts, green pants, blue socks',
      'Press 1 (red), 2 (green) or 3 (blue) while an item is in the sort zone',
      'Wrong bin = no credit and the item is wasted',
      'Sort 20 items to win',
    ],
    timeLimit: 50,

    enter: function (g) {
      items = [];
      spawnT = 0.3;
      sorted = 0;
      errT = 0;
      g.setObjective('Sorted: 0/' + NEED);
    },

    onKey: function (g, code) {
      if (code !== '1' && code !== '2' && code !== '3') return;
      const pressed = BINS[parseInt(code, 10) - 1];

      // in-zone items, sorted by distance to zone center
      const inZone = [];
      for (const it of items) {
        if (it.anim) continue;
        const d = Math.abs(it.x - ZONE_X);
        if (d <= ZONE_HALF) inZone.push({ it: it, d: d });
      }
      inZone.sort(function (a, b) { return a.d - b.d; });
      if (inZone.length === 0) { g.sfx.buzz(); return; }

      // the pressed key matches an in-zone item → sort it
      let target = null;
      for (const z of inZone) {
        if (z.it.bin.key === pressed.key) { target = z.it; break; }
      }
      if (target) {
        target.anim = { toX: pressed.x, toY: 545, t: 0 };
        sorted++;
        g.sfx.catchSound();
        g.setObjective('Sorted: ' + sorted + '/' + NEED);
        if (sorted >= NEED) {
          g.setObjective('All sorted!');
          g.win();
          return;
        }
      } else {
        // wrong bin: the nearest in-zone item falls into the pressed bin
        inZone[0].it.anim = { toX: pressed.x, toY: 545, t: 0 };
        errT = 0.5;
        g.sfx.buzz();
      }
    },

    update: function (g, dt) {
      errT = Math.max(0, errT - dt);
      spawnT -= dt;
      const interval = Math.max(0.28, 0.6 - g.t * (0.375 / 60));
      if (spawnT <= 0 && items.length < 3) {
        items.push({ bin: BINS[Math.floor(Math.random() * 3)], x: 990, anim: null });
        spawnT = interval;
      }
      for (let i = items.length - 1; i >= 0; i--) {
        const it = items[i];
        if (it.anim) {
          it.anim.t += dt / 0.18;
          if (it.anim.t >= 1) {
            items.splice(i, 1);
            spawnT = Math.min(spawnT, 0.2);
          }
        } else {
          it.x -= SPEED * dt;
          if (it.x < -60) items.splice(i, 1); // escaped past the zone
        }
      }
    },

    draw: function (g, c) {
      // laundry room
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#3d3054', '#241a38']);
      c.fillRect(0, 0, 960, 640);
      // clothesline decorations
      c.strokeStyle = 'rgba(255,255,255,0.25)';
      c.lineWidth = 2;
      c.beginPath();
      c.moveTo(0, 90);
      c.lineTo(960, 90);
      c.stroke();
      const deco = ['👕', '👖', '🧦', '👗', '🧢', '🩳', '🧣'];
      for (let i = 0; i < 7; i++) {
        GT.gfx.emoji(c, deco[i], 70 + i * 140, 108 + (i % 2) * 16, 22);
      }

      // conveyor
      c.fillStyle = 'rgba(255,255,255,0.08)';
      c.fillRect(0, 350, 960, 60);
      c.strokeStyle = 'rgba(255,255,255,0.3)';
      c.lineWidth = 3;
      c.beginPath();
      c.moveTo(0, 353);
      c.lineTo(960, 353);
      c.moveTo(0, 407);
      c.lineTo(960, 407);
      c.stroke();

      // sort zone
      const zoneFlash = errT > 0 ? 'rgba(255,93,115,0.5)' : 'rgba(201,160,255,0.30)';
      GT.gfx.glow(c, ZONE_X, 380, ZONE_HALF + 20, zoneFlash);
      c.strokeStyle = '#c9a0ff';
      c.setLineDash([6, 6]);
      c.lineWidth = 2;
      c.beginPath();
      c.moveTo(ZONE_X - ZONE_HALF, 320);
      c.lineTo(ZONE_X - ZONE_HALF, 440);
      c.moveTo(ZONE_X + ZONE_HALF, 320);
      c.lineTo(ZONE_X + ZONE_HALF, 440);
      c.stroke();
      c.setLineDash([]);

      // the items (with their key glyphs)
      for (const it of items) {
        let ix = it.x;
        let iy = 380;
        if (it.anim) {
          const t = it.anim.t;
          ix = it.x + (it.anim.toX - it.x) * t;
          iy = 380 + (it.anim.toY - 380) * t * t;
        }
        GT.gfx.emoji(c, it.bin.emoji, ix, iy, 44);
        if (!it.anim) {
          GT.gfx.text(c, it.bin.key, ix, iy - 44, {
            size: 26, color: it.bin.color, stroke: '#241a38', lineWidth: 4,
          });
        }
      }

      // bins
      for (const b of BINS) {
        c.fillStyle = b.color;
        c.globalAlpha = 0.22;
        c.beginPath();
        c.roundRect(b.x - 80, 520, 160, 80, 12);
        c.fill();
        c.globalAlpha = 1;
        c.strokeStyle = b.color;
        c.lineWidth = 3;
        c.beginPath();
        c.roundRect(b.x - 80, 520, 160, 80, 12);
        c.stroke();
        GT.gfx.emoji(c, b.emoji, b.x - 48, 560, 26);
        GT.gfx.text(c, b.label, b.x + 10, 548, { size: 15, color: b.color });
        GT.gfx.text(c, b.key, b.x + 10, 574, { size: 20, color: '#e9edf7' });
      }

      if (errT > 0) {
        GT.gfx.text(c, 'WRONG BIN!', 480, 270, {
          size: 40, color: '#ff5d73', stroke: '#241a38', lineWidth: 6,
        });
      }
    },
  });
})();
