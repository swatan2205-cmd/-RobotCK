# Thiết kế đánh giá đã công bố

Thời lượng yêu cầu 44 s, Ts=0.15 s. Dùng N=ceil(44/0.15)=294 bước để mỗi bước đủ Ts; khoảng đánh giá thực tế [0,44.1] s, 295 trạng thái. Lần tái lập dùng đúng chiều dài mẫu gốc, không đổi thành 44.1 s.

Hai quỹ đạo theo docs/theory.md; robot theo repo, b=0.1 m, 700 tập mở rộng ngoài terminal. Giới hạn từng bánh là 8, 10, 12 rad/s. Mức 8 cố ý khảo sát giới hạn khi tập điều khiển bảo thủ không bao phủ nhiễu tham chiếu số 8. Không coi lỗi kiểm tra điều kiện là phản ví dụ định lý.

Điều kiện đầu q0=q_r(0)+offset, giữ cùng offset khi đổi giới hạn. Nhãn nhỏ/vừa/lớn mô tả đồng thời sai lệch vị trí và hướng, không cô lập riêng hai thành phần.

| Mức | offset x m | offset y m | offset hướng rad |
|---|---|---|---|
| 1 | 0.05 | 0 | pi/12 |
| 2 | 0.30 | 0 | pi/3 |
| 3 | 0.60 | 0 | pi |

Với số 8 q_r(0)=[0,0,atan(0.5)]ᵀ; với tròn q_r(0)=[0.6,0,pi/2]ᵀ. Giá trị đầy đủ và số thực chính xác được lưu trong config của từng run.mat/summary.json; không dùng q0 gốc [0.6,0,pi] cho mọi mức đánh giá.

Hiệu chỉnh riêng: hai quỹ đạo, 22 s, offset [0.15,-0.075,pi/6]ᵀ và [0.45,-0.225,pi/6]ᵀ, Omega=10. Tìm 216 cấu hình: k,kx,ks∈{0.5,1,2}, a∈{2.1,7}, n∈{-1,0,1,2}. Chọn tổng RMSE bốn ca nhỏ nhất, đồng hạng giữ cấu hình xuất hiện trước. Dùng nghiệm tích phân chính xác dưới lệnh giữ hằng, đã kiểm tra với ode45. Không dùng kết quả 36 ca để chọn gain. Đây là tối ưu trên lưới công bố, không phải thông số tối ưu toàn cục; góc pi nằm ngoài góc hiệu chỉnh và là phép thử khó.

Thời gian: warm-up 10 bước mỗi cấu hình rồi chạy năm lần; không dùng vẽ/pause/xuất tệp trong đoạn đo. Đo từ trước tính sai số/ràng buộc đến sau chuyển bánh; tích phân robot và I/O nằm ngoài. Lưu từng lần, xuất mean/p95/max/số vượt Ts; các lần lặp xác định không tạo bằng chứng thống kê về nhiễu. Chiến dịch chính chạy sau khi hoàn tất tác vụ MATLAB khác; tải hệ điều hành vẫn có thể thay đổi.

Dung sai: kiểm tra dư ràng buộc chuẩn hóa 1e-7; kiểm tra bánh dùng 1e-7 rad/s; thành viên tập dùng biên bán kính 1e-9 m. Bộ giải validated dùng ConstraintTolerance=1e-9, OptimalityTolerance=1e-9; fmincon thêm StepTolerance=1e-12 và tối đa 2000 đánh giá. ODE RelTol=1e-8, AbsTol=1e-10. Đây là thiết lập số để hạn chế nghiệm sát biên bị loại sai và hỗ trợ tái lập, không phải ngưỡng chất lượng bám mong muốn.

Không có fallback. Ca không hợp lệ dừng, giữ lỗi và completedSteps. Không tính RMSE/IAE toàn khoảng cho lượt thiếu mẫu; NaN ở bảng tổng hợp được giữ nguyên. Mỗi cặp so sánh định lượng chỉ dùng hai ca hoàn thành cùng cấu hình.
