/* Level 13 — Bees' Dance 🐝
 * Watch the bees dance across the flowers, then repeat the sequence with
 * Q W E R. Sequences grow from 2 to 8 steps. A wrong key replays the same
 * dance so you can retry.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const FLOWERS = [
    { key: 'q', x: 380, y: 200, emoji: '🌼' },
    { key: 'w', x: 380, y: 440, emoji: '🌻' },
    { key: 'e', x: 580, y: 200, emoji: '🌷' },
    { key: 'r', x: 580, y: 440, emoji: '🌸' },
  ];
  const MAX_LEN = 8;

  let seq = [];
  let len = 2;
  let phase = 'show';   // 'show' | 'input'
  let showIdx = 0;
  let lit = false;
  let showT = 0.5;
  let inputIdx = 0;
  let flashFlower = -1;
  let flashT = 0;

  function newSeq(n) {
    const s = [];
    for (let i = 0; i < n; i++) s.push(Math.floor(Math.random() * 4));
    return s;
  }

  function startShow() {
    phase = 'show';
    showIdx = 0;
    lit = false;
    showT = 0.5;
    inputIdx = 0;
  }

  GT.registerLevel({
    name: 'Bees\' Dance',
    icon: '🐝',
    accent: '#ffd75a',
    tagline: 'Watch the bees dance, then repeat the sequence!',
    instructions: [
      'Flowers are Q (top-left), W (bottom-left), E (top-right), R (bottom-right)',
      'Watch which flowers the bees visit, in order',
      'Then repeat the dance with Q W E R',
      'A wrong key replays the same dance — learn all 8 steps!',
    ],
    timeLimit: 70,

    enter: function (g) {
      len = 2;
      seq = newSeq(len);
      startShow();
      flashFlower = -1;
      flashT = 0;
      g.setObjective('Learn the dance! Length ' + len + '/' + MAX_LEN);
    },

    onKey: function (g, code) {
      if (phase !== 'input') return;
      let idx = -1;
      for (let i = 0; i < FLOWERS.length; i++) {
        if (FLOWERS[i].key === code) { idx = i; break; }
      }
      if (idx === -1) return;
      if (idx === seq[inputIdx]) {
        inputIdx++;
        flashFlower = idx;
        flashT = 0.35;
        g.sfx.blipPitch(400 + idx * 80);
        if (inputIdx >= len) {
          if (len >= MAX_LEN) {
            g.setObjective('The dance is complete!');
            g.sfx.success();
            g.win();
            return;
          }
          len++;
          seq = newSeq(len);
          startShow();
          g.setObjective('Dance learned! New length ' + len + '/' + MAX_LEN);
          g.sfx.catchSound();
        } else {
          g.setObjective('Step ' + inputIdx + '/' + len + ' — keep going!');
        }
      } else {
        g.sfx.buzz();
        g.setObjective('Oops! Watch the dance again…');
        startShow(); // replay the same sequence
      }
    },

    update: function (g, dt) {
      flashT = Math.max(0, flashT - dt);
      if (phase === 'show') {
        showT -= dt;
        if (showT <= 0) {
          if (lit) {
            lit = false;
            showIdx++;
            if (showIdx >= seq.length) {
              phase = 'input';
              inputIdx = 0;
              g.sfx.tick();
              g.setObjective('Your turn! Repeat the dance (' + len + ' steps)');
            } else {
              showT = 0.28;
            }
          } else {
            lit = true;
            showT = 0.42;
            g.sfx.blipPitch(400 + seq[showIdx] * 80);
          }
        }
      }
    },

    draw: function (g, c) {
      // hive interior
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#4a3518', '#2a1c0a']);
      c.fillRect(0, 0, 960, 640);

      // honeycomb pattern
      c.strokeStyle = 'rgba(255,200,90,0.12)';
      c.lineWidth = 2;
      for (let row = -1; row < 13; row++) {
        const off = (row % 2) * 30;
        for (let col = -1; col < 9; col++) {
          const hx = col * 120 + off;
          const hy = row * 52 + 20;
          c.beginPath();
          for (let k = 0; k < 6; k++) {
            const a = Math.PI / 6 + k * Math.PI / 3;
            const px = hx + Math.cos(a) * 34;
            const py = hy + Math.sin(a) * 34;
            if (k === 0) c.moveTo(px, py);
            else c.lineTo(px, py);
          }
          c.closePath();
          c.stroke();
        }
      }

      // flowers
      for (let i = 0; i < FLOWERS.length; i++) {
        const f = FLOWERS[i];
        const isLit = (phase === 'show' && lit && showIdx === i) ||
          (flashT > 0 && flashFlower === i);
        if (isLit) GT.gfx.glow(c, f.x, f.y, 52, 'rgba(255,215,90,0.6)');
        GT.gfx.emoji(c, f.emoji, f.x, f.y, 42);
        GT.gfx.text(c, f.key.toUpperCase(), f.x, f.y + 40, {
          size: 18, color: isLit ? '#ffd75a' : 'rgba(255,255,255,0.55)',
        });
        if (isLit) {
          const jx = Math.sin(g.t * 22) * 6;
          const jy = Math.sin(g.t * 17) * 5;
          GT.gfx.emoji(c, '🐝', f.x + jx, f.y - 40 + jy, 26);
        }
      }

      // input progress dots (your turn)
      if (phase === 'input') {
        for (let i = 0; i < len; i++) {
          c.fillStyle = i < inputIdx ? '#ffd75a' : 'rgba(255,255,255,0.2)';
          c.beginPath();
          c.arc(400 + i * 36, 80, 11, 0, Math.PI * 2);
          c.fill();
        }
      }

      // honey pot progress
      GT.gfx.emoji(c, '🍯', 480, 560, 40);
      GT.gfx.text(c, 'DANCE ' + (len - 1) + '/' + (MAX_LEN - 1), 480, 600, {
        size: 14, color: '#d6b06a',
      });
      GT.gfx.bar(c, 480, 620, 240, 12, (len - 1) / (MAX_LEN - 1), '#ffd75a',
        'rgba(255,255,255,0.10)');
    },
  });
})();
