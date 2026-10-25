/* Level 14 — Pasta Timer 🍝
 * No clock allowed! Press SPACE when exactly 12 seconds have passed since the
 * prompt. Within ±1.0s and the pasta is perfect. 3 attempts.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const TARGET = 13;
  const TOLERANCE = 1.0;
  const MAX_ATTEMPTS = 3;

  let attempt = 0;
  let phase = 'prompt';    // 'prompt' | 'result'
  let startT = 0;
  let resultT = 0;
  let verdict = '';
  let bestErr = null;
  let pendingFail = false;

  function startAttempt(g) {
    phase = 'prompt';
    startT = g.t;
    verdict = '';
    g.setObjective('Press SPACE at exactly ' + TARGET + ' seconds!');
  }

  GT.registerLevel({
    name: 'Pasta Timer',
    icon: '🍝',
    accent: '#ff8fb2',
    tagline: 'Count 13 seconds in your head — no clock allowed!',
    instructions: [
      'When the prompt appears, press SPACE after exactly 13 seconds',
      'No timer is shown — use the bubbling pot… and your instinct',
      'Within ±1.0 seconds and the pasta is perfect',
      'You get 3 attempts',
    ],
    timeLimit: 45,

    enter: function (g) {
      attempt = 0;
      bestErr = null;
      pendingFail = false;
      startAttempt(g);
    },

    onKey: function (g, code) {
      if (code !== ' ') return;
      if (phase === 'prompt') {
        const elapsed = g.t - startT;
        const err = elapsed - TARGET;
        const abs = Math.abs(err);
        if (abs <= TOLERANCE) {
          verdict = 'PERFECT! ' + elapsed.toFixed(1) + 's';
          g.setObjective(verdict);
          g.sfx.success();
          g.win();
          return;
        }
        verdict = elapsed.toFixed(1) + 's — too ' + (err < 0 ? 'early' : 'late') + '!';
        if (bestErr === null || abs < bestErr) bestErr = abs;
        attempt++;
        phase = 'result';
        resultT = 1.4;
        pendingFail = attempt >= MAX_ATTEMPTS;
        g.sfx.buzz();
        g.setObjective(verdict + '  ·  best: ' + bestErr.toFixed(1) + 's off');
      }
    },

    update: function (g, dt) {
      if (phase === 'result') {
        resultT -= dt;
        if (resultT <= 0) {
          if (pendingFail) {
            g.fail('Out of attempts — the pasta is mush!');
          } else {
            startAttempt(g);
          }
        }
      }
    },

    draw: function (g, c) {
      // kitchen
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#5a4038', '#2e211c']);
      c.fillRect(0, 0, 960, 640);
      // backsplash tiles
      c.strokeStyle = 'rgba(255,255,255,0.06)';
      c.lineWidth = 2;
      for (let x = 0; x < 960; x += 96) {
        c.beginPath();
        c.moveTo(x, 0);
        c.lineTo(x, 380);
        c.stroke();
      }
      // counter
      c.fillStyle = '#7a5236';
      c.fillRect(0, 430, 960, 210);
      c.fillStyle = '#5e3f2a';
      c.fillRect(0, 430, 960, 14);

      // stove + pot
      c.fillStyle = '#23262e';
      c.beginPath();
      c.roundRect(320, 330, 320, 100, 14);
      c.fill();
      for (let i = 0; i < 2; i++) {
        GT.gfx.glow(c, 395 + i * 170, 380, 34, 'rgba(255,120,60,0.55)');
      }
      GT.gfx.emoji(c, '🍲', 480, 330, 74);

      // bubbling steam (constant rate — reveals nothing!)
      for (let i = 0; i < 9; i++) {
        const p = ((g.t * 26 + i * 53) % 170) / 170;
        const sx = 450 + Math.sin(g.t * 3 + i * 2) * 22;
        const sy = 250 - p * 170;
        c.fillStyle = 'rgba(255,255,255,' + ((1 - p) * 0.4).toFixed(2) + ')';
        c.beginPath();
        c.arc(sx, sy, 5 + p * 13, 0, Math.PI * 2);
        c.fill();
      }

      // chef
      GT.gfx.emoji(c, '🧑‍🍳', 820, 380, 56);

      // prompt bubble
      c.fillStyle = 'rgba(10,14,24,0.8)';
      c.beginPath();
      c.roundRect(130, 70, 700, 74, 20);
      c.fill();
      c.strokeStyle = '#ff8fb2';
      c.lineWidth = 2;
      c.beginPath();
      c.roundRect(130, 70, 700, 74, 20);
      c.stroke();
      const msg = phase === 'prompt'
        ? 'Press SPACE at exactly ' + TARGET + ' seconds!'
        : verdict;
      GT.gfx.text(c, msg, 480, 108, { size: 24, color: '#ffd9e4' });

      // attempts left
      GT.gfx.text(c, 'ATTEMPTS LEFT', 480, 500, { size: 13, color: '#cbb09a' });
      for (let i = 0; i < MAX_ATTEMPTS; i++) {
        GT.gfx.emoji(c, i < MAX_ATTEMPTS - attempt ? '🍲' : '🫠',
          430 + i * 50, 532, 28);
      }
    },
  });
})();
