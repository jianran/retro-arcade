/* GameTower — synthesized sound effects (Web Audio, no assets). */
(function () {
  'use strict';
  const GT = window.GT;

  let ctx = null;
  let master = null;
  let muted = false;

  function ensure() {
    if (!ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      ctx = new AC();
      master = ctx.createGain();
      master.gain.value = muted ? 0 : 0.5;
      master.connect(ctx.destination);
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function tone(freq, dur, type, vol, opts) {
    opts = opts || {};
    const c = ensure();
    if (!c) return;
    const t0 = c.currentTime + (opts.delay || 0);
    const osc = c.createOscillator();
    const g = c.createGain();
    osc.type = type || 'sine';
    osc.frequency.setValueAtTime(Math.max(freq, 1), t0);
    if (opts.slideTo) {
      osc.frequency.exponentialRampToValueAtTime(Math.max(opts.slideTo, 1), t0 + dur);
    }
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(vol || 0.15, t0 + (opts.attack || 0.01));
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.connect(g);
    g.connect(master);
    osc.start(t0);
    osc.stop(t0 + dur + 0.05);
  }

  let noiseBuf = null;
  function noise(dur, vol, opts) {
    opts = opts || {};
    const c = ensure();
    if (!c) return;
    if (!noiseBuf) {
      noiseBuf = c.createBuffer(1, c.sampleRate * 0.5, c.sampleRate);
      const d = noiseBuf.getChannelData(0);
      for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    }
    const t0 = c.currentTime + (opts.delay || 0);
    const src = c.createBufferSource();
    src.buffer = noiseBuf;
    const g = c.createGain();
    g.gain.setValueAtTime(vol || 0.12, t0);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    const f = c.createBiquadFilter();
    f.type = opts.filter || 'lowpass';
    f.frequency.value = opts.freq || 800;
    src.connect(f);
    f.connect(g);
    g.connect(master);
    src.start(t0);
    src.stop(t0 + dur + 0.05);
  }

  GT.sfx = {
    unlock: ensure,

    blip: function () { tone(440, 0.07, 'sine', 0.1); },
    blipPitch: function (freq) { tone(freq, 0.06, 'sine', 0.09); },
    press: function () { tone(520, 0.06, 'square', 0.08); },
    tick: function () { tone(880, 0.05, 'square', 0.1); },
    buzz: function () { tone(140, 0.14, 'sawtooth', 0.12); },
    catchSound: function () {
      tone(660, 0.08, 'triangle', 0.14);
      tone(880, 0.12, 'triangle', 0.12, { delay: 0.06 });
    },
    splash: function () { noise(0.3, 0.16, { freq: 500 }); },
    whoosh: function () { noise(0.15, 0.1, { freq: 2000, filter: 'bandpass' }); },
    drum: function () { noise(0.12, 0.2, { freq: 300 }); tone(90, 0.1, 'sine', 0.18); },
    countBeep: function (n) { tone(n === 3 ? 440 : n === 2 ? 440 : 880, 0.12, 'square', 0.12); },
    success: function () {
      [523, 659, 784, 1047].forEach(function (f, i) {
        tone(f, 0.15, 'triangle', 0.16, { delay: i * 0.12 });
      });
    },
    fail: function () { tone(300, 0.5, 'sawtooth', 0.14, { slideTo: 80 }); },
    gameOver: function () {
      [523, 392, 330, 196].forEach(function (f, i) {
        tone(f, 0.3, 'sawtooth', 0.14, { delay: i * 0.22 });
      });
    },
    fanfare: function () {
      [523, 659, 784, 1047, 1319, 1568].forEach(function (f, i) {
        tone(f, 0.22, 'triangle', 0.15, { delay: i * 0.13 });
      });
    },

    setMuted: function (b) {
      muted = !!b;
      if (master) master.gain.value = muted ? 0 : 0.5;
    },
    get muted() { return muted; },
  };
})();
