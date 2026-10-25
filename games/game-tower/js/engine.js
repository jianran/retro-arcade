/* GameTower — engine: state machine, fixed-timestep loop, timer, win/fail, level registry.
 *
 * States: HUB → INTRO → COUNTDOWN → PLAYING → WIN → (next INTRO | HUB)
 *                       PLAYING → FAIL → (retry INTRO | HUB)
 *                       any game state → PAUSED (P) / HUB (ESC, forfeit)
 *
 * SPACE-to-finish convention: a level that must end with SPACE calls
 * g.setGoal('Press SPACE to finish') once its objective is met; the engine
 * then intercepts SPACE and wins. Auto-completing levels call g.win() directly.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const STEP = 1 / 60;
  const MAX_STEPS = 4;

  GT.levels = [];
  GT.registerLevel = function (def) {
    def.id = GT.levels.length + 1;
    GT.levels.push(def);
  };

  const canvas = document.getElementById('canvas');
  const c2d = canvas.getContext('2d');
  const el = {
    hub: document.getElementById('hub'),
    game: document.getElementById('game'),
    hud: document.getElementById('hud'),
    timerBar: document.getElementById('timer-bar'),
    timerText: document.getElementById('timer-text'),
    floorLabel: document.getElementById('floor-label'),
    objective: document.getElementById('objective'),
    paused: document.getElementById('paused-label'),
    lives: document.getElementById('lives'),
    intro: document.getElementById('intro'),
    count: document.getElementById('count'),
    countNum: document.getElementById('count-num'),
    win: document.getElementById('win'),
    fail: document.getElementById('fail'),
    gameover: document.getElementById('gameover'),
  };

  const engine = {
    state: 'HUB',
    level: null,
    g: null,
    timeLeft: 0,
    goalReached: false,
    countT: 0,
    lastCountN: 4,
    acc: 0,
    last: 0,
    frames: 0,
    fpsT: 0,
    fps: 0,
  };
  GT.engine = engine;

  function el2(tag, cls, text) {
    const d = document.createElement(tag);
    if (cls) d.className = cls;
    if (text !== undefined) d.textContent = text;
    return d;
  }

  function buttonRow(target, buttons) {
    const row = el2('div', 'row');
    buttons.forEach(function (b) {
      const btn = el2('button', b[2] ? 'big' : null, b[0]);
      btn.addEventListener('click', function (e) {
        e.currentTarget.blur();
        b[1]();
      });
      row.appendChild(btn);
    });
    target.appendChild(row);
  }

  function setState(s) {
    engine.state = s;
    GT.input.clear();
    el.hub.classList.toggle('hidden', s !== 'HUB');
    el.game.classList.toggle('hidden', s === 'HUB');
    el.hud.classList.toggle('hidden', s !== 'PLAYING' && s !== 'PAUSED');
    el.paused.classList.toggle('hidden', s !== 'PAUSED');
    el.intro.classList.toggle('hidden', s !== 'INTRO');
    el.count.classList.toggle('hidden', s !== 'COUNTDOWN');
    el.win.classList.toggle('hidden', s !== 'WIN');
    el.fail.classList.toggle('hidden', s !== 'FAIL');
    el.gameover.classList.toggle('hidden', s !== 'GAMEOVER');
    if (s === 'HUB') GT.hub.render();
  }

  function createContext() {
    return {
      w: 960,
      h: 640,
      t: 0,
      get timeLeft() { return engine.timeLeft; },
      rng: Math.random,
      win: function () { engine.win(); },
      fail: function (msg) { engine.doFail(msg); },
      setObjective: function (text) {
        el.objective.textContent = text;
        el.objective.classList.remove('hidden');
      },
      clearObjective: function () {
        el.objective.classList.add('hidden');
      },
      setGoal: function (text) {
        engine.goalReached = true;
        el.objective.textContent = text;
        el.objective.classList.remove('hidden');
        GT.sfx.tick();
      },
      sfx: GT.sfx,
    };
  }

  function fillIntro(level) {
    const target = el.intro;
    target.innerHTML = '';
    const card = el2('div', 'card');
    card.style.setProperty('--accent', level.accent || '#52d8c4');
    card.appendChild(el2('div', 'card-icon', level.icon));
    card.appendChild(el2('div', 'card-floor', 'FLOOR ' + level.id + ' OF 20'));
    card.appendChild(el2('h1', null, level.name));
    card.appendChild(el2('p', 'tagline', level.tagline));
    const ul = document.createElement('ul');
    level.instructions.forEach(function (t) { ul.appendChild(el2('li', null, t)); });
    card.appendChild(ul);
    card.appendChild(el2('div', 'time-chip', '⏱ ' + level.timeLimit + ' seconds'));
    card.appendChild(el2('div', 'time-chip', hearts(GT.save.get().lives)));
    const row = el2('div', 'row');
    const start = el2('button', 'big', 'Start — SPACE');
    start.addEventListener('click', function (e) { e.currentTarget.blur(); engine.beginPlay(); });
    const back = el2('button', null, 'Back — ESC');
    back.addEventListener('click', function (e) { e.currentTarget.blur(); engine.toHub(); });
    row.appendChild(start);
    row.appendChild(back);
    card.appendChild(row);
    target.appendChild(card);
  }

  function fillWin() {
    const final = engine.level.id >= GT.levels.length;
    const used = Math.round(engine.level.timeLimit - engine.timeLeft);
    const target = el.win;
    target.innerHTML = '';
    const card = el2('div', 'card');
    if (final) {
      card.style.setProperty('--accent', '#ffd75a');
      card.appendChild(el2('div', 'card-icon', '👑'));
      card.appendChild(el2('h1', 'result-title', 'YOU CLIMBED THE TOWER!'));
      card.appendChild(el2('div', 'result-sub',
        'All 20 floors complete — you are the Tower Champion!'));
      buttonRow(target.appendChild(card), [
        ['Back to the Tower', function () { engine.toHub(); }, true],
      ]);
    } else {
      card.style.setProperty('--accent', engine.level.accent || '#52d8c4');
      card.appendChild(el2('div', 'card-icon', engine.level.icon));
      card.appendChild(el2('h1', 'result-title', engine.level.name + ' complete!'));
      card.appendChild(el2('div', 'result-sub',
        'Floor ' + engine.level.id + ' cleared in ' + used + 's · Floor ' +
        (engine.level.id + 1) + ' unlocked · ' + hearts(GT.save.get().lives)));
      buttonRow(target.appendChild(card), [
        ['Next Floor — SPACE', function () { engine.nextFloor(); }, true],
        ['Replay — R', function () { engine.retry(); }],
        ['Hub — ESC', function () { engine.toHub(); }],
      ]);
    }
  }

  function hearts(lives) {
    return '❤️'.repeat(lives) + '🖤'.repeat(3 - lives);
  }

  function fillFail(msg, lives) {
    const target = el.fail;
    target.innerHTML = '';
    const card = el2('div', 'card' + (lives === 1 ? ' danger' : ''));
    card.style.setProperty('--accent', '#ff5d73');
    if (lives === 1) {
      card.appendChild(el2('div', 'card-icon', '🚨'));
      card.appendChild(el2('h1', 'result-title', 'DANGER! BECAREFUL!'));
      card.appendChild(el2('div', 'result-sub', 'One life left!'));
      card.appendChild(el2('div', 'fail-reason', msg));
    } else {
      card.appendChild(el2('div', 'card-icon', '💥'));
      card.appendChild(el2('h1', 'result-title', msg || 'Failed!'));
      card.appendChild(el2('div', 'result-sub', '⚠️ Careful! ' + lives + ' lives left'));
    }
    card.appendChild(el2('div', 'lives-row', hearts(lives)));
    buttonRow(target.appendChild(card), [
      ['Retry — SPACE', function () { engine.retry(); }, true],
      ['Hub — ESC', function () { engine.toHub(); }],
    ]);
  }

  function fillGameOver(msg) {
    const target = el.gameover;
    target.innerHTML = '';
    const card = el2('div', 'card danger');
    card.style.setProperty('--accent', '#ff5d73');
    card.appendChild(el2('div', 'card-icon', '💀'));
    card.appendChild(el2('h1', 'result-title', 'YOU LOST!'));
    card.appendChild(el2('div', 'result-sub', 'GAME OVER'));
    card.appendChild(el2('div', 'lives-row', hearts(0)));
    card.appendChild(el2('div', 'fail-reason',
      'You fell at Floor ' + engine.level.id + (msg ? ' (' + msg + ')' : '') +
      ' — the tower has reset.'));
    buttonRow(target.appendChild(card), [
      ['Try Again — SPACE', function () { engine.toHub(); }, true],
    ]);
  }

  // ---------- public API ----------

  engine.startLevel = function (id) {
    const level = GT.levels[id - 1];
    if (!level) return;
    engine.level = level;
    engine.g = createContext();
    engine.goalReached = false;
    engine.timeLeft = level.timeLimit;
    el.floorLabel.textContent = 'FLOOR ' + level.id;
    level.enter(engine.g);
    fillIntro(level);
    GT.save.setLastPlayed(id);
    setState('INTRO');
  };

  engine.beginPlay = function () {
    if (engine.state !== 'INTRO') return;
    engine.countT = 2.4;
    engine.lastCountN = 4;
    engine.g.t = 0;
    setState('COUNTDOWN');
  };

  function startPlaying() {
    engine.timeLeft = engine.level.timeLimit;
    engine.g.t = 0;
    setState('PLAYING');
    GT.sfx.tick();
  }

  engine.win = function () {
    if (engine.state !== 'PLAYING') return;
    setState('WIN');
    GT.save.complete(engine.level.id);
    if (engine.level.id >= GT.levels.length) GT.sfx.fanfare();
    else GT.sfx.success();
    fillWin();
  };

  engine.doFail = function (msg) {
    if (engine.state !== 'PLAYING') return;
    const lives = Math.max(0, GT.save.get().lives - 1);
    GT.save.setLives(lives);
    if (lives <= 0) {
      setState('GAMEOVER');
      GT.save.reset(); // run over — the tower resets
      GT.sfx.gameOver();
      fillGameOver(msg);
    } else {
      setState('FAIL');
      GT.sfx.fail();
      fillFail(msg, lives);
    }
  };

  engine.retry = function () {
    if (engine.level) engine.startLevel(engine.level.id);
  };

  engine.nextFloor = function () {
    if (engine.level && engine.level.id < GT.levels.length) {
      engine.startLevel(engine.level.id + 1);
    } else {
      engine.toHub();
    }
  };

  engine.toHub = function () {
    setState('HUB');
  };

  engine.togglePause = function () {
    if (engine.state === 'PLAYING') {
      setState('PAUSED');
      GT.sfx.tick();
    } else if (engine.state === 'PAUSED') {
      setState('PLAYING');
      GT.sfx.tick();
    }
  };

  // ---------- key routing ----------

  function routeKey(code) {
    const s = engine.state;
    if (s === 'HUB') { GT.hub.handleKey(code); return; }
    if (s === 'INTRO') {
      if (code === ' ' || code === 'enter') engine.beginPlay();
      else if (code === 'escape') engine.toHub();
      return;
    }
    if (s === 'COUNTDOWN') {
      if (code === 'escape') engine.toHub();
      return;
    }
    if (s === 'PLAYING') {
      if (code === 'escape') { engine.toHub(); return; }
      if (code === 'p') { engine.togglePause(); return; }
      if (code === ' ' && engine.goalReached) { engine.win(); return; }
      if (engine.level.onKey) engine.level.onKey(engine.g, code);
      return;
    }
    if (s === 'PAUSED') {
      if (code === 'escape') engine.toHub();
      else if (code === 'p' || code === ' ' || code === 'enter') engine.togglePause();
      return;
    }
    if (s === 'WIN') {
      if (code === 'escape') engine.toHub();
      else if (code === 'r') engine.retry();
      else if (code === ' ' || code === 'enter') engine.nextFloor();
      return;
    }
    if (s === 'FAIL') {
      if (code === 'escape') engine.toHub();
      else if (code === ' ' || code === 'enter' || code === 'r') engine.retry();
      return;
    }
    if (s === 'GAMEOVER') {
      if (code === ' ' || code === 'enter' || code === 'escape') engine.toHub();
      return;
    }
  }

  // ---------- loop ----------

  function update(dt) {
    const s = engine.state;
    if (s === 'COUNTDOWN') {
      engine.countT -= dt;
      const n = Math.max(1, Math.ceil(engine.countT / 0.8));
      if (n !== engine.lastCountN) {
        engine.lastCountN = n;
        el.countNum.textContent = String(n);
        GT.sfx.countBeep(n);
      }
      if (engine.countT <= 0) startPlaying();
      return;
    }
    if (s !== 'PLAYING') return;

    engine.g.t += dt;
    engine.timeLeft -= dt;

    if (engine.level.onClick) {
      const pt = GT.input.consumeClick();
      if (pt) engine.level.onClick(engine.g, pt.x, pt.y);
      if (engine.state !== 'PLAYING') return;
    }

    if (engine.level.update) engine.level.update(engine.g, dt);
    if (engine.state !== 'PLAYING') return;

    if (engine.timeLeft <= 0) {
      engine.timeLeft = 0;
      engine.doFail("Time's up!");
    }
  }

  function drawHUD() {
    const p = Math.max(0, engine.timeLeft / engine.level.timeLimit);
    el.timerBar.style.width = (p * 100) + '%';
    el.timerBar.style.background = p > 0.5 ? '#52d8c4' : p > 0.25 ? '#ffb454' : '#ff5d73';
    const t = Math.ceil(engine.timeLeft);
    el.timerText.textContent = Math.floor(t / 60) + ':' + String(t % 60).padStart(2, '0');
    const h = hearts(GT.save.get().lives);
    if (el.lives.textContent !== h) el.lives.textContent = h;
  }

  function draw() {
    const s = engine.state;
    if (s === 'HUB') return;
    c2d.fillStyle = '#05070d';
    c2d.fillRect(0, 0, 960, 640);
    if (engine.level && engine.g && engine.level.draw) engine.level.draw(engine.g, c2d);
    if (s === 'PLAYING' || s === 'PAUSED') drawHUD();
  }

  function loop(ts) {
    if (!engine.last) engine.last = ts;
    let dt = (ts - engine.last) / 1000;
    engine.last = ts;
    if (dt > 0.25) dt = 0.25;
    engine.acc += dt;
    let steps = 0;
    while (engine.acc >= STEP && steps < MAX_STEPS) {
      update(STEP);
      engine.acc -= STEP;
      steps++;
    }
    if (steps === MAX_STEPS) engine.acc = 0;
    engine.frames++;
    engine.fpsT += dt;
    if (engine.fpsT >= 0.5) {
      engine.fps = Math.round(engine.frames / engine.fpsT);
      engine.frames = 0;
      engine.fpsT = 0;
      if (GT.debugBar) GT.debugBar.update();
    }
    draw();
    requestAnimationFrame(loop);
  }

  engine.init = function () {
    // hub cheat code: typing it at the tower unlocks every floor
    const CHEAT = '67240084022gametower';
    let cheatBuf = '';
    window.addEventListener('keydown', function (e) {
      if (e.repeat || e.metaKey || e.ctrlKey || e.altKey) return;
      const code = e.key.toLowerCase();
      if (e.key.length === 1) {
        cheatBuf = (cheatBuf + code).slice(-CHEAT.length);
        if (cheatBuf === CHEAT && engine.state === 'HUB') {
          GT.save.complete(20);
          GT.hub.render();
          GT.sfx.fanfare();
        }
      }
      routeKey(code);
    });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden && engine.state === 'PLAYING') engine.togglePause();
    });
    setState('HUB');
    requestAnimationFrame(loop);
  };
})();
