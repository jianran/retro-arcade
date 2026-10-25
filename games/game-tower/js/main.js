/* GameTower — boot + ?debug=1 harness. */
(function () {
  'use strict';
  const GT = window.GT;

  GT.debug = new URLSearchParams(location.search).get('debug') === '1';

  function buildDebugBar() {
    const bar = document.getElementById('debug-bar');
    bar.classList.remove('hidden');

    const fps = document.createElement('span');
    fps.id = 'debug-fps';
    bar.appendChild(fps);

    const add = function (label, fn) {
      const b = document.createElement('button');
      b.textContent = label;
      b.addEventListener('click', function (e) { e.currentTarget.blur(); fn(); });
      bar.appendChild(b);
    };

    add('Instant Win', function () { GT.engine.win(); });
    add('Instant Fail', function () { GT.engine.doFail('Debug fail'); });
    add('Unlock All', function () { GT.save.complete(20); GT.hub.render(); });
    add('Replay', function () { GT.engine.retry(); });
    add('Hub', function () { GT.engine.toHub(); });

    const sel = document.createElement('select');
    for (let i = 1; i <= 20; i++) {
      const o = document.createElement('option');
      o.value = String(i);
      o.textContent = 'Floor ' + i;
      sel.appendChild(o);
    }
    sel.addEventListener('change', function () {
      GT.engine.startLevel(parseInt(sel.value, 10));
    });
    bar.appendChild(sel);
  }

  GT.debugBar = {
    update: function () {
      const f = document.getElementById('debug-fps');
      if (f) f.textContent = GT.engine.fps + ' fps';
    },
  };

  GT.input.init();
  GT.hub.init();
  GT.engine.init(); // renders hub — must run after hub.init()
  GT.sfx.setMuted(GT.save.get().muted);

  if (GT.debug) buildDebugBar();
})();
