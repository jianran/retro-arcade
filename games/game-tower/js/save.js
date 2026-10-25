/* GameTower — localStorage progress (with in-memory fallback). */
(function () {
  'use strict';
  const GT = window.GT;
  const KEY = 'gametower.save.v1';

  let mem = { highestCompleted: 0, muted: false, lastPlayed: 1 };
  let warned = false;

  function defaults() {
    return { highestCompleted: 0, muted: false, lastPlayed: 1, lives: 3 };
  }

  function read() {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return defaults();
      const s = JSON.parse(raw);
      const d = defaults();
      return {
        highestCompleted: typeof s.highestCompleted === 'number' ? s.highestCompleted : d.highestCompleted,
        muted: !!s.muted,
        lastPlayed: typeof s.lastPlayed === 'number' ? s.lastPlayed : d.lastPlayed,
        lives: typeof s.lives === 'number' ? s.lives : d.lives,
      };
    } catch (e) {
      if (!warned) {
        warned = true;
        console.warn('GameTower: localStorage unavailable — progress will not persist.');
      }
      return Object.assign({}, mem);
    }
  }

  function write(s) {
    try {
      localStorage.setItem(KEY, JSON.stringify(s));
    } catch (e) { /* fall back to memory */ }
    mem = Object.assign({}, s);
  }

  GT.save = {
    get: read,

    complete: function (floorId) {
      const s = read();
      if (floorId > s.highestCompleted) {
        s.highestCompleted = floorId;
        write(s);
      }
    },

    setMuted: function (b) {
      const s = read();
      s.muted = !!b;
      write(s);
    },

    setLastPlayed: function (f) {
      const s = read();
      s.lastPlayed = f;
      write(s);
    },

    setLives: function (n) {
      const s = read();
      s.lives = Math.max(0, Math.min(3, n));
      write(s);
    },

    reset: function () {
      try { localStorage.removeItem(KEY); } catch (e) { /* ignore */ }
      mem = defaults();
    },
  };
})();
