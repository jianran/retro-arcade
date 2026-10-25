/* Level 5 — Drum Solo 🥁
 * Notes fall toward the hit zone. Press SPACE when a note reaches the ring
 * (±100 ms counts). Hit 14 notes to finish the song.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const N_NOTES = 14;
  const BPM = 128;          // ~0.47 s between notes
  const HIT_Y = 470;
  const FALL_SPEED = 170;
  const COLORS = ['#ff5d73', '#ffb454', '#ffd75a', '#7fe08a', '#7fc8ff', '#c9a0ff'];

  let notes = [];          // {at, done, color}
  let hits = 0;
  let streak = 0;
  let stickT = 0;          // stick bounce anim
  let flash = '';
  let flashT = 0;

  function hexToRgba(hex, a) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g2 = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return 'rgba(' + r + ',' + g2 + ',' + b + ',' + a + ')';
  }

  GT.registerLevel({
    name: 'Drum Solo',
    icon: '🥁',
    accent: '#ff5d73',
    tagline: 'Hit the falling notes in time to finish the song!',
    instructions: [
      'Notes fall toward the glowing ring',
      'Press SPACE exactly when a note reaches the ring',
      'PERFECT within a tiny window, GOOD still counts, MISS breaks your streak',
      'Hit all 14 notes to finish the solo',
    ],
    timeLimit: 60,

    enter: function (g) {
      notes = [];
      for (let i = 0; i < N_NOTES; i++) {
        notes.push({
          at: 2.0 + i * (60 / BPM),
          done: false,
          color: COLORS[i % COLORS.length],
        });
      }
      hits = 0;
      streak = 0;
      stickT = 0;
      flash = '';
      flashT = 0;
      g.setObjective('Hits: 0/' + N_NOTES);
    },

    onKey: function (g, code) {
      if (code !== ' ') return;
      let best = null;
      let bd = 1e9;
      for (const n of notes) {
        const d = Math.abs(n.at - g.t);
        if (!n.done && d <= 0.10 && d < bd) { bd = d; best = n; }
      }
      if (best) {
        best.done = true;
        hits++;
        streak++;
        stickT = 0.18;
        const err = Math.abs(best.at - g.t);
        flash = err <= 0.05 ? 'PERFECT!' : 'GOOD!';
        flashT = 0.5;
        g.sfx.drum();
        g.setObjective('Hits: ' + hits + '/' + N_NOTES +
          (streak >= 3 ? '  🔥 streak ' + streak : ''));
        if (hits >= N_NOTES) g.win();
      } else {
        streak = 0;
        flash = 'MISS';
        flashT = 0.4;
        g.sfx.buzz();
      }
    },

    update: function (g, dt) {
      stickT = Math.max(0, stickT - dt);
      flashT = Math.max(0, flashT - dt);
      // auto-miss notes that passed the zone
      for (const n of notes) {
        if (!n.done && g.t > n.at + 0.25) {
          n.done = true;
          streak = 0;
        }
      }
    },

    draw: function (g, c) {
      // stage with spotlights
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#2a1140', '#120a1e']);
      c.fillRect(0, 0, 960, 640);
      for (let i = 0; i < 3; i++) {
        const sx = 160 + i * 320;
        c.fillStyle = 'rgba(255,180,120,0.10)';
        c.beginPath();
        c.moveTo(sx - 90, 0);
        c.lineTo(sx + 90, 0);
        c.lineTo(sx + 220, 640);
        c.lineTo(sx - 220, 640);
        c.closePath();
        c.fill();
      }

      // drum kit
      c.fillStyle = '#3d2f52';
      c.beginPath();
      c.ellipse(250, 500, 90, 70, 0, 0, Math.PI * 2);
      c.fill();
      c.strokeStyle = '#c9d4e4';
      c.lineWidth = 4;
      c.beginPath();
      c.ellipse(250, 500, 90, 70, 0, 0, Math.PI * 2);
      c.stroke();
      c.beginPath();
      c.ellipse(250, 500, 58, 44, 0, 0, Math.PI * 2);
      c.stroke();
      c.fillStyle = '#52406e';
      c.beginPath();
      c.arc(390, 505, 34, 0, Math.PI * 2);
      c.fill();
      c.strokeStyle = '#c9d4e4';
      c.beginPath();
      c.arc(390, 505, 34, 0, Math.PI * 2);
      c.stroke();

      // drumstick (bounces on hit)
      const bounce = stickT > 0 ? Math.sin((0.18 - stickT) / 0.18 * Math.PI) * 60 : 0;
      c.strokeStyle = '#d9b98a';
      c.lineWidth = 5;
      c.lineCap = 'round';
      c.beginPath();
      c.moveTo(330, 430 - bounce);
      c.lineTo(375, 370 - bounce * 1.4);
      c.stroke();
      c.fillStyle = '#f0f4fa';
      c.beginPath();
      c.arc(375, 370 - bounce * 1.4, 7, 0, Math.PI * 2);
      c.fill();

      // hit zone ring
      c.strokeStyle = 'rgba(255,255,255,0.8)';
      c.lineWidth = 3;
      c.beginPath();
      c.arc(480, HIT_Y, 32, 0, Math.PI * 2);
      c.stroke();
      if (stickT > 0) GT.gfx.glow(c, 480, HIT_Y, 46, 'rgba(255,215,90,0.5)');

      // falling notes
      for (const n of notes) {
        if (n.done) continue;
        const y = HIT_Y - (n.at - g.t) * FALL_SPEED;
        if (y < -60 || y > 700) continue;
        GT.gfx.glow(c, 480, y, 40, hexToRgba(n.color, 0.35));
        c.fillStyle = n.color;
        c.beginPath();
        c.arc(480, y, 24, 0, Math.PI * 2);
        c.fill();
        c.strokeStyle = 'rgba(255,255,255,0.8)';
        c.lineWidth = 2;
        c.beginPath();
        c.arc(480, y, 24, 0, Math.PI * 2);
        c.stroke();
      }

      if (flashT > 0) {
        GT.gfx.text(c, flash, 480, 210, {
          size: 44,
          color: flash === 'MISS' ? '#ff5d73' : '#ffd75a',
          stroke: '#120a1e',
          lineWidth: 6,
        });
      }
      if (streak >= 3) {
        GT.gfx.emoji(c, '🔥', 860, 70, 40);
        GT.gfx.text(c, 'x' + streak, 900, 76, { size: 22, color: '#ffb454' });
      }
    },
  });
})();
