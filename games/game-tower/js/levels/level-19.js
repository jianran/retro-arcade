/* Level 19 — Magnetic Rescue 🧲
 * The rescue ball rolls left to right on its own. Hold ↑ to pull it up with
 * the top magnet, hold ↓ to push it down. Guide it through three moving
 * gates. Gate hits bounce you back — no fail, just lost time.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const GATES = [
    { x: 350, openY: 180, openH: 104, ph: 0.0, hitT: 0 },
    { x: 650, openY: 450, openH: 104, ph: 1.7, hitT: 0 },
    { x: 950, openY: 260, openH: 104, ph: 3.4, hitT: 0 },
  ];

  let ballX = 80;
  let ballY = 320;
  let vy = 0;
  let sparkT = 0;
  let finished = false;

  GT.registerLevel({
    name: 'Magnetic Rescue',
    icon: '🧲',
    accent: '#7fc8ff',
    tagline: 'Steer the rescue ball through the gates with the magnets!',
    instructions: [
      'The ball rolls to the right on its own',
      'Hold ↑ to pull the ball up, hold ↓ to push it down',
      'The ball drifts back to the middle — keep steering',
      'The gate openings drift up and down — track them!',
      'Hit a gate and you bounce back. Reach the goal to win',
    ],
    timeLimit: 70,

    enter: function (g) {
      ballX = 80;
      ballY = 320;
      vy = 0;
      sparkT = 0;
      finished = false;
      for (const gate of GATES) gate.hitT = 0;
      g.setObjective('Guide the ball through all 3 gates!');
    },

    update: function (g, dt) {
      sparkT = Math.max(0, sparkT - dt);
      if (finished) return;

      const steer = (GT.input.held('arrowup') ? -1 : 0) +
        (GT.input.held('arrowdown') ? 1 : 0);
      vy += steer * 300 * dt;
      vy += ((320 - ballY) * 0.9 - vy * 2) * dt; // soft center pull + damping
      ballY += vy * dt;
      if (ballY < 70) { ballY = 70; vy *= -0.5; }
      if (ballY > 570) { ballY = 570; vy *= -0.5; }

      ballX += 110 * dt;

      for (const gate of GATES) {
        gate.hitT = Math.max(0, gate.hitT - dt);
        const openY = gate.openY + Math.sin(g.t * 0.8 + gate.ph) * 36;
        if (gate.hitT <= 0 && ballX > gate.x && ballX < gate.x + 20) {
          if (Math.abs(ballY - openY) > gate.openH / 2 + 14) {
            ballX = gate.x - 30;
            vy *= 0.4;
            gate.hitT = 0.5;
            sparkT = 0.4;
            g.sfx.buzz();
            g.setObjective('Bonk! Line up with the gate opening');
          }
        }
      }

      if (ballX > 940) {
        finished = true;
        g.setObjective('Rescued!');
        g.sfx.success();
        g.win();
      }
    },

    draw: function (g, c) {
      // lab
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#2a3548', '#161d2a']);
      c.fillRect(0, 0, 960, 640);
      // grid lines
      c.strokeStyle = 'rgba(255,255,255,0.05)';
      c.lineWidth = 1;
      for (let x = 0; x < 960; x += 48) {
        c.beginPath();
        c.moveTo(x, 0);
        c.lineTo(x, 640);
        c.stroke();
      }
      for (let y = 0; y < 640; y += 48) {
        c.beginPath();
        c.moveTo(0, y);
        c.lineTo(960, y);
        c.stroke();
      }

      // track bounds (hazard stripes)
      for (const y of [58, 582]) {
        c.save();
        c.beginPath();
        c.rect(0, y, 960, 24);
        c.clip();
        for (let x = -30; x < 990; x += 44) {
          c.fillStyle = (x / 44) % 2 === 0 ? '#d9a441' : '#232833';
          c.beginPath();
          c.moveTo(x, y);
          c.lineTo(x + 22, y);
          c.lineTo(x, y + 24);
          c.lineTo(x - 22, y + 24);
          c.closePath();
          c.fill();
        }
        c.restore();
      }

      // magnets
      const upOn = GT.input.held('arrowup');
      const downOn = GT.input.held('arrowdown');
      if (upOn) GT.gfx.glow(c, 480, 40, 46, 'rgba(127,200,255,0.6)');
      if (downOn) GT.gfx.glow(c, 480, 600, 46, 'rgba(127,200,255,0.6)');
      GT.gfx.emoji(c, '🧲', 480, 34, 40);
      GT.gfx.emoji(c, '🧲', 480, 606, 40);
      GT.gfx.text(c, '↑', 540, 36, { size: 22, color: upOn ? '#ffd75a' : '#8fa0bf' });
      GT.gfx.text(c, '↓', 540, 604, { size: 22, color: downOn ? '#ffd75a' : '#8fa0bf' });

      // gates (two bars each)
      for (const gate of GATES) {
        const openY = gate.openY + Math.sin(g.t * 0.8 + gate.ph) * 36;
        c.fillStyle = '#7a8498';
        c.beginPath();
        c.roundRect(gate.x - 12, 82, 24, openY - gate.openH / 2 - 82, 8);
        c.fill();
        c.beginPath();
        c.roundRect(gate.x - 12, openY + gate.openH / 2, 24,
          558 - (openY + gate.openH / 2), 8);
        c.fill();
        // opening indicator
        GT.gfx.glow(c, gate.x, openY, 26, 'rgba(127,224,138,0.3)');
      }

      // goal flag
      GT.gfx.emoji(c, '🏁', 920, 120, 34);

      // ball
      if (sparkT > 0) {
        GT.gfx.glow(c, ballX, ballY, 44, 'rgba(255,215,90,0.7)');
        GT.gfx.emoji(c, '⚡', ballX, ballY - 34, 24);
      }
      GT.gfx.glow(c, ballX, ballY, 28, 'rgba(255,255,255,0.5)');
      c.fillStyle = '#e9edf7';
      c.beginPath();
      c.arc(ballX, ballY, 16, 0, Math.PI * 2);
      c.fill();
      c.strokeStyle = '#8fa0bf';
      c.lineWidth = 2;
      c.beginPath();
      c.arc(ballX, ballY, 16, 0, Math.PI * 2);
      c.stroke();

      // gates passed counter
      let passed = 0;
      for (const gate of GATES) if (ballX > gate.x + 30) passed++;
      GT.gfx.text(c, 'GATES PASSED: ' + passed + '/3', 480, 120, {
        size: 15, color: '#8fa0bf',
      });
    },
  });
})();
