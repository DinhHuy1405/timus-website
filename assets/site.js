/* Mã dùng chung cho mọi trang timusco.com */
(function () {
  var doc = document, html = doc.documentElement;
  function all(sel, root) { return [].slice.call((root || doc).querySelectorAll(sel)); }

  /* đổi ngôn ngữ */
  all('.lang button').forEach(function (b) {
    b.addEventListener('click', function () {
      var l = b.getAttribute('data-set');
      html.setAttribute('data-lang', l); html.lang = l;
      try { localStorage.setItem('timus-lang', l); } catch (e) {}
    });
  });

  /* menu điện thoại */
  var burger = doc.querySelector('.burger'), head = doc.querySelector('.top');
  if (burger && head) {
    burger.addEventListener('click', function () { burger.setAttribute('aria-expanded', head.classList.toggle('open')); });
    all('.nav a').forEach(function (a) {
      a.addEventListener('click', function () { head.classList.remove('open'); burger.setAttribute('aria-expanded', false); });
    });
  }

  /* hiện dần khi cuộn tới */
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    html.classList.add('anim');
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    all('.reveal').forEach(function (el) { io.observe(el); });
  }

  /* tab, danh sách chi tiết */
  var canHover = matchMedia('(hover: hover) and (pointer: fine)').matches;
  all('[data-tabs]').forEach(function (box) {
    var bs = all('[data-tab]', box), ps = all('[data-panel]', box);
    function act(id) {
      bs.forEach(function (b) { var on = b.getAttribute('data-tab') === id; b.classList.toggle('on', on); b.setAttribute('aria-selected', on); });
      ps.forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-panel') === id); });
    }
    box._act = act;
    bs.forEach(function (b) {
      b.addEventListener('click', function () { act(b.getAttribute('data-tab')); });
      if (canHover && box.hasAttribute('data-hover')) b.addEventListener('mouseenter', function () { act(b.getAttribute('data-tab')); });
    });
  });

  /* các bước: rê chuột hiện mô tả */
  all('[data-steps]').forEach(function (w) {
    var lis = all('li', w), d = w.querySelector('.step-desc'); if (!lis.length || !d) return;
    function act(li) {
      lis.forEach(function (x) { x.classList.toggle('on', x === li); });
      d.innerHTML = '';
      var sd = li.querySelector('.sd');
      if (sd) d.appendChild(sd.cloneNode(true)); else all('p', li).forEach(function (p) { d.appendChild(p.cloneNode(true)); });
    }
    lis.forEach(function (li) {
      li.tabIndex = 0;
      li.addEventListener('mouseenter', function () { act(li); });
      li.addEventListener('focus', function () { act(li); });
      li.addEventListener('click', function () { act(li); });
    });
    act(lis[0]);
    w._act = act; w._lis = lis;
  });

  /* quy trình: khi cuộn tới thì các bước sáng lần lượt, một lần */
  all('#cach-lam [data-steps]').forEach(function (w) {
    if (!w._lis || !('IntersectionObserver' in window)) return;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { w._lis.forEach(function (li) { li.classList.add('done'); }); return; }
    var ran = false, touched = false;
    w._lis.forEach(function (li) { ['mouseenter', 'click', 'focus'].forEach(function (ev) { li.addEventListener(ev, function (e) { if (e.isTrusted) touched = true; }); }); });
    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting || ran || !w.classList.contains('on') && w.hasAttribute('data-panel')) return;
        ran = true; io2.disconnect();
        w._lis.forEach(function (li, i) {
          setTimeout(function () { li.classList.add('done'); if (!touched) w._act(li); }, 400 + i * 2200);
        });
      });
    }, { threshold: .5 });
    io2.observe(w);
  });

  /* minh hoạ trong thẻ dịch vụ: chỉ chạy khi nhìn thấy */
  if ('IntersectionObserver' in window) {
    var ioR = new IntersectionObserver(function (es) { es.forEach(function (e) { e.target.classList.toggle('run', e.isIntersecting); }); }, { threshold: .15 });
    all('[data-run]').forEach(function (el) { ioR.observe(el); });
  } else all('[data-run]').forEach(function (el) { el.classList.add('run'); });

  /* menu sáng mục đang xem (chỉ với liên kết trong trang) */
  var links = all('.nav a').filter(function (a) { return a.getAttribute('href').charAt(0) === '#'; });
  var secs = links.map(function (a) { return doc.getElementById(a.getAttribute('href').slice(1)); });
  if (links.length) {
    var spy = function () {
      var cur = -1, best = -1e9;
      secs.forEach(function (sec, i) { if (!sec) return; var t = sec.getBoundingClientRect().top - 140; if (t <= 0 && t > best) { best = t; cur = i; } });
      links.forEach(function (a, i) { a.classList.toggle('cur', i === cur); });
    };
    addEventListener('scroll', spy, { passive: true }); spy();
  }

  /* nền động: dải vàng chạy chéo theo nét logo */
  var c = doc.getElementById('heroFx');
  if (c && c.getContext) {
    var x = c.getContext('2d'), hero = c.parentElement, W, H, D = Math.min(window.devicePixelRatio || 1, 2), R = [], on = true, L, ANG = -0.56;
    var still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    var mk = function (first) {
      var wide = Math.random() < .3;
      var len = (wide ? .45 + Math.random() * .4 : .2 + Math.random() * .45) * L;
      return { u: first ? (Math.random() * 2 - 1) * L : -L - len, v: (Math.random() * 2 - 1) * L * .62, len: len,
        w: wide ? 26 + Math.random() * 54 : 1 + Math.random() * 2.2, wide: wide, sp: wide ? .7 + Math.random() * .9 : 1.8 + Math.random() * 3.2,
        a: wide ? .06 + Math.random() * .09 : .3 + Math.random() * .35 };
    };
    var size = function () {
      W = hero.clientWidth; H = hero.clientHeight; c.width = W * D; c.height = H * D; L = Math.sqrt(W * W + H * H) / 2 + 60;
      var n = W < 700 ? 18 : 34; R = []; for (var i = 0; i < n; i++) R.push(mk(true));
    };
    var frame = function () {
      x.setTransform(D, 0, 0, D, 0, 0); x.clearRect(0, 0, W, H);
      x.translate(W / 2, H / 2); x.rotate(ANG);
      for (var i = 0; i < R.length; i++) {
        var r = R[i]; r.u += r.sp; if (r.u > L) R[i] = r = mk(false);
        var g = x.createLinearGradient(r.u, 0, r.u + r.len, 0);
        g.addColorStop(0, 'rgba(212,168,98,0)'); g.addColorStop(.55, 'rgba(212,168,98,' + r.a + ')');
        g.addColorStop(.85, 'rgba(240,210,150,' + (r.a * 1.25).toFixed(3) + ')'); g.addColorStop(1, 'rgba(212,168,98,0)');
        x.fillStyle = g; x.fillRect(r.u, r.v - r.w / 2, r.len, r.w);
        if (!r.wide) {
          var hx = r.u + r.len * .9, hg = x.createRadialGradient(hx, r.v, 0, hx, r.v, 9);
          hg.addColorStop(0, 'rgba(255,236,190,' + Math.min(1, r.a * 1.8).toFixed(3) + ')'); hg.addColorStop(1, 'rgba(255,236,190,0)');
          x.fillStyle = hg; x.fillRect(hx - 9, r.v - 9, 18, 18);
        }
      }
    };
    var loop = function () { if (on && !doc.hidden) frame(); requestAnimationFrame(loop); };
    size(); frame();
    var rt; addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { size(); frame(); }, 150); });
    if (!still) {
      addEventListener('scroll', function () { on = hero.getBoundingClientRect().bottom > 0; }, { passive: true });
      requestAnimationFrame(loop);
    }
  }

  /* phần đầu trang: các mảng dịch vụ tự chạy lần lượt; bấm tab nào thì ra phần đó và dừng tự chuyển.
     Tổng quan và Technology là cụm giao diện động (.sv-live); Logistics, E-commerce là video. */
  var sv = doc.querySelector('[data-svc]');
  if (sv) {
    var vids = all('.sv-v', sv), svBtns = all('[data-tab]', sv), svSeen = false, svAuto = true, svT = 0;
    var svIds = svBtns.map(function (b) { return b.getAttribute('data-tab'); });
    var isVid = function (v) { return v.tagName === 'VIDEO'; };
    var durOf = function (v) { return (isVid(v) && v.duration && isFinite(v.duration)) ? v.duration : (parseFloat(v.getAttribute('data-dur')) || 12); };
    var svNext = function (i) { svGo(svIds[(i + 1) % svIds.length], true); };
    var svBar = function () {
      var cur = vids.filter(function (v) { return v.classList.contains('on'); })[0];
      svBtns.forEach(function (b) {
        b.classList.remove('go', 'hold');
        if (!b.classList.contains('on')) return;
        if (!svAuto) { b.classList.add('hold'); return; }
        b.style.setProperty('--dur', durOf(cur).toFixed(2) + 's'); void b.offsetWidth; if (svSeen) b.classList.add('go');
      });
    };
    var liveRun = function (v, restart) {
      if (restart || !v.classList.contains('run')) { v.classList.remove('run'); void v.offsetWidth; v.classList.add('run'); }
      clearTimeout(svT);
      if (svAuto) svT = setTimeout(function () { if (svAuto && v.classList.contains('on') && svSeen) svNext(vids.indexOf(v)); }, durOf(v) * 1000);
    };
    var svPlay = function (restart) {
      vids.forEach(function (v) {
        var on = v.classList.contains('on') && svSeen;
        if (isVid(v)) {
          if (on) { if (restart) { try { v.currentTime = 0; } catch (e) {} } v.loop = !svAuto; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
          else v.pause();
        } else if (on) liveRun(v, restart);
        else v.classList.remove('run');
      });
      svBar();
    };
    var sv3d = null;
    var svGo = function (id, restart) { clearTimeout(svT); sv._act(id); svPlay(restart); if (sv3d) sv3d.show(id); };
    vids.forEach(function (v, i) {
      if (!isVid(v)) return;
      v.addEventListener('ended', function () { if (svAuto && v.classList.contains('on')) svNext(i); });
      v.addEventListener('loadedmetadata', function () { if (v.classList.contains('on')) svBar(); });
      v.addEventListener('error', function () { if (svAuto && v.classList.contains('on')) setTimeout(function () { svNext(i); }, 4000); });
    });
    svBtns.forEach(function (b) {
      b.addEventListener('click', function () { svAuto = false; svGo(b.getAttribute('data-tab'), true); });
    });
    var svVis = function () {
      var r = sv.getBoundingClientRect(); var s = r.top < innerHeight * .8 && r.bottom > innerHeight * .25;
      if (s !== svSeen) { svSeen = s; clearTimeout(svT); svPlay(s); }
    };
    addEventListener('scroll', svVis, { passive: true }); addEventListener('resize', svVis); svVis();
    var svHash = function () { var id = location.hash.slice(1); if (id && svIds.indexOf(id) >= 0) { svAuto = false; svGo(id, true); } };
    addEventListener('hashchange', svHash); svHash();

    /* cụm giao diện động: co theo khung, nghiêng theo chuột */
    var stage = sv.querySelector('.sv-stage'), txs = all('.tx', sv);
    if (stage && txs.length) {
      var fit = function () { txs.forEach(function (tx) { tx.style.setProperty('--k', (stage.clientWidth / 640).toFixed(4)); }); };
      fit(); addEventListener('resize', fit); addEventListener('load', fit);
      if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
        stage.addEventListener('mousemove', function (e) {
          var r = stage.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
          all('.tx-w', sv).forEach(function (w) { w.style.transform = 'rotateX(' + (9 - y * 10).toFixed(2) + 'deg) rotateY(' + (-11 + x * 14).toFixed(2) + 'deg)'; });
        });
        stage.addEventListener('mouseleave', function () { all('.tx-w', sv).forEach(function (w) { w.style.transform = ''; }); });
      }
    }
  }

  /* dải logo sàn chạy ngang */
  /* cảnh 3D ở ba mảng dịch vụ: tải ngay khi trang dựng xong, mỗi khung có hiệu ứng chờ cho tới khi mô hình sẵn sàng */
  var sts = [].slice.call(doc.querySelectorAll('[data-3d]'));
  if (sts.length) {
    var no3d = function () { sts.forEach(function (el) { el.classList.add('fail'); }); };
    if (!window.WebGLRenderingContext) no3d();
    else {
      var go3d = function (m) { sts.forEach(function (el) { var s = m.mount(el, { only: true }); if (s) s.show(el.getAttribute('data-3d')); else el.classList.add('fail'); }); };
      import('/assets/scene3d.js?v=8').then(go3d).catch(function () {
        setTimeout(function () { import('/assets/scene3d.js?v=8&r=1').then(go3d).catch(no3d); }, 1500);
      });
    }
  }

  var t = doc.getElementById('lgTrack');
  if (t) {
    var g0 = t.querySelector('.lg-grp');
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { t.style.animation = 'none'; t.parentElement.style.overflowX = 'auto'; }
    else {
      var base = [].slice.call(g0.children).map(function (n) { return n.cloneNode(true); });
      var build = function () {
        all('.lg-grp[aria-hidden]', t).forEach(function (n) { n.remove(); });
        g0.innerHTML = ''; base.forEach(function (n) { g0.appendChild(n.cloneNode(true)); });
        var guard = 0;
        while (g0.offsetWidth < innerWidth * 1.2 && guard++ < 10) base.forEach(function (n) { var k = n.cloneNode(true); k.alt = ''; g0.appendChild(k); });
        var cp = g0.cloneNode(true); cp.setAttribute('aria-hidden', 'true'); t.appendChild(cp);
        t.style.animationDuration = Math.max(24, Math.round(g0.offsetWidth / 60)) + 's';
      };
      build(); addEventListener('load', build);
      var to; addEventListener('resize', function () { clearTimeout(to); to = setTimeout(build, 200); });
    }
  }
})();
