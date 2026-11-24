# Kế thừa và thay đổi

| Hạng mục | Kế thừa | Tự thực hiện và lý do | Kiểm chứng |
|---|---|---|---|
| Thuật toán chính | Tiriolo–Lucia, repo Apache-2.0 | Tách mô-đun, chuẩn hóa dữ liệu | compare_baseline |
| Bản nguyên gốc | 12 tệp trùng upstream; AGENTS.md là tệp hướng dẫn thêm | Giữ original/provided, SHA-256 | provided_manifest.json |
| Tương thích MPT3 | mpt_call_linprog | Bỏ đối số x0 cũ, options hiện hành; không đổi bài toán LP | Constructor và biến đổi Polyhedron trong baseline |
| Tương thích ET | Lớp ellipsoid và cấu hình công khai | Nạp jar và cấu hình; không gọi CVX cho chức năng không dùng | check_environment |
| Lệnh vẽ baseline | plot(ell_d) | Bỏ duy nhất lệnh này ở original/repaired vì nested variable SData không tương thích R2023a | Lỗi nguyên bản và chạy bản sửa |
| Bộ giải đánh giá | fmincon, quadprog | Lưu exitflag/iterations/residual; dùng dung sai tường minh | Kiểm tra nghiệm từng bước |
| Tập offline | Proposition 2 | Tính bán kính cầu trực tiếp, cận tham chiếu lưới dày có biên | Kiểm tra bán kính; không mở rộng ellipsoid tổng quát |
| Tham chiếu | Số 8 tác giả | unwrap tổng quát, đường tròn, đạo hàm giải tích | Kiểm tra đạo hàm và hướng |
| Đối chứng | Blažič (18) | Chuyển lệnh bánh, bão hòa, lưới hiệu chỉnh riêng | dV và kiểm tra bão hòa |
| Đánh giá | Quy tắc AGENTS.md | 36 ca, đo thời gian, chỉ số, lưu lỗi và xuất hình | Dữ liệu tự chạy |
| Báo cáo | Tài liệu nguồn và rubric | Tổng hợp, phân tích nguyên nhân và giới hạn | Hồ sơ rubric |

Mã bản sửa chỉ phục vụ tương thích được tách khỏi mở rộng và hệ thống đánh giá. Mô hình vật lý không được đổi để tạo kết quả tốt hơn. Hàm mục tiêu repo không có thành phần phạt nỗ lực 0.5||u||² như thực nghiệm trong bài báo; đánh giá chính giữ mục tiêu repo và công bố khác biệt này.

AI hỗ trợ phân tích tài liệu, viết mã, chạy công cụ, tổ chức bằng chứng và soạn thảo. Không gán các thao tác này thành đóng góp độc lập của người học; người học chịu trách nhiệm kiểm tra và tuân thủ quy định học phần.
