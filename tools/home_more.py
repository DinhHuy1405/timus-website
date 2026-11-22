"""Hai khối sáng của trang chủ: "Gồm trong mọi gói vận hành / Chi phí" và "Cách TIMUS làm việc".
Chữ là cặp (tiếng Việt, tiếng Anh). Sửa ở đây rồi chạy python3 tools/build.py."""

ZALO = 'https://zalo.me/0796796492'


def L(t):
    return f'<span data-l="vi">{t[0]}</span><span data-l="en">{t[1]}</span>'


def _ic(d):
    return f'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'


TRACK = [
    (_ic('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'), ('Doanh thu', 'Revenue'), ('Bán được bao nhiêu trên từng sàn.', 'What sold on each marketplace.')),
    (_ic('<circle cx="12" cy="12" r="9"/><path d="M15 9.5c-.6-1-1.7-1.5-3-1.5-1.7 0-3 .9-3 2.1 0 2.9 6 1.4 6 4.2 0 1.200-1.300 2.200-3 2.200-1.400 0-2.600-.6-3.100-1.600M12 6v2M12 16.500V18"/>'), ('Lời lãi', 'Margin'), ('Còn lại bao nhiêu sau các khoản phí.', 'What is left after all fees.')),
    (_ic('<path d="M3 8l9-5 9 5v8l-9 5-9-5V8z"/><path d="M3 8l9 5 9-5M12 13v8"/>'), ('Tồn kho', 'Inventory'), ('Hàng còn trong kho và hàng sắp hết.', 'Stock on hand and items running low.')),
    (_ic('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.300-4.300M8 12l2-2 2 1.500 2.500-3"/>'), ('Thị trường', 'Market'), ('Số liệu sản phẩm cùng loại trên sàn.', 'Data on comparable products on the marketplace.')),
]

COST = [
    ('Báo giá theo phạm vi từng doanh nghiệp, gửi sau buổi trao đổi đầu.', 'Quoted per scope, sent after a first call.'),
    ('Chi phí bên thứ ba (vận chuyển, kho, thuế, phí sàn, quảng cáo, hàng mẫu) doanh nghiệp trả theo thực tế.', 'Third party costs (shipping, warehousing, duties, marketplace fees, ads, samples) are paid at actual cost.'),
    ('TIMUS không cộng phí vào các khoản bên thứ ba.', 'TIMUS adds no markup to third party costs.'),
]


def included():
    tiles = ''.join(f'<li>{ic}<b>{L(t)}</b><span>{L(d)}</span></li>' for ic, t, d in TRACK)
    cost = ''.join(f'<li>{L(c)}</li>' for c in COST)
    cal = _ic('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>')
    return f'''
<section class="sec sec-alt light">
  <div class="wrap">
    <div class="inc reveal">
      <div class="inc-l">
        <p class="eyebrow">{L(('Gồm trong mọi gói vận hành', 'Included with every operations plan'))}</p>
        <h2>{L(('Trang theo dõi riêng cho từng doanh nghiệp', 'A private dashboard for each brand'))}</h2>
        <ul class="inc-g">{tiles}</ul>
        <p class="inc-n">{cal}<span>{L(('Báo cáo và đối soát gửi hằng tháng trước ngày 05.', 'Monthly report and reconciliation before the 5th.'))}</span></p>
      </div>
      <div class="inc-c">
        <h3>{L(('Chi phí', 'Pricing'))}</h3>
        <ul>{cost}</ul>
        <a class="btn btn-gold" href="#lien-he">{L(('Liên hệ báo giá', 'Get a quote'))}</a>
      </div>
    </div>
  </div>
</section>
'''


COLS = [('TIMUS làm', 'TIMUS does'), ('Doanh nghiệp chuẩn bị', 'You prepare'), ('Kết quả nhận được', 'What you get')]

OPS = [
    {'t': ('Nghiên cứu trước', 'Research first'), 'ms': ('Quyết định trước khi bỏ tiền làm hàng', 'Decide before money goes into stock'),
     'c': [('Lọc số liệu sàn, so sánh sản phẩm cùng loại, ước tính giá bán và lời lãi dự kiến.', 'Filter marketplace data, compare similar products, estimate price and expected margin.'),
           ('Thông tin sản phẩm, giá vốn và thị trường muốn bán.', 'Product details, unit cost and the market you want to sell in.'),
           ('Báo cáo nghiên cứu. Hai bên cùng quyết định làm tiếp, đổi sản phẩm hay dừng.', 'A research report. We decide together to go ahead, change product or stop.')]},
    {'t': ('Chuẩn bị hàng', 'Get the goods ready'), 'ms': ('Làm khi doanh nghiệp cần nguồn hàng', 'Only when you need sourcing'),
     'c': [('Tìm và so sánh nhà máy, làm mẫu, bao bì, tem nhãn, giấy tờ xuất nhập khẩu, đưa hàng đi và nhập kho.', 'Find and compare factories, samples, packaging, labels, export and import paperwork, shipping and warehousing.'),
           ('Duyệt mẫu, duyệt bao bì; trả chi phí bên thứ ba theo thực tế.', 'Approve samples and packaging; pay third party costs at actual cost.'),
           ('Hàng đạt yêu cầu của sàn, nằm sẵn trong kho.', 'Goods that meet marketplace requirements, ready in the warehouse.')]},
    {'t': ('Mở gian hàng', 'Open the store'), 'ms': ('Đơn đầu thường có trong tháng vận hành đầu tiên', 'First orders usually within the first month'),
     'c': [('Thiết lập gian hàng, đăng sản phẩm, cài quảng cáo, kết nối KOC và creator.', 'Set up the store, list products, set up ads, connect KOCs and creators.'),
           ('Giấy tờ doanh nghiệp, tài khoản nhận tiền, hình ảnh và thông tin sản phẩm.', 'Company documents, a payout account, product images and information.'),
           ('Gian hàng mở bán. Đơn đầu thường có trong tháng vận hành đầu tiên.', 'A live store. First orders usually come within the first month of operations.')]},
    {'t': ('Vận hành và báo cáo', 'Run and report'), 'ms': ('Báo cáo, đối soát trước ngày 05', 'Report and reconciliation by the 5th'),
     'c': [('Vận hành hằng ngày: đơn hàng, quảng cáo, chăm sóc người mua, theo dõi tồn kho.', 'Daily operations: orders, ads, customer service, stock tracking.'),
           ('Duyệt ngân sách quảng cáo và các quyết định lớn về giá, về hàng.', 'Approve the ad budget and major decisions on price and stock.'),
           ('Báo cáo và đối soát hằng tháng trước ngày 05, trên trang theo dõi riêng.', 'Monthly report and reconciliation before the 5th, on your private dashboard.')]},
]

AI = [
    {'t': ('Khảo sát từng vị trí', 'Survey every role'),
     'c': [('Gửi phiếu khảo sát và tổng hợp việc của từng vị trí.', 'Send the survey and summarise the work of each role.'),
           ('Mỗi nhân viên điền phiếu khoảng 15 phút: việc phụ trách, phần mềm, việc lặp lại, từng bước đang làm.', 'Each staff member fills a 15 minute form: duties, software, repetitive tasks and the steps they follow.'),
           ('Danh sách việc lặp lại của từng vị trí.', 'A list of repetitive tasks for each role.')]},
    {'t': ('Lộ trình theo phòng ban', 'Roadmap by department'),
     'c': [('Viết báo cáo hiện trạng và lộ trình theo phòng ban.', 'Write a current state report and a roadmap by department.'),
           ('Chọn phòng ban làm trước và người duyệt kết quả.', 'Pick the first department and who reviews the results.'),
           ('Lộ trình: phòng nào làm trước, việc nào làm ngay, việc nào để sau.', 'A roadmap: which department first, what to do now, what can wait.')]},
    {'t': ('Dựng và cài trợ lý', 'Build and install'),
     'c': [('Cài kết nối cần thiết, dựng skill cho từng việc trên đúng phần mềm của đội.', 'Set up the needed connections and build a skill for each task on the team\'s own software.'),
           ('Cấp quyền truy cập phần mềm và cử người duyệt kết quả.', 'Grant software access and name a reviewer.'),
           ('Trợ lý làm được từng việc đã chọn.', 'An assistant that can do each chosen task.')]},
    {'t': ('Chạy song song', 'Run side by side'),
     'c': [('Cho trợ lý chạy cùng cách làm tay trong 5 ngày và so kết quả.', 'Run the assistant alongside the manual process for 5 days and compare results.'),
           ('Vẫn làm tay như cũ để đối chiếu.', 'Keep doing the task by hand for comparison.'),
           ('Kết quả khớp mới chuyển hẳn sang trợ lý.', 'The assistant takes over only once results match.')]},
    {'t': ('Bàn giao và mở rộng', 'Hand over and expand'),
     'c': [('Bàn giao hướng dẫn và đo số giờ tiết kiệm thực tế.', 'Hand over guides and measure real hours saved.'),
           ('Dùng hằng ngày và báo lại chỗ cần sửa.', 'Use it daily and report what needs fixing.'),
           ('Tài liệu hướng dẫn, số giờ tiết kiệm đã đo, rồi làm tiếp phòng ban sau.', 'Guides, measured hours saved, then on to the next department.')]},
]


def _steps(items, cls):
    out = []
    for s in items:
        ms = f'<em class="ms">{L(s["ms"])}</em>' if s.get('ms') else ''
        cols = ''.join(f'<div class="sd-c"><i>{L(h)}</i><p>{L(c)}</p></div>' for h, c in zip(COLS, s['c']))
        out.append(f'''          <li>
            <b>{L(s['t'])}</b>{ms}
            <div class="sd">{cols}</div>
          </li>''')
    return f'''        <ol class="steps {cls}hov tl">
{chr(10).join(out)}
        </ol>
        <div class="step-desc" aria-live="polite"></div>'''


def process():
    return f'''<section id="cach-lam" class="sec light">
  <div class="wrap">
    <p class="eyebrow">{L(('Quy trình', 'Process'))}</p>
    <h2>{L(('Cách TIMUS làm việc', 'How we work'))}</h2>
    <p class="sub">{L(('Mỗi bước ghi rõ TIMUS làm gì, doanh nghiệp cần chuẩn bị gì và nhận lại gì. Bấm vào từng bước để xem.', 'Each step states what TIMUS does, what you prepare and what you get. Select a step to see the details.'))}</p>
    <div class="tabs" data-tabs id="procTabs">
      <div class="tab-row" role="tablist">
        <button type="button" class="tab on" data-tab="ops" role="tab" aria-selected="true">{L(('Vận hành sàn', 'Marketplace operations'))}</button>
        <button type="button" class="tab" data-tab="ai" role="tab" aria-selected="false">{L(('Trợ lý AI', 'AI assistants'))}</button>
      </div>
      <div class="tab-p on" data-panel="ops" role="tabpanel" data-steps>
{_steps(OPS, '')}
      </div>
      <div class="tab-p" data-panel="ai" role="tabpanel" data-steps>
{_steps(AI, 'five ')}
      </div>
    </div>
    <div class="proc-cta">
      <p>{L(('Việc đầu tiên là một buổi trao đổi để TIMUS hiểu sản phẩm và phạm vi công việc.', 'It starts with a call so TIMUS understands your product and the scope of work.'))}</p>
      <a class="btn btn-gold" href="{ZALO}" target="_blank" rel="noopener">{L(('Nhắn Zalo', 'Message on Zalo'))}</a>
      <a class="link" href="mailto:info@timusco.com?subject=TIMUS%20-%20Lien%20he%20bao%20gia">{L(('Gửi email báo giá', 'Request a quote'))} →</a>
    </div>
  </div>
</section>
'''
