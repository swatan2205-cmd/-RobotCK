# Bài toán và mục tiêu kiểm chứng

Xét một robot hai bánh vi sai, trạng thái q=[x,y,theta]ᵀ, đầu vào vận tốc góc bánh [omega_R,omega_L]ᵀ. Thiết kế và đánh giá điều khiển bám tham chiếu q_r(t) có thời gian xác định, dưới ràng buộc từng bánh |omega|≤Omega. Đây là bám quỹ đạo theo thời gian: cùng vị trí trên đường nhưng đến sai thời điểm vẫn tạo sai số.

Giả thiết: mặt phẳng, không trượt, biết trạng thái, mô hình động học, vận tốc bánh được áp dụng tức thời và giữ hằng trong chu kỳ. Chưa xét động cơ, encoder, nhiễu, truyền thông, va chạm hoặc tiêu thụ năng lượng.

| Mục tiêu | Phép thử | Chỉ số | Minh chứng |
|---|---|---|---|
| Tái lập có kiểm chứng | Chạy nguyên bản rồi bản sửa tương thích | Trạng thái, lệnh, lỗi, sai khác | results/baseline*, original/repaired |
| Triển khai đúng mô hình và điều khiển | Kiểm tra độc lập, đối chiếu công thức | Đạo hàm, dấu quay, dư ràng buộc | tests, docs/theory.md |
| So sánh công bằng | 36 cấu hình chung, hiệu chỉnh riêng | RMSE, IAE, max, bão hòa, biến thiên, thời gian | results, tables/summary.csv |
| Làm rõ giới hạn | Điều kiện tập và ca bất lợi | Nhãn khả thi, lỗi, sai số phía trước | run.mat, báo cáo |
| Tái tạo báo cáo từ dữ liệu | Xuất lại không chạy controller | Số liệu và hình khớp nguồn | export_results, report |

Không đặt điều kiện T-ST-RHC phải tốt hơn mọi ca. Mức hoàn thành căn cứ bằng chứng và tính đúng đắn, không căn cứ hình quỹ đạo đẹp hoặc số trang.
