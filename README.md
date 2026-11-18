**Website TIMUS (timusco.com)**

Trang tĩnh một trang, song ngữ Việt Anh (nút VI / EN, hoặc thêm `?lang=en` vào đường dẫn). Không có bảng giá, chỉ "Liên hệ báo giá".

**File**
- `index.html`: toàn bộ nội dung, mỗi câu có hai bản `data-l="vi"` và `data-l="en"`.
- `style.css`: màu đen và vàng theo logo (#D4A862).
- `assets/`: logo cắt từ `Hợp đồng Ami - bản cuối (20-10-2026)/TIMUS - logo vàng (nền đen).png`, favicon, ảnh chia sẻ.
- `CNAME`: timusco.com, để GitHub Pages nhận tên miền.

**Xem thử trên máy**
Trong app: preview `timus-web` (cổng 8131, khai báo ở `Desktop/Huy Tim/.claude/launch.json`).

**Đưa lên web (chỉ khi Huy nói "push")**
1. Tạo repo mới `DinhHuy1405/timus-website` (công khai, vì GitHub Pages bản miễn phí cần repo công khai).
2. Đẩy thư mục này lên nhánh `main`, bật Settings > Pages > Deploy from branch `main` / root, điền Custom domain `timusco.com`, bật Enforce HTTPS khi GitHub cấp xong chứng chỉ.

**Trỏ DNS timusco.com (Google Workspace / Squarespace Domains > DNS > Custom records)**
Chỉ thêm các bản ghi dưới đây. Không xoá hay sửa bản ghi MX, TXT (SPF, DKIM, xác minh Google) của email info@timusco.com.

| Host | Loại | Giá trị |
|---|---|---|
| @ | A | 185.199.108.153 |
| @ | A | 185.199.109.153 |
| @ | A | 185.199.110.153 |
| @ | A | 185.199.111.153 |
| @ | AAAA | 2606:50c0:8000::153 |
| @ | AAAA | 2606:50c0:8001::153 |
| @ | AAAA | 2606:50c0:8002::153 |
| @ | AAAA | 2606:50c0:8003::153 |
| www | CNAME | dinhhuy1405.github.io |

Nếu Squarespace đang có sẵn bản ghi A hoặc CNAME `www` mặc định (trang đỗ tên miền của Squarespace) thì xoá các bản ghi web đó trước, giữ nguyên bản ghi email. DNS thường chạy sau vài phút đến vài giờ.
