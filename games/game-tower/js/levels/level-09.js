/* Level 9 — Space Trash Typist 🚀
 * Worded asteroids drift toward your ship. Type the word to fire a bolt.
 * Wrong keys make the nearest asteroid speed up. 3 wrong words and it's over.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const WORD_POOLS = [
    ['go', 'hi', 'of', 'it', 'be', 'do', 'no', 'so', 'at', 'in', 'on', 'my', 'by', 'we', 'he', 'us', 'or', 'if', 'as', 'an', 'ox'],
    ['cat', 'dog', 'sun', 'run', 'sky', 'fly', 'ant', 'bee', 'cow', 'egg', 'hat', 'ice', 'jam', 'key', 'leg', 'mix', 'net', 'owl', 'bed', 'rug', 'sit', 'toy', 'van', 'web', 'zoo', 'box', 'day', 'end'],
    ['star', 'moon', 'fish', 'bird', 'fire', 'wind', 'rock', 'sand', 'tree', 'door', 'sail', 'wave', 'lake', 'rain', 'snow', 'cake', 'game', 'hero', 'lion', 'mint', 'nose', 'oven', 'road'],
    ['amber', 'brave', 'cloud', 'dream', 'eagle', 'flame', 'green', 'honey', 'juice', 'koala', 'lemon', 'magic', 'night', 'ocean', 'zebra', 'queen', 'river', 'stone', 'tiger', 'ultra', 'vivid', 'whale'],
  ];
  const WORD_FONT = '"Trebuchet MS","Segoe UI",sans-serif';
  const NEED = 15;
  const MAX_MISTAKES = 3;

  let rocks = [];       // {word, x, y, vx, hit}
  let stars = [];       // {x, y, s, ph, v}
  let destroyed = 0;
  let mistakes = 0;
  let spawnT = 0;
  let bolt = null;      // {x0, y0, x1, y1, t, rock}
  let booms = [];       // {x, y, t}
  let target = null;    // rock currently being typed
  let typed = '';       // letters typed so far on the target

  function randomWord() {
    const pool = WORD_POOLS[Math.floor(Math.random() * WORD_POOLS.length)];
    return pool[Math.floor(Math.random() * pool.length)];
  }

  function obj(g) {
    g.setObjective('Destroyed: ' + destroyed + '/' + NEED +
      '   Mistakes: ' + mistakes + '/' + MAX_MISTAKES +
      (typed ? '   ⌨ ' + typed.toUpperCase() : ''));
  }

  GT.registerLevel({
    name: 'Space Trash Typist',
    icon: '🚀',
    accent: '#7fc8ff',
    tagline: 'Type the words to blast the asteroids before they reach your ship!',
    instructions: [
      'Each asteroid carries a 2–5 letter word — type it to fire a bolt',
      'Words never use the letter P — P pauses the game',
      'Wrong letters cost you a chance — 3 wrong words and the mission fails',
      'Backspace erases a letter — typing a new first letter switches targets',
      'Destroy 15 asteroids to win',
    ],
    timeLimit: 70,

    enter: function (g) {
      rocks = [];
      stars = [];
      for (let i = 0; i < 60; i++) {
        stars.push({
          x: Math.random() * 960,
          y: Math.random() * 640,
          s: 0.6 + Math.random() * 1.6,
          ph: Math.random() * 6.28,
          v: 15 + Math.random() * 40,
        });
      }
      destroyed = 0;
      mistakes = 0;
      spawnT = 0.5;
      bolt = null;
      booms = [];
      target = null;
      typed = '';
      if (GT.debug) {
        // test harness peek at the on-screen words
        GT.debugBar.level9 = function () {
          return { rocks: rocks.map(function (r) { return r.word; }), typed: typed };
        };
      }
      obj(g);
    },

    onKey: function (g, code) {
      if (code === 'backspace') {
        typed = typed.slice(0, -1);
        if (typed === '') target = null;
        g.sfx.blip();
        obj(g);
        return;
      }
      if (!/^[a-z]$/.test(code)) return;

      // keep going on the current word
      if (target && !target.hit && target.word[typed.length] === code) {
        typed += code;
        if (typed === target.word) {
          target.hit = true;
          bolt = { x0: 200, y0: 340, x1: target.x, y1: target.y, t: 0, rock: target };
          target = null;
          typed = '';
          g.sfx.catchSound();
        }
        obj(g);
        return;
      }

      // switch to another on-screen word that starts with this letter
      for (const r of rocks) {
        if (!r.hit && r.word[0] === code) {
          target = r;
          typed = code;
          obj(g);
          return;
        }
      }

      // wrong letter: speed up the nearest asteroid and drop the word
      let nearest = null;
      let nd = 1e9;
      for (const r of rocks) {
        if (!r.hit && r.x < nd) { nd = r.x; nearest = r; }
      }
      if (nearest) nearest.vx *= 1.3;
      target = null;
      typed = '';
      mistakes++;
      g.sfx.buzz();
      if (mistakes >= MAX_MISTAKES) {
        g.fail('Three wrong words!');
        return;
      }
      obj(g);
    },

    update: function (g, dt) {
      spawnT -= dt;
      const interval = Math.max(0.9, 1.7 - g.t * (0.8 / 60));
      if (spawnT <= 0 && rocks.length < 6) {
        // pick a word whose first letter isn't already on screen
        const used = rocks.map(function (r) { return r.word[0]; });
        let word = randomWord();
        let guard = 0;
        while (used.indexOf(word[0]) !== -1 && guard++ < 50) word = randomWord();
        rocks.push({
          word: word,
          x: 1000,
          y: 100 + Math.random() * 440,
          vx: 75 + Math.random() * 40,
          hit: false,
        });
        spawnT = interval;
      }

      for (let i = rocks.length - 1; i >= 0; i--) {
        const r = rocks[i];
        r.x -= r.vx * dt;
        if (!r.hit && r.x < 190) {
          // missed rock sails past the ship — it only costs you time
          booms.push({ x: 190, y: r.y, t: 0 });
          g.sfx.buzz();
          rocks.splice(i, 1);
          if (target === r) { target = null; typed = ''; }
          obj(g);
        }
      }

      // bolt flight
      if (bolt) {
        bolt.t += dt / 0.25;
        if (bolt.t >= 1) {
          booms.push({ x: bolt.x1, y: bolt.y1, t: 0 });
          destroyed++;
          obj(g);
          const i = rocks.indexOf(bolt.rock);
          if (i !== -1) rocks.splice(i, 1);
          bolt = null;
          if (destroyed >= NEED) {
            g.setObjective('Sector clear!');
            g.win();
            return;
          }
        }
      }

      for (const s of stars) {
        s.x -= s.v * dt;
        if (s.x < -5) { s.x = 965; s.y = Math.random() * 640; }
      }
      for (let i = booms.length - 1; i >= 0; i--) {
        booms[i].t += dt;
        if (booms[i].t > 0.45) booms.splice(i, 1);
      }
    },

    draw: function (g, c) {
      // space
      c.fillStyle = GT.gfx.grad(c, 0, 0, 0, 640, ['#0a0f24', '#05060f']);
      c.fillRect(0, 0, 960, 640);
      GT.gfx.stars(c, stars, g.t);

      // ship
      const bob = Math.sin(g.t * 2) * 6;
      GT.gfx.glow(c, 170, 340 + bob, 40, 'rgba(127,200,255,0.35)');
      GT.gfx.emoji(c, '🚀', 170, 340 + bob, 52);
      // mistake pips under ship
      for (let i = 0; i < MAX_MISTAKES; i++) {
        GT.gfx.emoji(c, i < mistakes ? '❌' : '▫️', 120 + i * 34, 430, 18);
      }

      // asteroids
      for (const r of rocks) {
        const flicker = r.hit ? 0.5 + 0.5 * Math.sin(g.t * 40) : 0;
        c.fillStyle = r.vx > 90 ? '#8a6a5a' : '#6e5c50';
        c.beginPath();
        c.arc(r.x, r.y, 30, 0, Math.PI * 2);
        c.fill();
        c.strokeStyle = 'rgba(255,255,255,' + (0.2 + flicker).toFixed(2) + ')';
        c.lineWidth = 3;
        c.beginPath();
        c.arc(r.x, r.y, 30, 0, Math.PI * 2);
        c.stroke();
        // craters
        c.fillStyle = '#4e4138';
        c.beginPath();
        c.arc(r.x - 9, r.y - 7, 6, 0, Math.PI * 2);
        c.arc(r.x + 10, r.y + 8, 4, 0, Math.PI * 2);
        c.fill();
        // word on the rock, typed prefix highlighted
        const up = r.word.toUpperCase();
        const size = up.length <= 3 ? 18 : 15;
        c.font = size + 'px ' + WORD_FONT;
        const widths = [];
        let total = 0;
        for (let i = 0; i < up.length; i++) {
          const w = c.measureText(up[i]).width;
          widths.push(w);
          total += w;
        }
        let lx = r.x - total / 2;
        for (let i = 0; i < up.length; i++) {
          const isTyped = r === target && i < typed.length;
          GT.gfx.text(c, up[i], lx + widths[i] / 2, r.y + 1, {
            size: size,
            color: isTyped ? '#ffd75a' : '#ffffff',
            stroke: '#222',
            lineWidth: 3,
          });
          lx += widths[i];
        }
      }

      // bolt
      if (bolt) {
        const p = Math.min(1, bolt.t);
        const x = bolt.x0 + (bolt.x1 - bolt.x0) * p;
        const y = bolt.y0 + (bolt.y1 - bolt.y0) * p;
        GT.gfx.glow(c, x, y, 24, 'rgba(255,215,90,0.8)');
        c.strokeStyle = '#ffd75a';
        c.lineWidth = 5;
        c.beginPath();
        c.moveTo(bolt.x0, bolt.y0);
        c.lineTo(x, y);
        c.stroke();
      }

      // explosions
      for (const b of booms) {
        const r = 8 + b.t * 90;
        c.strokeStyle = 'rgba(255,180,80,' + (0.9 - b.t).toFixed(2) + ')';
        c.lineWidth = 4;
        c.beginPath();
        c.arc(b.x, b.y, r, 0, Math.PI * 2);
        c.stroke();
        GT.gfx.glow(c, b.x, b.y, r * 0.7, 'rgba(255,140,60,' + (0.5 - b.t * 0.5).toFixed(2) + ')');
      }

      // current word progress
      if (target && typed) {
        GT.gfx.text(c, 'TYPING  ' + typed.toUpperCase(), 480, 610, {
          size: 20, color: '#ffd75a', stroke: '#0a0f24', lineWidth: 4,
        });
      }
    },
  });
})();
