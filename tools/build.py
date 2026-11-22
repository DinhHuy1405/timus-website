#!/usr/bin/env python3
"""Dựng các trang dịch vụ của timusco.com.

Chạy từ thư mục gốc của repo:  python3 tools/build.py
- Ghi <slug>/index.html cho từng dịch vụ trong PAGES.
- Điền hai khối thẻ dịch vụ trên trang chủ, giữa <!-- SVC:START --> và <!-- SVC:END -->.
- Ghi sitemap.xml.
Sửa chữ của trang dịch vụ thì sửa trong file này rồi chạy lại, không sửa tay file index.html của từng trang.
Mỗi câu là một cặp (tiếng Việt, tiếng Anh).
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import home_parts
import home_more

SITE = 'https://timusco.com'
CSS_V = '20'
JS_V = '12'
ZALO = 'https://zalo.me/0796796492'
MAIL = 'info@timusco.com'

GROUPS = {
    'logi': {'id': 'logistics', 'name': ('Logistics', 'Logistics')},
    'tmdt': {'id': 'thuong-mai-dien-tu', 'name': ('E-commerce', 'E-commerce')},
    'tech': {'id': 'cong-nghe', 'name': ('Technology', 'Technology')},
}

# ---------- phần dùng chung cho nhóm vận hành sàn ----------
OPS_GIVE = [
    ('Trang theo dõi riêng cho doanh nghiệp: doanh thu, lời lãi, tồn kho, thị trường.', 'A private dashboard for your company: revenue, margin, inventory and market data.'),
    ('Báo cáo và đối soát gửi hằng tháng trước ngày 05; doanh nghiệp có 05 ngày làm việc để nêu ý kiến.', 'Monthly report and reconciliation before the 5th; you have 5 working days to comment.'),
    ('Một đầu mối TIMUS phụ trách gian hàng và trả lời doanh nghiệp.', 'One TIMUS contact who owns the store and answers your questions.'),
]
OPS_YOU = [
    ('Cung cấp hàng, thông tin và giấy tờ sản phẩm.', 'Provide stock, product information and documents.'),
    ('Duyệt ngân sách quảng cáo và khuyến mãi.', 'Approve advertising and promotion budgets.'),
    ('Trả trực tiếp chi phí bên thứ ba: phí sàn, quảng cáo, vận chuyển, kho, hàng mẫu. TIMUS không cộng phí vào các khoản này.', 'Pay third party costs directly: marketplace fees, ads, shipping, warehousing, samples. TIMUS adds no markup.'),
]
OPS_STEPS = [
    (('Trao đổi đầu', 'First call'), ('Doanh nghiệp cho biết sản phẩm, sàn muốn bán và khâu cần TIMUS làm. TIMUS gửi báo giá theo phạm vi.', 'You tell us the product, target marketplaces and the stages you need. TIMUS sends a scoped quote.')),
    (('Thiết lập gian hàng', 'Store setup'), ('Mở hoặc chuẩn hoá gian hàng, đăng sản phẩm, nội dung trang, kết nối kho.', 'Open or tidy up the store, list products, write store content and connect the warehouse.')),
    (('Vận hành hằng ngày', 'Daily operations'), ('Giá và khuyến mãi, quảng cáo trong ngân sách đã duyệt, chăm sóc người mua, xử lý vi phạm.', 'Pricing and promotions, ads within the approved budget, customer service and policy issues.')),
    (('Báo cáo và đối soát', 'Report and reconcile'), ('Mỗi tháng một báo cáo kèm đối soát, hai bên xem lại và thống nhất việc tháng sau.', 'A monthly report with reconciliation; we review it together and agree on next month.')),
]
Q_FIRST_ORDER = (('Bao lâu thì có đơn hàng đầu tiên?', 'How soon do first orders come in?'),
                 ('Khi gian hàng đã mở và hàng đã sẵn sàng, đơn đầu thường có trong tháng vận hành đầu tiên. TIMUS không cam kết con số doanh thu; kết quả được báo cáo bằng số liệu thật hằng tháng.',
                  'Once the store is live and stock is ready, first orders usually come within the first month of operations. We do not promise revenue figures; results are reported with real data every month.'))
Q_ONLY_ONE = (('Chỉ làm khâu này, không ký vận hành, có được không?', 'Can we take only this stage without an operations contract?'),
              ('Được. Các dịch vụ tách rời nhau, doanh nghiệp chọn khâu nào trả khâu đó.', 'Yes. Services are separate and you only pay for the stages you choose.'))

PAGES = [
    # ================= CÔNG NGHỆ =================
    {
        'slug': 'tro-ly-ai', 'group': 'tech', 'num': '01',
        'title': ('Trợ lý AI cho đội ngũ', 'AI assistants for your team'),
        'short': ('Dạy trợ lý làm thay việc lặp lại trên máy tính cho từng phòng ban. Người trong đội vẫn là người duyệt và quyết định.',
                  'Teach an assistant to take over repetitive computer work for each department. Your people still review and decide.'),
        'lead': ('Nhân viên bán hàng, marketing, kế toán, kho mỗi ngày mất hàng giờ cho việc lặp lại: chép số giữa các phần mềm, làm báo cáo, trả lời câu hỏi quen thuộc, xuất ảnh nhiều cỡ. TIMUS khảo sát từng vị trí, rồi dựng trợ lý AI làm thay những việc đó trên chính phần mềm doanh nghiệp đang dùng.',
                 'Sales, marketing, accounting and warehouse staff lose hours every day to repetitive work: copying numbers between tools, building reports, answering the same questions, exporting images in many sizes. TIMUS surveys each role, then builds AI assistants that do this work inside the software your team already uses.'),
        'desc': 'Trợ lý AI làm thay việc lặp lại trên máy tính cho từng phòng ban: báo cáo, chép số liệu, soạn câu trả lời, xuất ảnh. TIMUS khảo sát, dựng, chạy song song rồi bàn giao.',
        'for': [
            ('Doanh nghiệp đã tự bán hàng, có đội ngũ nhiều phòng ban.', 'Companies that already sell on their own and have several departments.'),
            ('Nhân viên đang mất nhiều giờ cho việc chép số, làm báo cáo, trả lời câu hỏi lặp lại.', 'Teams losing hours to copying numbers, building reports and answering repeated questions.'),
            ('Chủ doanh nghiệp muốn chuyển đổi số từng bước, bắt đầu từ một phòng ban.', 'Owners who want to digitise step by step, starting with one department.'),
        ],
        'scope': [
            ('Mỗi việc lặp lại được dạy cho trợ lý một lần và lưu thành một skill, nhân viên gọi tên là trợ lý làm lại đúng các bước.', 'Each repetitive task is taught to the assistant once and saved as a skill; staff call it by name and the assistant repeats the exact steps.'),
            ('Trợ lý làm việc qua kết nối với Google Sheets, Google Drive, Canva; trang web và phần mềm không có kết nối thì trợ lý thao tác trên màn hình như người.', 'The assistant works through connections to Google Sheets, Google Drive and Canva; for websites and software without a connection, it operates the screen the way a person does.'),
            ('Chạy khi được gọi hoặc theo lịch: báo cáo mỗi sáng, kiểm quảng cáo, quét giá.', 'Runs on request or on a schedule: morning reports, ad checks, price scans.'),
            ('Mọi việc gửi ra ngoài, sửa giá, sửa đơn đều dừng chờ người duyệt.', 'Anything sent outside, any price or order change, waits for a person to approve.'),
        ],
        'depts': [
            (('Marketing', 'Marketing'), [('Lấy chỉ số Facebook, TikTok, YouTube, sàn vào bảng báo cáo mỗi sáng.', 'Pull Facebook, TikTok, YouTube and marketplace metrics into the report every morning.'), ('Lên ý tưởng, lịch nội dung, caption nháp.', 'Draft content ideas, calendars and captions.')]),
            (('Thương mại điện tử', 'E-commerce'), [('Quét gian hàng bán dưới giá, theo dõi giá và chương trình của đối thủ.', 'Scan for sellers below your price, track competitor prices and promotions.'), ('Chép đơn từ các sàn sang bảng tính, phần mềm kế toán.', 'Copy orders from marketplaces into spreadsheets and accounting software.')]),
            (('Chăm sóc khách hàng', 'Customer service'), [('Soạn sẵn câu trả lời tin nhắn và đánh giá theo kịch bản đã duyệt, người đọc lại rồi gửi.', 'Draft replies to messages and reviews from approved scripts for a person to check and send.'), ('Gom câu khách hay hỏi thành bộ câu trả lời mẫu.', 'Turn frequent questions into a reply library.')]),
            (('Thiết kế, nội dung', 'Design and content'), [('Viết brief thiết kế từ nội dung bài.', 'Write design briefs from post content.'), ('Tách nền, đổi nền, xuất ảnh đủ cỡ cho từng kênh.', 'Remove and change backgrounds, export images in every channel size.')]),
            (('Kế toán', 'Accounting'), [('Đối chiếu tiền về và phí sàn với đơn hàng.', 'Reconcile payouts and marketplace fees against orders.'), ('Gom chứng từ, lập bảng tổng hợp cuối tháng.', 'Collect documents and build month end summaries.')]),
            (('Kho vận, nhân sự', 'Warehouse and HR'), [('Theo dõi tồn kho, nhắc nhập hàng.', 'Track stock and flag reorders.'), ('Tổng hợp chấm công, hồ sơ ứng viên vào một bảng.', 'Compile timesheets and candidate files into one sheet.')]),
        ],
        'give_h': ('Nguyên tắc an toàn', 'Safety rules'),
        'give': [
            ('Trợ lý không biết mật khẩu; tài khoản, dữ liệu và bảng tính vẫn đứng tên doanh nghiệp.', "The assistant never holds passwords; accounts, data and spreadsheets stay in your company's name."),
            ('Ưu tiên quyền chỉ xem; việc gửi ra ngoài, sửa giá, sửa đơn luôn chờ người duyệt.', 'View-only access first; sending, price or order changes always wait for approval.'),
            ('Không chép thông tin khách hàng ra ngoài hệ thống của doanh nghiệp.', "Customer data never leaves your company's systems."),
            ('Mỗi trợ lý có hướng dẫn và cách tắt, đội ngũ tự quản lý sau bàn giao.', 'Every assistant comes with a guide and an off switch; your team manages it after handover.'),
        ],
        'you_h': ('Doanh nghiệp cần chuẩn bị', 'What you need to prepare'),
        'you': [
            ('Một người phụ trách phía doanh nghiệp.', 'One point of contact on your side.'),
            ('Mỗi nhân viên dành khoảng 15 phút điền phiếu khảo sát.', 'About 15 minutes per staff member for the survey form.'),
            ('Máy tính có trình duyệt Chrome. TIMUS hướng dẫn cài phần còn lại.', 'Computers with Chrome. TIMUS guides the rest of the setup.'),
        ],
        'steps': [
            (('Khảo sát từng vị trí', 'Survey every role'), ('Mỗi nhân viên điền phiếu khoảng 15 phút: việc phụ trách, phần mềm, việc lặp lại, từng bước đang làm.', 'Each staff member fills a 15 minute form: duties, software, repetitive tasks and the steps they follow.')),
            (('Lộ trình theo phòng ban', 'Roadmap by department'), ('TIMUS gửi báo cáo hiện trạng và lộ trình: phòng nào làm trước, việc nào làm ngay, việc nào để sau.', 'TIMUS sends a current state report and roadmap: which department first, what to do now, what can wait.')),
            (('Dựng và cài trợ lý', 'Build and install'), ('Cài kết nối cần thiết, dựng skill cho từng việc trên đúng phần mềm của đội.', "Set up the needed connections and build a skill for each task on the team's own software.")),
            (('Chạy song song', 'Run side by side'), ('Trợ lý chạy song song với cách làm tay 5 ngày; kết quả khớp mới chuyển hẳn.', 'The assistant runs alongside the manual process for 5 days; it takes over only once results match.')),
            (('Bàn giao và mở rộng', 'Hand over and expand'), ('Bàn giao hướng dẫn, đo số giờ tiết kiệm thực tế, rồi làm tiếp phòng ban sau.', 'Hand over guides, measure real hours saved, then move to the next department.')),
        ],
        'facts': [
            (('Trợ lý đầu tiên', 'First assistant'), ('Chạy thử trong 2 đến 3 tuần sau khảo sát', 'On trial within 2 to 3 weeks of the survey')),
            (('Trước khi chuyển hẳn', 'Before it takes over'), ('5 ngày chạy song song với cách làm tay', '5 days side by side with the manual process')),
            (('Chi phí', 'Pricing'), ('Báo giá sau buổi khảo sát', 'Quoted after the survey')),
        ],
        'tools': 'Shopee · TikTok Shop · Lazada · Pancake · Zalo · Google Sheets · Google Drive · Canva · MISA · Meta · TikTok Ads · Photoshop',
        'note': ('Phần mềm, tài khoản bên thứ ba doanh nghiệp trả theo thực tế, TIMUS không cộng phí. TIMUS không hứa trước số giờ tiết kiệm, con số được đo sau khi chạy thật.',
                 'Third party software and accounts are paid at actual cost with no markup. We do not promise hours saved upfront; the figure is measured after a real run.'),
        'faq': [
            (('Trợ lý AI khác chatbot ở chỗ nào?', 'How is an AI assistant different from a chatbot?'), ('Chatbot chỉ trả lời câu hỏi. Trợ lý AI của TIMUS làm việc trên phần mềm của doanh nghiệp: lấy số, ghi bảng tính, soạn nháp, xuất file, theo đúng các bước đội đang làm, và dừng chờ người duyệt ở những chỗ quan trọng.', "A chatbot only answers questions. A TIMUS assistant works inside your software: it pulls numbers, fills spreadsheets, drafts replies and exports files following your team's own steps, and stops for approval where it matters.")),
            (('Dữ liệu của doanh nghiệp có an toàn không?', 'Is our data safe?'), ('Trợ lý không giữ mật khẩu, ưu tiên quyền chỉ xem, không chép thông tin khách hàng ra ngoài. Mọi tài khoản và dữ liệu vẫn đứng tên doanh nghiệp; doanh nghiệp quyết định loại dữ liệu nào trợ lý được đọc.', 'The assistant holds no passwords, uses view-only access where possible and never copies customer data out. Accounts and data stay in your name, and you decide which data it may read.')),
            (('Cần chuẩn bị gì để bắt đầu?', 'What do we need to start?'), ('Một người phụ trách phía doanh nghiệp, mỗi nhân viên dành khoảng 15 phút điền phiếu khảo sát, và máy tính có trình duyệt Chrome. TIMUS hướng dẫn cài phần còn lại.', 'One point of contact, about 15 minutes per staff member for the survey form, and computers with Chrome. TIMUS guides the rest of the setup.')),
            (('Bao lâu thì dùng được?', 'How soon can we use it?'), ('Trợ lý đầu tiên thường chạy thử trong 2 đến 3 tuần sau khảo sát. TIMUS đo số giờ tiết kiệm thực tế sau 5 ngày chạy song song, không hứa trước con số.', 'The first assistant usually runs on trial within 2 to 3 weeks of the survey. We measure real hours saved after 5 days side by side and do not promise numbers upfront.')),
        ],
        'cta': ('Đặt lịch khảo sát', 'Book a survey'), 'subject': 'TIMUS - Tro ly AI cho doanh nghiep',
    },
    {
        'slug': 'dashboard-ket-noi-website', 'group': 'tech', 'num': '02',
        'title': ('Dashboard, kết nối sàn và website', 'Dashboards, marketplace sync and websites'),
        'short': ('Số liệu mọi sàn trên một trang, đồng bộ sản phẩm, đơn hàng, tồn kho giữa các hệ thống, và website công ty, website bán hàng.',
                  'Every channel on one page, products, orders and inventory in sync across systems, plus company websites and online stores.'),
        'lead': ('Khi bán trên nhiều sàn, số liệu nằm rải rác ở từng trang quản trị và nhân viên phải nhập tay hai lần. TIMUS dựng dashboard gom số về một chỗ, kết nối sàn, website, kho, kế toán với nhau, và làm website cho doanh nghiệp.',
                 'When you sell on several marketplaces, data sits in separate admin pages and staff enter things twice. TIMUS builds a dashboard that brings the numbers together, connects marketplaces, website, warehouse and accounting, and builds your website.'),
        'desc': 'Dashboard báo cáo doanh thu, lời lãi, tồn kho, quảng cáo của mọi sàn; hệ thống đồng bộ sản phẩm, đơn hàng, tồn kho; website công ty và website bán hàng do TIMUS dựng.',
        'for': [
            ('Doanh nghiệp bán trên từ hai sàn trở lên, khó nhìn tổng doanh thu và lời lãi.', 'Companies selling on two or more marketplaces that struggle to see total revenue and margin.'),
            ('Đội ngũ đang nhập đơn, tồn kho bằng tay giữa sàn, kho và phần mềm kế toán.', 'Teams entering orders and stock by hand between marketplaces, warehouse and accounting.'),
            ('Doanh nghiệp cần website công ty hoặc website bán hàng riêng.', 'Companies that need a company website or their own online store.'),
        ],
        'options': [
            (('Dashboard báo cáo', 'Reporting dashboards'), [
                ('Doanh thu, lời lãi, tồn kho, quảng cáo của mọi sàn trên một trang.', 'Revenue, margin, inventory and ads from every channel on one page.'),
                ('Cập nhật theo lịch, mỗi doanh nghiệp một trang riêng.', 'Updated on a schedule, with a private page for each company.'),
                ('Công cụ phân tích dữ liệu theo câu hỏi của doanh nghiệp.', 'Data analysis tools built around your questions.')]),
            (('Kết nối sàn, website và kho', 'Marketplace, website and warehouse sync'), [
                ('Đồng bộ sản phẩm, đơn hàng, tồn kho giữa các sàn, website và kho.', 'Sync products, orders and inventory between marketplaces, website and warehouse.'),
                ('Nối sang phần mềm kế toán, bớt nhập tay hai lần.', 'Connect to accounting software so nothing is entered twice.')]),
            (('Website', 'Websites'), [
                ('Website công ty và website bán hàng.', 'Company websites and online stores.'),
                ('Song ngữ khi cần, gắn với dashboard và kết nối sàn.', 'Bilingual when needed, tied into your dashboard and marketplace sync.')]),
        ],
        'give_h': ('Doanh nghiệp nhận được gì', 'What you get'),
        'give': [
            ('Hệ thống chạy trên tài khoản và tên miền của doanh nghiệp.', "A system running on your company's own accounts and domain."),
            ('Hướng dẫn sử dụng cho người phụ trách.', 'A user guide for the person in charge.'),
            ('Khách đang dùng dịch vụ vận hành sàn của TIMUS đã có trang theo dõi riêng, gồm trong phí vận hành.', 'Clients on a TIMUS operations plan already get a private dashboard, included in the fee.'),
        ],
        'you_h': ('Phần việc của doanh nghiệp', 'Your part'),
        'you': [
            ('Cho biết các sàn, phần mềm kho và kế toán đang dùng.', 'Tell us which marketplaces, warehouse and accounting software you use.'),
            ('Cấp quyền truy cập cần thiết, ưu tiên quyền chỉ xem.', 'Grant the access needed, view-only where possible.'),
            ('Chốt các chỉ số và trang cần có trước khi dựng.', 'Agree on the metrics and pages before we build.'),
        ],
        'steps': [
            (('Khảo sát', 'Survey'), ('TIMUS xem các sàn, phần mềm và cách đội đang làm báo cáo, nhập liệu.', 'TIMUS reviews your marketplaces, software and how the team reports and enters data today.')),
            (('Thống nhất phạm vi', 'Agree on scope'), ('Hai bên chốt chỉ số, trang, luồng đồng bộ cần làm và báo giá.', 'We agree on metrics, pages, sync flows and the quote.')),
            (('Dựng và kết nối', 'Build and connect'), ('Dựng dashboard, luồng đồng bộ hoặc website trên tài khoản của doanh nghiệp.', "Build the dashboard, sync flows or website on your company's accounts.")),
            (('Bàn giao', 'Handover'), ('Kiểm số liệu cùng doanh nghiệp, hướng dẫn người phụ trách và bàn giao.', 'Check the numbers with you, train the person in charge and hand over.')),
        ],
        'facts': [
            (('Làm riêng từng phần', 'Each part on its own'), ('Chỉ dashboard, chỉ kết nối hoặc chỉ website đều được', 'Dashboard only, sync only or website only')),
            (('Chi phí', 'Pricing'), ('Báo giá theo phạm vi sau buổi trao đổi đầu', 'Quoted per scope after a first call')),
            (('Bên thứ ba', 'Third party costs'), ('Trả theo thực tế, TIMUS không cộng phí', 'Paid at actual cost, no markup')),
        ],
        'faq': [
            (('Chỉ cần dashboard hoặc website, có được không?', 'Can we take just a dashboard or a website?'), ('Được. Các dịch vụ tách rời nhau, doanh nghiệp có thể chỉ làm dashboard báo cáo, website hoặc hệ thống kết nối các sàn mà không cần ký vận hành.', 'Yes. Services are separate, so you can take only a reporting dashboard, a website or a multichannel system without an operations contract.')),
            (('Dữ liệu và tài khoản đứng tên ai?', 'Who owns the data and accounts?'), ('Hệ thống chạy trên tài khoản của doanh nghiệp. TIMUS ưu tiên quyền chỉ xem và không chép thông tin khách hàng ra ngoài.', "The system runs on your company's accounts. TIMUS uses view-only access where possible and never copies customer data out.")),
        ],
        'cta': ('Nhắn Zalo', 'Message on Zalo'), 'subject': 'TIMUS - Dashboard ket noi website',
    },
    # ================= THƯƠNG MẠI ĐIỆN TỬ =================
    {
        'slug': 'nghien-cuu-san-pham', 'group': 'tech', 'num': '03',
        'title': ('Nghiên cứu sản phẩm và phân tích thị trường', 'Product research and market analysis'),
        'short': ('Biết sản phẩm nào có nhu cầu, giá bán, lời lãi dự kiến và lô đầu nên nhập bao nhiêu, trước khi bỏ tiền làm hàng.',
                  'Know which product has demand, at what price and margin, and how big the first order should be, before money goes into inventory.'),
        'lead': ('Trước khi bỏ tiền làm hàng, TIMUS xem sản phẩm nào có nhu cầu, đối thủ đang bán giá bao nhiêu, lời lãi dự kiến sau phí sàn và vận chuyển, và lô đầu nên nhập bao nhiêu. Kết quả là một báo cáo kèm bộ dữ liệu để hai bên cùng quyết định.',
                 'Before any money goes into inventory, TIMUS checks which products have demand, what competitors charge, the projected margin after marketplace fees and shipping, and how big the first order should be. You get a report with the full dataset so we can decide together.'),
        'desc': 'TIMUS nghiên cứu ngách, đối thủ, khung giá, lời lãi dự kiến và số lượng lô đầu trên các sàn tại Việt Nam và Mỹ, giao báo cáo kèm bộ dữ liệu trong khoảng 2 tuần.',
        'for': [
            ('Doanh nghiệp, xưởng có năng lực sản xuất nhưng chưa biết nên bán sản phẩm nào trên sàn.', 'Businesses and factories that can produce but do not yet know which product to sell online.'),
            ('Thương hiệu muốn thử thị trường Mỹ và cần số liệu trước khi làm hàng.', 'Brands that want to test the US market and need data before producing.'),
            ('Người đã có sản phẩm, muốn kiểm tra giá bán và lời lãi trước khi nhập lô lớn.', 'Sellers with a product who want to check price and margin before a large order.'),
        ],
        'scope': [
            ('Nghiên cứu ngách, đối thủ, khung giá, lời lãi dự kiến và số lượng lô đầu.', 'Niche, competitor and price research with projected margin and first order quantity.'),
            ('Phân tích thị trường Việt Nam và Mỹ theo số liệu bán hàng thực tế trên các sàn.', 'Vietnam and US market analysis based on real marketplace sales data.'),
            ('Phân tích năng lực doanh nghiệp: công thức, nhà xưởng, kho, nguyên liệu sẵn có, để chọn sản phẩm làm được và bán được.', 'Assess what your company already has (formulas, factory, warehouse, raw materials) to pick products you can make and sell.'),
            ('Tính lời lãi dự kiến sau phí sàn và vận chuyển.', 'Projected margin after marketplace fees and shipping.'),
        ],
        'give_h': ('Doanh nghiệp nhận được gì', 'What you get'),
        'give': [
            ('Một báo cáo: ngách, đối thủ, khung giá, lời lãi dự kiến, số lượng lô đầu.', 'A report: niche, competitors, price range, projected margin and first order quantity.'),
            ('Bộ dữ liệu đi kèm để doanh nghiệp tự xem lại.', 'The full dataset so you can check it yourself.'),
            ('Đề xuất 1 đến 2 sản phẩm nên thử trước.', 'A proposal of 1 to 2 products to test first.'),
        ],
        'you_h': ('Phần việc của doanh nghiệp', 'Your part'),
        'you': [
            ('Cho biết sản phẩm hoặc năng lực sản xuất đang có.', 'Tell us the product or production capacity you have.'),
            ('Cho biết thị trường muốn bán và mức vốn dự kiến cho lô đầu.', 'Tell us the target market and the budget planned for the first order.'),
            ('Cùng TIMUS xem báo cáo và quyết định bước tiếp theo.', 'Review the report with TIMUS and decide the next step.'),
        ],
        'steps': [
            (('Trao đổi đầu', 'First call'), ('Doanh nghiệp cho biết sản phẩm, năng lực sẵn có và thị trường muốn bán.', 'You tell us about your product, existing capacity and target market.')),
            (('Thu thập dữ liệu', 'Collect data'), ('TIMUS lấy số liệu bán hàng thực tế trên các sàn: ngách, đối thủ, giá.', 'TIMUS gathers real marketplace sales data: niches, competitors, prices.')),
            (('Phân tích', 'Analyse'), ('Tính lời lãi dự kiến sau phí sàn và vận chuyển, ước số lượng lô đầu.', 'Work out projected margin after fees and shipping, and estimate first order quantity.')),
            (('Báo cáo và quyết định', 'Report and decide'), ('Gửi báo cáo kèm bộ dữ liệu. Hai bên cùng quyết định trước khi bỏ tiền làm hàng.', 'Deliver the report and dataset. We decide together before any money goes into inventory.')),
        ],
        'facts': [
            (('Thời gian', 'Timeline'), ('Khoảng 2 tuần cho một dòng sản phẩm', 'About 2 weeks per product line')),
            (('Cách tính phí', 'How it is charged'), ('Phí cố định theo dòng sản phẩm, trả một lần', 'Fixed fee per product line, paid once')),
            (('Chi phí', 'Pricing'), ('Báo giá sau buổi trao đổi đầu', 'Quoted after a first call')),
        ],
        'faq': [
            (('Chưa có sản phẩm để bán online thì bắt đầu từ đâu?', 'We do not have a product for online sales yet. Where do we start?'), ('Bắt đầu từ khâu nghiên cứu. TIMUS xem năng lực sẵn có của doanh nghiệp, phân tích thị trường và đề xuất 1 đến 2 sản phẩm để thử trước. Hai bên cùng quyết định rồi mới bỏ tiền làm hàng.', 'Start with research. We look at what your company can already do, analyse the market and propose 1 to 2 products to test first. We decide together before any money goes into inventory.')),
            Q_ONLY_ONE,
        ],
        'cta': ('Nhắn Zalo', 'Message on Zalo'), 'subject': 'TIMUS - Nghien cuu san pham',
    },
    {
        'slug': 'nguon-hang', 'group': 'logi', 'num': '01',
        'title': ('Phát triển sản phẩm và nguồn hàng', 'Product development and sourcing'),
        'short': ('Tìm và so sánh nhà máy tại Việt Nam, Trung Quốc; phát triển mẫu, bao bì và làm lô thử trước khi làm lô lớn.',
                  'Find and compare factories in Vietnam and China; develop samples and packaging and run a test batch before scaling.'),
        'lead': ('Khi đã chọn được sản phẩm, TIMUS tìm và so sánh nhà máy, phát triển mẫu mã, quy cách, bao bì cho từng thị trường, rồi làm lô mẫu để thử nhu cầu trên sàn trước khi doanh nghiệp làm lô lớn.',
                 'Once the product is chosen, TIMUS finds and compares factories, develops the product spec and packaging for each market, then runs a sample batch to test demand on marketplaces before you commit to a large order.'),
        'desc': 'TIMUS tìm và so sánh nhà máy, nhà cung cấp tại Việt Nam và Trung Quốc, phát triển mẫu mã, bao bì và làm lô thử trước khi doanh nghiệp làm lô lớn.',
        'for': [
            ('Thương hiệu đã chọn được sản phẩm nhưng chưa có nhà máy.', 'Brands that have picked a product but have no factory yet.'),
            ('Doanh nghiệp muốn so sánh giá và điều kiện của nhiều nhà cung cấp trước khi đặt hàng.', 'Companies that want to compare prices and terms from several suppliers before ordering.'),
            ('Người bán muốn thử nhu cầu bằng một lô nhỏ trước khi làm lô lớn.', 'Sellers who want to test demand with a small batch before scaling.'),
        ],
        'scope': [
            ('Tìm và so sánh nhà máy, nhà cung cấp tại Trung Quốc và Việt Nam: giá, số lượng tối thiểu, quy cách, thời gian sản xuất.', 'Find and compare factories and suppliers in China and Vietnam: unit cost, MOQ, specs, lead time.'),
            ('Phát triển mẫu mã, quy cách, bao bì cho từng thị trường.', 'Develop product specs and packaging for each market.'),
            ('Làm lô mẫu, thử nhu cầu trên sàn trước khi làm lô lớn.', 'Run a sample batch and test demand on marketplaces before scaling.'),
        ],
        'give_h': ('Doanh nghiệp nhận được gì', 'What you get'),
        'give': [
            ('Bảng so sánh nhà cung cấp: giá, số lượng tối thiểu, quy cách, thời gian sản xuất.', 'A supplier comparison: unit cost, MOQ, specs and lead time.'),
            ('Mẫu sản phẩm và bao bì đã chốt cho thị trường muốn bán.', 'Agreed product and packaging samples for your target market.'),
            ('Kết quả lô thử để quyết định có làm lô lớn hay không.', 'Test batch results to decide whether to scale.'),
        ],
        'you_h': ('Phần việc của doanh nghiệp', 'Your part'),
        'you': [
            ('Chốt yêu cầu sản phẩm và mức giá vốn mong muốn.', 'Agree on product requirements and target unit cost.'),
            ('Duyệt mẫu và nhà cung cấp.', 'Approve samples and the supplier.'),
            ('Trả trực tiếp tiền hàng mẫu, tiền sản xuất và vận chuyển theo thực tế. TIMUS không cộng phí vào các khoản này.', 'Pay sample, production and shipping costs directly at actual cost. TIMUS adds no markup.'),
        ],
        'steps': [
            (('Chốt yêu cầu', 'Agree on requirements'), ('Sản phẩm, quy cách, giá vốn mong muốn và thị trường sẽ bán.', 'Product, specs, target unit cost and the market you will sell in.')),
            (('Tìm và so sánh nhà máy', 'Find and compare factories'), ('TIMUS gửi bảng so sánh giá, số lượng tối thiểu, quy cách, thời gian sản xuất.', 'TIMUS sends a comparison of unit cost, MOQ, specs and lead time.')),
            (('Làm mẫu', 'Sampling'), ('Phát triển mẫu mã, bao bì và chỉnh cho đến khi doanh nghiệp duyệt.', 'Develop the product and packaging samples and revise until you approve.')),
            (('Lô thử', 'Test batch'), ('Làm một lô nhỏ, thử nhu cầu trên sàn rồi mới quyết định lô lớn.', 'Produce a small batch, test demand on marketplaces, then decide on scaling.')),
        ],
        'facts': [
            (('Nguồn hàng', 'Sourcing'), ('Nhà máy tại Việt Nam và Trung Quốc', 'Factories in Vietnam and China')),
            (('Chi phí', 'Pricing'), ('Báo giá riêng theo phạm vi hàng', 'Quoted separately per scope')),
            (('Tiền hàng, hàng mẫu', 'Goods and samples'), ('Trả theo thực tế, TIMUS không cộng phí', 'Paid at actual cost, no markup')),
        ],
        'faq': [
            (('TIMUS có cộng thêm vào giá của nhà máy không?', "Does TIMUS add a margin on the factory's price?"), ('Không. Tiền hàng mẫu, tiền sản xuất và vận chuyển doanh nghiệp trả trực tiếp theo thực tế. TIMUS chỉ thu phí dịch vụ ghi trong báo giá.', 'No. You pay sample, production and shipping costs directly at actual cost. TIMUS only charges the service fee stated in the quote.')),
            Q_ONLY_ONE,
        ],
        'cta': ('Nhắn Zalo', 'Message on Zalo'), 'subject': 'TIMUS - Nguon hang',
    },
    {
        'slug': 'ban-hang-tai-my', 'group': 'tmdt', 'num': '02',
        'title': ('Bán hàng tại Mỹ', 'Selling in the United States'),
        'short': ('Mở gian hàng và vận hành trên Amazon, TikTok Shop US, Walmart, eBay, Etsy, Shopify. Có gói thử nghiệm 3 tháng.',
                  'Store setup and operations on Amazon, TikTok Shop US, Walmart, eBay, Etsy and Shopify, with a 3 month test plan.'),
        'lead': ('TIMUS đưa sản phẩm của thương hiệu Việt lên các sàn và nền tảng thương mại điện tử lớn tại Mỹ: mở gian hàng, đăng sản phẩm, chạy quảng cáo trong ngân sách đã duyệt, làm việc với creator, chăm sóc người mua và báo cáo hằng tháng.',
                 'TIMUS takes Vietnamese brands onto the major US marketplaces and e-commerce platforms: opening the store, listing products, running ads within the approved budget, working with creators, serving customers and reporting every month.'),
        'desc': 'TIMUS mở gian hàng và vận hành cho thương hiệu Việt trên Amazon, TikTok Shop US, Walmart, eBay, Etsy, Shopify: quảng cáo, creator, chăm sóc khách, báo cáo tháng. Có gói thử nghiệm 3 tháng.',
        'for': [
            ('Thương hiệu, xưởng Việt Nam muốn bán lẻ trực tiếp cho người mua tại Mỹ.', 'Vietnamese brands and factories that want to sell directly to US consumers.'),
            ('Doanh nghiệp đang xuất khẩu số lượng lớn, muốn thử thêm kênh bán lẻ trên sàn.', 'Exporters who want to add a marketplace retail channel.'),
            ('Doanh nghiệp đã có gian hàng tại Mỹ nhưng chưa có người vận hành.', 'Companies with a US store but no one to run it.'),
        ],
        'tags': 'Amazon · TikTok Shop US · Walmart · eBay · Etsy · Shopify',
        'options': [
            (('Thiết lập gian hàng', 'Store setup'), [
                ('Mở kênh, đăng sản phẩm, viết nội dung trang.', 'Open the channel, list products and write store content.'),
                ('Kết nối kho để giao đơn.', 'Connect the warehouse for fulfilment.')]),
            (('Vận hành và quản lý sàn', 'Marketplace management'), [
                ('Quản trị gian hàng, giá và khuyến mãi.', 'Store operations, pricing and promotions.'),
                ('Quảng cáo trong ngân sách đã duyệt, làm việc với creator.', 'Ads within the approved budget, and creator partnerships.'),
                ('Chăm sóc người mua, xử lý vi phạm, báo cáo tháng.', 'Customer service, policy issues and monthly reports.')]),
            (('Gói thử nghiệm 3 tháng', '3 month test plan'), [
                ('1 kênh, 1 đến 2 sản phẩm, trong 3 tháng.', '1 channel, 1 to 2 products, for 3 months.'),
                ('Hết 3 tháng, hai bên xem số liệu rồi quyết định có vận hành tiếp.', 'After 3 months we review the data and decide whether to continue.')]),
        ],
        'give_h': ('Doanh nghiệp nhận được gì', 'What you get'), 'give': OPS_GIVE,
        'you_h': ('Phần việc của doanh nghiệp', 'Your part'), 'you': OPS_YOU,
        'steps': OPS_STEPS,
        'facts': [
            (('Hợp đồng vận hành', 'Operations contract'), ('Tối thiểu 6 tháng', 'At least 6 months')),
            (('Gói thử nghiệm', 'Test plan'), ('3 tháng, 1 kênh, 1 đến 2 sản phẩm', '3 months, 1 channel, 1 to 2 products')),
            (('Chi phí', 'Pricing'), ('Báo giá theo phạm vi sau buổi trao đổi đầu', 'Quoted per scope after a first call')),
        ],
        'note': ('Việc pháp lý, thuế, đăng ký công ty và đứng tên nhập khẩu tại Mỹ do đơn vị chuyên môn đối tác thực hiện; TIMUS kết nối, phối hợp hồ sơ và theo dõi tiến độ.',
                 'Legal, tax, company registration and importer of record work in the US is done by partner specialists; TIMUS connects you, coordinates the paperwork and follows up.'),
        'faq': [
            Q_FIRST_ORDER,
            (('Hợp đồng vận hành kéo dài bao lâu?', 'How long is an operations contract?'), ('Hợp đồng vận hành tối thiểu 6 tháng, vì gian hàng cần thời gian để có dữ liệu và cải thiện. Nếu muốn thử trước, có gói thử nghiệm 3 tháng cho 1 kênh và 1 đến 2 sản phẩm.', 'Operations contracts run for at least 6 months, since a store needs time to gather data and improve. To test first, there is a 3 month plan covering 1 channel and 1 to 2 products.')),
            (('Chưa có công ty, kho hay giấy tờ tại Mỹ thì sao?', 'What if we have no US company, warehouse or paperwork?'), ('TIMUS nhận phần kho và đưa hàng đi ở dịch vụ Hậu cần. Phần pháp lý, thuế, đăng ký công ty do đơn vị chuyên môn tại Mỹ thực hiện, TIMUS kết nối và phối hợp hồ sơ thay doanh nghiệp.', 'TIMUS covers warehousing and shipping under our Logistics service. Legal, tax and company registration are handled by US specialists; TIMUS connects you and coordinates the paperwork.')),
        ],
        'cta': ('Nhắn Zalo', 'Message on Zalo'), 'subject': 'TIMUS - Ban hang tai My',
    },
    {
        'slug': 'ban-hang-tai-viet-nam', 'group': 'tmdt', 'num': '01',
        'title': ('Bán hàng tại Việt Nam', 'Selling in Vietnam'),
        'short': ('Mở gian hàng và vận hành trên Shopee, TikTok Shop, Lazada, Tiki: quảng cáo, KOC, chăm sóc khách, báo cáo tháng.',
                  'Store setup and operations on Shopee, TikTok Shop, Lazada and Tiki: ads, KOCs, customer service and monthly reports.'),
        'lead': ('TIMUS vận hành gian hàng của doanh nghiệp trên các sàn tại Việt Nam: đăng sản phẩm, giá và khuyến mãi, quảng cáo trong ngân sách đã duyệt, làm việc với KOC, chăm sóc người mua, xử lý vi phạm và báo cáo hằng tháng.',
                 "TIMUS runs your company's stores on Vietnamese marketplaces: listings, pricing and promotions, ads within the approved budget, KOC partnerships, customer service, policy issues and monthly reports."),
        'desc': 'TIMUS mở gian hàng và vận hành cho doanh nghiệp trên Shopee, TikTok Shop, Lazada, Tiki: quảng cáo, KOC, chăm sóc khách, công cụ chỉnh sửa video, báo cáo và đối soát hằng tháng.',
        'for': [
            ('Doanh nghiệp có sản phẩm nhưng chưa có gian hàng trên sàn.', 'Companies with a product but no marketplace store yet.'),
            ('Doanh nghiệp đã có gian hàng nhưng thiếu người vận hành hằng ngày.', 'Companies with a store but no one to run it day to day.'),
            ('Thương hiệu muốn mở thêm sàn sau khi sàn đầu đã chạy ổn.', 'Brands that want to add marketplaces once the first one is running well.'),
        ],
        'tags': 'Shopee · TikTok Shop · Lazada · Tiki · Website',
        'scope': [
            ('Thiết lập gian hàng: mở hoặc chuẩn hoá gian hàng, đăng sản phẩm, trang shop. Phần này gồm trong tháng vận hành đầu tiên.', 'Store setup: open or tidy up the store, list products and build the shop page. Included in the first month of operations.'),
            ('Vận hành sàn: quản trị gian hàng, giá và khuyến mãi, quảng cáo trong ngân sách đã duyệt.', 'Marketplace operations: store management, pricing and promotions, ads within the approved budget.'),
            ('Làm việc với KOC, chăm sóc người mua, xử lý vi phạm.', 'KOC partnerships, customer service and policy issues.'),
            ('Công cụ chỉnh sửa video trực tuyến cho nội dung bán hàng.', 'Online video editing tools for sales content.'),
            ('Mở thêm sàn khi sàn đầu đã chạy ổn.', 'Add more marketplaces once the first one is running well.'),
        ],
        'give_h': ('Doanh nghiệp nhận được gì', 'What you get'), 'give': OPS_GIVE,
        'you_h': ('Phần việc của doanh nghiệp', 'Your part'), 'you': OPS_YOU,
        'steps': OPS_STEPS,
        'facts': [
            (('Hợp đồng vận hành', 'Operations contract'), ('Tối thiểu 6 tháng', 'At least 6 months')),
            (('Thiết lập gian hàng', 'Store setup'), ('Gồm trong tháng vận hành đầu tiên', 'Included in the first month')),
            (('Gian hàng và dữ liệu', 'Store and data'), ('Đứng tên thương hiệu', "In the brand's name")),
        ],
        'faq': [
            Q_FIRST_ORDER,
            (('Gian hàng và tài khoản quảng cáo đứng tên ai?', 'Who owns the store and ad accounts?'), ('Gian hàng, tài khoản quảng cáo và dữ liệu bán hàng tại Việt Nam đứng tên thương hiệu. TIMUS vận hành trên tài khoản đó.', "The store, ad accounts and sales data in Vietnam are in the brand's name. TIMUS operates on those accounts.")),
            (('Hợp đồng vận hành kéo dài bao lâu?', 'How long is an operations contract?'), ('Hợp đồng vận hành tối thiểu 6 tháng, vì gian hàng cần thời gian để có dữ liệu và cải thiện.', 'Operations contracts run for at least 6 months, since a store needs time to gather data and improve.')),
        ],
        'cta': ('Nhắn Zalo', 'Message on Zalo'), 'subject': 'TIMUS - Ban hang tai Viet Nam',
    },
    {
        'slug': 'hau-can', 'group': 'logi', 'num': '02',
        'title': ('Hậu cần và đưa hàng đi', 'Logistics and fulfillment'),
        'short': ('Bao bì, tem nhãn, phối hợp giấy tờ xuất nhập khẩu, vận chuyển, và kho tại Mỹ kết nối các sàn.',
                  'Packaging, labels, export and import paperwork, shipping, and a US warehouse connected to marketplaces.'),
        'lead': ('Để hàng Việt tới tay người mua tại Mỹ cần bao bì và tem nhãn đúng yêu cầu, giấy tờ xuất nhập khẩu, vận chuyển và một kho giao đơn tại Mỹ. TIMUS nhận phối hợp các khâu này và theo dõi tiến độ thay doanh nghiệp.',
                 'Getting Vietnamese goods to US buyers takes compliant packaging and labels, export and import paperwork, shipping and a fulfilment warehouse in the US. TIMUS coordinates these stages and follows up on your behalf.'),
        'desc': 'TIMUS phối hợp bao bì, tem nhãn, giấy tờ xuất nhập khẩu, vận chuyển và vận hành kho tại Mỹ kết nối các sàn, kết nối đơn vị chuyên môn về pháp lý và thuế tại Mỹ.',
        'for': [
            ('Doanh nghiệp đã có hàng, cần đưa sang Mỹ và giao đơn từ kho tại Mỹ.', 'Companies with stock that needs to reach the US and ship from a US warehouse.'),
            ('Thương hiệu chưa rõ yêu cầu bao bì, tem nhãn của sàn và thị trường.', 'Brands unsure about marketplace and market packaging and label requirements.'),
            ('Doanh nghiệp cần một đầu mối theo dõi cả chặng thay vì làm việc với nhiều bên.', 'Companies that want one contact for the whole route instead of several vendors.'),
        ],
        'scope': [
            ('Bao bì, tem nhãn theo yêu cầu của sàn và thị trường.', 'Packaging and labels that meet marketplace and market requirements.'),
            ('Phối hợp giấy tờ xuất nhập khẩu và vận chuyển.', 'Coordination of export and import paperwork and shipping.'),
            ('Nhận hàng và vận hành kho tại Mỹ, kết nối các sàn.', 'Receiving and warehouse operations in the US, connected to marketplaces.'),
            ('Tìm và kết nối đơn vị chuyên môn tại Mỹ về pháp lý, thuế, đăng ký công ty, đứng tên nhập khẩu; TIMUS phối hợp hồ sơ và theo dõi tiến độ thay doanh nghiệp.', 'Find and connect you with US specialists for legal, tax, company registration and importer of record; TIMUS coordinates the paperwork and follows up on your behalf.'),
            ('Vận hành chuyên sâu theo nhu cầu riêng.', 'Custom operations on request.'),
        ],
        'give_h': ('Doanh nghiệp nhận được gì', 'What you get'),
        'give': [
            ('Một đầu mối theo dõi từ lúc đóng gói đến khi hàng nhập kho tại Mỹ.', 'One contact from packing to arrival at the US warehouse.'),
            ('Tồn kho và đơn giao được kết nối với các sàn đang bán.', 'Inventory and shipments connected to the marketplaces you sell on.'),
            ('Cập nhật tiến độ từng chặng.', 'Progress updates at each stage.'),
        ],
        'you_h': ('Phần việc của doanh nghiệp', 'Your part'),
        'you': [
            ('Thống nhất sản phẩm và số lượng trước khi báo giá.', 'Agree on the product and quantity before we quote.'),
            ('Cung cấp thông tin và giấy tờ sản phẩm.', 'Provide product information and documents.'),
            ('Trả trực tiếp cước vận chuyển, phí kho, thuế theo thực tế. TIMUS không cộng phí vào các khoản này.', 'Pay shipping, warehousing and duties directly at actual cost. TIMUS adds no markup.'),
        ],
        'steps': [
            (('Thống nhất hàng', 'Agree on the goods'), ('Hai bên chốt sản phẩm, số lượng và sàn sẽ bán. TIMUS gửi báo giá theo phạm vi.', 'We agree on the product, quantity and marketplaces. TIMUS sends a scoped quote.')),
            (('Bao bì và giấy tờ', 'Packaging and paperwork'), ('Chuẩn bị bao bì, tem nhãn và phối hợp giấy tờ xuất nhập khẩu.', 'Prepare packaging and labels and coordinate export and import paperwork.')),
            (('Vận chuyển', 'Shipping'), ('Phối hợp đưa hàng sang Mỹ và cập nhật tiến độ.', 'Coordinate shipping to the US and keep you updated.')),
            (('Nhập kho và giao đơn', 'Warehouse and fulfilment'), ('Kho tại Mỹ nhận hàng, kết nối các sàn và giao đơn.', 'The US warehouse receives the goods, connects to marketplaces and ships orders.')),
        ],
        'facts': [
            (('Chi phí', 'Pricing'), ('Báo giá riêng sau khi thống nhất sản phẩm và số lượng', 'Quoted separately once product and quantity are agreed')),
            (('Cước, kho, thuế', 'Shipping, storage, duties'), ('Trả theo thực tế, TIMUS không cộng phí', 'Paid at actual cost, no markup')),
            (('Pháp lý và thuế', 'Legal and tax'), ('Do đơn vị đối tác chuyên môn thực hiện', 'Handled by partner specialists')),
        ],
        'note': ('Ý kiến chuyên môn về pháp lý và thuế do đơn vị đối tác đưa ra.', 'Legal and tax opinions are given by our partner specialists.'),
        'faq': [
            (('TIMUS có tư vấn pháp lý hay thuế tại Mỹ không?', 'Does TIMUS give US legal or tax advice?'), ('Không. TIMUS tìm và kết nối đơn vị chuyên môn tại Mỹ, phối hợp hồ sơ và theo dõi tiến độ thay doanh nghiệp. Ý kiến chuyên môn do đơn vị đối tác đưa ra.', 'No. TIMUS finds and connects you with US specialists, coordinates the paperwork and follows up on your behalf. Professional opinions come from the partner.')),
            Q_ONLY_ONE,
        ],
        'cta': ('Nhắn Zalo', 'Message on Zalo'), 'subject': 'TIMUS - Hau can',
    },
]


# ---------- khung HTML ----------
def L(t):
    return f'<span data-l="vi">{t[0]}</span><span data-l="en">{t[1]}</span>'


def UL(items, cls=''):
    c = f' class="{cls}"' if cls else ''
    vi = ''.join(f'<li>{a}</li>' for a, _ in items)
    en = ''.join(f'<li>{b}</li>' for _, b in items)
    return f'<ul{c} data-l="vi">{vi}</ul><ul{c} data-l="en">{en}</ul>'


def P(t, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<p{c} data-l="vi">{t[0]}</p><p{c} data-l="en">{t[1]}</p>'


NAV = [('dich-vu', ('Dịch vụ', 'Services')),
       ('cach-lam', ('Cách làm việc', 'How we work')), ('dao-tao', ('Đào tạo', 'Training')),
       ('ve-timus', ('Về TIMUS', 'About')), ('lien-he', ('Liên hệ', 'Contact'))]


def header(home=False):
    def href(i):
        return f'#{i}' if home or i == 'lien-he' else f'/#{i}'
    links = '\n'.join(f'      <a href="{href(i)}">{L(n)}</a>' for i, n in NAV)
    return f'''<header class="top">
  <div class="wrap top-in">
    <a href="{'#' if home else '/'}" class="brand" aria-label="TIMUS">
      <img src="/assets/timus-mark.webp" alt="" width="44" height="27">
      <span>TIMUS</span>
    </a>
    <nav class="nav" id="nav" aria-label="Menu">
{links}
    </nav>
    <div class="lang" role="group" aria-label="Ngôn ngữ / Language">
      <button type="button" data-set="vi">VI</button>
      <button type="button" data-set="en">EN</button>
    </div>
    <a class="btn btn-gold btn-sm top-cta" href="#lien-he">{L(('Liên hệ báo giá', 'Get a quote'))}</a>
    <button type="button" class="burger" aria-label="Menu" aria-controls="nav" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</header>'''


LANG_JS = '''<script>
  (function () {
    var q = new URLSearchParams(location.search).get('lang');
    var saved = null;
    try { saved = localStorage.getItem('timus-lang'); } catch (e) {}
    var lang = q === 'en' || q === 'vi' ? q : (saved || 'vi');
    document.documentElement.setAttribute('data-lang', lang);
    document.documentElement.lang = lang;
  })();
</script>'''


def scard(p):
    return f'''      <a class="scard" href="/{p['slug']}/">
        <span class="num">{p['num']}</span>
        <h3>{L(p['title'])}</h3>
        {P(p['short'])}
        <span class="link">{L(('Xem chi tiết', 'View details'))} →</span>
      </a>'''


def page(p):
    g = GROUPS[p['group']]
    url = f"{SITE}/{p['slug']}/"
    mail = f"mailto:{MAIL}?subject={p['subject'].replace(' ', '%20')}"
    ld = {'@context': 'https://schema.org', '@type': 'Service', 'name': p['title'][0], 'alternateName': p['title'][1],
          'description': p['desc'], 'url': url, 'areaServed': ['VN', 'US'],
          'provider': {'@type': 'Organization', 'name': 'TIMUS CO., LTD', 'url': SITE + '/'}}
    out = [f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p['title'][0]} | TIMUS CO., LTD</title>
<meta name="description" content="{p['desc']}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{p['title'][0]} | TIMUS">
<meta property="og:description" content="{p['desc']}">
<meta property="og:image" content="{SITE}/assets/og.jpg">
<meta name="theme-color" content="#0B0B0B">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600&family=Montserrat:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css?v={CSS_V}">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{LANG_JS}
</head>
<body class="svc-page">

{header()}

<main>

<section class="hero pg-hero">
  <canvas id="heroFx" class="hero-fx" aria-hidden="true"></canvas>
  <div class="wrap hero-in one">
    <div>
      <p class="crumb"><a href="/">TIMUS</a> <span>/</span> <a href="/#{g['id']}">{L(g['name'])}</a> <span>/</span> {L(p['title'])}</p>
      <p class="eyebrow">{p['num']} · {L(g['name'])}</p>
      <h1>{L(p['title'])}</h1>
      <p class="lead">{L(p['lead'])}</p>
      <div class="cta">
        <a class="btn btn-gold" href="{ZALO}" target="_blank" rel="noopener">{L(p['cta'])}</a>
        <a class="btn btn-line" href="{mail}">{L(('Gửi email', 'Email us'))}</a>
      </div>
    </div>
  </div>
</section>
''']

    # ai phù hợp + TIMUS làm gì
    right = ''
    if p.get('scope'):
        right = f'''<div>
      <h2 class="h-sm">{L(('TIMUS làm gì', 'What TIMUS does'))}</h2>
      {UL(p['scope'], 'safe')}
      {f'<p class="tags">{p["tags"]}</p>' if p.get('tags') else ''}
    </div>'''
    elif p.get('tags'):
        right = f'''<div>
      <h2 class="h-sm">{L(('Sàn và nền tảng', 'Marketplaces and platforms'))}</h2>
      <p class="tools big">{p['tags']}</p>
    </div>'''
    out.append(f'''<section class="sec light">
  <div class="wrap pg-two{'' if right else ' single'} reveal">
    <div>
      <h2 class="h-sm">{L(('Phù hợp với ai', 'Who it is for'))}</h2>
      {UL(p['for'], 'safe')}
    </div>
    {right}
  </div>
</section>
''')

    if p.get('options'):
        cards = '\n'.join(f'''      <article class="card">
        <span class="num">{i:02d}</span>
        <h3>{L(t)}</h3>
        {UL(items)}
      </article>''' for i, (t, items) in enumerate(p['options'], 1))
        out.append(f'''<section class="sec sec-alt light">
  <div class="wrap">
    <h2>{L(('Các phần việc', 'What is included'))}</h2>
    <div class="svc three reveal">
{cards}
    </div>
  </div>
</section>
''')

    if p.get('depts'):
        row = '\n'.join(f'        <button type="button" class="tab{" on" if i == 0 else ""}" data-tab="d{i}" role="tab" aria-selected="{"true" if i == 0 else "false"}">{L(n)}</button>' for i, (n, _) in enumerate(p['depts']))
        pan = '\n'.join(f'      <div class="tab-p dept-p{" on" if i == 0 else ""}" data-panel="d{i}" role="tabpanel">{UL(items)}</div>' for i, (_, items) in enumerate(p['depts']))
        out.append(f'''<section class="sec tech">
  <div class="wrap">
    <h2>{L(('Trợ lý AI làm được gì cho từng phòng ban', 'What an AI assistant does for each department'))}</h2>
    <div class="tabs reveal" data-tabs data-hover>
      <div class="tab-row" role="tablist">
{row}
      </div>
{pan}
    </div>
    <h3 class="t-h">{L(('Làm việc trên công cụ doanh nghiệp đang dùng', 'Works with the tools you already use'))}</h3>
    <p class="tools">{p['tools']}</p>
  </div>
</section>
''')

    out.append(f'''<section class="sec {'light' if p.get('depts') else ('light' if p.get('options') else 'sec-alt light')}">
  <div class="wrap pg-two reveal">
    <div>
      <h2 class="h-sm">{L(p['give_h'])}</h2>
      {UL(p['give'], 'safe')}
    </div>
    <div>
      <h2 class="h-sm">{L(p['you_h'])}</h2>
      {UL(p['you'], 'safe')}
    </div>
  </div>
</section>
''')

    lis = '\n'.join(f'''        <li>
          <b>{L(t)}</b>
          {P(d)}
        </li>''' for t, d in p['steps'])
    out.append(f'''<section class="sec sec-alt light">
  <div class="wrap" data-steps>
    <h2>{L(('Quy trình', 'Process'))}</h2>
    <ol class="steps hov{' five' if len(p['steps']) == 5 else ''}">
{lis}
    </ol>
    <div class="step-desc" aria-live="polite"></div>
  </div>
</section>
''')

    facts = '\n'.join(f'      <div class="c-item"><span class="label">{L(a)}</span><span class="val">{L(b)}</span></div>' for a, b in p['facts'])
    out.append(f'''<section class="sec facts">
  <div class="wrap">
    <h2>{L(('Thời gian và điều kiện', 'Timeline and terms'))}</h2>
    <div class="contact-grid reveal">
{facts}
    </div>
    {P(p['note'], 'note') if p.get('note') else ''}
  </div>
</section>
''')

    qa = '\n'.join(f'''      <details class="qa">
        <summary>{L(q)}</summary>
        {P(a)}
      </details>''' for q, a in p['faq'])
    out.append(f'''<section class="sec sec-alt light">
  <div class="wrap faq">
    <h2>{L(('Câu hỏi thường gặp', 'Frequently asked questions'))}</h2>
    <div class="qa-list">
{qa}
    </div>
  </div>
</section>
''')

    others = [o for o in PAGES if o['slug'] != p['slug']]
    others.sort(key=lambda o: (o['group'] != p['group'], PAGES.index(o)))
    out.append(f'''<section class="sec light">
  <div class="wrap">
    <h2>{L(('Dịch vụ khác của TIMUS', 'Other TIMUS services'))}</h2>
    <div class="sgrid reveal">
{chr(10).join(scard(o) for o in others[:3])}
    </div>
    <p class="t-link"><a class="link" href="/">{L(('Về trang chủ, xem tất cả dịch vụ', 'Back to home, see all services'))} →</a></p>
  </div>
</section>

<section id="lien-he" class="sec contact">
  <div class="wrap">
    <h2>{L(('Liên hệ', 'Contact'))}</h2>
    <p class="sub">{L(('Cho TIMUS biết tình hình của doanh nghiệp và phần việc đang cần. Chúng tôi trả lời và gửi báo giá theo phạm vi.', 'Tell us about your company and the work you need. We will reply with a scoped quote.'))}</p>
    <div class="contact-grid reveal">
      <a class="c-item" href="{ZALO}" target="_blank" rel="noopener"><span class="label">Zalo</span><span class="val">0796 796 492</span></a>
      <a class="c-item" href="{mail}"><span class="label">Email</span><span class="val">{MAIL}</span></a>
      <div class="c-item"><span class="label">{L(('Trụ sở', 'Office'))}</span><span class="val">{L(('Đà Nẵng, Việt Nam', 'Da Nang, Vietnam'))}</span></div>
    </div>
  </div>
</section>

</main>

<a class="fab" href="{ZALO}" target="_blank" rel="noopener" aria-label="Zalo">Zalo</a>

<footer class="foot">
  <div class="wrap foot-in">
    <span>© 2026 TIMUS CO., LTD</span>
    {L(('Hệ sinh thái dịch vụ Logistics, E-Commerce &amp; Technology', 'Logistics, E-Commerce &amp; Technology services'))}
  </div>
</footer>

<script src="/assets/site.js?v={JS_V}"></script>
</body>
</html>
''')
    return ''.join(out)


def home_blocks():
    by = {p['slug']: p for p in PAGES}
    return home_parts.services(by, P) + home_more.included()


def main():
    for p in PAGES:
        os.makedirs(p['slug'], exist_ok=True)
        with open(os.path.join(p['slug'], 'index.html'), 'w') as f:
            f.write(page(p))
    s = open('index.html').read()
    a, b = s.index('<!-- SVC:START -->'), s.index('<!-- SVC:END -->')
    s = s[:a] + '<!-- SVC:START -->\n' + home_blocks() + s[b:]
    a, b = s.index('<!-- HERO:START -->'), s.index('<!-- HERO:END -->')
    s = s[:a] + '<!-- HERO:START -->\n' + home_parts.hero() + '\n' + s[b:]
    a, b = s.index('<!-- PROC:START -->'), s.index('<!-- PROC:END -->')
    s = s[:a] + '<!-- PROC:START -->\n' + home_more.process() + s[b:]
    h1, h2 = s.index('<header class="top">'), s.index('</header>') + len('</header>')
    s = s[:h1] + header(home=True) + s[h2:]
    open('index.html', 'w').write(s)
    urls = [SITE + '/'] + [f"{SITE}/{p['slug']}/" for p in PAGES]
    open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                   + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    print('built', len(PAGES), 'pages')


if __name__ == '__main__':
    main()
