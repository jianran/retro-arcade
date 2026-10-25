/* Level 10 — Frog Pond Leap 🐸
 * Hold SPACE to charge your jump, release to leap. Land on the next lily pad.
 * Short or long and you splash back — progress is never lost, only time.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const PADS = [
    { x: 140, r: 42 },
    { x: 340, r: 38 },
    { x: 540, r: 34 },
    { x: 700, r: 31 },
    { x: 820, r: 28 },
    { x: 930, r: 27 },
  ];
  const PAD_Y = 430;
  const JUMP_MIN = 40;
  const JUMP_RANGE = 240;

  let pad = 0;          // current pad index
  let power = 0;        // 0..1 charge
  let charging = false;
  let lastStep = 0;
  let jump = null;      // {from, to, t} while in the air
  let lockT = 0;        // input lock after a splash
  let splashFx = [];    // {x, t}

  GT.registerLevel({
    name: 'Frog Pond Leap',
    icon: '🐸',
    accent: '#7fe08a',
    tagline: 'Charge your jump and hop across the lily pads!',
    instructions: [
      'Hold SPACE to charge your jump power',
      'Release SPACE to leap toward the next lily pad',
      'Land on the pad to advance — splash down and you try again',
      'Cross all 6 lily pads to win',
    ],
    timeLimit: 65,

    enter: function (g) {
      pad = 0;
      power = 0;
      charging = false;
      lastStep = 0;
      jump = null;
      lockT = 0;
      splashFx = [];
      g.setObjective('Pad 1/' + PADS.length);
    },

    update: function (g, dt) {
      if (jump) {
        jump.t += dt / 0.5;
        if (jump.t >= 1) {
          const land = jump.from + JUMP_MIN + jump.power * JUMP_RANGE;
          const next = PADS[pad + 1];
          if (Math.abs(land - next.x) < next.r) {
            pad++;
            g.sfx.blipPitch(380 + pad * 70);
            g.setObjective('Pad ' + (pad + 1) + '/' + PADS.length);
            if (pad >= PADS.length - 1) {
              g.setObjective('Across the pond!');
              g.win();
              return;
            }
          } else {
            splashFx.push({ x: land, t: 0 });
            g.sfx.splash();
            lockT = 1.5;
            g.setObjective('Splash! Pad ' + (pad + 1) + '/' + PADS.length + ' — try again');
          }
          jump = null;
          power = 0;
          charging = false;
        }
        return;
      }

      lockT = Math.max(0, lockT - dt);
      if (lockT > 0) return;

      if (GT.input.held(' ')) {
        if (!charging) {
          charging = true;
          power = 0;
          lastStep = 0;
        }
        power = Math.min(1, power + dt / 1.2);
        const step = Math.floor(power * 4);
        if (step > lastStep) {
          lastStep = step;
          g.sfx.blipPitch(260 + step * 120);
        }
      } else if (charging) {
        // release!
        jump = { from: PADS[pad].x, to: 0, t: 0, power: power };
        g.sfx.press();
        charging = false;
      }

      for (let i = splashFx.length - 1; i >= 0; i--) {
        splashFx[i].t += dt;
        if (splashFx[i].t > 0.6) splashFx.splice(i, 1);
      }
    },

    draw: function (g, c) {
      // pond
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#3fa8a0', '#1c6a6a']);
      c.fillRect(0, 0, 960, 640);
      GT.gfx.glow(c, 880, 80, 44, 'rgba(255,244,200,0.9)');
      GT.gfx.emoji(c, '☀️', 880, 80, 42);

      // water shimmer lines
      c.strokeStyle = 'rgba(255,255,255,0.10)';
      c.lineWidth = 2;
      for (let i = 0; i < 6; i++) {
        const y = 90 + i * 90;
        c.beginPath();
        for (let x = 0; x <= 960; x += 20) {
          const yy = y + Math.sin(x * 0.04 + g.t * 1.6 + i) * 5;
          if (x === 0) c.moveTo(x, yy);
          else c.lineTo(x, yy);
        }
        c.stroke();
      }

      // lily pads
      for (let i = 0; i < PADS.length; i++) {
        const p = PADS[i];
        const bob = Math.sin(g.t * 2 + i) * 4;
        c.fillStyle = i === pad + 1 ? '#5fbf5a' : '#3f8f4a';
        c.beginPath();
        c.ellipse(p.x, PAD_Y + bob, p.r, p.r * 0.42, 0, 0, Math.PI * 2);
        c.fill();
        if (i === pad + 1) {
          GT.gfx.glow(c, p.x, PAD_Y + bob, p.r + 16, 'rgba(127,224,138,0.35)');
        }
      }

      // frog (mid-jump arc or on pad)
      let fx, fy;
      if (jump) {
        const t = jump.t;
        const from = jump.from;
        const to = from + JUMP_MIN + jump.power * JUMP_RANGE;
        fx = from + (to - from) * t;
        fy = PAD_Y - Math.sin(t * Math.PI) * 110;
      } else {
        fx = PADS[pad].x;
        fy = PAD_Y + Math.sin(g.t * 2 + pad) * 4;
      }
      if (lockT > 0) GT.gfx.emoji(c, '💫', fx + 30, fy - 30, 24);
      GT.gfx.emoji(c, '🐸', fx, fy, 46);

      // splash rings
      for (const s of splashFx) {
        const r = 8 + s.t * 70;
        c.strokeStyle = 'rgba(255,255,255,' + (0.8 - s.t).toFixed(2) + ')';
        c.lineWidth = 3;
        c.beginPath();
        c.arc(s.x, PAD_Y + 10, r, 0, Math.PI * 2);
        c.stroke();
      }

      // power meter
      GT.gfx.text(c, 'JUMP POWER', 480, 578, { size: 14, color: '#d6f5ef' });
      GT.gfx.bar(c, 480, 602, 320, 16, power, charging ? '#ffd75a' : '#7fe08a',
        'rgba(255,255,255,0.15)');
    },
  });
})();
