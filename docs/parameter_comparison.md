# Đối chiếu cấu hình repo và thực nghiệm bài báo

Nguồn repo: script chính tại commit c57e98262ff21d8bab711b892a14c7afc98e0c08. Nguồn bài báo: Mục IV, đoạn thiết lập và thuật toán của PDF cung cấp. Giữ các giá trị khác nhau như các cấu hình khác nhau; không tự sửa khoảng cách hai bánh để khớp số liệu thực nghiệm.

| Đại lượng | Mô phỏng repo | Thực nghiệm bài báo | Quyết định dự án |
|---|---|---|---|
| Bán kính bánh | r=0.0205 m | R=0.021 m | Giữ repo cho baseline và 36 ca |
| Khoảng cách hai bánh trong T | d=0.053 m | D=0.1047 m | Không nhân/chia hai nếu chưa có nguồn giải thích ký hiệu |
| Điểm phía trước | b=0.1 m | Không tìm thấy giá trị b tường minh trong đoạn thiết lập | Không tự suy ra và gán cho bài báo |
| Chu kỳ | 0.15 s | 0.15 s | Giữ chung |
| Giới hạn góc bánh | 10 rad/s | 10 rad/s | Baseline 10; đánh giá 8/10/12 |
| Tham chiếu số 8 | 0.6 sin(t/3.5), 0.6 sin(t/7) | Cùng công thức | Giữ cùng luật thời gian |
| Trạng thái đầu | [0.6,0,pi]ᵀ | [0.6,0,pi]ᵀ | Chỉ baseline dùng giá trị này; đánh giá theo offset công bố |
| Thời gian | Lưới 0:0.15:(4pi*3.5−0.15); 293 lệnh | Công bố kf=44 s | Baseline giữ 293 bước; đánh giá 294 bước tới 44.1 s |
| Tập mở rộng | Nsets=700, cộng terminal | N=396 theo đoạn thực nghiệm | Giữ 700; không nhầm index MATLAB 1 với chỉ số terminal 0 |
| Hàm mục tiêu pha ngoài | ||e+Ts*u_hat||², Rd=0 | ||e+Ts*u−Ts*ur||²+0.5||u||² | Giữ repo; không nhận là tái tạo chính xác mục tiêu thực nghiệm |
| Pha cuối | QP chiếu tham chiếu lên lệnh hợp lệ | Bài toán (27) | Cùng cấu trúc; log exitflag và dư riêng |
| Bộ giải | fmincon, quadprog | fmincon, quadprog | Không thay bằng solver khác |
| Cập nhật robot | ode45, lệnh giữ hằng, lưới đầu ra 1e-5 | Robot thật, encoder/odometry | Mô phỏng không đại diện sai số đo và truyền thông |
| MATLAB | README ghi R2022a | Mục IV ghi R2022b | Môi trường tự chạy R2023a, có bản sửa tương thích công bố |

Bài báo công bố bán kính tập nhiễu 0.0287 và miền điều khiển 0.1982. Không dùng hai con số này để âm thầm thay thế bán kính tính từ cấu hình robot hiện tại. Mọi kiểm tra khả thi của dự án tính lại từ cấu hình và tham chiếu thực sự được lưu.
