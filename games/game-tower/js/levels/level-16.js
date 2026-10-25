/* Level 16 — Sphinx Math 🐫
 * Solve the stone tablet's sums. Type the answer with number keys,
 * Backspace to fix, Enter to submit. 8 correct answers opens the door.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const NEED = 8;

  let a = 0, b = 0, op = '+', ans = 0;
  let typed = '';
  let correct = 0;
  let shakeT = 0;
  let crumbleFx = [];    // {x, y, t}

  function newProblem() {
    const r = Math.random();
    if (r < 0.4) {
      op = '-';
      a = 5 + Math.floor(Math.random() * 26);
      b = 5 + Math.floor(Math.random() * 26);
      if (a < b) { const tmp = a; a = b; b = tmp; }
      ans = a - b;
    } else if (r < 0.65) {
      op = '+';
      a = 5 + Math.floor(Math.random() * 26);
      b = 5 + Math.floor(Math.random() * 26);
      ans = a + b;
    } else {
      op = '×';
      a = 3 + Math.floor(Math.random() * 7);
      b = 3 + Math.floor(Math.random() * 7);
      ans = a * b;
    }
  }

  GT.registerLevel({
    name: 'Sphinx Math',
    icon: '🐫',
    accent: '#ffb454',
    tagline: 'Answer the Sphinx\'s stone-tablet riddles!',
    instructions: [
      'The stone tablet shows a maths riddle — type the answer with the number keys',
      'Backspace fixes a typo, Enter submits',
      'Solve 8 tablets to open the hall door',
    ],
    timeLimit: 70,

    enter: function (g) {
      newProblem();
      typed = '';
      correct = 0;
      shakeT = 0;
      crumbleFx = [];
      g.setObjective('Tablets solved: 0/' + NEED);
    },

    onKey: function (g, code) {
      if (/^[0-9]$/.test(code)) {
        if (typed.length < 3) {
          typed += code;
          g.sfx.blipPitch(300 + typed.length * 100);
        }
        return;
      }
      if (code === 'backspace') {
        typed = typed.slice(0, -1);
        g.sfx.blip();
        return;
      }
      if (code === 'enter') {
        if (typed === '') return;
        if (parseInt(typed, 10) === ans) {
          correct++;
          g.sfx.catchSound();
          g.setObjective('Tablets solved: ' + correct + '/' + NEED);
          // tablet crumble
          crumbleFx.push({ x: 480, y: 300, t: 0 });
          if (correct >= NEED) {
            g.setObjective('The door opens!');
            g.sfx.success();
            g.win();
            return;
          }
          newProblem();
          typed = '';
        } else {
          shakeT = 0.5;
          g.sfx.buzz();
          typed = '';
        }
      }
    },

    update: function (g, dt) {
      shakeT = Math.max(0, shakeT - dt);
      for (let i = crumbleFx.length - 1; i >= 0; i--) {
        crumbleFx[i].t += dt;
        if (crumbleFx[i].t > 0.8) crumbleFx.splice(i, 1);
      }
    },

    draw: function (g, c) {
      c.save();
      if (shakeT > 0) {
        c.translate(Math.sin(g.t * 70) * 6 * shakeT, Math.cos(g.t * 63) * 6 * shakeT);
      }

      // Egyptian hall
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#b08348', '#6e4f26']);
      c.fillRect(0, 0, 960, 640);
      // pillars
      for (let i = 0; i < 4; i++) {
        c.fillStyle = '#8a6436';
        c.fillRect(90 + i * 260, 0, 56, 640);
        c.fillStyle = '#a37b46';
        c.fillRect(100 + i * 260, 0, 14, 640);
        c.fillRect(126 + i * 260, 0, 14, 640);
      }
      // hieroglyph frieze
      c.fillStyle = 'rgba(60,40,10,0.5)';
      c.fillRect(0, 0, 960, 40);
      GT.gfx.text(c, '𓀀 𓀁 𓀂 𓀃 𓀄', 480, 22, { size: 22, color: '#3c280a' });

      // sphinx
      GT.gfx.emoji(c, '🐫', 150, 480, 90);

      // stone tablet
      c.fillStyle = '#d9c9a8';
      c.beginPath();
      c.roundRect(330, 200, 300, 200, 18);
      c.fill();
      c.strokeStyle = '#8a7448';
      c.lineWidth = 6;
      c.beginPath();
      c.roundRect(330, 200, 300, 200, 18);
      c.stroke();
      GT.gfx.text(c, a + ' ' + op + ' ' + b + ' = ?', 480, 268, {
        size: 52, color: '#4a3c20',
      });
      GT.gfx.text(c, typed === '' ? '···' : typed, 480, 338, {
        size: 48, color: typed === '' ? '#a89870' : '#c0452c',
      });

      // door (opens as you solve)
      const open = Math.min(1, correct / NEED);
      c.fillStyle = '#5e4a2a';
      c.beginPath();
      c.roundRect(690, 120, 220, 400, 14);
      c.fill();
      c.fillStyle = '#2a1c0a';
      c.beginPath();
      c.roundRect(710, 140, 180, 360 * (1 - open), 10);
      c.fill();
      c.strokeStyle = '#d9c9a8';
      c.lineWidth = 3;
      for (let i = 0; i < 4; i++) {
        c.beginPath();
        c.arc(752, 180 + i * 80, 18, 0, Math.PI * 2);
        c.stroke();
      }

      // crumble particles
      for (const fx of crumbleFx) {
        const p = fx.t / 0.8;
        for (let i = 0; i < 8; i++) {
          const a = i * 0.785 + p;
          const r = 30 + p * 90;
          c.fillStyle = 'rgba(217,201,168,' + (1 - p).toFixed(2) + ')';
          c.beginPath();
          c.arc(fx.x + Math.cos(a) * r, fx.y + Math.sin(a) * r * 0.7 + p * 60, 4 + p * 6, 0, Math.PI * 2);
          c.fill();
        }
      }

      // progress
      GT.gfx.text(c, 'TABLETS SOLVED', 480, 500, { size: 14, color: '#e8d9b8' });
      GT.gfx.bar(c, 480, 526, 300, 14, correct / NEED, '#ffb454', 'rgba(0,0,0,0.25)');
      GT.gfx.text(c, 'Type answer · Enter to submit · Backspace to fix', 480, 580, {
        size: 16, color: 'rgba(255,255,255,0.55)',
      });

      c.restore();
    },
  });
})();
