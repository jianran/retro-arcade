/* Level 11 — Cheese Heist 🧀
 * Press ↑ to creep toward the cheese, ↓ to retreat from the sweeping
 * flashlight. If the beam touches you, you scurry back two tiles (no fail).
 * Reach the pedestal and press SPACE to grab the cheese.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const TILES = 5;        // mouse hole at 0, pedestal at 5
  const TILE_W = 130;
  const MOUSE_X0 = 140;
  const GUARD_X = 480;
  const GUARD_Y = 250;
  const FLOOR_Y = 460;
  const BEAM_HALF = 0.28; // cone half-angle, rad

  let tile = 0;
  let invulnT = 0;
  let alertT = 0;
  let grabbed = false;

  GT.registerLevel({
    name: 'Cheese Heist',
    icon: '🧀',
    accent: '#ffd75a',
    tagline: 'Sneak past the guard\'s flashlight and grab the cheese!',
    instructions: [
      'Press ↑ to creep one tile toward the cheese',
      'Press ↓ to retreat — use it to dodge the beam',
      'If the flashlight catches you, you scurry back two tiles',
      'Reach the pedestal, then press SPACE to grab the cheese',
    ],
    timeLimit: 45,

    enter: function (g) {
      tile = 0;
      invulnT = 0;
      alertT = 0;
      grabbed = false;
      g.setObjective('Sneak to the cheese!');
    },

    onKey: function (g, code) {
      if (grabbed) return;
      if (code === 'arrowup') {
        tile = Math.min(TILES, tile + 1);
        g.sfx.blipPitch(300 + tile * 80);
        g.setObjective(tile >= TILES
          ? 'Press SPACE to grab the cheese!'
          : 'Tile ' + tile + '/' + TILES);
        if (tile >= TILES) g.setGoal('Press SPACE to grab the cheese!');
      } else if (code === 'arrowdown') {
        tile = Math.max(0, tile - 1);
        g.sfx.blip();
        g.setObjective('Tile ' + tile + '/' + TILES);
      }
    },

    update: function (g, dt) {
      invulnT = Math.max(0, invulnT - dt);
      alertT = Math.max(0, alertT - dt);

      if (invulnT <= 0 && tile > 0 && tile < TILES) {
        const theta = Math.sin(g.t * 2 * Math.PI * 0.72) * 1.05;
        const xfL = GUARD_X + Math.tan(theta - BEAM_HALF) * (FLOOR_Y - GUARD_Y);
        const xfR = GUARD_X + Math.tan(theta + BEAM_HALF) * (FLOOR_Y - GUARD_Y);
        const mx = MOUSE_X0 + tile * TILE_W;
        if (mx >= Math.min(xfL, xfR) && mx <= Math.max(xfL, xfR)) {
          tile = Math.max(0, tile - 3);
          invulnT = 0.6;
          alertT = 0.8;
          g.sfx.buzz();
          g.setObjective('Spotted! Scurried back to tile ' + tile + '/' + TILES);
        }
      }
    },

    draw: function (g, c) {
      // dark corridor
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#171226', '#0c0916']);
      c.fillRect(0, 0, 960, 640);
      // floor
      c.fillStyle = '#2a1f3d';
      c.fillRect(0, FLOOR_Y, 960, 180);
      // wall lamp glows
      for (let x = 120; x < 960; x += 240) {
        GT.gfx.glow(c, x, 60, 34, 'rgba(255,220,150,0.14)');
      }

      // mouse hole
      c.fillStyle = '#050308';
      c.beginPath();
      c.arc(MOUSE_X0, FLOOR_Y, 46, Math.PI, 0);
      c.fill();

      // guard + flashlight beam
      const theta = Math.sin(g.t * 2 * Math.PI * 0.72) * 1.05;
      const xfL = GUARD_X + Math.tan(theta - BEAM_HALF) * (FLOOR_Y - GUARD_Y);
      const xfR = GUARD_X + Math.tan(theta + BEAM_HALF) * (FLOOR_Y - GUARD_Y);
      c.fillStyle = 'rgba(255,240,160,0.22)';
      c.beginPath();
      c.moveTo(GUARD_X, GUARD_Y);
      c.lineTo(xfL, FLOOR_Y);
      c.lineTo(xfR, FLOOR_Y);
      c.closePath();
      c.fill();
      GT.gfx.glow(c, GUARD_X, GUARD_Y, 46, 'rgba(255,240,160,0.4)');
      GT.gfx.emoji(c, '👮', GUARD_X, GUARD_Y, 52);

      // pedestal + cheese
      c.fillStyle = '#4a3b60';
      c.beginPath();
      c.roundRect(MOUSE_X0 + TILES * TILE_W - 34, FLOOR_Y - 66, 68, 66, 8);
      c.fill();
      GT.gfx.glow(c, MOUSE_X0 + TILES * TILE_W, FLOOR_Y - 86, 36, 'rgba(255,215,90,0.55)');
      GT.gfx.emoji(c, '🧀', MOUSE_X0 + TILES * TILE_W, FLOOR_Y - 92, 44);

      // mouse
      const mx = MOUSE_X0 + tile * TILE_W;
      GT.gfx.emoji(c, '🐭', mx, FLOOR_Y - 16, 42);

      // alert flash
      if (alertT > 0) {
        c.fillStyle = 'rgba(255,60,60,' + (alertT * 0.28).toFixed(2) + ')';
        c.fillRect(0, 0, 960, 640);
        GT.gfx.emoji(c, '❗', mx, FLOOR_Y - 90, 40);
      }
    },
  });
})();
