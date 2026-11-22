"""Khối "hành trình năm khâu" trên trang chủ: mô hình khối 3D vẽ bằng SVG, chạy theo lúc cuộn trang."""

U = 22
OX, OY = 120, 86


def _pt(x, y, z):
    return f'{(x - y) * 0.866 * U + OX:.1f},{(x + y) * 0.5 * U - z * U + OY:.1f}'


def prism(x, y, z, w, d, h, k):
    top = ' '.join([_pt(x, y, z + h), _pt(x + w, y, z + h), _pt(x + w, y + d, z + h), _pt(x, y + d, z + h)])
    left = ' '.join([_pt(x, y + d, z + h), _pt(x + w, y + d, z + h), _pt(x + w, y + d, z), _pt(x, y + d, z)])
    right = ' '.join([_pt(x + w, y, z + h), _pt(x + w, y + d, z + h), _pt(x + w, y + d, z), _pt(x + w, y, z)])
    return f'<polygon class="{k} l" points="{left}"/><polygon class="{k} r" points="{right}"/><polygon class="{k} t" points="{top}"/>'


BASE = prism(0, 0, 0, 6, 6, .4, 'k')
MODELS = {
    'research': [(.8, 2.5, .4, 1, 1, 1.0, 'g'), (2.4, 2.5, .4, 1, 1, 1.8, 'g'), (4.0, 2.5, .4, 1, 1, 2.8, 'g')],
    'factory': [(1, 1, .4, 4, 3, 1.6, 'k'), (1, 1, 2.0, 1.3, 3, .5, 'g'), (2.5, 1, 2.0, 1.3, 3, .5, 'g'), (4.2, 1.3, 2.0, .6, .6, 1.7, 'g'), (2.5, 4, .4, 1, .3, .9, 'g')],
    'ship': [(.8, 1, .4, 4.4, 1.8, 1.6, 'g'), (1, 3.6, .4, 1.4, 1.4, 1.2, 'k'), (3, 3.6, .4, 1.4, 1.4, 1.2, 'k'), (2, 3.8, 1.6, 1.2, 1.2, 1.0, 'g')],
    'store': [(1, 1, .4, 4, 2.6, 2.0, 'k'), (1.6, 1.4, 2.4, 2.8, .4, .7, 'g'), (.8, 3.4, 1.5, 4.4, 1, .25, 'g'), (4.2, 4.4, .4, 1, 1, .8, 'g')],
    'report': [(2.7, 2.2, .4, .6, .3, .6, 'g'), (.8, 2.2, 1.0, 4.4, .3, 2.6, 'k'), (1.3, 2.5, 1.3, .6, .08, .8, 'g'), (2.3, 2.5, 1.3, .6, .08, 1.4, 'g'), (3.3, 2.5, 1.3, .6, .08, 2.0, 'g')],
}


def model(name):
    body = ''.join(prism(*q) for q in MODELS[name])
    extra = ''
    if name == 'research':
        cx, cy = [float(v) for v in _pt(3.4, 5.0, 1.5).split(',')]
        extra = (f'<circle class="lens" cx="{cx:.1f}" cy="{cy:.1f}" r="13"/>'
                 f'<line class="lens" x1="{cx + 9:.1f}" y1="{cy + 9:.1f}" x2="{cx + 21:.1f}" y2="{cy + 21:.1f}"/>')
    return f'<svg class="iso" viewBox="0 0 240 226" aria-hidden="true"><g class="iso-base">{BASE}</g><g class="iso-m">{body}{extra}</g></svg>'


def parcel():
    """Kiện hàng nhỏ chạy dọc chuỗi theo lúc cuộn."""
    return f'<svg class="iso" viewBox="60 40 120 110" aria-hidden="true">{prism(2, 2, 0, 2, 2, 1.6, "g")}</svg>'


JOURNEY = [
    {'m': 'research', 't': ('Nghiên cứu', 'Research'), 'h': ('Nghiên cứu sản phẩm và thị trường', 'Product and market research'),
     'd': ('Biết nên bán gì, giá bao nhiêu, lời lãi dự kiến và lô đầu nhập bao nhiêu, trước khi bỏ tiền làm hàng.', 'Know what to sell, at what price and margin, and how big the first order should be, before money goes into inventory.'),
     'b': [('Ngách, đối thủ, khung giá trên các sàn tại Việt Nam và Mỹ.', 'Niches, competitors and price ranges on marketplaces in Vietnam and the US.'),
           ('Báo cáo kèm bộ dữ liệu, khoảng 2 tuần cho một dòng sản phẩm.', 'A report with the full dataset, about 2 weeks per product line.')],
     'tech': ('Công cụ phân tích dữ liệu bán hàng thực tế trên các sàn.', 'Analysis tools working on real marketplace sales data.'),
     'route': None,
     'links': [('nghien-cuu-san-pham', ('Xem dịch vụ nghiên cứu', 'See research service'))]},
    {'m': 'factory', 't': ('Nguồn hàng', 'Sourcing'), 'h': ('Phát triển sản phẩm và nguồn hàng', 'Product development and sourcing'),
     'd': ('Có nhà máy phù hợp, có mẫu và bao bì đã chốt, có lô thử trước khi làm lô lớn.', 'The right factory, agreed samples and packaging, and a test batch before scaling.'),
     'b': [('Tìm và so sánh nhà máy tại Việt Nam và Trung Quốc: giá, số lượng tối thiểu, thời gian sản xuất.', 'Find and compare factories in Vietnam and China: unit cost, MOQ and lead time.'),
           ('Làm mẫu, bao bì và lô thử nhu cầu trên sàn.', 'Samples, packaging and a test batch on marketplaces.')],
     'tech': None,
     'route': ('Hàng từ nhà máy Việt Nam, Trung Quốc', 'Goods from factories in Vietnam and China'),
     'links': [('nguon-hang', ('Xem dịch vụ nguồn hàng', 'See sourcing service'))]},
    {'m': 'ship', 't': ('Đưa hàng đi', 'Logistics'), 'h': ('Hậu cần và đưa hàng đi', 'Logistics and fulfillment'),
     'd': ('Hàng được đóng gói đúng yêu cầu, có giấy tờ, tới kho và sẵn sàng giao đơn.', 'Goods packed to requirements, with paperwork, in the warehouse and ready to ship.'),
     'b': [('Bao bì, tem nhãn, phối hợp giấy tờ xuất nhập khẩu và vận chuyển.', 'Packaging, labels and coordination of export, import and shipping.'),
           ('Nhận hàng và vận hành kho tại Mỹ.', 'Receiving and warehouse operations in the US.')],
     'tech': ('Phần mềm kho kết nối các sàn, đơn về là kho giao.', 'Warehouse software connected to marketplaces, so orders flow straight to fulfilment.'),
     'route': ('Sang kho tại Mỹ, lên sàn', 'To the US warehouse and onto marketplaces'),
     'links': [('hau-can', ('Xem dịch vụ hậu cần', 'See logistics service'))]},
    {'m': 'store', 't': ('Bán hàng trên sàn', 'Selling'), 'h': ('Mở gian hàng và vận hành hằng ngày', 'Store setup and daily operations'),
     'd': ('Gian hàng có đơn và được vận hành hằng ngày tại Việt Nam và Mỹ.', 'A store with orders, run every day in Vietnam and the United States.'),
     'b': [('Việt Nam: Shopee, TikTok Shop, Lazada, Tiki.', 'Vietnam: Shopee, TikTok Shop, Lazada, Tiki.'),
           ('Mỹ: Amazon, TikTok Shop US, Walmart, eBay, Etsy, Shopify.', 'United States: Amazon, TikTok Shop US, Walmart, eBay, Etsy, Shopify.'),
           ('Đăng sản phẩm, quảng cáo, KOC và creator, chăm sóc người mua.', 'Listings, ads, KOCs and creators, customer service.')],
     'tech': ('Hệ thống đồng bộ sản phẩm, đơn hàng, tồn kho giữa sàn, website và kho; trợ lý AI lo việc lặp lại như báo cáo sáng, quét giá.', 'Systems that sync products, orders and inventory across marketplaces, website and warehouse; AI assistants handle repetitive work such as morning reports and price scans.'),
     'route': None,
     'links': [('ban-hang-tai-viet-nam', ('Bán hàng tại Việt Nam', 'Selling in Vietnam')), ('ban-hang-tai-my', ('Bán hàng tại Mỹ', 'Selling in the US'))]},
    {'m': 'report', 't': ('Báo cáo', 'Reporting'), 'h': ('Theo dõi lời lãi và đối soát', 'Margin tracking and reconciliation'),
     'd': ('Doanh nghiệp xem được doanh thu, lời lãi, tồn kho bất cứ lúc nào.', 'You can see revenue, margin and inventory at any time.'),
     'b': [('Trang theo dõi riêng cho từng doanh nghiệp, gồm trong phí vận hành.', 'A private dashboard for each company, included in the operations fee.'),
           ('Báo cáo và đối soát gửi hằng tháng trước ngày 05.', 'Monthly report and reconciliation before the 5th.')],
     'tech': ('Dashboard gom số liệu của mọi sàn về một trang.', 'A dashboard that brings every channel onto one page.'),
     'route': None,
     'links': [('dashboard-ket-noi-website', ('Xem dashboard và kết nối sàn', 'See dashboards and sync'))]},
]


def journey(L, P, UL):
    parts = []
    for i, j in enumerate(JOURNEY, 1):
        on = ' on' if i == 1 else ''
        sel = 'true' if i == 1 else 'false'
        route = f'<span class="jr-route">{L(j["route"])}</span>' if j['route'] else ''
        parts.append(
            f'      <button type="button" class="jr-b{on}" data-tab="j{i}" role="tab" aria-selected="{sel}" style="--i:{i}">\n'
            f'        {model(j["m"])}\n'
            f'        <span class="jr-n">0{i}</span>\n'
            f'        <span class="jr-t">{L(j["t"])}</span>\n'
            f'        {route}\n'
            f'      </button>')
        tech = ''
        if j['tech']:
            tech = f'<p class="jr-tech"><b>{L(("Công nghệ ở khâu này", "Technology at this stage"))}</b>{L(j["tech"])}</p>'
        links = ''.join(f'<a class="link" href="/{sl}/">{L(t)} →</a>' for sl, t in j['links'])
        parts.append(
            f'      <div class="jr-p{on}" data-panel="j{i}" role="tabpanel">\n'
            f'        <div>\n          <h3>{L(j["h"])}</h3>\n          {P(j["d"], "jr-d")}\n          <p class="jr-links">{links}</p>\n        </div>\n'
            f'        <div>\n          {UL(j["b"], "safe")}\n          {tech}\n        </div>\n'
            f'      </div>')
    rail = ('      <a class="jr-rail" href="#cong-nghe"><b>' + L(('Công nghệ chạy xuyên suốt', 'Technology runs underneath')) + '</b><span>'
            + L(('Trợ lý AI · Dashboard · Kết nối sàn, website và kho', 'AI assistants · Dashboards · Marketplace, website and warehouse sync'))
            + '</span><i aria-hidden="true">→</i></a>')
    box = f'      <span class="jr-box" aria-hidden="true">{parcel()}</span>'
    return '    <div class="jr" data-tabs role="tablist">\n' + '\n'.join(parts) + '\n' + rail + '\n' + box + '\n    </div>'
