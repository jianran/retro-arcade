/* Level 2 — Hook the Fish 🎣
 * Fish swim past the hook at three depths, bobbing. Press ↑ when a fish is
 * inside the glowing catch window. A miss darts the nearest fish away, so
 * blind mashing can't win. 7 fish, then SPACE.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const HOOK_X = 300;
  const HOOK_Y = 330;
  const WINDOW = 42;
  const NEED = 7;
  const DEPTHS = [280, 330, 380];
  const FISH_EMOJI = ['🐟', '🐠', '🐡'];

  let fish = [];        // {x, baseY, phase, emoji, dartT}
  let spawnT = 0;
  let catches = 0;
  let splashFx = [];    // {x, y, t}
  let banner = '';
  let bannerT = 0;

  GT.registerLevel({
    name: 'Hook the Fish',
    icon: '🎣',
    accent: '#7fc8ff',
    tagline: 'Snap the line the moment a fish reaches your hook!',
    instructions: [
      'Fish swim past your hook at three depths, bobbing up and down',
      'Press ↑ when a fish is inside the glowing catch window',
      'A miss scares the fish away — wait for the right moment',
      'Catch 7 fish, then press SPACE to finish',
    ],
    timeLimit: 45,

    enter: function (g) {
      fish = [];
      spawnT = 0.5;
      catches = 0;
      splashFx = [];
      banner = '';
      bannerT = 0;
      g.setObjective('Fish caught: 0/' + NEED);
    },

    onKey: function (g, code) {
      if (code !== 'arrowup') return;
      // catch: nearest fish inside the window
      let caught = null;
      let bestD = 1e9;
      for (let i = 0; i < fish.length; i++) {
        const f = fish[i];
        if (f.dartT > 0) continue;
        const fy = f.baseY + Math.sin(g.t * 2.5 + f.phase) * 14;
        if (Math.abs(f.x - HOOK_X) < WINDOW && Math.abs(fy - HOOK_Y) < WINDOW) {
          const d = Math.abs(f.x - HOOK_X) + Math.abs(fy - HOOK_Y);
          if (d < bestD) { bestD = d; caught = f; }
        }
      }
      if (caught) {
        fish.splice(fish.indexOf(caught), 1);
        catches++;
        g.sfx.catchSound();
        splashFx.push({ x: HOOK_X, y: HOOK_Y, t: 0 });
        g.setObjective('Fish caught: ' + catches + '/' + NEED);
        if (catches >= NEED) {
          g.setGoal('Press SPACE to finish!');
          g.sfx.success();
        }
      } else {
        // near miss: dart the nearest fish
        let nearest = null;
        let nd = 1e9;
        for (let i = 0; i < fish.length; i++) {
          const f = fish[i];
          if (f.dartT > 0) continue;
          const fy = f.baseY + Math.sin(g.t * 2.5 + f.phase) * 14;
          const d = Math.abs(f.x - HOOK_X) + Math.abs(fy - HOOK_Y);
          if (d < nd) { nd = d; nearest = f; }
        }
        if (nearest) {
          nearest.dartT = 0.7;
          banner = 'MISS!';
          bannerT = 0.8;
        }
        g.sfx.buzz();
      }
    },

    update: function (g, dt) {
      spawnT -= dt;
      if (spawnT <= 0 && fish.length < 3) {
        fish.push({
          x: 980 + Math.random() * 80,
          baseY: DEPTHS[Math.floor(Math.random() * DEPTHS.length)],
          phase: Math.random() * 6.28,
          emoji: FISH_EMOJI[Math.floor(Math.random() * FISH_EMOJI.length)],
          dartT: 0,
        });
        spawnT = 1.7 + Math.random() * 0.7;
      }
      for (let i = fish.length - 1; i >= 0; i--) {
        const f = fish[i];
        f.x -= (f.dartT > 0 ? 380 : 75) * dt;
        f.dartT -= dt;
        if (f.x < -80) fish.splice(i, 1);
      }
      for (let i = splashFx.length - 1; i >= 0; i--) {
        splashFx[i].t += dt;
        if (splashFx[i].t > 0.5) splashFx.splice(i, 1);
      }
      if (bannerT > 0) bannerT -= dt;
    },

    draw: function (g, c) {
      // moonlit pond
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#0e2540', '#0a1830']);
      c.fillRect(0, 0, 960, 640);
      GT.gfx.glow(c, 780, 90, 46, 'rgba(255,250,220,0.9)');
      GT.gfx.emoji(c, '🌙', 780, 90, 40);

      // reeds along the far shore
      c.strokeStyle = '#12304a';
      c.lineWidth = 4;
      for (let x = 30; x < 960; x += 64) {
        c.beginPath();
        c.moveTo(x, 640);
        c.quadraticCurveTo(x + 8, 540 + (x % 130), x + 22, 640);
        c.stroke();
      }

      // fishing rod and line
      c.strokeStyle = '#8b5a2b';
      c.lineWidth = 7;
      c.lineCap = 'round';
      c.beginPath();
      c.moveTo(60, 30);
      c.quadraticCurveTo(220, 90, HOOK_X, 140);
      c.stroke();
      c.strokeStyle = 'rgba(255,255,255,0.55)';
      c.lineWidth = 2;
      c.beginPath();
      c.moveTo(HOOK_X, 140);
      c.lineTo(HOOK_X, HOOK_Y);
      c.stroke();
      // hook: J curve
      c.strokeStyle = '#c9d4e4';
      c.lineWidth = 4;
      c.beginPath();
      c.arc(HOOK_X, HOOK_Y + 6, 12, -Math.PI / 2, Math.PI * 0.7, false);
      c.stroke();

      // catch window
      GT.gfx.glow(c, HOOK_X, HOOK_Y, WINDOW + 18, 'rgba(127,200,255,0.30)');
      c.strokeStyle = 'rgba(127,200,255,0.8)';
      c.lineWidth = 2;
      c.setLineDash([6, 6]);
      c.beginPath();
      c.arc(HOOK_X, HOOK_Y, WINDOW, 0, Math.PI * 2);
      c.stroke();
      c.setLineDash([]);

      // fish
      for (const f of fish) {
        const fy = f.baseY + Math.sin(g.t * 2.5 + f.phase) * 14;
        if (f.dartT > 0) {
          c.strokeStyle = 'rgba(255,255,255,0.5)';
          c.lineWidth = 2;
          for (let i = 0; i < 3; i++) {
            c.beginPath();
            c.moveTo(f.x + 34, fy - 10 + i * 10);
            c.lineTo(f.x + 58, fy - 10 + i * 10);
            c.stroke();
          }
        }
        GT.gfx.emoji(c, f.emoji, f.x, fy, 40);
      }

      // splash particles
      for (const s of splashFx) {
        const r = 8 + s.t * 90;
        c.strokeStyle = 'rgba(255,255,255,' + (0.8 - s.t).toFixed(2) + ')';
        c.lineWidth = 3;
        c.beginPath();
        c.arc(s.x, s.y, r, Math.PI, Math.PI * 2);
        c.stroke();
      }

      // tally slots top-right
      GT.gfx.text(c, 'YOUR NET', 830, 26, { size: 14, color: '#8fa0bf' });
      for (let i = 0; i < NEED; i++) {
        GT.gfx.emoji(c, i < catches ? '🐟' : '·', 790 + i * 42, 58, 30);
      }

      if (bannerT > 0) {
        GT.gfx.text(c, banner, 480, 200, {
          size: 46, color: '#ff5d73', stroke: '#0a0f1a', lineWidth: 6,
        });
      }
    },
  });
})();
