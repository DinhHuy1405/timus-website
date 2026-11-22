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
      all('p', li).forEach(function (p) { d.appendChild(p.cloneNode(true)); });
    }
    lis.forEach(function (li) {
      li.tabIndex = 0;
      li.addEventListener('mouseenter', function () { act(li); });
      li.addEventListener('focus', function () { act(li); });
      li.addEventListener('click', function () { act(li); });
    });
    act(lis[0]);
  });

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

  /* hành trình năm khâu: chạy theo lúc cuộn trang */
  var jr = doc.querySelector('.jr');
  if (jr) {
    var jsec = jr.closest('.jr-sec'), pin = jsec.querySelector('.jr-pin'), jbs = all('.jr-b', jr), jbox = jr.querySelector('.jr-box');
    var jcur = -1, jlock = 0;
    var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
    var isPinned = function () { return getComputedStyle(pin).position === 'sticky'; };
    var isRow = function () { return getComputedStyle(jr).display === 'grid'; };
    var jprog = function () {
      var vh = innerHeight, r;
      if (isPinned()) { r = jsec.getBoundingClientRect(); return clamp((64 - r.top) / Math.max(1, r.height - (vh - 64))); }
      r = jr.getBoundingClientRect();
      if (isRow()) return clamp((vh * .72 - r.top) / (vh * .6));
      return clamp((vh * .5 - r.top) / Math.max(1, r.height));
    };
    var jset = function (i) {
      if (i === jcur) return; jcur = i;
      jr._act('j' + (i + 1));
      jbs.forEach(function (b, k) { b.classList.toggle('done', k < i); });
    };
    var jtick = function () {
      var p = jprog(), n = jbs.length;
      if (Date.now() > jlock) jset(Math.round(p * (n - 1)));
      if (jbox && isRow()) {
        var t = p * (n - 1), i = Math.min(n - 2, Math.floor(t)), f = t - i, jrR = jr.getBoundingClientRect();
        var c = function (b) { var s = b.querySelector('svg').getBoundingClientRect(); return { x: s.left + s.width / 2 - jrR.left, y: s.top + s.height * .42 - jrR.top }; };
        var A = c(jbs[i]), B = c(jbs[i + 1]);
        var hop = Math.sin(f * Math.PI) * 16;
        jbox.style.transform = 'translate(' + (A.x + (B.x - A.x) * f - 23).toFixed(1) + 'px,' + (A.y + (B.y - A.y) * f - 40 - hop).toFixed(1) + 'px)';
        jbox.style.opacity = 1;
      }
    };
    jbs.forEach(function (b, k) {
      b.addEventListener('click', function () {
        if (isPinned()) {
          var r = jsec.getBoundingClientRect(), travel = r.height - (innerHeight - 64);
          scrollTo({ top: scrollY + r.top - 64 + travel * (k / (jbs.length - 1)) * .98 + 2, behavior: 'smooth' });
        } else { jlock = Date.now() + 2500; jcur = k; jbs.forEach(function (x, m) { x.classList.toggle('done', m < k); }); }
      });
    });
    var jraf = 0;
    var jreq = function () { if (!jraf) jraf = requestAnimationFrame(function () { jraf = 0; jtick(); }); };
    addEventListener('scroll', jreq, { passive: true }); addEventListener('resize', jreq); addEventListener('load', jtick); jtick();
  }

  /* dải logo sàn chạy ngang */
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
