# Nhật ký triển khai ngày 16 tháng 11 năm 2026

## Mốc 1 và 2

Đã đọc AGENTS gốc và trong mã tác giả, toàn bộ rubric Word, bài báo chính và nguồn Blažič đầy đủ. Đã lập bài toán, quy ước, đối chiếu công thức–mã, hồ sơ nguồn và thiết kế đánh giá. Nguồn có commit bất biến và kiểm tra byte mã cung cấp.

## Mốc 3

MATLAB R2023a chạy được, Optimization Toolbox khả dụng. Thiết lập ET/MPT3 trong dự án, không thay startup. Hai lần lỗi nền được giữ: chưa trỏ đúng lớp ET; sau đó lỗi SData trong hàm vẽ ET. Tạo original/repaired bỏ plot(ell_d), giữ mã điều khiển nguyên vẹn. Bản nền hoàn thành. MPT3 cần adapter linprog cho MATLAB hiện hành; ET dùng cấu hình công khai và jar, không gọi chức năng CVX không sử dụng.

## Mốc 4 và 5

Đã tách pipeline mô phỏng và dữ liệu. So cấu trúc bằng thiết lập tác giả đạt sai khác trạng thái khoảng 3.97e-8, bánh 1.28e-6 rad/s. Profile validated có khác biệt lớn hơn ngưỡng baseline và được công bố riêng. Đối chứng dùng Blažič (18), có kiểm tra dV trước bão hòa. Hiệu chỉnh 216 cấu hình trên bốn ca riêng, chọn k=2, kx=0.5, ks=0.5, a=2.1, n=2.

## Mốc 6

Giữ kết quả khảo sát ban đầu trong results/pilot. Sau khi khóa thông số, chạy chiến dịch chính riêng: 36 cấu hình, 33 hoàn thành và 3 dừng kiểm tra điều kiện. Lặp năm lần sau warm-up; dữ liệu lặp xác định nhất quán. Tám nhóm kiểm tra MATLAB đạt. Bốn ca mức đầu vừa cho ode45 gần nghiệm chính xác. Ba ca tròn đầu lớn có kiểm tra riêng: chênh lệch mô hình thiết kế giải thích phần lớn sai số cao; cùng RMSE gần nhau không bảo đảm khớp từng mẫu.

## Mốc 7

Đã tạo báo cáo từ dữ liệu, hình có run_id và nguồn, bảng toàn bộ ca. Trình render_docx.py đóng gói không tìm thấy LibreOffice trên Windows; dùng Microsoft Word xuất PDF, Poppler tạo ảnh để rà soát toàn bộ trang. Trạng thái QA và đóng gói cuối cùng được ghi tại docs/delivery_audit.json.

## Giới hạn giữ nguyên

Cận tham chiếu là kiểm tra số; không gọi đây là chứng minh cận liên tục. Không kéo bảo đảm định lý sang mô hình giữ lệnh; không kéo chứng minh Lyapunov sang luật bão hòa. Không có nhiễu/robot thật. Không kết luận điểm số hoặc ưu thế tổng quát.
