/* Level 20 — Tower Top: The Crown 👑 (finale)
 * Phase A: time the swinging grappling hook — press SPACE when it passes over
 * the next ledge (windows shrink 70 → 50 → 35). 3 hooks to cross.
 * Phase B: type O P E N to open the stone door. The crown is yours.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const LEDGES = [120, 360, 600, 840];
  const TARGETS = [360, 600, 840];
  const WINDOWS = [70, 50, 35];
  const WORD = 'open';
  const PIVOT_Y = 150;
  const ROPE = 240;

  let phase = 'hook';    // 'hook' | 'word'
  let playerX = 120;
  let hooks = 0;
  let swingAnim = null;  // {fromX, toX, t}
  let word = '';
  let flashT = 0;
  let stars = [];

  GT.registerLevel({
    name: 'Tower Top: The Crown',
    icon: '👑',
    accent: '#ffd75a',
    tagline: 'The final floor — swing across and claim the crown!',
    instructions: [
      'Press SPACE when the grappling hook swings over the next ledge',
      'The timing window shrinks with each hook — 3 hooks to cross',
      'Then type O P E N to open the stone door',
      'A wrong letter resets the word',
    ],
    timeLimit: 90,

    enter: function (g) {
      phase = 'hook';
      playerX = 120;
      hooks = 0;
      swingAnim = null;
      word = '';
      flashT = 0;
      stars = [];
      for (let i = 0; i < 50; i++) {
        stars.push({ x: Math.random() * 960, y: Math.random() * 320, s: 1.5, ph: i });
      }
      g.setObjective('Grapple 0/3 — time your SPACE with the hook!');
    },

    onKey: function (g, code) {
      if (phase === 'hook') {
        if (swingAnim) return;
        if (code !== ' ') return;
        const swing = Math.sin(g.t * 3.1) * 1.08;
        const tipX = playerX + Math.sin(swing) * ROPE;
        const target = TARGETS[hooks];
        if (Math.abs(tipX - target) <= WINDOWS[hooks]) {
          swingAnim = { fromX: playerX, toX: target, t: 0 };
          g.sfx.catchSound();
        } else {
          flashT = 0.3;
          g.sfx.buzz();
        }
      } else {
        const key = code.toLowerCase();
        if (WORD[word.length] === key) {
          word += key;
          g.sfx.blipPitch(400 + word.length * 100);
          if (word.length === WORD.length) {
            g.setObjective('The crown is yours!');
            g.sfx.fanfare();
            g.win();
            return;
          }
          g.setObjective('Type the word: O P E N — so far ' + word.toUpperCase());
        } else if (/^[a-z]$/.test(key)) {
          word = '';
          g.sfx.buzz();
          g.setObjective('Type the word: O P E N');
        }
      }
    },

    update: function (g, dt) {
      flashT = Math.max(0, flashT - dt);
      if (swingAnim) {
        swingAnim.t += dt / 0.7;
        const p = Math.min(1, swingAnim.t);
        playerX = swingAnim.fromX + (swingAnim.toX - swingAnim.fromX) * p;
        if (p >= 1) {
          swingAnim = null;
          hooks++;
          if (hooks >= 3) {
            phase = 'word';
            g.setObjective('Type the word: O P E N');
          } else {
            g.setObjective('Grapple ' + hooks + '/3 — time your SPACE with the hook!');
          }
        }
      }
    },

    draw: function (g, c) {
      // night sky above the clouds
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#101a38', '#05070f']);
      c.fillRect(0, 0, 960, 640);
      GT.gfx.stars(c, stars, g.t);
      GT.gfx.glow(c, 860, 70, 44, 'rgba(255,250,220,0.9)');
      GT.gfx.emoji(c, '🌙', 860, 70, 40);
      // cloud sea below
      for (let x = -40; x < 1000; x += 130) {
        c.fillStyle = 'rgba(180,200,230,0.14)';
        c.beginPath();
        c.ellipse(x + Math.sin(g.t * 0.4 + x) * 10, 610, 90, 34, 0, 0, Math.PI * 2);
        c.fill();
      }

      // ledges
      for (let i = 0; i < LEDGES.length; i++) {
        const lx = LEDGES[i];
        c.fillStyle = '#4a5568';
        c.beginPath();
        c.roundRect(lx - 44, 430, 88, 90, 10);
        c.fill();
        c.fillStyle = '#5f6d82';
        c.beginPath();
        c.roundRect(lx - 44, 430, 88, 16, 8);
        c.fill();
        if (i === hooks + 1 && phase === 'hook') {
          GT.gfx.glow(c, lx, 444, 44, 'rgba(255,215,90,0.4)');
        }
      }

      // stone door on the last ledge
      if (phase === 'word') {
        c.fillStyle = '#3a4252';
        c.beginPath();
        c.roundRect(790, 170, 100, 260, 12);
        c.fill();
        c.strokeStyle = '#7a8498';
        c.lineWidth = 4;
        c.beginPath();
        c.roundRect(790, 170, 100, 260, 12);
        c.stroke();
        for (let i = 0; i < 4; i++) {
          const lit = i < word.length;
          c.fillStyle = lit ? 'rgba(255,215,90,0.35)' : 'rgba(0,0,0,0.4)';
          c.beginPath();
          c.roundRect(808, 190 + i * 56, 64, 44, 8);
          c.fill();
          c.strokeStyle = lit ? '#ffd75a' : '#5f6d82';
          c.lineWidth = 2;
          c.beginPath();
          c.roundRect(808, 190 + i * 56, 64, 44, 8);
          c.stroke();
          GT.gfx.text(c, lit ? word[i].toUpperCase() : WORD[i].toUpperCase(),
            840, 212 + i * 56, { size: 24, color: lit ? '#ffd75a' : '#8fa0bf' });
        }
      }

      // grappling rope + hook
      let tipX, tipY;
      if (swingAnim) {
        tipX = swingAnim.toX;
        tipY = 430;
      } else {
        const swing = Math.sin(g.t * 3.1) * 1.08;
        tipX = playerX + Math.sin(swing) * ROPE;
        tipY = PIVOT_Y + Math.cos(swing) * ROPE;
      }
      c.strokeStyle = 'rgba(255,255,255,0.5)';
      c.lineWidth = 3;
      c.beginPath();
      c.moveTo(playerX, PIVOT_Y);
      c.lineTo(tipX, tipY);
      c.stroke();
      if (phase === 'hook') {
        // timing window marker on the target ledge
        const target = TARGETS[hooks];
        const w = WINDOWS[hooks];
        c.fillStyle = 'rgba(127,224,138,0.25)';
        c.beginPath();
        c.roundRect(target - w, 452, w * 2, 26, 8);
        c.fill();
        c.strokeStyle = 'rgba(127,224,138,0.8)';
        c.lineWidth = 2;
        c.beginPath();
        c.roundRect(target - w, 452, w * 2, 26, 8);
        c.stroke();
      }
      GT.gfx.emoji(c, '🪝', tipX, tipY, 30);

      // player (the cat from floor 1, all grown up)
      const playerY = swingAnim
        ? 430 - Math.sin(Math.min(1, swingAnim.t) * Math.PI) * 160
        : 430;
      if (flashT > 0) GT.gfx.glow(c, playerX, playerY - 20, 36, 'rgba(255,93,115,0.5)');
      GT.gfx.emoji(c, '🐱', playerX, playerY - 24, 52);
      if (phase === 'word' && word.length === WORD.length) {
        GT.gfx.emoji(c, '👑', playerX, playerY - 64, 40);
      }

      if (phase === 'hook') {
        GT.gfx.text(c, 'GRAPPLES ' + hooks + '/3', 480, 70, {
          size: 18, color: '#8fa0bf',
        });
      }
    },
  });
})();
