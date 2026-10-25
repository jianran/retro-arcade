/* Level 8 — Turtle Balance 🐢
 * The turtle wobbles on a rock with the waves. Hold ←/→ to lean against the
 * tilt — lean with the waves, not against them. Tip past ±30° and you're
 * turtle soup. Survive 40 seconds.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const LIMIT = 0.52;   // radians, ~30°
  const SURVIVE = 40;

  let angle = 0.05;
  let angVel = 0;
  let survived = 0;

  GT.registerLevel({
    name: 'Turtle Balance',
    icon: '🐢',
    accent: '#7fe08a',
    tagline: 'Keep the turtle upright on the rocking rock!',
    instructions: [
      'Waves and wobbles tilt the turtle',
      'Hold ← or → to lean the other way and fight the tilt',
      'Leaning the wrong way makes it tip faster — watch the gauge!',
      'Stay balanced for 40 seconds to win',
    ],
    timeLimit: 50,

    enter: function (g) {
      angle = 0.05;
      angVel = 0;
      survived = 0;
      g.setObjective('Keep balanced for ' + SURVIVE + 's');
    },

    update: function (g, dt) {
      let lean = 0;
      if (GT.input.held('arrowleft')) lean = -1;
      if (GT.input.held('arrowright')) lean = 1;

      const wave = Math.sin(g.t * 1.1 + 2.0) * (10 + g.t * 0.5);
      angVel += (lean * 22 + wave - angle * 55 - angVel * 6) * dt;
      angVel = Math.max(-3, Math.min(3, angVel));
      angle += angVel * dt;

      if (Math.abs(angle) > LIMIT) {
        g.fail('The turtle tipped over!');
        return;
      }
      survived += dt;
      g.setObjective('Balanced: ' + Math.floor(survived) + '/' + SURVIVE + 's');
      if (survived >= SURVIVE) {
        g.setObjective('Steady!');
        g.win();
      }
    },

    draw: function (g, c) {
      // beach at dusk
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#ff9d76', '#ffd9a0']);
      c.fillRect(0, 0, 960, 640);
      GT.gfx.glow(c, 820, 90, 46, 'rgba(255,240,200,0.9)');
      GT.gfx.emoji(c, '🌅', 820, 90, 44);

      // sea with animated waves
      c.fillStyle = GT.gfx.grad(c, 0, 420, 0, 640, ['#2a7fae', '#165d85']);
      c.beginPath();
      c.moveTo(0, 640);
      for (let x = 0; x <= 960; x += 16) {
        c.lineTo(x, 480 + Math.sin(x * 0.03 + g.t * 2) * 8);
      }
      c.lineTo(960, 640);
      c.closePath();
      c.fill();

      // sand
      c.fillStyle = '#e8c98a';
      c.fillRect(0, 520, 960, 120);

      // rock pedestal
      c.fillStyle = '#8d8a94';
      c.beginPath();
      c.ellipse(480, 500, 96, 30, 0, 0, Math.PI * 2);
      c.fill();
      c.fillStyle = '#6f6c76';
      c.beginPath();
      c.ellipse(480, 505, 84, 22, 0, 0, Math.PI * 2);
      c.fill();

      // turtle, rotated by tilt
      c.save();
      c.translate(480, 468);
      c.rotate(angle);
      if (Math.abs(angle) > 0.36) GT.gfx.emoji(c, '😰', 0, -64, 26);
      GT.gfx.emoji(c, '🐢', 0, 0, 74);
      c.restore();

      // tilt gauge
      const gx = 480, gy = 592, gr = 66;
      c.fillStyle = 'rgba(10,14,24,0.55)';
      c.beginPath();
      c.arc(gx, gy, gr, Math.PI, Math.PI * 2);
      c.fill();
      // safe zone (green arc) ±LIMIT
      const safeHalf = (LIMIT / 0.7) * (Math.PI / 2);
      c.strokeStyle = 'rgba(127,224,138,0.85)';
      c.lineWidth = 7;
      c.beginPath();
      c.arc(gx, gy, gr - 10, Math.PI * 1.5 - safeHalf, Math.PI * 1.5 + safeHalf);
      c.stroke();
      // danger ticks
      c.strokeStyle = 'rgba(255,93,115,0.8)';
      c.lineWidth = 4;
      for (let i = 0; i < 3; i++) {
        c.beginPath();
        c.arc(gx, gy, gr - 10, Math.PI + i * 0.1, Math.PI + i * 0.1 + 0.05);
        c.stroke();
        c.beginPath();
        c.arc(gx, gy, gr - 10, Math.PI * 2 - i * 0.1 - 0.05, Math.PI * 2 - i * 0.1);
        c.stroke();
      }
      // needle
      const needle = Math.PI * 1.5 + angle * (Math.PI / 2) / 0.7;
      c.strokeStyle = '#ffd75a';
      c.lineWidth = 4;
      c.lineCap = 'round';
      c.beginPath();
      c.moveTo(gx, gy);
      c.lineTo(gx + Math.cos(needle) * (gr - 18), gy + Math.sin(needle) * (gr - 18));
      c.stroke();

      // survival progress bar
      GT.gfx.text(c, 'BALANCE METER', 480, 100, { size: 14, color: '#5a3c28' });
      GT.gfx.bar(c, 480, 122, 320, 14, survived / SURVIVE, '#7fe08a', 'rgba(0,0,0,0.18)');
    },
  });
})();
