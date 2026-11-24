# Phân tích kết quả tự chạy

Chiến dịch gồm 36 cấu hình, 33 lượt hoàn thành và 3 lượt dừng do kiểm tra điều kiện. Mỗi cấu hình được đo năm lần sau warm-up; đây là các lần chạy xác định phục vụ đo thời gian.

Với quỹ đạo eight, T-ST-RHC có RMSE nhỏ hơn đối chứng trong 6/6 cặp hoàn thành. Kết luận chỉ áp dụng cho cấu hình, hàm mục tiêu repo và lưới hiệu chỉnh đã công bố; các ca không chạy được không được tính thành chiến thắng cho phương pháp nào.

Với quỹ đạo circle, T-ST-RHC có RMSE nhỏ hơn đối chứng trong 7/9 cặp hoàn thành. Kết luận chỉ áp dụng cho cấu hình, hàm mục tiêu repo và lưới hiệu chỉnh đã công bố; các ca không chạy được không được tính thành chiến thắng cho phương pháp nào.

Ca circle_i3_w10_tstrhc có RMSE 1.33 m, trong khi cùng trạng thái đầu tại 8 rad/s là 0.1265 m. Tăng giới hạn vận tốc không bảo đảm giảm sai số. Việc tăng miền lệnh thay đổi nghiệm và chuyển động quay trong một chu kỳ; cần đọc đồng thời sai số phía trước, chỉ số tập và phần dư mô hình trước khi suy luận nguyên nhân.

circle_i3_w8_tstrhc: sai số phía trước lớn nhất 0.6325 m; phần dư tuyến tính hóa lớn nhất 0.04207 m/bước; số lần chỉ số tập tăng 0. Đây là chẩn đoán trên mô hình giữ lệnh thực thi, không phải bằng chứng định lý của mô hình thiết kế đã được áp dụng chính xác.

circle_i3_w10_tstrhc: sai số phía trước lớn nhất 1.736 m; phần dư tuyến tính hóa lớn nhất 0.06484 m/bước; số lần chỉ số tập tăng 126. Đây là chẩn đoán trên mô hình giữ lệnh thực thi, không phải bằng chứng định lý của mô hình thiết kế đã được áp dụng chính xác.

circle_i3_w12_tstrhc: sai số phía trước lớn nhất 1.742 m; phần dư tuyến tính hóa lớn nhất 0.09184 m/bước; số lần chỉ số tập tăng 132. Đây là chẩn đoán trên mô hình giữ lệnh thực thi, không phải bằng chứng định lý của mô hình thiết kế đã được áp dụng chính xác.

Phép đối chiếu circle_i3_w8_tstrhc: RMSE robot ode45 0.1265 m, nghiệm giữ lệnh chính xác 0.1265 m, còn mô hình z tuyến tính kèm cập nhật hướng cho 0.1175 m. Chỉ số tập tăng 0 lần ở robot và 0 lần ở mô hình thiết kế. Phần dư lấy mẫu tham chiếu tối đa 0.0001397 m/bước. Max sai khác thành phần trạng thái ode45 so nghiệm chính xác là 0.0008334, theo đơn vị m hoặc rad của thành phần tương ứng.

Phép đối chiếu circle_i3_w10_tstrhc: RMSE robot ode45 1.33 m, nghiệm giữ lệnh chính xác 1.33 m, còn mô hình z tuyến tính kèm cập nhật hướng cho 0.07898 m. Chỉ số tập tăng 126 lần ở robot và 0 lần ở mô hình thiết kế. Phần dư lấy mẫu tham chiếu tối đa 0.0001397 m/bước. Max sai khác thành phần trạng thái ode45 so nghiệm chính xác là 0.1564, theo đơn vị m hoặc rad của thành phần tương ứng.

Phép đối chiếu circle_i3_w12_tstrhc: RMSE robot ode45 1.328 m, nghiệm giữ lệnh chính xác 1.328 m, còn mô hình z tuyến tính kèm cập nhật hướng cho 0.06828 m. Chỉ số tập tăng 132 lần ở robot và 0 lần ở mô hình thiết kế. Phần dư lấy mẫu tham chiếu tối đa 0.0001397 m/bước. Max sai khác thành phần trạng thái ode45 so nghiệm chính xác là 0.07919, theo đơn vị m hoặc rad của thành phần tương ứng.

Phép đối chiếu thay riêng cập nhật robot bằng cập nhật z của mô hình thiết kế, giữ cấu hình và bộ điều khiển. Kết quả hỗ trợ giải thích rằng chênh lệch mô hình giữ lệnh có vai trò lớn trong ca bất lợi; mô hình chẩn đoán này không thay thế robot trong 36 ca chính và không phải cải tiến thuật toán. Sai khác ode45 so nghiệm chính xác ở cùng ca giúp phân biệt lỗi tích phân với chênh lệch cấu trúc mô hình. Không giảm tốc tham chiếu hoặc loại ca bất lợi.

Ở ca đầu lớn, RMSE gần nhau giữa ode45 và nghiệm chính xác nhưng sai khác trạng thái tức thời có thể đáng kể, cho thấy tính nhạy của vòng kín với sai khác số. Vì vậy không kết luận hai diễn biến từng mẫu tương đương trên các ca này; kết quả kiểm tra rất nhỏ ở mức đầu vừa chỉ có phạm vi riêng.

Với số 8 ở 8 rad/s, bán kính miền điều khiển bảo thủ nhỏ hơn cận tham chiếu. T-ST-RHC chủ động dừng trước bước điều khiển; đây là không đáp ứng điều kiện của cách dựng tập đang dùng, không kết luận mọi bộ điều khiển đều không thể bám quỹ đạo này.

tstrhc: trung bình thời gian theo cấu hình hoàn thành 3.647 ms, cực đại mọi lần đo 115 ms; tổng bước vượt Ts là 0. Mức trung bình giữa cấu hình chỉ là mô tả chiến dịch; p95 và biến thiên từng cấu hình ở bảng thời gian. Không suy ra đáp ứng thời gian thực trên robot.

lyapunov: trung bình thời gian theo cấu hình hoàn thành 0.02658 ms, cực đại mọi lần đo 2.186 ms; tổng bước vượt Ts là 0. Mức trung bình giữa cấu hình chỉ là mô tả chiến dịch; p95 và biến thiên từng cấu hình ở bảng thời gian. Không suy ra đáp ứng thời gian thực trên robot.
