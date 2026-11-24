# AGENTS.md — Dự án cuối kỳ Kỹ thuật Robot

## 1. Mục đích và cách sử dụng

Tài liệu này hướng dẫn trợ lý AI và người thực hiện dự án:

**Mô phỏng và đánh giá điều khiển bám quỹ đạo robot di động hai bánh có giới hạn vận tốc bằng phương pháp T-ST-RHC trên MATLAB.**

Đặt tệp này tại thư mục gốc của dự án robot. Mọi đường dẫn bên dưới được tính từ thư mục gốc đó. Không mặc định sử dụng thư mục hoặc mã nguồn của dự án khác.

Mục tiêu chất lượng: có đủ bằng chứng đáp ứng mô tả **Xuất sắc (9–10)** của cả C1–C5 trong “RUBRIC ĐÁNH GIÁ BÁO CÁO CUỐI KỲ”, học phần Kỹ thuật Robot. Đây là tiêu chuẩn thực hiện và tự kiểm tra; không phải cam kết điểm số của giảng viên.

Nếu hướng dẫn hoặc rubric chính thức được cập nhật, đọc bản mới, ghi rõ thay đổi và điều chỉnh kế hoạch. Không tự ý mở rộng sang đề tài khác.

## 2. Phạm vi đã chốt

- Một robot di động hai bánh vi sai trên mặt phẳng, sử dụng mô hình động học.
- Điều khiển bám quỹ đạo **theo thời gian**; phân biệt với bài toán chỉ bám đường hình học.
- Phương pháp chính: T-ST-RHC, kế thừa bài báo và mã MATLAB của tác giả.
- Đối chứng: một luật điều khiển dựa trên Lyapunov, xác định rõ công thức, nguồn và cách xử lý bão hòa vận tốc bánh.
- Hai quỹ đạo chính: hình số 8 và đường tròn.
- Khảo sát sai lệch trạng thái ban đầu và giới hạn vận tốc góc hai bánh.
- Thực hiện hoàn toàn bằng mô phỏng MATLAB; không cần chế tạo robot.
- Giai đoạn cơ bản giả thiết bánh không trượt, biết trạng thái robot. Các giả thiết phải được ghi rõ trong báo cáo.
- Nhiễu, sai số mô hình và cải tiến thuật toán là phần mở rộng sau khi hoàn thành đối chứng và đánh giá cơ bản.

Đóng góp tự thực hiện: tái lập có kiểm chứng, xây dựng bộ đối chứng, tổ chức thử nghiệm, tự động hóa đo lường và phân tích kết quả. Không đặt điều kiện phải tốt hơn tác giả ở mọi tình huống.

## 3. Nguồn và khả năng truy xuất

Ưu tiên tài liệu gốc, bài báo học thuật và tài liệu chính thức:

1. C. Tiriolo, W. Lucia, “A Set-Theoretic Control Approach to the Trajectory Tracking Problem for Input–Output Linearized Wheeled Mobile Robots,” IEEE Control Systems Letters, 2023. DOI: https://doi.org/10.1109/LCSYS.2023.3286774
2. PDF tác giả: https://users.encs.concordia.ca/~wlucia/files/STMPC_tracking_robot2023.pdf
3. Repo: https://github.com/cristiri/T_ST_RHC_mobile_robots
4. Nguồn Lyapunov có thể nghiên cứu: S. Blažič, “A novel trajectory-tracking control law for wheeled mobile robots,” Robotics and Autonomous Systems, 2011. DOI: https://doi.org/10.1016/j.robot.2011.06.005
5. Tài liệu MATLAB cho `fmincon`, `quadprog`, `ode45`; tài liệu chính thức của Ellipsoidal Toolbox ET và MPT3.

Nguồn Lyapunov ở trên là ứng viên, chưa phải luật đã triển khai. Đọc đầy đủ công thức và điều kiện áp dụng trước khi chọn. Nếu chọn nguồn khác, giải thích lựa chọn và cập nhật hồ sơ nguồn.

Tạo `docs/references.md`: tác giả, tiêu đề, năm, DOI/URL, ngày truy cập thực tế, vai trò trong đề tài. Với repo, ghi commit/tag cụ thể; không ghi nhánh `main` thay cho phiên bản bất biến. Giữ giấy phép và thông tin tác giả khi tái sử dụng.

## 4. Ma trận yêu cầu rubric

Điểm tổng: `0.10*C1 + 0.20*C2 + 0.30*C3 + 0.25*C4 + 0.15*C5`.

| Tiêu chí | Yêu cầu hướng tới Xuất sắc | Bằng chứng bắt buộc của dự án |
| --- | --- | --- |
| C1 — 10% | Chủ đề đúng kỹ thuật robot; có ý nghĩa; vấn đề, mục tiêu kiểm chứng và phạm vi nhất quán | Phát biểu bài toán, giả thiết, đầu vào/đầu ra, mục tiêu gắn chỉ số và ma trận thử nghiệm |
| C2 — 20% | Nguồn đáng tin; giải thích nguyên lý đúng, sâu; tổng hợp/đối chiếu và liên hệ bài toán | Công thức có dẫn nguồn, bảng ký hiệu, phân tích giả thiết, so sánh tài liệu, liên hệ lý thuyết với mã |
| C3 — 30% | Phương pháp có lý giải; phân tích chuyên sâu; thông số và quy trình đủ để kiểm tra | Lưu đồ, thuật toán, bảng tham số có lý do, cấu hình tái lập, kiểm tra khả thi và log bộ giải |
| C4 — 25% | Kết quả có minh chứng; so sánh theo tiêu chí rõ; đánh giá ưu/nhược và giới hạn khách quan | Dữ liệu tự chạy, phép đo thống nhất, bảng so sánh, đồ thị, phân tích nguyên nhân và trường hợp thất bại |
| C5 — 15% | Bố cục logic; đánh số và dẫn chiếu chuẩn; nguồn nhất quán; rõ đóng góp | Báo cáo kiểm tra định dạng, danh mục nguồn, bảng kế thừa/tự làm, mã có hướng dẫn chạy |

Các số lượng thử nghiệm và sản phẩm quy định dưới đây là cách triển khai của dự án, không tự nhận là quy định nguyên văn của rubric. Chất lượng giải thích và kiểm chứng quan trọng hơn độ dài hoặc số hình.

## 5. Quy tắc làm việc của trợ lý

- Giao tiếp và giải thích bằng tiếng Việt, ngắn gọn, logic, dễ hiểu; giải thích ý nghĩa trước khi đưa ví dụ.
- Đọc mã và tài liệu hiện có trước khi sửa. Bảo toàn nội dung người dùng đã làm và bản mã gốc.
- Thực hiện công việc trong phạm vi đã được giao; chỉ hỏi khi thiếu thông tin làm thay đổi đáng kể lựa chọn kỹ thuật.
- Với việc phụ thuộc môi trường máy người dùng, yêu cầu đúng đầu ra cần thiết; không giả định đã cài MATLAB hoặc toolbox.
- Sau mỗi mốc: nêu đã làm gì, bằng chứng ở đâu, điểm chưa kiểm chứng và bước tiếp theo.
- Không bịa dữ liệu, nguồn, kết quả mô phỏng, thông số máy, commit hoặc trạng thái đã chạy.
- Nếu không có MATLAB, có thể đọc mã và chuẩn bị chương trình nhưng phải ghi **chưa chạy xác nhận trên MATLAB**. Không coi kiểm tra tĩnh hoặc chạy ở môi trường khác là xác nhận MATLAB.
- Không tự tạo kết quả đẹp, bỏ ca bất lợi, thay dữ liệu hoặc ngầm sửa điều kiện để đạt kết luận mong muốn.
- Phân biệt: kết quả gốc của tác giả; kết quả nhóm tự tái lập; kết quả đối chứng/mở rộng.
- Mỗi thay đổi thuật toán, bộ giải hoặc mô hình phải có lý do, ảnh hưởng dự kiến và phép kiểm chứng.
- Không đánh dấu hoàn thành bằng kế hoạch, mã chưa chạy hoặc ảnh minh họa không có dữ liệu tương ứng.

## 6. Tổ chức thư mục đề xuất

| Thư mục/tệp | Nội dung |
| --- | --- |
| `AGENTS.md` | Quy tắc thực hiện dự án |
| `README.md` | Môi trường, cài đặt, lệnh chạy và tái tạo kết quả |
| `original/` | Bản mã tác giả nguyên trạng, phiên bản và giấy phép |
| `src/` | Mô hình, quỹ đạo, bộ điều khiển, tính tập và chỉ số |
| `config/` | Cấu hình gốc và từng nhóm thử nghiệm |
| `scripts/` | Các lệnh chạy tái lập, chạy bộ thử nghiệm và xuất kết quả |
| `tests/` | Kiểm tra kỹ thuật có ý nghĩa |
| `results/<run_id>/` | Cấu hình, dữ liệu, log và trạng thái từng lượt chạy |
| `figures/`, `tables/` | Hình và bảng sinh tự động từ dữ liệu |
| `docs/` | Bài toán, công thức, nguồn, nhật ký, hồ sơ rubric và đóng góp |
| `report/` | Báo cáo, phụ lục và slide khi được yêu cầu |

Không tạo hàng loạt tệp rỗng chỉ để đủ danh mục. Dùng đường dẫn tương đối hoặc `fullfile`; tránh cố định đường dẫn máy cá nhân trong mã.

## 7. Trình tự thực hiện và điều kiện chuyển bước

### Mốc 1 — Chốt bài toán (C1)

- Viết `docs/problem_statement.md`: câu hỏi nghiên cứu, ý nghĩa kỹ thuật, trạng thái, đầu vào, tham chiếu, ràng buộc, giả thiết và phạm vi.
- Lập quan hệ `mục tiêu → phép thử → chỉ số → kết quả cần lưu`.
- Không tự đặt ngưỡng cải thiện phần trăm hoặc sai số tuyệt đối thiếu căn cứ. Nếu cần ngưỡng, công bố và lý giải trước khi đánh giá chính thức.
- Chuyển bước khi mọi mục tiêu đều có cách kiểm chứng và phạm vi thực hiện khả thi.

### Mốc 2 — Lý thuyết và đối chiếu nguồn (C2, C3)

- Phân tích động học; quan hệ vận tốc hai bánh với vận tốc tiến/quay; tạo tham chiếu từ vị trí và đạo hàm.
- Trình bày điểm điều khiển phía trước robot, vai trò `b > 0`, phép biến đổi đầu vào và sai số tương ứng.
- Giải thích miền cuối, tính bất biến, các tập điều khiển về đích, miền thu hút và thuật toán hai chế độ.
- Phát biểu điều kiện bảo đảm của bài báo; phân biệt sai số bị chặn với hội tụ chính xác về không.
- Đối chiếu ít nhất phương pháp chính và phương pháp đối chứng: giả thiết, xử lý ràng buộc, yêu cầu tính toán và giới hạn.
- Lập bảng `công thức/thuật toán → ý nghĩa → tệp/hàm → phép kiểm tra`; thống nhất dấu sai số và đơn vị.
- Chuyển bước khi giải thích được toàn bộ một bước điều khiển, từ trạng thái hiện tại đến lệnh hai bánh.

### Mốc 3 — Môi trường và tái lập nguyên bản (C3)

- Ghi phiên bản MATLAB, toolbox, hệ điều hành và cấu hình phần cứng thực tế.
- README gốc nêu MATLAB R2022a và Ellipsoidal Toolbox ET; kiểm tra thêm Optimization Toolbox (`fmincon`, `quadprog`) và MPT3 (`Polyhedron`) theo mã thực tế.
- Kiểm tra đúng lớp `ellipsoid` của thư viện cần dùng; không chỉ dựa vào việc trùng tên hàm.
- Các tệp chính: `ST_FL_Trajectory_Tracking_Differential_Drive_CDC23.m`, `DiffDrive.m`, `one_step_ellipsoidal_reachable_set.m`, `online_phase_CDC.m`, `online_terminal_optim_QP.m`.
- Lập bảng khác biệt giữa cấu hình mô phỏng repo và cấu hình thực nghiệm bài báo: kích thước robot, chu kỳ lấy mẫu, giới hạn bánh, quỹ đạo, tham số điều khiển, hàm mục tiêu và số tập.
- Đối chiếu định nghĩa khoảng cách hai bánh và ký hiệu trước khi sửa giá trị. Không ngầm đồng nhất tham số repo với bài báo.
- Chạy nguyên bản trước khi tái cấu trúc. Ghi mọi sửa chữa cần thiết để chạy được; giữ bản trước và sau sửa.
- Lưu dữ liệu, cấu hình, log và hình của lần chạy nền. Không đòi mô phỏng phải trùng số liệu thực nghiệm của tác giả.
- Chuyển bước khi chạy hoàn chỉnh hoặc đã chỉ rõ lỗi cản trở và xử lý có kiểm chứng.

### Mốc 4 — Hệ thống mô phỏng và đo lường (C3, C4)

- Tách cấu hình, tạo tham chiếu, tính tập, điều khiển, cập nhật trạng thái, ghi dữ liệu và xuất kết quả.
- Giữ một lệnh tái lập gốc và một lệnh chạy bộ thử nghiệm; ghi tên lệnh thực tế trong README khi triển khai xong.
- Sau tái cấu trúc, so với kết quả nền bằng dung sai có lý giải; không ngầm thay đổi bài toán.
- Mỗi `run_id` lưu cấu hình đầy đủ, nguồn/phiên bản mã, trục thời gian, trạng thái/tham chiếu, lệnh bánh, sai số, chỉ số tập, thời gian tính và trạng thái bộ giải.
- Kiểm tra chiều dữ liệu, căn chỉnh mẫu và đơn vị. Trạng thái thường có thể nhiều hơn lệnh một mẫu; xử lý rõ ràng.
- Chuyển bước khi chỉ cần dữ liệu đã lưu là tái tạo được bảng và hình, không chép số thủ công.

### Mốc 5 — Đối chứng Lyapunov (C2–C4)

- Chốt một luật cụ thể có nguồn đọc được, công thức và giả thiết rõ; tên “Lyapunov” đơn thuần chưa đủ.
- Kiểm tra bộ điều khiển riêng trên ca đơn giản trước khi so sánh.
- Mô tả cách chuyển sang vận tốc bánh và cách áp dụng bão hòa; lưu cả lệnh yêu cầu và lệnh thực sự áp dụng nếu cần phân tích.
- Không suy ra rằng chứng minh ổn định của luật gốc vẫn đúng sau khi thêm bão hòa hoặc sửa luật.
- Hiệu chỉnh thông số trên các ca riêng, ghi cách lựa chọn và chốt thông số trước khi đánh giá chính thức; công khai mọi ngoại lệ.
- Chuyển bước khi có cơ sở xác nhận đối chứng được triển khai đúng và không bị cố ý chọn thông số bất lợi.

### Mốc 6 — Thử nghiệm, phân tích và giới hạn (C4)

- Bộ đánh giá dự kiến: 2 quỹ đạo × 3 điều kiện đầu × 3 giới hạn vận tốc × 2 bộ điều khiển = 36 lượt chạy chính, ngoài ca tái lập.
- Đây là thiết kế dự kiến; chỉ chốt các giá trị sau khi kiểm tra khả thi. Nếu thay đổi quy mô, ghi lý do và giữ khả năng trả lời câu hỏi nghiên cứu.
- Công bố chính xác trạng thái ban đầu `(x0, y0, theta0)`; giải thích mức sai lệch nhỏ/vừa/lớn.
- Khi khảo sát một yếu tố, giữ nguyên các yếu tố còn lại. Không đồng thời giảm giới hạn bánh và giảm tốc tham chiếu rồi quy toàn bộ khác biệt cho giới hạn bánh.
- Hai bộ điều khiển dùng chung mô hình, tham chiếu theo thời gian, trạng thái đầu, chu kỳ lấy mẫu, bộ tích phân, thời lượng và giới hạn bánh.
- Kiểm tra điều kiện áp dụng của T-ST-RHC cho mỗi cấu hình, gồm quan hệ tập nhiễu tham chiếu với miền điều khiển và sai số đầu trong miền thu hút. Phân biệt miền khả thi lý thuyết với việc tham chiếu chỉ thỏa giới hạn bánh danh định.
- Tính lại tập chuẩn bị khi đổi tham số ảnh hưởng đến tập: robot, `b`, chu kỳ lấy mẫu, giới hạn bánh hoặc đặc trưng tham chiếu. Chỉ tái dùng khi chứng minh được cấu hình cũ còn bao phủ cấu hình mới.
- Ca ngoài điều kiện bảo đảm phải gắn nhãn khảo sát giới hạn; không kết luận chúng bác bỏ định lý.
- Với phép đo thời gian: có khởi động trước, lặp đo hợp lý, nêu số lần; báo cáo biến thiên. Các lần lặp xác định chỉ phục vụ đo thời gian, không tạo bằng chứng thống kê về nhiễu.
- Nếu bổ sung nhiễu: quy định mô hình, mức nhiễu, seed, số lần lặp và dùng cùng dữ liệu nhiễu để so sánh.
- Chuyển bước khi có đủ dữ liệu cho kết luận và không còn lỗi cốt lõi chưa giải thích.

### Mốc 7 — Báo cáo và hồ sơ minh chứng (C1–C5)

- Bố cục: bài toán/mục tiêu → tổng quan và lý thuyết → phương pháp/triển khai → thử nghiệm → kết quả/thảo luận → kết luận.
- Viết kết luận theo từng mục tiêu, ghi mức hoàn thành và giới hạn.
- Trình bày theo yêu cầu chính thức của giảng viên. Khi chưa có mẫu khác, dùng Times New Roman cỡ 13 cho báo cáo Word theo sở thích người dùng.
- Hình có nhãn, đơn vị, chú thích và nguồn; hình/bảng/công thức đánh số và được dẫn chiếu trong nội dung. Không để tham chiếu hỏng.
- Trích dẫn nhất quán; có bảng kế thừa/tự làm và ghi nhận vai trò AI nếu có theo hướng dẫn học phần.
- Kiểm tra bản xuất thực tế, tính đọc được và sự thống nhất số liệu giữa báo cáo với dữ liệu gốc.

## 8. Quy định chỉ số và phép đo

Thống nhất sai số vị trí tại tâm robot:

`ep(k) = sqrt((x(k)-xr(k))^2 + (y(k)-yr(k))^2)`.

| Chỉ số | Quy ước |
| --- | --- |
| RMSE vị trí | `sqrt(mean(ep.^2))`, đơn vị m |
| IAE | Tích phân số `ep` theo thời gian, đơn vị m·s; công bố quy tắc tích phân |
| Sai số cực đại | `max(ep)`, đơn vị m |
| Vi phạm vận tốc | Số mẫu, tỷ lệ mẫu và mức vượt lớn nhất của từng bánh; công bố dung sai số |
| Độ biến thiên lệnh | Tổng bình phương chuẩn sai khác vector vận tốc hai bánh liên tiếp; giữ cùng chu kỳ lấy mẫu và khoảng đánh giá |
| Thời gian tính điều khiển | Trung bình, phân vị 95%, lớn nhất và số bước vượt chu kỳ lấy mẫu |
| Trạng thái bộ giải | Exit flag, độ vi phạm ràng buộc, số lỗi/ca thất bại |

- Bổ sung sai số điểm điều khiển phía trước và diễn biến chỉ số tập để liên hệ kết quả với lý thuyết T-ST-RHC.
- Sai số hướng cần xử lý tính tuần hoàn của góc; công bố cách tính, không trừ góc thô khi đi qua biên ±pi.
- Chỉ số `eps` ở cuối script gốc là trung bình bình phương sai số vị trí; phải lấy căn nếu báo cáo RMSE.
- Phân biệt hàm mục tiêu của bộ điều khiển với các chỉ số dùng đánh giá sau mô phỏng.
- Đo toàn bộ bước điều khiển, gồm cập nhật ràng buộc/tìm tập/giải tối ưu/chuyển lệnh; tách riêng chi phí offline. Loại vẽ hình, `pause` và xuất tệp khỏi phép đo điều khiển.
- Nếu chỉ đo thời gian bộ giải, phải ghi rõ. Kết quả thời gian trên máy mô phỏng không tự động chứng minh đáp ứng thời gian thực trên robot.

## 9. Kiểm tra kỹ thuật bắt buộc

Chỉ thêm kiểm tra có ý nghĩa với tính đúng đắn; không viết kiểm tra chỉ lặp lại mã triển khai.

- Kiểm tra chuyển đổi vận tốc bánh ↔ vận tốc robot và dấu quay bằng trường hợp biết trước.
- Kiểm tra quỹ đạo/tham chiếu, đạo hàm, tính liên tục hướng và điều kiện không xác định của công thức tham chiếu.
- Kiểm tra ma trận định dạng tập, kích thước, tính đối xứng/xác định dương khi cần và phép kiểm tra thuộc tập.
- Phân biệt phép toán phần tử với phép toán ma trận; không tổng quát hóa công thức chỉ đúng cho trường hợp ma trận đặc biệt.
- Kiểm tra `exitflag`, giá trị hữu hạn và dư ràng buộc của nghiệm tối ưu; dùng dung sai có lý giải, tránh so sánh số thực với bất đẳng thức nghiêm ngặt thiếu dung sai.
- Không âm thầm cắt lệnh T-ST-RHC để che nghiệm sai ràng buộc. Nếu dùng phương án dự phòng, công bố và đếm số lần áp dụng.
- Kiểm tra khớp kết quả trước/sau tái cấu trúc và thử độ nhạy với thiết lập tích phân trên một số ca đại diện.
- Ghi nhận khác biệt giữa mô hình thiết kế rời rạc và mô hình robot tích phân liên tục; không tự coi hai cách cập nhật là tương đương chính xác.

## 10. Phân tích kết quả và đóng góp

Mỗi nhận xét phải theo chuỗi: **bằng chứng → hiện tượng → nguyên nhân kỹ thuật → giới hạn kết luận**.

- Định lượng đánh đổi giữa sai số, bão hòa, độ biến thiên lệnh và chi phí tính toán.
- Phân tích vì sao giới hạn vận tốc, độ cong hoặc sai lệch đầu làm thay đổi kết quả, có dữ liệu đối chiếu.
- Không chỉ nhận xét “bám tốt”, “ổn định” hoặc “tốt hơn” từ một hình quỹ đạo.
- Không kết luận ưu thế tổng quát từ một ca; nêu rõ phạm vi thử nghiệm.
- Không loại bỏ ca thất bại. Ghi cấu hình, lỗi, nguyên nhân đã biết/chưa biết và ảnh hưởng tới kết luận.
- Không gọi độ biến thiên lệnh là tiêu thụ năng lượng khi chưa có mô hình năng lượng.
- Giữ các phần sửa lỗi, đối chứng và mở rộng kịch bản tách bạch trong hồ sơ đóng góp.

## 11. Hồ sơ tự kiểm tra và điều kiện hoàn thành

Tạo `docs/rubric_evidence.md`, mỗi dòng ghi: tiêu chí, yêu cầu, đường dẫn minh chứng, trạng thái, thiếu sót và việc khắc phục.

Chỉ dùng ba trạng thái: **chưa có / đã có nhưng chưa kiểm chứng / đã kiểm chứng**. Mặc định mọi mục chưa có cho đến khi có bằng chứng thực tế.

- [ ] C1: Phát biểu bài toán, mục tiêu và phạm vi rõ; mỗi mục tiêu có phép kiểm chứng.
- [ ] C2: Công thức đúng; giải thích sâu; có đối chiếu nguồn và liên hệ mã.
- [ ] C3: Có cấu hình, lý do chọn tham số, lưu đồ, kiểm tra khả thi và quy trình chạy lại.
- [ ] C4: Có dữ liệu tự chạy, so sánh công bằng, chỉ số thống nhất, phân tích nguyên nhân và giới hạn.
- [ ] C5: Báo cáo logic, đánh số/dẫn chiếu đúng, nguồn nhất quán và rõ đóng góp.
- [ ] Mã chạy được trên môi trường đã công bố; README có lệnh thực tế.
- [ ] Dữ liệu, bảng và hình truy ngược được tới cấu hình và phiên bản mã.
- [ ] Các lỗi, ca thất bại và phần chưa kiểm chứng được công bố.
- [ ] Gói nộp có báo cáo, mã, cấu hình, dữ liệu cần thiết, nguồn và giấy phép liên quan.

Chỉ kết luận **đã có đủ bằng chứng hướng tới mức Xuất sắc** khi mọi tiêu chí C1–C5 có minh chứng đã kiểm chứng và không còn thiếu sót kỹ thuật trọng yếu. Nếu chưa đủ, báo cáo trung thực tiêu chí còn thiếu và công việc phải hoàn thành; không gán điểm chắc chắn.
