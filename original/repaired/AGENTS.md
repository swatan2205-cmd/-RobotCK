# AGENTS.md

## Mục tiêu dự án

Đây là repo MATLAB mô phỏng và kiểm chứng bộ điều khiển bám quỹ đạo kiểu T-ST-RHC cho robot di động hai bánh vi sai. Mục tiêu chính là tái lập, hiểu và mở rộng thuật toán trong bài báo:

- C. Tiriolo, W. Lucia, "A Set-Theoretic Control Approach to the Trajectory Tracking Problem for Input–Output Linearized Wheeled Mobile Robots", IEEE Control Systems Letters, 2023.
- Mã trong repo dùng để mô phỏng và kiểm chứng trên robot thật Khepera IV.

AI agent làm việc trong repo này phải luôn giữ đúng phạm vi kỹ thuật của bài toán: robot di động vi sai, điều khiển bám quỹ đạo theo thời gian, ràng buộc đầu vào, tập khả dụng/miền thu hút, và mô phỏng MATLAB.

## Bắt đầu làm việc

1. Đọc trước [README.md](./README.md) để hiểu mục tiêu, phụ thuộc và cách chạy.
2. Đọc script chính [ST_FL_Trajectory_Tracking_Differential_Drive_CDC23.m](./ST_FL_Trajectory_Tracking_Differential_Drive_CDC23.m) trước khi sửa logic điều khiển hoặc tham số mô phỏng.
3. Khi cần sửa logic tối ưu hoặc tập, đọc lần lượt các file liên quan:
   - [one_step_ellipsoidal_reachable_set.m](./one_step_ellipsoidal_reachable_set.m)
   - [online_phase_CDC.m](./online_phase_CDC.m)
   - [online_terminal_optim_QP.m](./online_terminal_optim_QP.m)
   - [DiffDrive.m](./DiffDrive.m)
4. Nếu làm phần thực nghiệm robot Khepera IV, đọc thư mục [Khepera_IV_TCP](./Khepera_IV_TCP) và script chính trong đó.

## Cấu trúc repo quan trọng

- [ST_FL_Trajectory_Tracking_Differential_Drive_CDC23.m](./ST_FL_Trajectory_Tracking_Differential_Drive_CDC23.m): script mô phỏng chính, xây dựng quỹ đạo tham chiếu, tập khả thi, vòng online optimization.
- [one_step_ellipsoidal_reachable_set.m](./one_step_ellipsoidal_reachable_set.m): tính tập tiếp cận một bước theo mô hình ellipsoid.
- [online_phase_CDC.m](./online_phase_CDC.m): tối ưu hóa online ở pha điều khiển, dùng fmincon và ràng buộc dựa trên tập đi trước.
- [online_terminal_optim_QP.m](./online_terminal_optim_QP.m): bài toán QP cuối cùng để tìm đầu vào tiếp theo/điều chỉnh lệnh bánh.
- [DiffDrive.m](./DiffDrive.m): mô hình động học robot vi sai, dùng trong ode45.
- [Khepera_IV_TCP](./Khepera_IV_TCP): mô phỏng/kiểm chứng trên robot Khepera IV, bao gồm giao tiếp Bluetooth và tham số điều khiển.

## Quy tắc làm việc của agent

- Giữ nguyên mã gốc khi chưa cần sửa; sửa theo kiểu cục bộ, không “đóng gói lại” toàn bộ script nếu chỉ cần thay đổi một hàm.
- Không suy đoán các tham số từ bài báo mà không đối chiếu với mã hiện có; khi đổi `Ts`, `r`, `d`, `b`, giới hạn bánh, quỹ đạo tham chiếu, phải kiểm tra ảnh hưởng đến tập và điều kiện ràng buộc.
- Luôn phân biệt giữa:
  - mục tiêu điều khiển (bám quỹ đạo),
  - hàm mục tiêu tối ưu hóa,
  - chỉ số đánh giá sau mô phỏng.
- Không tự gán kết quả “đúng” nếu chưa có xác nhận bằng MATLAB trên môi trường này. Nếu không có MATLAB hoặc toolbox cần thiết, phải ghi rõ rằng chưa chạy xác nhận trên MATLAB.
- Không bịa dữ liệu, không giả lập khung thời gian, log, hoặc số liệu và không viết kết luận vượt quá bằng chứng thực tế.
- Nếu sửa mục tiêu tối ưu hoặc ràng buộc, phải kiểm tra lại: kích thước ma trận, tính xác định dương, cận trên/dưới, và nghiệm tối ưu có hợp lệ không.

## Giới hạn kỹ thuật cần tuân theo

- Dự án hoạt động theo mô hình differential-drive, không phải robot kinh điển 3-DOF tổng quát.
- Vận tốc bánh `omega_L`, `omega_R` là biến điều khiển chính; các biến chuyển đổi sang vận tốc tiến/quay là phần cần giữ đúng dấu và đơn vị.
- Quỹ đạo tham chiếu là quỹ đạo theo thời gian, không chỉ là đường hình học: các thành phần `xr`, `yr`, `thetar` và đạo hàm phải tương thích.
- Về bộ điều khiển: thuật toán là set-theoretic receding-horizon, nên các tập `Q_k`, `Qpre`, `U_curr`, `U_uni` phải được tính/giữ cùng cấu trúc mà script đang dùng.
- Khi làm việc với `fmincon` / `quadprog`, phải giữ các options và ràng buộc hợp lệ, tránh “cắt dữ liệu” để qua điều kiện ràng buộc mà không ghi nhận.

## Hướng dẫn thay đổi code

### Nếu sửa mô hình hoặc tham số robot
- Kiểm tra các dòng quan trọng trong script chính như:
  - `Ts`, `r`, `d`, `b`, `wrlmax`
  - `eta`, `alpha`, quỹ đạo `xr`, `yr`, `thetar`
  - `Qd`, `Qu`, `U_dd`, `U_uni`
- Sau khi đổi, phải tính lại tập ở offline phase, vì comment trong script ghi rõ: nếu thay đổi hệ thống, ràng buộc hoặc nhiễu thì các phần offline phải được tính lại.

### Nếu sửa logic offline set computation
- Đọc [one_step_ellipsoidal_reachable_set.m](./one_step_ellipsoidal_reachable_set.m) và xác nhận ảnh hưởng lên khối:
  - `Q0`, `Qcurr`, `Q_k`
  - tính toán một bước reachable set
  - cấu trúc ellipsoid và đối chiếu với `Qd`

### Nếu sửa online optimization
- Đọc [online_phase_CDC.m](./online_phase_CDC.m) và [online_terminal_optim_QP.m](./online_terminal_optim_QP.m).
- Kiểm tra lại:
  - biến `x_curr`, `Qpre`, `A`, `B`, `H`, `g`, `ur`, `u_pre`
  - hàm mục tiêu và ràng buộc
  - dấu và phần tử trong ma trận chuyển đổi
  - `exitflag`/điều kiện lỗi nếu solver không tìm được nghiệm

### Nếu sửa phần thực nghiệm Khepera IV
- Chỉ sửa sau khi đã đọc [Khepera_IV_TCP/Khepera_iv_ST_disturbance_traj_track.m](./Khepera_IV_TCP/Khepera_iv_ST_disturbance_traj_track.m) và các file liên quan.
- Không giả định rằng robot thật là một bản sao của mô phỏng; phần thực nghiệm có yêu cầu cổng Bluetooth, server trên robot và cấu hình port cụ thể.

## Kiểm tra hợp lệ trước khi kết luận

Agent chỉ được xác nhận sửa code nếu đã thực hiện một trong các cách sau:

- Chạy script MATLAB chính (nếu môi trường có MATLAB và toolbox cần thiết), hoặc
- Đọc và kiểm tra chặt chẽ chỗ sửa, ghi rõ là chưa chạy trên MATLAB do thiếu môi trường/toolbox, và không kết luận là “đã hoạt động”.

Các kiểm tra quan trọng:

- Đảm bảo hàm chuyển đổi vận tốc bánh ↔ vận tốc robot và dấu quay là nhất quán.
- Kiểm tra quỹ đạo tham chiếu và đạo hàm, đặc biệt `thetar` và góc đi qua biên ±π.
- Kiểm tra cấu trúc ma trận/dạng tập và độ xác định dương khi thực hiện với ellipsoid/Polyhedron.
- Kiểm tra nghiệm tối ưu hợp lệ: hữu hạn, không NaN/Inf, và tuân ràng buộc với dung sai hợp lý.
- Không che lỗi bằng cách cắt đầu vào hoặc ép lệnh điều khiển mà không ghi nhận.

## Môi trường và phụ thuộc

- Môi trường được repo ghi nhận là MATLAB 2022a.
- Cần có Ellipsoidal Toolbox ET và các công cụ tối ưu tương ứng như `fmincon`, `quadprog`.
- Nếu làm việc ngoài môi trường chạy MATLAB, hãy coi đó là giai đoạn chuẩn bị và không kết luận là đã xác thực trên MATLAB.

## Kết luận và ghi nhớ

Đây là repo nghiên cứu/kiểm chứng thuật toán điều khiển, không phải repo ứng dụng sản phẩm. Cần ưu tiên:

- độ đúng của mô hình,
- tính nhất quán giữa lý thuyết, mã và quỹ đạo tham chiếu,
- bằng chứng thực tế thay vì khẳng định từ mặt hình thức.

Mọi thay đổi lớn nên được mô tả rõ ràng: mục tiêu, ảnh hưởng, cách kiểm chứng, và trạng thái xác nhận MATLAB.
