/* GameTower — tower hub screen: 20 floor cards, keyboard + click navigation. */
(function () {
  'use strict';
  const GT = window.GT;

  const el = {
    header: document.getElementById('hub-header'),
    tower: document.getElementById('tower'),
  };

  let selected = 1;

  function renderHeader() {
    el.header.innerHTML = '';
    el.header.appendChild(el2('span', 'hub-title', '🏰 GameTower'));
    const done = el2('span', 'floors-done');
    done.id = 'floors-done';
    el.header.appendChild(done);
    const livesSpan = el2('span', 'hub-lives');
    livesSpan.id = 'hub-lives';
    el.header.appendChild(livesSpan);
    const mute = el2('button', null, '🔊 Sound');
    mute.id = 'btn-mute';
    mute.addEventListener('click', function (e) {
      e.currentTarget.blur();
      const m = !GT.sfx.muted;
      GT.sfx.setMuted(m);
      GT.save.setMuted(m);
      updateMuteLabel();
    });
    el.header.appendChild(mute);
    const reset = el2('button', null, '↺ Reset Progress');
    reset.addEventListener('click', function (e) {
      e.currentTarget.blur();
      if (confirm('Reset all progress? Every floor will lock again.')) {
        GT.save.reset();
        GT.sfx.setMuted(GT.save.get().muted);
        GT.hub.render();
      }
    });
    el.header.appendChild(reset);
  }

  function updateMuteLabel() {
    const btn = document.getElementById('btn-mute');
    if (btn) btn.textContent = GT.sfx.muted ? '🔇 Muted' : '🔊 Sound';
  }

  function el2(tag, cls, text) {
    const d = document.createElement(tag);
    if (cls) d.className = cls;
    if (text !== undefined) d.textContent = text;
    return d;
  }

  const hub = {
    init: function () {
      renderHeader();
      updateMuteLabel();
    },

    render: function () {
      const s = GT.save.get();
      selected = Math.min(Math.max(selected, 1), 20);
      const doneEl = document.getElementById('floors-done');
      if (doneEl) doneEl.textContent = 'Floors: ' + s.highestCompleted + '/20';
      const livesEl = document.getElementById('hub-lives');
      if (livesEl) {
        livesEl.textContent = '❤️'.repeat(s.lives) + '🖤'.repeat(3 - s.lives);
      }
      el.tower.innerHTML = '';
      GT.levels.forEach(function (L) {
        const floor = L.id;
        const status = floor <= s.highestCompleted ? 'done'
          : floor === s.highestCompleted + 1 ? 'current' : 'locked';
        const card = el2('div', 'floor ' + status + (floor === selected ? ' selected' : ''));
        card.style.setProperty('--accent', L.accent || '#3a4a6b');
        card.appendChild(el2('div', 'floor-icon', status === 'locked' ? '🔒' : L.icon));
        card.appendChild(el2('div', 'floor-num', 'F' + floor));
        card.appendChild(el2('div', 'floor-name', L.name));
        card.appendChild(el2('div', 'floor-status',
          status === 'done' ? '⭐' : status === 'current' ? 'PLAY ▶' : ''));
        card.addEventListener('click', function () {
          if (status === 'locked') { GT.sfx.buzz(); return; }
          selected = floor;
          GT.hub.render();
          GT.sfx.press();
          GT.engine.startLevel(floor);
        });
        el.tower.appendChild(card);
      });
      const sel = el.tower.querySelector('.selected');
      if (sel) sel.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    },

    handleKey: function (code) {
      if (code === 'arrowup') {
        selected = selected - 1 < 1 ? 20 : selected - 1;
        GT.sfx.blip();
        GT.hub.render();
      } else if (code === 'arrowdown') {
        selected = selected + 1 > 20 ? 1 : selected + 1;
        GT.sfx.blip();
        GT.hub.render();
      } else if (code === ' ' || code === 'enter') {
        const s = GT.save.get();
        if (selected <= s.highestCompleted + 1) {
          GT.sfx.press();
          GT.engine.startLevel(selected);
        } else {
          GT.sfx.buzz();
        }
      }
    },
  };

  GT.hub = hub;
})();
