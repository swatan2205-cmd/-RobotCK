# Mô phỏng và đánh giá điều khiển bám quỹ đạo robot di động hai bánh có giới hạn vận tốc bằng phương pháp T-ST-RHC trên MATLAB.

Dự án mô phỏng MATLAB theo `AGENTS.md`: tái lập Tiriolo–Lucia (2023), đối chứng Blažič (2011), khảo sát điều kiện đầu và giới hạn vận tốc bánh. Kết quả thực tế và giới hạn được lưu cùng dữ liệu; không thay thế dữ liệu bằng hình minh họa.

## Chạy từ thư mục gốc

```matlab
setup_project;
check_environment;
run_checks;
run_original(true);   % bản sửa duy nhất: bỏ plot(ell_d) không tương thích ET
compare_baseline;     % đối chiếu với cùng options và lưới ode45 của tác giả
tune_lyapunov;        % hiệu chỉnh riêng, cần chạy trước run_suite
run_suite;           % 36 cấu hình, warm-up và 5 lần đo mỗi cấu hình
check_sensitivity;
diagnose_model_gap;   % chẩn đoán mô hình riêng, giữ nguyên 36 ca chính
audit_results;
export_results;      % chỉ đọc dữ liệu đã lưu
```

`run_original(false)` chạy đúng bản cung cấp, hiện dừng ở hàm vẽ ET trên R2023a. Log hai lần lỗi đầu ở `results/baseline_attempt01` và `baseline_attempt02`. Lệnh chạy lại sẽ ghi đè kết quả cùng tên; sao lưu thư mục results/tables/figures trước khi muốn giữ một chiến dịch cũ.

## Môi trường đã khảo sát

MATLAB R2023a, Optimization Toolbox; thông tin thực tế ở `results/environment.json`. ET và MPT3 được đóng gói trong `external/`, commit ở `external/manifest.json`. Không cần `savepath`, chỉnh startup hoặc dùng mã ở dự án khác. ET chỉ khởi tạo cấu hình và chức năng dựng đối tượng; các phép SDP/CVX không được dùng hoặc xác nhận. MPT3 dùng hàm thích nghi `src/compat/mpt_call_linprog.m` cho chữ ký MATLAB mới. Không cần LCP/HYSDEL cho kịch bản này.

## Tổ chức và truy xuất

- `original/provided`: bản sao bất biến mã đầu vào; `original/repaired`: bản bỏ một lệnh vẽ; thư mục đầu vào vẫn nguyên vẹn.
- `src`, `config`, `scripts`, `tests`: hệ thống tự thực hiện; mỗi lượt lưu SHA-256 mã MATLAB.
- `results/<run_id>/run.mat`: cấu hình, tham chiếu, trạng thái, cả hai loại lệnh, tập, chẩn đoán bộ giải và thời gian; `summary.json`: bản đọc nhanh.
- `tables/summary.csv`: toàn bộ ca, kể cả ca thất bại với chỉ số đầy đủ khoảng thời gian là NaN.
- `docs`: nguồn, mô hình, thiết kế thử nghiệm, sửa chữa, minh chứng rubric và đóng góp.
- `report`: báo cáo sinh từ dữ liệu thực tế; `figures`: đồ thị tương ứng run_id.

## Quy ước

Thứ tự bánh `[phải; trái]`; trạng thái `3×(N+1)`, lệnh `2×N`; `t_state` và `t_control` riêng. RMSE tại tâm robot; IAE dùng trapz trên mẫu trạng thái từ 0 đến thời điểm cuối. Lệnh giữ hằng trong từng chu kỳ và robot tích phân liên tục. Kết quả thời gian là trên máy mô phỏng, không chứng minh khả năng thời gian thực của robot.

Chi tiết lý thuyết: `docs/theory.md`. Giấy phép mã kế thừa giữ tại các thư mục nguồn. Công cụ AI tham gia lập trình, kiểm thử, tổ chức dữ liệu và soạn báo cáo; người học cần kiểm tra, hiểu và khai báo theo quy định học phần.

## Tạo lại báo cáo

Chạy `scripts/build_report.py` với Python có python-docx, sau khi đã có các bảng, JSON kiểm chứng và chẩn đoán. Chạy `scripts/render_report.ps1` trên Windows có Microsoft Word để xuất PDF. Phiên thực hiện dùng Python đóng gói của Codex; trình render LibreOffice đóng gói không có trên môi trường Windows này, nên PDF được xuất bằng Word và kiểm tra qua ảnh Poppler. Không cần Python để chạy mô phỏng MATLAB.
