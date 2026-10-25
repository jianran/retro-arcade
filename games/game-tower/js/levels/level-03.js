/* Level 3 — Climb the Ladder 🧗
 * Mash ↑ to climb. Stop pressing for ~1 second and you slide back down.
 * Reach the top, then press SPACE.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const RUNGS = 90;

  let rung = 0;
  let lastPressT = -10;
  let wobble = 0;

  GT.registerLevel({
    name: 'Climb the Ladder',
    icon: '🧗',
    accent: '#ffd75a',
    tagline: 'Mash ↑ to climb the cliff ladder — don\'t stop or you\'ll slide!',
    instructions: [
      'Keep pressing ↑ as fast as you can to climb the rope ladder',
      'If you pause for more than a second, you slide back down',
      'Reach the top, then press SPACE to finish',
    ],
    timeLimit: 45,

    enter: function (g) {
      rung = 0;
      lastPressT = -10;
      wobble = 0;
      g.setObjective('Rung 0/' + RUNGS);
    },

    onKey: function (g, code) {
      if (code !== 'arrowup') return;
      rung = Math.min(RUNGS, rung + 1);
      lastPressT = g.t;
      wobble = 1;
      g.sfx.blipPitch(320 + rung * 9);
      g.setObjective('Rung ' + Math.floor(rung) + '/' + RUNGS);
      if (rung >= RUNGS) {
        g.setGoal('The summit! Press SPACE to finish');
        g.sfx.success();
      }
    },

    update: function (g, dt) {
      if (g.t - lastPressT > 1.2) {
        rung = Math.max(0, rung - 1.2 * dt); // slide 1.2 rungs/s
      }
      wobble = Math.max(0, wobble - 5 * dt);
    },

    draw: function (g, c) {
      // night cliff face
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#1c2540', '#0e1324']);
      c.fillRect(0, 0, 960, 640);
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#26304f', '#171e33']);
      c.beginPath();
      c.moveTo(300, 0);
      c.lineTo(660, 0);
      c.lineTo(660, 640);
      c.lineTo(300, 640);
      c.closePath();
      c.fill();
      // stars
      const stars = [];
      for (let i = 0; i < 40; i++) {
        stars.push({ x: (i * 137) % 960, y: (i * 89) % 300, s: 1.5, ph: i });
      }
      GT.gfx.stars(c, stars, g.t);

      // summit flag
      c.strokeStyle = '#c9d4e4';
      c.lineWidth = 4;
      c.beginPath();
      c.moveTo(520, 90);
      c.lineTo(520, 30);
      c.stroke();
      GT.gfx.emoji(c, '🏁', 552, 36, 34);

      // ladder rails + rungs
      const railL = 420, railR = 510, top = 62, bottom = 600;
      c.strokeStyle = '#9a7b52';
      c.lineWidth = 5;
      c.beginPath();
      c.moveTo(railL, top);
      c.lineTo(railL, bottom);
      c.moveTo(railR, top);
      c.lineTo(railR, bottom);
      c.stroke();
      c.lineWidth = 3;
      for (let y = top + 9; y < bottom; y += 18) {
        c.beginPath();
        c.moveTo(railL, y);
        c.lineTo(railR, y);
        c.stroke();
      }

      // climber
      const climberY = 600 - (rung / RUNGS) * 538;
      const sliding = g.t - lastPressT > 1.2;
      GT.gfx.glow(c, 465, climberY, 30, 'rgba(255,215,90,0.35)');
      GT.gfx.emoji(c, '🧗', 465, climberY, 42);
      if (sliding) GT.gfx.emoji(c, '😰', 415, climberY, 24);

      // progress bar
      GT.gfx.text(c, 'SUMMIT', 830, 578, { size: 14, color: '#8fa0bf' });
      GT.gfx.bar(c, 830, 604, 240, 14, rung / RUNGS, '#ffd75a', 'rgba(255,255,255,0.10)');
    },
  });
})();
