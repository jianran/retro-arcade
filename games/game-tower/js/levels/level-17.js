/* Level 17 — Tug of War 💪
 * Mash SPACE to pull the rope. Every press builds tension — mash too hard and
 * the rope snaps! The robot drags in phases, so pace yourself. Pull the knot
 * to your side to win.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const WIN_AT = 100;

  let knot = 50;         // 0 (robot side) .. 100 (your side)
  let tension = 0;       // 0..100; 100 = snap
  let aiPhaseT = 0;      // time into the current robot cycle
  let smokeFx = [];      // {x, t}
  let tauntT = 0;
  let taunt = '';

  const TAUNTS = ['Beep boop!', 'You call that pulling?', 'My motors are unbeatable!', 'Rope\'s getting warm…'];

  GT.registerLevel({
    name: 'Tug of War',
    icon: '💪',
    accent: '#ffb454',
    tagline: 'Out-pull the robot — but don\'t let the rope snap!',
    instructions: [
      'Mash SPACE to pull the knot toward you',
      'Every pull adds tension to the rope',
      'The robot drags back in phases — mash hard during its pulls',
      'Tension over 90% smokes, 100% snaps the rope. Pace yourself!',
    ],
    timeLimit: 70,

    enter: function (g) {
      knot = 50;
      tension = 0;
      aiPhaseT = 0;
      smokeFx = [];
      tauntT = 0;
      taunt = '';
      g.setObjective('Pull the knot to your side!');
    },

    onKey: function (g, code) {
      if (code !== ' ') return;
      knot = Math.min(WIN_AT, knot + 1.0);
      tension = Math.min(100, tension + 3.5);
      g.sfx.press();
      g.setObjective('Knot ' + Math.round(knot) + '%  ·  tension ' + Math.round(tension) + '%');
      if (tension >= 100) {
        g.fail('The rope snapped!');
        return;
      }
      if (knot >= WIN_AT) {
        g.setObjective('Victory!');
        g.sfx.success();
        g.win();
        return;
      }
    },

    update: function (g, dt) {
      // robot pull cycle: every 3.4s, drags for 2.0s
      aiPhaseT = (aiPhaseT + dt) % 3.4;
      if (aiPhaseT < 2.0) {
        knot = Math.max(0, knot - 2.2 * dt);
        if (Math.floor(aiPhaseT * 10) !== Math.floor((aiPhaseT - dt) * 10)) {
          // occasional robot grind sound
        }
      } else if (aiPhaseT - dt < 2.0 && Math.random() < 0.5) {
        taunt = TAUNTS[Math.floor(Math.random() * TAUNTS.length)];
        tauntT = 1.6;
      }
      // tension decays when not pressing (engine can't know, so decay always)
      tension = Math.max(0, tension - 4 * dt);
      tauntT = Math.max(0, tauntT - dt);

      if (tension > 90) {
        smokeFx.push({ x: 480 + (knot - 50) * 3, t: 0 });
      }
      for (let i = smokeFx.length - 1; i >= 0; i--) {
        smokeFx[i].t += dt;
        if (smokeFx[i].t > 0.7) smokeFx.splice(i, 1);
      }
    },

    draw: function (g, c) {
      // beach at midday
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#6fb8e8', '#cfe8ff']);
      c.fillRect(0, 0, 960, 640);
      GT.gfx.glow(c, 150, 80, 50, 'rgba(255,244,200,0.95)');
      GT.gfx.emoji(c, '☀️', 150, 80, 48);
      // sea
      c.fillStyle = 'rgba(42,127,174,0.85)';
      c.beginPath();
      c.moveTo(0, 640);
      for (let x = 0; x <= 960; x += 16) {
        c.lineTo(x, 500 + Math.sin(x * 0.03 + g.t * 2) * 8);
      }
      c.lineTo(960, 640);
      c.closePath();
      c.fill();
      // sand
      c.fillStyle = '#e8c98a';
      c.fillRect(0, 500, 960, 140);

      // rope
      const knotX = 160 + (knot / 100) * 640;
      c.strokeStyle = '#c9a86a';
      c.lineWidth = 9;
      c.lineCap = 'round';
      c.beginPath();
      c.moveTo(120, 420);
      c.quadraticCurveTo(480, 470 - tension * 0.25, 840, 420);
      c.stroke();
      // knot
      GT.gfx.glow(c, knotX, 420 + (knot - 50) * -0.01, 26, 'rgba(255,90,90,0.5)');
      c.fillStyle = '#d94a4a';
      c.beginPath();
      c.arc(knotX, 420, 16, 0, Math.PI * 2);
      c.fill();

      // smoke when rope is straining
      for (const s of smokeFx) {
        const p = s.t / 0.7;
        c.fillStyle = 'rgba(120,120,130,' + ((1 - p) * 0.5).toFixed(2) + ')';
        c.beginPath();
        c.arc(s.x + Math.sin(p * 9) * 8, 400 - p * 60, 6 + p * 14, 0, Math.PI * 2);
        c.fill();
      }

      // players
      GT.gfx.emoji(c, '💪', 130, 400, 64);
      const robotLean = aiPhaseT < 2.0 ? 10 : -4;
      GT.gfx.emoji(c, '🤖', 830, 400 + robotLean, 64);
      if (aiPhaseT < 2.0) GT.gfx.emoji(c, '⚙️', 870, 360, 26);

      // tension meter
      GT.gfx.text(c, 'ROPE TENSION', 480, 90, { size: 14, color: '#ffffff' });
      const tcol = tension > 90 ? '#ff5d73' : tension > 60 ? '#ffb454' : '#7fe08a';
      GT.gfx.bar(c, 480, 114, 380, 18, tension / 100, tcol, 'rgba(0,0,0,0.3)');
      if (tension > 90) {
        GT.gfx.text(c, '⚠ ROPE SMOKING!', 480, 148, {
          size: 20, color: '#ff5d73', stroke: '#0a0f1a', lineWidth: 4,
        });
      }

      // victory line
      c.strokeStyle = 'rgba(127,224,138,0.7)';
      c.lineWidth = 3;
      c.setLineDash([8, 8]);
      c.beginPath();
      c.moveTo(760, 380);
      c.lineTo(760, 470);
      c.stroke();
      c.setLineDash([]);
      GT.gfx.text(c, 'YOUR SIDE', 720, 356, { size: 13, color: '#7fe08a' });

      if (tauntT > 0) {
        GT.gfx.text(c, taunt, 830, 300, {
          size: 18, color: '#ffd75a', stroke: '#0a0f1a', lineWidth: 4,
        });
      }
    },
  });
})();
