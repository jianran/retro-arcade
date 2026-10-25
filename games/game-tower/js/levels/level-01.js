/* Level 1 — Wake the Cat 🐱
 * Press ← and → alternately to wave the silvervine stick. Same key twice = no
 * energy (the cat grumbles). At 250 energy the cat wakes and jumps — press SPACE.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const ENERGY_MAX = 250;

  let energy = 0;
  let lastKey = null;
  let awake = false;
  let jumpT = 0;
  let waveAngle = 0;      // spring-animated stick angle
  let waveImpulse = 0;    // decays after each press
  let grumbleT = 0;       // cat "grr" flash when the same key is pressed twice
  let penaltyT = 0;       // floating "-10" text after a mad-cat penalty

  GT.registerLevel({
    name: 'Wake the Cat',
    icon: '🐱',
    accent: '#ffb86c',
    tagline: 'Wave the silvervine stick to wake the sleeping cat!',
    instructions: [
      'Press ← and → alternately to wave the silvervine stick',
      'Same key twice makes the cat mad — you lose 10 wake-up power!',
      'When the cat is awake and jumping, press SPACE to finish',
    ],
    timeLimit: 90,

    enter: function (g) {
      energy = 0;
      lastKey = null;
      awake = false;
      jumpT = 0;
      waveAngle = 0;
      waveImpulse = 0;
      grumbleT = 0;
      penaltyT = 0;
      g.setObjective('Wave the stick! ' + energy + '/' + ENERGY_MAX);
    },

    onKey: function (g, code) {
      if (awake) return;
      if (code !== 'arrowleft' && code !== 'arrowright') return;
      if (lastKey !== null && code === lastKey) {
        // mad cat! repeating the same key costs wake-up power
        grumbleT = 0.6;
        penaltyT = 0.8;
        energy = Math.max(0, energy - 10);
        g.sfx.buzz();
        g.setObjective('Mad cat! -10 power · ' + energy + '/' + ENERGY_MAX);
        return;
      }
      lastKey = code;
      energy = Math.min(ENERGY_MAX, energy + 1);
      waveImpulse = code === 'arrowleft' ? 0.9 : -0.9;
      g.sfx.press();
      g.setObjective('Wave the stick! ' + energy + '/' + ENERGY_MAX);
      if (energy >= ENERGY_MAX) {
        awake = true;
        jumpT = 0;
        g.setGoal('The cat is awake! Press SPACE to finish');
        g.sfx.catchSound();
      }
    },

    update: function (g, dt) {
      if (awake) jumpT += dt;
      waveAngle += waveImpulse * 8 * dt;
      waveImpulse *= (1 - 7 * dt);
      waveAngle += -waveAngle * 8 * dt;
      if (grumbleT > 0) grumbleT -= dt;
      if (penaltyT > 0) penaltyT -= dt;
    },

    draw: function (g, c) {
      // night bedroom
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#141d3a', '#0b1024']);
      c.fillRect(0, 0, 960, 640);

      // window with moon
      c.fillStyle = '#1d2a52';
      c.beginPath();
      c.roundRect(640, 90, 220, 260, 16);
      c.fill();
      c.fillStyle = '#0e1529';
      c.fillRect(744, 90, 12, 260);
      c.fillRect(640, 212, 220, 12);
      GT.gfx.glow(c, 700, 160, 42, 'rgba(255,244,200,0.9)');
      GT.gfx.emoji(c, '🌙', 700, 160, 44);

      // floor + cushion
      c.fillStyle = '#241a33';
      c.fillRect(0, 520, 960, 120);
      c.fillStyle = '#3d2f52';
      c.beginPath();
      c.ellipse(320, 520, 190, 34, 0, 0, Math.PI * 2);
      c.fill();

      // sleeping / awake cat (base y bounces when awake)
      let catY = 470;
      if (awake) catY = 470 - Math.abs(Math.sin(jumpT * 7)) * 70;
      if (!awake) {
        // Zzz floating up
        for (let i = 0; i < 3; i++) {
          const zy = 380 - ((g.t * 22 + i * 34) % 90);
          GT.gfx.emoji(c, '💤', 320 + i * 26, zy, 20 + i * 5);
        }
      } else {
        // sparkles while jumping
        GT.gfx.glow(c, 250, catY - 40, 34, 'rgba(255,215,90,0.55)');
        GT.gfx.glow(c, 390, catY - 40, 34, 'rgba(255,215,90,0.55)');
      }
      if (grumbleT > 0) GT.gfx.emoji(c, '😾', 250, catY - 90, 34);
      if (penaltyT > 0) {
        const rise = (0.8 - penaltyT) * 50;
        GT.gfx.text(c, '-10', 390, catY - 100 - rise, {
          size: 34, color: '#ff5d73', stroke: '#0a0f1a', lineWidth: 5,
        });
      }
      GT.gfx.emoji(c, awake ? '🐱' : '🐱', 320, catY, 88);

      // silvervine stick dangling from top-right, waving with waveAngle
      const sway = Math.sin(g.t * 3) * 0.12 + waveAngle;
      c.save();
      c.translate(700, 60);
      c.rotate(sway);
      c.strokeStyle = '#8b5a2b';
      c.lineWidth = 9;
      c.lineCap = 'round';
      c.beginPath();
      c.moveTo(0, 0);
      c.lineTo(150, 180);
      c.stroke();
      // silvervine leaves at the tip
      c.fillStyle = '#6fbf5a';
      c.beginPath();
      c.ellipse(158, 192, 20, 9, 0.5, 0, Math.PI * 2);
      c.fill();
      c.beginPath();
      c.ellipse(132, 196, 18, 8, -0.5, 0, Math.PI * 2);
      c.fill();
      c.beginPath();
      c.ellipse(172, 168, 16, 7, 0.9, 0, Math.PI * 2);
      c.fill();
      c.restore();

      // wake-energy bar
      GT.gfx.text(c, 'WAKE-UP POWER', 480, 578, { size: 15, color: '#8fa0bf' });
      GT.gfx.bar(c, 480, 604, 320, 16, energy / ENERGY_MAX, '#ffb86c', 'rgba(255,255,255,0.10)');

      // hint arrows
      if (!awake) {
        const bob = Math.abs(Math.sin(g.t * 4)) * 8;
        GT.gfx.emoji(c, '⬅️', 170, 440 - bob, 30);
        GT.gfx.emoji(c, '➡️', 210, 440 - bob, 30);
      }
    },
  });
})();
