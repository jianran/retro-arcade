/* GameTower — keyboard & pointer input manager.
 *
 * Conventions for levels:
 *  - Use the level's onKey(g, code) hook for press events (dispatched by the engine).
 *  - Use GT.input.held(code) inside update(g, dt) for hold/release state.
 *  - The press queue is cleared at every engine state change, so a SPACE that
 *    started a level can never trigger level logic.
 */
(function () {
  'use strict';
  const GT = window.GT;

  const queue = [];
  const held = new Set();
  const clickQueue = [];

  GT.input = {
    init: function () {
      window.addEventListener('keydown', function (e) {
        if (e.repeat) return;
        GT.sfx.unlock();
        const code = e.key.toLowerCase();
        if (code === ' ' || code.startsWith('arrow') || code === 'enter') e.preventDefault();
        if (e.metaKey || e.ctrlKey || e.altKey) return;
        queue.push(code);
        held.add(code);
      });
      window.addEventListener('keyup', function (e) {
        held.delete(e.key.toLowerCase());
      });
      window.addEventListener('blur', function () {
        held.clear();
      });
      const canvas = document.getElementById('canvas');
      canvas.addEventListener('pointerdown', function (e) {
        GT.sfx.unlock();
        const rect = canvas.getBoundingClientRect();
        clickQueue.push({
          x: (e.clientX - rect.left) * (960 / rect.width),
          y: (e.clientY - rect.top) * (640 / rect.height),
        });
      });
    },

    pressed: function (code) {
      const i = queue.indexOf(code.toLowerCase());
      if (i === -1) return false;
      queue.splice(i, 1);
      return true;
    },

    held: function (code) {
      return held.has(code.toLowerCase());
    },

    consumeClick: function () {
      return clickQueue.length ? clickQueue.shift() : null;
    },

    clear: function () {
      queue.length = 0;
      clickQueue.length = 0;
      held.clear();
    },
  };
})();
