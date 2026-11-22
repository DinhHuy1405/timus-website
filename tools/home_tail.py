"""Phần cuối trang chủ: Về TIMUS, Câu hỏi thường gặp, Liên hệ, và chân trang dùng chung cho mọi trang.
Chữ là cặp (tiếng Việt, tiếng Anh). Sửa ở đây rồi chạy python3 tools/build.py."""

ZALO = 'https://zalo.me/0796796492'
MAIL = 'mailto:info@timusco.com?subject=TIMUS%20-%20Lien%20he%20bao%20gia'


def L(t):
    return f'<span data-l="vi">{t[0]}</span><span data-l="en">{t[1]}</span>'


FACTS = [
    (('Đà Nẵng', 'Da Nang'), ('Trụ sở', 'Office')),
    (('Việt Nam, Mỹ', 'Vietnam, United States'), ('Thị trường bán hàng', 'Selling markets')),
    (('Việt Nam, Trung Quốc', 'Vietnam, China'), ('Nguồn hàng', 'Sourcing')),
    (('Trước ngày 05', 'Before the 5th'), ('Báo cáo, đối soát hằng tháng', 'Monthly report and reconciliation')),
]


def about():
    facts = ''.join(f'<li><b>{L(v)}</b><span>{L(k)}</span></li>' for v, k in FACTS)
    return f'''<section id="ve-timus" class="sec sec-alt">
  <div class="wrap">
    <div class="about reveal">
      <div>
        <p class="eyebrow">{L(('Công ty', 'Company'))}</p>
        <h2>{L(('Về TIMUS', 'About TIMUS'))}</h2>
        <p>{L(('TIMUS CO., LTD là công ty công nghệ và thương mại điện tử có trụ sở tại Đà Nẵng, Việt Nam. Chúng tôi giúp doanh nghiệp và thương hiệu Việt bán hàng trên sàn, trong nước và tại Mỹ, và triển khai trợ lý AI, dashboard báo cáo, hệ thống kết nối cho đội ngũ của doanh nghiệp.', 'TIMUS CO., LTD is a technology and e-commerce company based in Da Nang, Vietnam. We help Vietnamese businesses and brands sell on marketplaces at home and in the United States, and deploy AI assistants, reporting dashboards and connected systems for their teams.'))}</p>
        <p class="muted">{L(('TIMUS làm thương mại điện tử và công nghệ cho doanh nghiệp, không liên quan đến các công ty khác cùng tên Timus.', 'TIMUS works in e-commerce and business technology and is not affiliated with other companies using the Timus name.'))}</p>
      </div>
      <div class="founder">
        <img src="/assets/timus-mark.webp" alt="" width="56" height="56" loading="lazy">
        <p class="label">{L(('Người sáng lập', 'Founder'))}</p>
        <p class="name">Nguyễn Đình Huy</p>
        <p>{L(('Bán hàng trên các sàn tại Việt Nam và Mỹ, chia sẻ kiến thức thương mại điện tử dưới tên Huy Tim.', 'Sells on marketplaces in Vietnam and the US, and shares e-commerce know-how as Huy Tim.'))}</p>
        <a class="link" href="https://huytim.com" target="_blank" rel="noopener">huytim.com →</a>
      </div>
    </div>
    <ul class="ab-facts reveal">{facts}</ul>
  </div>
</section>
'''


QA = [
    (('Chưa có sản phẩm thì bắt đầu từ đâu?', 'We have no product yet. Where do we start?'),
     ('Bắt đầu từ nghiên cứu sản phẩm. TIMUS lọc số liệu sàn để hai bên cùng quyết định bán gì, giá bao nhiêu, trước khi bỏ tiền làm hàng.', 'Start with product research. TIMUS filters marketplace data so we decide together what to sell and at what price, before money goes into inventory.')),
    (('Chi phí được tính thế nào?', 'How is pricing calculated?'),
     ('Mỗi khâu có một mức phí cố định, doanh nghiệp chỉ trả cho khâu mình chọn. TIMUS gửi báo giá theo phạm vi sau buổi trao đổi đầu. Chi phí bên thứ ba như vận chuyển, kho, phí sàn, quảng cáo doanh nghiệp trả theo thực tế, TIMUS không cộng thêm.', 'Each stage has a fixed fee and you only pay for the stages you choose. We send a scoped quote after a first call. Third party costs such as shipping, warehousing, marketplace fees and ads are paid at actual cost with no markup.')),
    (('Doanh nghiệp theo dõi kết quả bằng cách nào?', 'How do we track results?'),
     ('Mỗi doanh nghiệp có một trang theo dõi riêng để xem doanh thu, lời lãi, tồn kho và thị trường. Báo cáo và đối soát gửi hằng tháng trước ngày 05.', 'Each brand gets a private dashboard showing revenue, margin, inventory and market data. The monthly report and reconciliation arrive before the 5th.')),
    (('Chỉ cần một phần việc, ví dụ dashboard hoặc website, có được không?', 'Can we hire TIMUS for just one piece, such as a dashboard or a website?'),
     ('Được. Các dịch vụ tách rời nhau, doanh nghiệp có thể chỉ làm nghiên cứu sản phẩm, chỉ làm dashboard báo cáo, website hoặc hệ thống kết nối các sàn mà không cần ký vận hành.', 'Yes. Services are separate, so you can take only product research, a reporting dashboard, a website or a multichannel system without an operations contract.')),
    (('Pháp lý và thuế tại Mỹ do ai làm?', 'Who handles legal and tax matters in the US?'),
     ('Các đơn vị đối tác chuyên về pháp lý và thuế tại Mỹ thực hiện. TIMUS kết nối doanh nghiệp với các đơn vị đó.', 'Partner firms that specialise in US legal and tax matters handle them. TIMUS connects you with those firms.')),
    (('TIMUS có cam kết doanh thu không?', 'Does TIMUS guarantee revenue?'),
     ('Không. Doanh thu phụ thuộc sản phẩm, giá bán và thị trường. Phần TIMUS chịu trách nhiệm là công việc vận hành hằng ngày, báo cáo và đối soát hằng tháng trước ngày 05.', 'No. Revenue depends on the product, the price and the market. What TIMUS is responsible for is the daily operations work and the monthly report and reconciliation before the 5th.')),
]


def faq():
    qa = ''.join(f'''
        <details class="qa">
          <summary>{L(q)}</summary>
          <p>{L(a)}</p>
        </details>''' for q, a in QA)
    return f'''<section id="hoi-dap" class="sec sec-alt light">
  <div class="wrap faq2">
    <div class="faq-l reveal">
      <p class="eyebrow">{L(('Hỏi đáp', 'FAQ'))}</p>
      <h2>{L(('Câu hỏi thường gặp', 'Frequently asked questions'))}</h2>
      <p>{L(('Câu hỏi riêng của từng dịch vụ nằm ở trang dịch vụ đó. Chưa thấy câu mình cần thì nhắn TIMUS.', 'Questions about a specific service are answered on that service page. If yours is not here, message TIMUS.'))}</p>
      <a class="link" href="{ZALO}" target="_blank" rel="noopener">{L(('Nhắn Zalo', 'Message on Zalo'))} →</a>
    </div>
    <div class="qa-list reveal">{qa}
    </div>
  </div>
</section>
'''


SEND = [
    ('Sản phẩm đang có hoặc đang định làm.', 'The product you have or plan to make.'),
    ('Thị trường muốn bán: Việt Nam, Mỹ hoặc cả hai.', 'The market you want to sell in: Vietnam, the US or both.'),
    ('Công việc đội ngũ muốn tự động hoá, nếu cần phần công nghệ.', 'The work your team wants to automate, if you need the technology side.'),
]


def contact():
    send = ''.join(f'<li>{L(s)}</li>' for s in SEND)
    return f'''<section id="lien-he" class="sec contact">
  <div class="wrap ct reveal">
    <div class="ct-l">
      <p class="eyebrow">{L(('Liên hệ', 'Contact'))}</p>
      <h2>{L(('Bắt đầu bằng một buổi trao đổi', 'Start with a conversation'))}</h2>
      <p class="sub">{L(('Cho TIMUS biết sản phẩm, thị trường muốn bán, hoặc công việc đội ngũ muốn tự động hoá. Chúng tôi trả lời và gửi báo giá theo phạm vi.', 'Tell us about your product and target market, or the work your team wants to automate. We will reply with a scoped quote.'))}</p>
      <div class="ct-b">
        <a class="ct-a gold" href="{ZALO}" target="_blank" rel="noopener"><span>Zalo</span><b>0796 796 492</b></a>
        <a class="ct-a" href="{MAIL}"><span>Email</span><b>info@timusco.com</b></a>
      </div>
      <p class="ct-o">{L(('Trụ sở: Đà Nẵng, Việt Nam', 'Office: Da Nang, Vietnam'))}</p>
    </div>
    <div class="ct-r">
      <h3>{L(('Nên gửi trước cho TIMUS', 'What to send us first'))}</h3>
      <ol>{send}</ol>
    </div>
  </div>
</section>
'''


def footer(pages):
    """pages: danh sách (slug, (tên VI, tên EN)) của các trang dịch vụ."""
    svc = ''.join(f'<a href="/{s}/">{L(t)}</a>' for s, t in pages)
    return f'''<footer class="foot ft">
  <div class="wrap ft-in">
    <div class="ft-b">
      <a class="brand" href="/"><img src="/assets/timus-mark.webp" alt="" width="34" height="34" loading="lazy"><span>TIMUS</span></a>
      <p>{L(('Logistics, E-Commerce &amp; Technology cho doanh nghiệp Việt.', 'Logistics, E-Commerce &amp; Technology for Vietnamese businesses.'))}</p>
    </div>
    <nav class="ft-c" aria-label="Dịch vụ">
      <b>{L(('Dịch vụ', 'Services'))}</b>
      {svc}
    </nav>
    <nav class="ft-c" aria-label="Công ty">
      <b>{L(('Công ty', 'Company'))}</b>
      <a href="/#cach-lam">{L(('Cách làm việc', 'How we work'))}</a>
      <a href="/#ve-timus">{L(('Về TIMUS', 'About TIMUS'))}</a>
      <a href="/#dao-tao">{L(('Đào tạo', 'Training'))}</a>
      <a href="/#hoi-dap">{L(('Hỏi đáp', 'FAQ'))}</a>
    </nav>
    <div class="ft-c">
      <b>{L(('Liên hệ', 'Contact'))}</b>
      <a href="{ZALO}" target="_blank" rel="noopener">Zalo 0796 796 492</a>
      <a href="{MAIL}">info@timusco.com</a>
      <span>{L(('Đà Nẵng, Việt Nam', 'Da Nang, Vietnam'))}</span>
    </div>
  </div>
  <div class="wrap ft-end"><span>© 2026 TIMUS CO., LTD</span></div>
</footer>'''
