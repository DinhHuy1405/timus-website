/* Ba cảnh 3D ở phần đầu trang timusco.com: Logistics, E-commerce, Technology.
   Mô hình: các bộ CC0 của Kenney (kenney.nl), đã đổi sang màu TIMUS. Chỉ tải trên máy tính, khi trang đã tải xong. */
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { MTLLoader } from 'three/addons/loaders/MTLLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const BASE = '/assets/3d/';
const GOLD = 0xd4a862, CREAM = 0xe9e2d2, DARK = 0x1c1915, INK = 0x0e0e0e;
const ease = (u) => { u = Math.min(1, Math.max(0, u)); return u * u * (3 - 2 * u); };
const M = {
  gold: new THREE.MeshStandardMaterial({ color: GOLD, metalness: .7, roughness: .35 }),
  cream: new THREE.MeshStandardMaterial({ color: CREAM, metalness: .1, roughness: .65 }),
  dark: new THREE.MeshStandardMaterial({ color: DARK, metalness: .2, roughness: .8 }),
  ink: new THREE.MeshStandardMaterial({ color: 0x121110, metalness: .4, roughness: .5 }),
  glow: new THREE.MeshStandardMaterial({ color: 0xffe2a8, emissive: 0xe3bd7e, emissiveIntensity: 1.6, roughness: .4 }),
};

/* ---------- tải mô hình: tối đa 3 file cùng lúc, lỗi thì thử lại ---------- */
const gl = new GLTFLoader(), ol = new OBJLoader();
let running = 0; const queue = [];
function slot(fn) {
  return new Promise((res, rej) => {
    const run = async () => {
      running++;
      try { let e; for (let i = 0; i < 4; i++) { try { res(await fn()); e = null; break; } catch (x) { e = x; await new Promise((r) => setTimeout(r, 350)); } } if (e) rej(e); }
      finally { running--; if (queue.length) queue.shift()(); }
    };
    running < 3 ? run() : queue.push(run);
  });
}
const glb = (p) => slot(() => new Promise((res, rej) => gl.load(BASE + p + '.glb', (g) => res(g.scene), undefined, rej)));
function ramp(c) {                                  /* màu gốc của bộ nội thất → tông TIMUS theo độ sáng */
  const L = .299 * c.r + .587 * c.g + .114 * c.b, mx = Math.max(c.r, c.g, c.b), mn = Math.min(c.r, c.g, c.b), S = mx ? (mx - mn) / mx : 0;
  const stops = S > .25 ? [[0, 0x16120c], [.4, 0x8a6426], [.7, 0xd4a862], [1, 0xf0e2c4]] : [[0, 0x121110], [.5, 0x4a443a], [1, 0xece6da]];
  for (let i = 0; i < stops.length - 1; i++) if (L <= stops[i + 1][0]) { const u = (L - stops[i][0]) / (stops[i + 1][0] - stops[i][0]); return new THREE.Color(stops[i][1]).lerp(new THREE.Color(stops[i + 1][1]), u); }
  return new THREE.Color(stops[stops.length - 1][1]);
}
const obj = (name) => slot(() => new Promise((res, rej) => {
  const ml = new MTLLoader(); ml.setPath(BASE + 'furn/');
  ml.load(name + '.mtl', (mats) => {
    mats.preload(); const o = new OBJLoader(); o.setMaterials(mats); o.setPath(BASE + 'furn/');
    o.load(name + '.obj', (g) => {
      g.traverse((m) => { if (m.isMesh) { const arr = Array.isArray(m.material) ? m.material : [m.material]; const out = arr.map((x) => new THREE.MeshStandardMaterial({ color: ramp(x.color || new THREE.Color(0x888888)), metalness: .15, roughness: .65 })); m.material = Array.isArray(m.material) ? out : out[0]; } });
      res(g);
    }, undefined, rej);
  }, undefined, rej);
}));
function prep(o, size) {                             /* đổ bóng, đo kích thước, co về cỡ mong muốn */
  o.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; if (m.material && !Array.isArray(m.material) && m.material.map) { m.material.metalness = .25; m.material.roughness = .6; } } });
  let b = new THREE.Box3().setFromObject(o); const d = b.getSize(new THREE.Vector3());
  if (size) o.scale.multiplyScalar(size / Math.max(d.x, d.y, d.z));
  b = new THREE.Box3().setFromObject(o); o.userData.min = b.min.y; o.userData.h = b.max.y - b.min.y; return o;
}
function put(parent, o, x, y, z, ry = 0) { o.position.set(x, y - o.userData.min, z); o.rotation.y = ry; parent.add(o); return o; }
function box(w, h, d, mat) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.castShadow = true; m.receiveShadow = true; return m; }
function platform(parent, w, d, x = 0, z = 0) {
  const g = new THREE.Group();
  const b = box(w, .6, d, M.dark); b.position.y = .3; g.add(b);
  const e = box(w + .12, .08, d + .12, M.gold); e.position.y = .62; e.castShadow = false; g.add(e);
  const t = box(w - .1, .05, d - .1, M.dark); t.position.y = .67; t.castShadow = false; g.add(t);
  g.position.set(x, 0, z); parent.add(g); return g;
}
const TOP = .7;
function dashed(parent, pts) {
  const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineDashedMaterial({ color: GOLD, dashSize: .3, gapSize: .26, transparent: true, opacity: .85 }));
  l.computeLineDistances(); parent.add(l); return l;
}
function screen(w, h, draw, cw = 512, ch = 320) {     /* màn hình tự phát sáng, vẽ bằng canvas */
  const c = document.createElement('canvas'); c.width = cw; c.height = ch; const x = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false }));
  m.userData.draw = (t) => { draw(x, cw, ch, t); tex.needsUpdate = true; }; m.userData.draw(0); return m;
}
const rr = (x, a, b, w, h, r, fill) => { x.beginPath(); x.roundRect(a, b, w, h, r); x.fillStyle = fill; x.fill(); };

/* ================= LOGISTICS: Trung Quốc → Việt Nam → Mỹ ================= */
async function logistics() {
  const root = new THREE.Group(); root.scale.setScalar(.78);
  /* mặt biển: mờ dần ra mép để hoà vào nền trang */
  const ac = document.createElement('canvas'); ac.width = ac.height = 256; const ax = ac.getContext('2d'); const gr = ax.createRadialGradient(128, 128, 30, 128, 128, 128);
  gr.addColorStop(0, '#fff'); gr.addColorStop(.62, '#fff'); gr.addColorStop(1, '#000'); ax.fillStyle = gr; ax.fillRect(0, 0, 256, 256);
  const sea = new THREE.Mesh(new THREE.PlaneGeometry(48, 30), new THREE.MeshStandardMaterial({ color: 0x1d1810, metalness: .8, roughness: .38, transparent: true, alphaMap: new THREE.CanvasTexture(ac) }));
  sea.rotation.x = -Math.PI / 2; sea.position.y = .02; sea.receiveShadow = true; root.add(sea);
  platform(root, 6, 10, -12.5); platform(root, 7, 10, -3.2); platform(root, 7, 10, 11.5);
  const r1 = dashed(root, Array.from({ length: 21 }, (_, i) => new THREE.Vector3(-9.3 + 2.4 * i / 20, .06, 1.6)));
  const r2 = dashed(root, Array.from({ length: 41 }, (_, i) => new THREE.Vector3(.6 + 7.2 * i / 40, .06, 1.6)));
  const [ship, boat, facA, facB, chim, tank, c1, c2, c3, pile, wh, whB, truck, van] = await Promise.all([
    glb('water/ship-cargo-a'), glb('water/ship-cargo-c'), glb('city/building-a'), glb('city/building-d'), glb('city/chimney-medium'), glb('city/detail-tank'), glb('city/shipping-container-a'),
    glb('city/shipping-container-b'), glb('water/cargo-container-a'), glb('water/cargo-pile-a'), glb('city/building-g'), glb('city/building-d'), glb('car/truck'), glb('car/delivery')]);
  /* Trung Quốc: nhà máy */
  put(root, prep(facA, 4.2), -13, TOP, -2.2); put(root, prep(chim, 3), -14.2, TOP, -4.2); put(root, prep(c1, 1.9), -11.4, TOP, 3.4, Math.PI / 2);
  /* Việt Nam: nhà máy và kho gom hàng */
  put(root, prep(facB, 3.4), -4.4, TOP, -2.6); put(root, prep(tank, 1.5), -1.6, TOP, -3); put(root, prep(c2, 1.9), -4.6, TOP, 3.6, Math.PI / 2);
  put(root, prep(truck, 2.2), -4.8, TOP, 1.2, Math.PI / 2);
  /* Mỹ: kho */
  put(root, prep(wh, 4.6), 12.6, TOP, -2.2); put(root, prep(whB, 3), 9.6, TOP, -3.4);
  put(root, prep(c3, 2), 9.4, TOP, 3.4, Math.PI / 2); put(root, prep(pile, 1.9), 9.6, TOP, 4.8); put(root, prep(van, 2.2), 10.6, TOP, 1.3, Math.PI / 2);
  put(root, prep(boat, 3), -8.9, 0, 1.6, Math.PI / 2); put(root, prep(ship, 6), 1.2, 0, 1.6, Math.PI / 2);
  for (const o of [ship, boat]) o.traverse((m) => { if (m.isMesh) { m.material = m.material.clone(); m.material.transparent = true; } });
  const sy = ship.position.y, by = boat.position.y, T = 13;
  return { root, T, cam: [11, 28.5], labels: [[['Trung Quốc', 'China'], -12.5 * .78, 5.2, -2.2], [['Việt Nam', 'Vietnam'], -3.2 * .78, 4.6, -2.6], [['Kho tại Mỹ', 'US warehouse'], 11.5 * .78, 5.4, -2.2]],
    update(t) {
      /* 0–3,5s: tàu nhỏ Trung Quốc → Việt Nam; 3–4,5s: xe tải ra cảng; 4,5–9,8s: tàu container Việt Nam → Mỹ; 9,8–12s: xe giao hàng rời kho */
      const u1 = ease((t - .4) / 3); boat.position.x = -8.9 + 1.6 * u1; boat.position.y = by + Math.sin(t * 2.6) * .04;
      truck.position.x = -4.8 + 2.4 * ease((t - 3) / 1.5);
      const u2 = ease((t - 4.5) / 5.3); ship.position.x = 1.2 + 6 * u2; ship.position.y = sy + Math.sin(t * 2.2) * .05; ship.rotation.z = Math.sin(t * 1.6) * .012;
      const f = t > T - 1 ? 1 - ease((t - (T - 1)) / .9) : ease(t / .8);
      for (const o of [ship, boat]) o.traverse((m) => { if (m.isMesh) m.material.opacity = f; });
      van.position.x = 10.6 + 5 * ease((t - 9.8) / 2.2); van.visible = t < 12.1;
      r1.material.dashOffset = -t * .6; r2.material.dashOffset = -t * .6;
    } };
}

/* ================= E-COMMERCE ================= */
async function ecommerce() {
  const root = new THREE.Group();
  platform(root, 20, 9.5);
  /* điện thoại: gian hàng trên sàn */
  const phone = new THREE.Group();
  const body = box(3.3, 6.2, .34, M.ink); phone.add(body);
  const rim = box(3.42, 6.32, .22, M.gold); rim.castShadow = false; phone.add(rim);
  const scr = screen(2.95, 5.7, (x, w, h, t) => {
    x.fillStyle = '#14120e'; x.fillRect(0, 0, w, h); rr(x, 16, 16, w - 32, 44, 10, '#d4a862');
    const hi = Math.floor(t / 1.6) % 6;
    for (let i = 0; i < 6; i++) { const cx = 16 + (i % 2) * ((w - 44) / 2 + 12), cy = 78 + Math.floor(i / 2) * 128, tw = (w - 44) / 2;
      rr(x, cx, cy, tw, 112, 10, i === hi ? '#f0e2c4' : '#2a251c'); rr(x, cx + 12, cy + 12, tw - 24, 56, 6, i === hi ? '#d4a862' : '#4a4030'); rr(x, cx + 12, cy + 78, tw - 54, 8, 4, i === hi ? '#8a6426' : '#5a503e');
      if (i === hi) { x.lineWidth = 4; x.strokeStyle = '#d4a862'; x.beginPath(); x.roundRect(cx, cy, tw, 112, 10); x.stroke(); } }
    rr(x, 16, h - 70, w - 32, 50, 12, (t % 1.6) > 1.1 ? '#f0e2c4' : '#d4a862');
  }, 320, 600);
  scr.position.z = .18; phone.add(scr);
  phone.position.set(-6.9, TOP + 3.25, -.6); phone.rotation.set(-.12, .5, 0); root.add(phone);
  const stand = box(1.6, .3, 1.2, M.gold); stand.position.set(-6.9, TOP + .15, -.9); root.add(stand);
  /* băng chuyền */
  const belt = box(9.2, .5, 1.5, M.ink); belt.position.set(.2, TOP + .55, 1.2); root.add(belt);
  for (const z of [.42, 1.98]) { const r = box(9.3, .16, .1, M.gold); r.position.set(.2, TOP + .86, z); r.castShadow = false; root.add(r); }
  for (const x of [-3.8, .2, 4.2]) { const l = box(.3, .5, 1.3, M.dark); l.position.set(x, TOP + .15, 1.2); root.add(l); }
  const [b1, b2, pile, van, c1] = await Promise.all([obj('cardboardBoxClosed'), obj('cardboardBoxOpen'), glb('water/cargo-pile-a'), glb('car/delivery'), glb('city/shipping-container-a')]);
  prep(b1, .95); const boxes = [0, 1, 2, 3].map((k) => { const o = k ? b1.clone() : b1; o.userData = b1.userData; put(root, o, 0, TOP + .8, 1.2); return o; });
  put(root, prep(b2, 1.2), -4.6, TOP, 3.2, .4); put(root, prep(pile, 2.4), -2.2, TOP, -2.6); put(root, prep(c1, 2.6), 2.2, TOP, -2.8, Math.PI / 2);
  put(root, prep(van, 3.4), 7.4, TOP, 1.2, Math.PI / 2);
  const vx = van.position.x, by = boxes[0].position.y, T = 12;
  return { root, T, cam: [9.4, 20.8, 3.3], labels: [[['Gian hàng trên sàn', 'Marketplace store'], -6.9, 8.4, -.6], [['Đóng gói, giao đơn', 'Packing and delivery'], 2.4, 4.2, 1.2]],
    update(t) {
      scr.userData.draw(t);
      boxes.forEach((o, k) => { const u = ((t / 6) + k / 4) % 1; o.position.x = -4.2 + 9.2 * u; const s = Math.min(1, u * 8, (1 - u) * 8); o.scale.setScalar(b1.scale.x * Math.max(.01, s)); o.position.y = by; o.rotation.y = k * .7; });
      van.position.x = vx + (t > 9.6 ? 5.5 * ease((t - 9.6) / 1.6) : 0) - (t < 1 ? 5.5 * (1 - ease(t / 1)) : 0); van.position.y = TOP - van.userData.min + Math.abs(Math.sin(t * 6)) * .012;
      phone.position.y = TOP + 3.25 + Math.sin(t * 1.4) * .06;
    } };
}

/* ================= TECHNOLOGY ================= */
async function technology() {
  const root = new THREE.Group();
  platform(root, 20, 10);
  /* màn hình dashboard lớn: phân tích dữ liệu */
  const dash = new THREE.Group(); dash.add(box(6.6, 4, .3, M.ink)); const dr = box(6.75, 4.15, .18, M.gold); dr.castShadow = false; dash.add(dr);
  const ds = screen(6.2, 3.6, (x, w, h, t) => {
    x.fillStyle = '#14120e'; x.fillRect(0, 0, w, h);
    for (let i = 0; i < 3; i++) { rr(x, 18 + i * 162, 16, 148, 58, 8, '#231f17'); rr(x, 30 + i * 162, 28, 60, 8, 4, '#6b5f48'); rr(x, 30 + i * 162, 44, 90 + 20 * Math.sin(t * .8 + i), 16, 4, '#d4a862'); }
    for (let i = 0; i < 9; i++) { const bh = 40 + 110 * (.5 + .5 * Math.sin(t * 1.1 + i * .7)) * (.5 + i / 16); rr(x, 26 + i * 52, h - 22 - bh, 30, bh, 4, i % 3 === 2 ? '#d4a862' : '#5a4a2a'); }
    x.beginPath(); for (let i = 0; i <= 40; i++) { const px = 20 + i * (w - 40) / 40, py = 150 - 34 * Math.sin(t * .9 + i * .32) - i * 1.2; i ? x.lineTo(px, py) : x.moveTo(px, py); } x.lineWidth = 4; x.strokeStyle = '#f0e2c4'; x.stroke();
  });
  ds.position.z = .16; dash.add(ds); dash.position.set(0, TOP + 3.6, -3.4); root.add(dash);
  const pole = box(.4, 1.6, .4, M.dark); pole.position.set(0, TOP + .8, -3.5); root.add(pole);
  /* bàn làm việc: website */
  const [desk, chair, kb, lap, bopen] = await Promise.all([obj('desk'), obj('chairDesk'), obj('computerKeyboard'), obj('laptop'), obj('cardboardBoxOpen')]);
  put(root, prep(desk, 3.4), -6.6, TOP, .4, .35); const dh = desk.userData.h;
  put(root, prep(lap, 1.3), -6.5, TOP + dh, .3, .35); put(root, prep(chair, 1.9), -5.6, TOP, 2.4, Math.PI + .5);
  const site = screen(2.6, 1.7, (x, w, h) => { x.fillStyle = '#f2efe8'; x.fillRect(0, 0, w, h); rr(x, 0, 0, w, 40, 0, '#14120e'); rr(x, 20, 12, 70, 16, 4, '#d4a862'); rr(x, 26, 70, 250, 26, 6, '#14120e'); rr(x, 26, 108, 180, 12, 5, '#a39e93'); rr(x, 26, 140, 110, 34, 6, '#d4a862'); for (let i = 0; i < 3; i++) rr(x, 26 + i * 158, 204, 144, 92, 8, ['#e9dcc0', '#dce3ee', '#d6e8db'][i]); });
  const sf = new THREE.Group(); sf.add(box(2.8, 1.9, .14, M.ink)); site.position.z = .08; sf.add(site); sf.position.set(-7.4, TOP + dh + 1.75, -.9); sf.rotation.y = .35; root.add(sf);
  const sp = box(.2, .9, .2, M.dark); sp.position.set(-7.4, TOP + dh + .45, -1); root.add(sp);
  put(root, prep(kb, .9), -6, TOP + dh, 1.1, .35);
  /* nghiên cứu sản phẩm: sản phẩm trên bệ, vòng quét */
  const ped = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.35, .7, 28), M.ink); ped.position.set(6.6, TOP + .35, .6); ped.castShadow = true; root.add(ped);
  put(root, prep(bopen, 1.3), 6.6, TOP + .7, .6, .5);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(1.35, .05, 10, 48), M.glow); ring.rotation.x = Math.PI / 2; root.add(ring);
  /* robot: AI agents */
  const bot = new THREE.Group();
  const bb = box(1.3, 1.4, 1, M.cream); bb.position.y = 1.1; bot.add(bb); const hd = box(1.1, .85, .9, M.cream); hd.position.y = 2.35; bot.add(hd);
  for (const ex of [-.26, .26]) { const e = box(.2, .2, .06, M.glow); e.position.set(ex, 2.4, .47); bot.add(e); }
  const an = box(.07, .45, .07, M.dark); an.position.y = 3; bot.add(an); const ab = new THREE.Mesh(new THREE.SphereGeometry(.13, 16, 12), M.glow); ab.position.y = 3.3; bot.add(ab);
  for (const ax of [-.82, .82]) { const a = box(.26, .95, .3, M.gold); a.position.set(ax, 1.15, 0); bot.add(a); }
  const ft = new THREE.Mesh(new THREE.CylinderGeometry(.8, .95, .4, 24), M.dark); ft.position.y = .2; ft.castShadow = true; bot.add(ft);
  bot.position.set(1.4, TOP, 2.2); root.add(bot);
  const targets = [new THREE.Vector3(-6.4, TOP + 2.6, .2), new THREE.Vector3(0, TOP + 3.4, -2.8), new THREE.Vector3(6.6, TOP + 2.6, .6)];
  const home = new THREE.Vector3(1.4, TOP + 3.4, 2.2);
  const drones = targets.map((tg) => {
    const g = new THREE.Group(); g.add(box(.42, .22, .42, M.glow)); const p = box(.26, .2, .26, M.gold); p.position.y = -.24; g.add(p); root.add(g);
    const mid = home.clone().lerp(tg, .5); mid.y += 1.6; const cv = new THREE.QuadraticBezierCurve3(home, mid, tg);
    dashed(root, [new THREE.Vector3(1.4, TOP + .06, 2.2), new THREE.Vector3(tg.x, TOP + .06, tg.z)]); return { g, cv };
  });
  const T = 12;
  return { root, T, cam: [9.6, 20.6, 3.2], labels: [[['Website', 'Websites'], -7.2, 5.7, -.9], [['Phân tích dữ liệu', 'Data analysis'], 0, 7.7, -3.4], [['Nghiên cứu sản phẩm', 'Product research'], 6.6, 4.9, .6], [['AI agents', 'AI agents'], 1.4, 5.2, 2.2]],
    update(t) {
      ds.userData.draw(t);
      ring.position.set(6.6, TOP + 1.3 + .8 * Math.sin(t * 1.6), .6);
      bot.position.y = TOP + Math.sin(t * 2.4) * .06; bot.rotation.y = Math.sin(t * .5) * .35;
      drones.forEach((d, k) => { const u = ((t / 6) + k / 3) % 1, w = ease(1 - Math.abs(2 * u - 1)); d.g.position.copy(d.cv.getPoint(w)); d.g.rotation.y = t * 2; });
    } };
}

const BUILD = { 'logistics': logistics, 'thuong-mai-dien-tu': ecommerce, 'cong-nghe': technology };

/* ---------- gắn vào khung ---------- */
export function mount(host) {
  let renderer;
  try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); } catch (e) { return null; }
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.55;
  host.prepend(renderer.domElement);
  const scene = new THREE.Scene();
  scene.add(new THREE.HemisphereLight(0xfff1d6, 0x2a2010, 1.5));
  const sun = new THREE.DirectionalLight(0xffe2b0, 2.5); sun.position.set(-9, 17, 12); sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -16, right: 16, top: 12, bottom: -12, near: 1, far: 60 }); sun.shadow.bias = -.0006; scene.add(sun);
  const rim = new THREE.DirectionalLight(GOLD, 1.2); rim.position.set(12, 8, -12); scene.add(rim);
  const cam = new THREE.PerspectiveCamera(30, 4 / 3, .1, 200); cam.position.set(0, 13, 35);
  const ctl = new OrbitControls(cam, renderer.domElement); ctl.target.set(0, 2.2, 0); ctl.enableZoom = false; ctl.enablePan = false; ctl.enableDamping = true;
  ctl.minPolarAngle = .8; ctl.maxPolarAngle = 1.35; ctl.minAzimuthAngle = -.6; ctl.maxAzimuthAngle = .6;
  const size = () => { const w = host.clientWidth, h = host.clientHeight; if (!w || !h) return; renderer.setSize(w, h, false); cam.aspect = w / h; cam.fov = 30 * Math.max(1, 1.34 / cam.aspect); cam.updateProjectionMatrix(); };
  size(); addEventListener('resize', size);

  const scenes = {}, lbs = [], v3 = new THREE.Vector3();
  let cur = null, t0 = performance.now(), seen = true, want = null;
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function labels(list) {
    lbs.forEach((l) => l.el.remove()); lbs.length = 0;
    (list || []).forEach(([txt, x, y, z]) => { const el = document.createElement('div'); el.className = 'hx-lb'; el.innerHTML = '<span data-l="vi">' + txt[0] + '</span><span data-l="en">' + txt[1] + '</span>'; host.appendChild(el); lbs.push({ el, x, y, z }); });
  }
  async function show(id) {
    want = id;
    if (!BUILD[id]) { cur = null; host.classList.remove('on'); return; }
    if (!scenes[id]) { try { scenes[id] = await BUILD[id](); } catch (e) { scenes[id] = null; } }
    if (want !== id) return;
    const s = scenes[id]; if (!s) { cur = null; host.classList.remove('on'); return; }
    if (cur) scene.remove(cur.root);
    cur = s; scene.add(s.root); labels(s.labels); t0 = performance.now(); ctl.reset(); cam.position.set(0, s.cam[0], s.cam[1]); ctl.target.set(0, s.cam[2] || 2.2, 0); ctl.update(); size(); host.classList.add('on');
  }
  new IntersectionObserver((es) => { seen = es[0].isIntersecting; }).observe(host);
  (function tick() {
    requestAnimationFrame(tick);
    if (!cur || !seen || document.hidden) return;
    const t = still ? cur.T * .5 : ((performance.now() - t0) / 1000) % cur.T;
    cur.update(t); ctl.update(); renderer.render(scene, cam);
    const w = host.clientWidth, h = host.clientHeight;
    lbs.forEach((l) => { v3.set(l.x, l.y, l.z).project(cam); l.el.style.transform = 'translate(-50%,-100%) translate(' + ((v3.x * .5 + .5) * w).toFixed(1) + 'px,' + ((-v3.y * .5 + .5) * h).toFixed(1) + 'px)'; });
  })();
  /* dựng sẵn cả ba cảnh ở nền để lúc chuyển tab không phải chờ */
  (async () => { for (const id of Object.keys(BUILD)) if (!scenes[id]) { try { scenes[id] = await BUILD[id](); } catch (e) { scenes[id] = null; } } })();
  return { show };
}
