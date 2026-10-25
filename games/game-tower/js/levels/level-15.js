/* Level 15 — Station Repair 🔧
 * A dial hand spins at a constant speed. Press SPACE to clamp it while the
 * hand is inside the green zone. Each leak's dial is faster and the zone
 * smaller. A miss stuns you for 2 seconds. Seal all 4 leaks.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const SPEEDS = [1.7, 2.2, 2.8, 3.4];       // rad/s per leak
  const ZONE_HALF = [45, 34, 23, 18];        // degrees per leak
  const LEAK_POS = [[300, 190], [660, 190], [300, 450], [660, 450]];
  const TWO_PI = Math.PI * 2;

  let leak = 0;
  let dialAngle = 0;
  let zoneCenter = 0;
  let stunT = 0;
  let sparkT = 0;

  function startLeak() {
    dialAngle = Math.random() * TWO_PI;
    zoneCenter = 1.5 + Math.random() * 3.3; // rad, avoids the 0 wrap
    stunT = 0;
    sparkT = 0;
  }

  GT.registerLevel({
    name: 'Station Repair',
    icon: '🔧',
    accent: '#c9a0ff',
    tagline: 'Clamp the spinning dial inside the green zone to seal the leaks!',
    instructions: [
      'The dial hand spins at a constant speed',
      'Press SPACE while the hand is inside the green zone',
      'A miss sparks and stuns you for 2 seconds',
      'Each leak spins faster with a smaller zone — seal all 4!',
    ],
    timeLimit: 70,

    enter: function (g) {
      leak = 0;
      startLeak();
      g.setObjective('Seal leak 1/4');
    },

    onKey: function (g, code) {
      if (code !== ' ') return;
      if (stunT > 0) return;
      const a = ((dialAngle % TWO_PI) + TWO_PI) % TWO_PI;
      const h = ZONE_HALF[leak] * Math.PI / 180;
      let dz = Math.abs(a - zoneCenter);
      if (dz > Math.PI) dz = TWO_PI - dz;
      if (dz <= h) {
        leak++;
        g.sfx.catchSound();
        if (leak >= 4) {
          g.setObjective('All leaks sealed!');
          g.win();
          return;
        }
        startLeak();
        g.setObjective('Seal leak ' + (leak + 1) + '/4');
      } else {
        stunT = 2.5;
        sparkT = 0.6;
        g.sfx.buzz();
        g.setObjective('Sparks! Wait for the stun to clear…');
      }
    },

    update: function (g, dt) {
      dialAngle += SPEEDS[leak] * dt;
      stunT = Math.max(0, stunT - dt);
      sparkT = Math.max(0, sparkT - dt);
    },

    draw: function (g, c) {
      c.save();
      if (sparkT > 0) {
        c.translate(Math.sin(g.t * 80) * 5, Math.cos(g.t * 70) * 5);
      }

      // station panel
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#3a4252', '#232833']);
      c.fillRect(0, 0, 960, 640);
      // rivets
      c.fillStyle = 'rgba(255,255,255,0.14)';
      for (let x = 30; x < 960; x += 90) {
        for (let y = 26; y < 640; y += 84) {
          c.beginPath();
          c.arc(x, y, 4, 0, TWO_PI);
          c.fill();
        }
      }
      // warning stripes
      c.save();
      c.beginPath();
      c.rect(0, 0, 960, 26);
      c.clip();
      for (let x = -30; x < 990; x += 60) {
        c.fillStyle = (x / 60) % 2 === 0 ? '#d9a441' : '#232833';
        c.beginPath();
        c.moveTo(x, 0);
        c.lineTo(x + 30, 0);
        c.lineTo(x, 26);
        c.lineTo(x - 30, 26);
        c.closePath();
        c.fill();
      }
      c.restore();

      // leak markers
      for (let i = 0; i < 4; i++) {
        const p = LEAK_POS[i];
        if (i < leak) {
          c.fillStyle = '#2f9e5a';
          c.beginPath();
          c.arc(p[0], p[1], 22, 0, TWO_PI);
          c.fill();
          GT.gfx.text(c, '✓', p[0], p[1], { size: 22, color: '#0a2413' });
        } else if (i === leak) {
          GT.gfx.glow(c, p[0], p[1], 34, 'rgba(255,90,90,0.5)');
          c.strokeStyle = '#ff5d5d';
          c.lineWidth = 3;
          c.beginPath();
          c.arc(p[0], p[1], 22, 0, TWO_PI);
          c.stroke();
          GT.gfx.emoji(c, '💨', p[0], p[1], 26);
        } else {
          c.strokeStyle = 'rgba(255,255,255,0.2)';
          c.lineWidth = 3;
          c.beginPath();
          c.arc(p[0], p[1], 22, 0, TWO_PI);
          c.stroke();
        }
      }

      // dial
      const dx = 480, dy = 340, dr = 92;
      c.fillStyle = '#4d5568';
      c.beginPath();
      c.arc(dx, dy, dr, 0, TWO_PI);
      c.fill();
      c.strokeStyle = '#7a8498';
      c.lineWidth = 5;
      c.beginPath();
      c.arc(dx, dy, dr, 0, TWO_PI);
      c.stroke();
      // tick marks
      for (let i = 0; i < 24; i++) {
        const a = i * TWO_PI / 24;
        c.strokeStyle = 'rgba(255,255,255,0.25)';
        c.lineWidth = 2;
        c.beginPath();
        c.moveTo(dx + Math.cos(a) * (dr - 10), dy + Math.sin(a) * (dr - 10));
        c.lineTo(dx + Math.cos(a) * (dr - 18), dy + Math.sin(a) * (dr - 18));
        c.stroke();
      }
      // green target zone
      const h = ZONE_HALF[leak] * Math.PI / 180;
      c.strokeStyle = '#5fe08a';
      c.lineWidth = 12;
      c.beginPath();
      c.arc(dx, dy, dr - 30, zoneCenter - h, zoneCenter + h);
      c.stroke();
      // dial hand
      c.strokeStyle = '#ffd75a';
      c.lineWidth = 6;
      c.lineCap = 'round';
      c.beginPath();
      c.moveTo(dx, dy);
      c.lineTo(dx + Math.cos(dialAngle) * (dr - 34), dy + Math.sin(dialAngle) * (dr - 34));
      c.stroke();
      c.fillStyle = '#ffd75a';
      c.beginPath();
      c.arc(dx, dy, 9, 0, TWO_PI);
      c.fill();

      // stun effect
      if (stunT > 0) {
        GT.gfx.emoji(c, '⚡', dx + 60, dy - 60, 44);
        GT.gfx.text(c, 'STUNNED ' + stunT.toFixed(1), dx, dy - dr - 26, {
          size: 20, color: '#ffd75a',
        });
      }

      c.restore();
    },
  });
})();
