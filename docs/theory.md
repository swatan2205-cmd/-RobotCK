# Mô hình và liên hệ lý thuyết với mã

## Động học và dấu

T=[r/2,r/2; r/d,-r/d], [v;omega]=T[omega_R;omega_L]. d là khoảng cách hai bánh theo đúng công thức mã; chưa đồng nhất giá trị 0.053 của repo với 0.1047 của thực nghiệm bài báo. Hai bánh cùng chiều cùng tốc độ tạo chuyển động thẳng; bánh phải nhanh hơn tạo quay dương.

dx/dt=v cos(theta), dy/dt=v sin(theta), dtheta/dt=omega. Đơn vị x,y,r,d,b là m; theta là rad; v là m/s; omega và vận tốc góc bánh là rad/s.

## Tham chiếu

v_r=sqrt(dx_r²+dy_r²); omega_r=(dx_r ddy_r-dy_r ddx_r)/(dx_r²+dy_r²); theta_r=unwrap(atan2(dy_r,dx_r)). Điều kiện tốc độ khác không được kiểm tra; không điền tùy ý hướng tại điểm kỳ dị. Sai số hướng dùng atan2(sin(theta-theta_r),cos(theta-theta_r)).

Số 8: x_r=0.6 sin(t/3.5), y_r=0.6 sin(t/7). Tròn: x_r=0.6 cos(t/7), y_r=0.6 sin(t/7). Đạo hàm giải tích nằm trong make_reference; hai quỹ đạo giữ nguyên khi thay giới hạn bánh.

## Điểm phía trước và T-ST-RHC

z=[x+b cos(theta);y+b sin(theta)], b>0. T_FL=[cos(theta),sin(theta);-sin(theta)/b,cos(theta)/b], [v;omega]=T_FL u. Khi b=0 phép nghịch đảo suy biến. Trong mô hình thiết kế z(k+1)=z(k)+Ts u(k). e=z-z_r, u_r=T_FL(theta_r)^(-1)[v_r;omega_r], e(k+1)=e(k)+Ts(u-u_r). Dấu này nhất quán với mã; sai số của đối chứng có dấu ngược và hệ tọa độ khác.

Đặt rho=max ||u_r||, ru=2 Omega r b/sqrt(4b²+d²). Điều kiện thiết kế rho<ru. Nhiễu theo bài báo là -Ts*u_r nên bán kính tập D=Ts*rho. Terminal T0 là cầu bán kính r0=Ts*rho; r_i=r_(i-1)+Ts*(ru-rho). Công thức chỉ dùng vì A=I, B=Ts I và các tập là cầu đồng tâm. Không dùng sqrt phần tử hoặc so sánh từng phần tử để kết luận thứ tự ma trận tổng quát.

rho trong đánh giá được ước lượng bằng lưới dày ít nhất 20001 điểm, cộng biên tương đối 1e-6. Đây là kiểm tra số trên quỹ đạo hữu hạn, không phải chứng minh cận giải tích liên tục. Nhãn within_design_conditions có nghĩa vượt qua các phép kiểm tra thiết kế số; không khẳng định định lý tự động đúng cho mô hình robot tích phân liên tục.

Online chọn i nhỏ nhất chứa e. Với i>0, tìm u_hat tối thiểu ||e+Ts*u_hat||², thỏa H(u_hat+u_r)≤1 và (e+Ts*u_hat)ᵀQ_(i-1)^(-1)(e+Ts*u_hat)≤1; áp dụng u=u_hat+u_r. Với i=0, u0=-e/Ts; QP chọn u_r_hat gần u_r nhất sao cho H(u0+u_r_hat)≤1. H=Hd*T^(-1)*T_FL(theta). Chuyển ngược sang vận tốc bánh bằng T^(-1)*T_FL*u.

Theo [1], tính khả thi đệ quy và bị chặn cuối cùng đòi hỏi giả thiết tập, sai số đầu trong miền thu hút và mô hình thiết kế. Bị chặn trong tập cuối không đồng nghĩa sai số tâm/hướng hội tụ chính xác về 0. Đặc biệt e phía trước nhỏ không buộc sai số tâm nhỏ khi hướng lệch lớn: p-p_r=e-b(h(theta)-h(theta_r)), nên ||p-p_r||≤||e||+2b. Cần phân tích cả hai sai số.

Mô hình cập nhật z tuyến tính là mô hình thiết kế; robot thực thi trong mô phỏng dùng ode45 dưới lệnh bánh giữ hằng. Khi theta thay đổi trong bước, cập nhật điểm z không trùng chính xác mô hình tuyến tính. Tính khả thi số và độ nhạy tích phân được đánh giá riêng, không dùng kết quả mô phỏng để tuyên bố mở rộng định lý.

## Đối chứng Blažič

Theo [2], phương trình (10), (14), (18): ex=cos(theta)(xr-x)+sin(theta)(yr-y), ey=-sin(theta)(xr-x)+cos(theta)(yr-y); es=sin(theta_r-theta), ec=cos(theta_r-theta)-1, h=1+ec/a, a>2.

v=v_r*cos(theta_r-theta)+kx*ex; omega=omega_r+k*v_r*ey*h²+ks*es*h^(2n), với k,kx,ks>0, n nguyên. V=k(ex²+ey²)/2+(es²+ec²)/(2h). Trong mô hình liên tục không bão hòa, dV/dt=-k*kx*ex²-ks*es²*h^(2n-2)≤0. Giả thiết kích thích của v_r hoặc omega_r, tính liên tục và điều kiện hướng trong chứng minh cần được giữ khi diễn giải hội tụ; dV≤0 một mình chưa đủ chứng minh toàn bộ trạng thái hội tụ.

Triển khai đổi [v;omega] sang bánh rồi giới hạn độc lập từng bánh. Khi bão hòa hoặc lấy mẫu, đẳng thức dV gốc không tự động giữ; báo cáo chỉ so sánh hành vi thực nghiệm của bản này. Kiểm tra đạo hàm Lyapunov dùng lệnh yêu cầu chưa bão hòa.

## Đối chiếu

| Nội dung | T-ST-RHC | Blažič có bão hòa |
|---|---|---|
| Sai số thiết kế | Điểm phía trước, tọa độ toàn cục | ex,ey cục bộ; sin/cos hướng |
| Ràng buộc bánh | Đưa vào bài toán tối ưu | Cắt độc lập sau luật |
| Tính toán | Chuẩn bị tập, tìm tập, QCQP/QP | Công thức tường minh |
| Bảo đảm nguồn | Bị chặn, có giả thiết tập và mô hình | Chứng minh gốc liên tục không bão hòa |
| Giới hạn đánh giá | Sai khác rời rạc/liên tục, cận số rho | Bão hòa, lấy mẫu, miền hiệu chỉnh |

| Công thức | Ý nghĩa | Hàm | Kiểm tra |
|---|---|---|---|
| T và nghịch đảo | Hai bánh sang robot | wheel_to_body, body_to_wheel | chuyển động thẳng/quay |
| Đạo hàm và hướng | Tham chiếu có thời gian | make_reference | sai phân tâm và qua biên góc |
| r_i, Q_i | Miền thu hút | prepare_sets | dương, tăng, bán kính một bước |
| Hai chế độ | Lệnh hợp ràng buộc | controller_step | exitflag, hữu hạn, dư |
| Blažič (18) | Đối chứng | controller_step | đẳng thức dV, bão hòa |
| Động học giữ lệnh | Robot mô phỏng | integrate_robot | ode45 so nghiệm chính xác |
| RMSE và IAE | Đánh giá hậu nghiệm | compute_metrics | sai số 3–4–5 biết trước |
