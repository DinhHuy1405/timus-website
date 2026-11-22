"""Các khối của trang chủ: phần đầu trang (các mảng dịch vụ tự chạy lần lượt) và lưới 6 dịch vụ có minh hoạ động.
Chữ là cặp (tiếng Việt, tiếng Anh). Sửa ở đây rồi chạy python3 tools/build.py."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ZALO = 'https://zalo.me/0796796492'


def L(t):
    return f'<span data-l="vi">{t[0]}</span><span data-l="en">{t[1]}</span>'


def chips(names):
    return ''.join(f'<i>{n}</i>' for n in names)


# ---------- luồng vận hành tổng quan (dựng bằng HTML, không dùng video) ----------
TABS = [
    {'id': 'tong-quan', 't': ('Tổng quan', 'Overview'),
     'h': ('Thương mại điện tử và công nghệ cho doanh nghiệp Việt', 'E-commerce and technology for Vietnamese businesses'),
     'd': ('Từ nguồn hàng tại Việt Nam, Trung Quốc đến đơn hàng trên sàn tại Việt Nam và Mỹ. TIMUS điều phối cả chuỗi và báo cáo rõ từng tháng.',
           'From sourcing in Vietnam and China to orders on marketplaces in Vietnam and the United States. TIMUS coordinates the whole chain and reports every month.'),
     'links': [('#dich-vu', ('Xem các dịch vụ', 'See the services'))]},
    {'id': 'logistics', 't': ('Logistics', 'Logistics'),
     'h': ('Logistics: nhập hàng Trung Quốc về Việt Nam, đưa hàng sang Mỹ', 'Logistics: China to Vietnam imports, and shipping to the US'),
     'd': ('Tìm nhà máy và nhập hàng từ Trung Quốc về Việt Nam; bao bì, tem nhãn, giấy tờ xuất nhập khẩu, vận chuyển sang Mỹ và kho tại Mỹ kết nối các sàn.',
           'Factory sourcing and imports from China to Vietnam; packaging, labels, export and import paperwork, shipping to the US and a US warehouse connected to marketplaces.'),
     'links': [('/nguon-hang/', ('Nguồn hàng', 'Sourcing')), ('/hau-can/', ('Hậu cần', 'Logistics'))]},
    {'id': 'thuong-mai-dien-tu', 't': ('E-commerce', 'E-commerce'),
     'h': ('E-commerce: bán hàng trên sàn tại Việt Nam và Mỹ', 'E-commerce: selling on marketplaces in Vietnam and the US'),
     'd': ('Mở gian hàng, quảng cáo, KOC và creator, chăm sóc người mua, báo cáo và đối soát hằng tháng trước ngày 05.',
           'Store setup, ads, KOCs and creators, customer service, with a monthly report and reconciliation before the 5th.'),
     'links': [('/ban-hang-tai-viet-nam/', ('Bán tại Việt Nam', 'Selling in Vietnam')), ('/ban-hang-tai-my/', ('Bán tại Mỹ', 'Selling in the US'))]},
    {'id': 'cong-nghe', 't': ('Technology', 'Technology'),
     'h': ('Technology: website, dữ liệu và AI agents', 'Technology: websites, data and AI agents'),
     'd': ('Hệ thống website, nghiên cứu sản phẩm, phân tích dữ liệu và hệ thống AI agents tự động cho doanh nghiệp.',
           'Website systems, product research, data analysis and automated AI agent systems for businesses.'),
     'links': [('/tro-ly-ai/', ('AI agents', 'AI agents')), ('/dashboard-ket-noi-website/', ('Dashboard, website', 'Dashboards, websites')), ('/nghien-cuu-san-pham/', ('Nghiên cứu sản phẩm', 'Product research'))]},
]


def hero():
    copy = []
    for i, t in enumerate(TABS):
        tag = 'h1' if i == 0 else 'p'
        links = ''.join(f'<a class="link" href="{h}">{L(x)} →</a>' for h, x in t['links'])
        copy.append(f'''        <div class="hx-c{' on' if i == 0 else ''}" data-panel="{t['id']}">
          <{tag} class="hx-h">{L(t['h'])}</{tag}>
          <p class="lead">{L(t['d'])}</p>
          <p class="hx-links">{links}</p>
        </div>''')
    tabs = '\n'.join(f'''      <button type="button" class="hx-t{' on' if i == 0 else ''}" id="{t['id']}" data-tab="{t['id']}" role="tab" aria-selected="{'true' if i == 0 else 'false'}"><span class="hx-n">0{i + 1}</span><b>{L(t['t'])}</b><i class="hx-pg" aria-hidden="true"></i></button>''' for i, t in enumerate(TABS))

    marks = ''.join(f'<i class="sv-v sv-live{" on" if i == 0 else ""}" data-panel="{t["id"]}" data-dur="7" hidden></i>' for i, t in enumerate(TABS))
    return f'''<section class="hero hx" data-svc data-tabs>
  <canvas id="heroFx" class="hero-fx" aria-hidden="true"></canvas>
  <div class="wrap hx-in">
    <div class="hx-l">
      <p class="eyebrow">Logistics, E-Commerce &amp; Technology</p>
      <div class="hx-copy">
{chr(10).join(copy)}
      </div>
      <div class="cta">
        <a class="btn btn-gold" href="{ZALO}" target="_blank" rel="noopener">{L(('Nhắn Zalo', 'Message on Zalo'))}</a>
        <a class="btn btn-line" href="mailto:info@timusco.com?subject=TIMUS%20-%20Lien%20he%20bao%20gia">{L(('Gửi email báo giá', 'Request a quote'))}</a>
      </div>
    </div>
    <div class="hx-r">
      <img class="hx-logo" src="/assets/timus-logo.webp" alt="Logo TIMUS" width="900" height="760">
      {marks}
    </div>
  </div>
  <div class="wrap">
    <div class="hx-tabs" role="tablist">
{tabs}
    </div>
  </div>
</section>'''


# ---------- 6 dịch vụ, mỗi thẻ một minh hoạ động ----------
def _mi_research():
    return '''<div class="mi mi-res"><div class="mi-bars"><i style="--h:38%;--d:0s"></i><i style="--h:62%;--d:.15s"></i><i style="--h:48%;--d:.3s"></i><i style="--h:84%;--d:.45s"></i><i style="--h:66%;--d:.6s"></i><i style="--h:30%;--d:.75s"></i></div><span class="mi-lens"></span></div>'''


def _mi_source():
    row = '<span class="mi-row"><em></em><b></b></span>'
    return f'''<div class="mi mi-src"><div class="mi-col"><strong>{L(('Việt Nam', 'Vietnam'))}</strong>{row * 3}</div><div class="mi-col pick"><strong>{L(('Trung Quốc', 'China'))}</strong>{row * 3}</div><span class="mi-box">{L(('Mẫu', 'Sample'))}</span></div>'''


def _mi_shop(names, cls):
    return f'''<div class="mi mi-shop {cls}"><div class="mi-chips">{''.join(f'<i style="--d:{i * .9:.1f}s">{n}</i>' for i, n in enumerate(names))}</div><div class="mi-orders"><span style="--d:.4s"></span><span style="--d:1.3s"></span><span style="--d:2.2s"></span><span style="--d:3.1s"></span><em>{L(('đơn mới', 'new orders'))}</em></div></div>'''


def _mi_tech():
    return f'''<div class="mi mi-tech"><svg viewBox="0 0 220 96" aria-hidden="true"><path class="mi-l" d="M40 26 L110 74 L180 26 Z"/><circle class="mi-d" r="3.5"><animateMotion dur="3s" repeatCount="indefinite" path="M40 26 L110 74 L180 26 Z"/></circle><circle class="mi-d" r="3.5"><animateMotion dur="3s" begin="-1.5s" repeatCount="indefinite" path="M40 26 L110 74 L180 26 Z"/></circle></svg><b style="left:6%;top:8%">{L(('Sàn', 'Marketplaces'))}</b><b style="right:6%;top:8%">Website</b><b style="left:50%;bottom:4%;transform:translateX(-50%)">{L(('Kho', 'Warehouse'))}</b></div>'''


def _mi_logi():
    steps = (('Đóng gói', 'Pack'), ('Giấy tờ', 'Paperwork'), ('Vận chuyển', 'Ship'), ('Kho tại Mỹ', 'US warehouse'))
    return f'''<div class="mi mi-logi"><span class="mi-track"><i></i></span><div class="mi-steps">{''.join(f'<span style="--d:{i * 1.1:.1f}s">{L(s)}</span>' for i, s in enumerate(steps))}</div></div>'''


CARDS = [
    ('nghien-cuu-san-pham', _mi_research, ('Lọc số liệu sàn để biết bán gì, giá bao nhiêu, lời lãi dự kiến, trước khi bỏ tiền làm hàng.', 'Filter marketplace data to know what to sell, at what price and margin, before money goes into inventory.')),
    ('nguon-hang', _mi_source, ('So sánh nhà máy Việt Nam, Trung Quốc; làm mẫu, bao bì và lô thử trước khi làm lô lớn.', 'Compare factories in Vietnam and China; samples, packaging and a test batch before scaling.')),
    ('ban-hang-tai-my', lambda: _mi_shop(['Amazon', 'TikTok Shop US', 'Walmart', 'Shopify'], 'us'), ('Mở gian hàng, quảng cáo, creator và vận hành hằng ngày trên các sàn tại Mỹ.', 'Store setup, ads, creators and daily operations on US marketplaces.')),
    ('ban-hang-tai-viet-nam', lambda: _mi_shop(['Shopee', 'TikTok Shop', 'Lazada', 'Tiki'], 'vn'), ('Mở gian hàng, quảng cáo, KOC và vận hành hằng ngày trên các sàn tại Việt Nam.', 'Store setup, ads, KOCs and daily operations on Vietnamese marketplaces.')),
    ('dashboard-ket-noi-website', _mi_tech, ('Dashboard tổng hợp và đồng bộ đơn hàng, tồn kho giữa sàn, website và kho; kèm AI agents tự động.', 'Unified dashboards and order and stock sync across marketplaces, website and warehouse; plus automated AI agents.')),
    ('hau-can', _mi_logi, ('Đóng gói, tem nhãn, giấy tờ xuất nhập khẩu, kho tại Mỹ; pháp lý và thuế do đơn vị đối tác làm.', 'Packing, labels, export and import paperwork, US warehouse; legal and tax handled by partner specialists.')),
]


PILLARS = [
    {'id': 'logistics', 'name': 'Logistics',
     'h': ('Từ nhà máy đến kho tại Mỹ', 'From the factory to a US warehouse'),
     'd': ('Hàng đi theo hai chặng: nhập từ Trung Quốc về Việt Nam, rồi từ Việt Nam sang kho tại Mỹ. TIMUS lo nhà máy, bao bì, giấy tờ và vận chuyển.',
           'Goods move in two legs: from China into Vietnam, then from Vietnam to a US warehouse. TIMUS handles factories, packaging, paperwork and shipping.'),
     'items': ['nguon-hang', 'hau-can']},
    {'id': 'thuong-mai-dien-tu', 'name': 'E-commerce',
     'h': ('Vận hành gian hàng tại Việt Nam và Mỹ', 'Running stores in Vietnam and the US'),
     'd': ('Gian hàng trên các sàn tại Việt Nam và Mỹ, từ lúc mở gian hàng đến quảng cáo, chăm sóc người mua và đối soát hằng tháng.',
           'Stores on marketplaces in Vietnam and the US, from setup to ads, customer service and monthly reconciliation.'),
     'items': ['ban-hang-tai-viet-nam', 'ban-hang-tai-my']},
    {'id': 'cong-nghe', 'name': 'Technology',
     'h': ('Website, dữ liệu và AI agents', 'Websites, data and AI agents'),
     'd': ('Website, dashboard số liệu, nghiên cứu sản phẩm và các AI agents làm việc tự động cho doanh nghiệp.',
           'Websites, data dashboards, product research and AI agents that run tasks automatically for your business.'),
     'items': ['nghien-cuu-san-pham', 'dashboard-ket-noi-website', 'tro-ly-ai']},
]


def services(by, P):
    short = {slug: sh for slug, _mi, sh in CARDS}
    out, n = [], 0
    for i, pl in enumerate(PILLARS):
        rows = []
        for slug in pl['items']:
            n += 1
            pg = by[slug]
            title = ('AI agents cho đội ngũ', 'AI agents for your team') if slug == 'tro-ly-ai' else pg['title']
            sh = short.get(slug) or pg['short']
            if slug == 'dashboard-ket-noi-website':
                sh = ('Dashboard tổng hợp và đồng bộ đơn hàng, tồn kho giữa sàn, website và kho.', 'Unified dashboards and order and stock sync across marketplaces, website and warehouse.')
            rows.append(f'''          <a class="pl-a" href="/{slug}/"><span class="num">0{n}</span><span class="pl-at"><b>{L(title)}</b><span>{L(sh)}</span></span><i aria-hidden="true">→</i></a>''')
        out.append(f'''      <div class="pl{' rev' if i % 2 else ''} reveal" id="mang-{pl['id']}">
        <div class="pl-tx">
          <p class="pl-k">{pl['name']}</p>
          <h3 class="pl-h">{L(pl['h'])}</h3>
          <p class="pl-d">{L(pl['d'])}</p>
          <div class="pl-ls">
{chr(10).join(rows)}
          </div>
        </div>
        <div class="pl-st" data-3d="{pl['id']}" aria-hidden="true">
          <div class="pl-wait"><span class="pl-bars"><i></i><i></i><i></i></span><em>{L(('Đang tải mô hình 3D', 'Loading the 3D model'))}</em></div>
        </div>
      </div>''')
    return f'''<section id="dich-vu" class="sec pillars">
  <div class="wrap">
    <p class="eyebrow">{L(('Dịch vụ', 'Services'))}</p>
    <h2>{L(('Ba mảng dịch vụ, chọn đúng khâu doanh nghiệp cần', 'Three service areas, take only the stages you need'))}</h2>
    <p class="sub">{L(('Mỗi khâu là một phần việc riêng, có trang chi tiết riêng. Doanh nghiệp có thể bắt đầu từ nghiên cứu, hoặc vào thẳng khâu vận hành nếu đã có sản phẩm.', 'Each stage is a separate scope with its own page. Start with research, or go straight to operations if your product is ready.'))}</p>
{chr(10).join(out)}
  </div>
</section>
'''
