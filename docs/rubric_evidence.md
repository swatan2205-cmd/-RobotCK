# Hồ sơ minh chứng rubric

Trạng thái đánh giá bằng bằng chứng thực tế, không gán điểm. Cột thiếu sót thể hiện giới hạn còn lại của từng minh chứng.

| Tiêu chí | Yêu cầu | Đường dẫn minh chứng | Trạng thái | Thiếu sót và khắc phục |
|---|---|---|---|---|
| C1 | Vấn đề, phạm vi và mục tiêu đo được | docs/problem_statement.md; docs/experiment_design.md | đã kiểm chứng | Không dùng ngưỡng cải thiện tùy ý; chỉ kết luận trong thiết kế công bố |
| C2 | Mô hình, nguồn, ký hiệu, công thức và liên hệ mã | docs/theory.md; docs/references.md; tests/test_robot_project.m | đã kiểm chứng | Chứng minh nguồn có giả thiết; không suy ra bảo đảm cho mô hình giữ lệnh hoặc Lyapunov bão hòa |
| C2 | Cận tham chiếu liên tục có chứng minh giải tích | src/prepare_sets.m | đã có nhưng chưa kiểm chứng | Hiện là lưới dày cộng biên số; chưa có chứng nhận cận liên tục, cần bổ sung nếu yêu cầu bảo đảm hình thức |
| C3 | Môi trường và phụ thuộc thực tế | results/environment.json; external/manifest.json | đã kiểm chứng | ET chỉ xác nhận chức năng dùng; không xác nhận CVX/SDP/LCP/HYSDEL |
| C3 | Tái lập và đối chiếu tái cấu trúc | results/baseline; results/baseline_attempt01; results/baseline_attempt02; results/baseline_comparison.json | đã kiểm chứng | Bản chạy nền bỏ duy nhất lệnh vẽ không tương thích; giữ nguyên bản cung cấp |
| C3 | Ảnh hưởng thay thiết lập số | results/baseline_comparison_validated.json; tables/sensitivity.csv | đã kiểm chứng | Profile validated không khớp ngưỡng baseline gốc; đã tách khỏi kiểm tra tương đương cấu trúc |
| C3 | Tham số, quy trình và kiểm tra kỹ thuật | config/default_config.m; docs/experiment_design.md; results/test_summary.json | đã kiểm chứng | Tám nhóm kiểm tra có ý nghĩa; không đại diện mọi đầu vào tùy ý |
| C4 | So sánh công bằng và hiệu chỉnh riêng | results/calibration.mat; tables/calibration.csv; results/evaluation_design.mat | đã kiểm chứng | Lưới hữu hạn và góc hiệu chỉnh pi/6; không gọi tối ưu toàn cục |
| C4 | 36 cấu hình, dữ liệu và lỗi được lưu | tables/summary.csv; results/*_i*_w*/run.mat; tables/audit.csv | đã kiểm chứng | 33 hoàn thành, 3 dừng do điều kiện; không tính RMSE toàn khoảng cho ca thiếu mẫu |
| C4 | Chẩn đoán ca bất lợi và giới hạn mô hình | tables/model_gap.csv; results/*_design_diagnostic.mat; docs/results_analysis.md | đã kiểm chứng | Phép đối chiếu có bằng chứng; chưa chứng minh một định lý mới cho robot giữ lệnh |
| C4 | Thời gian toàn bước và biến thiên | timing và repeatTiming trong run.mat; tables/summary.csv | đã kiểm chứng | Năm lần sau warm-up; tải hệ điều hành chưa kiểm soát; không chứng minh thời gian thực |
| C5 | Bố cục, đánh số, trích dẫn và đóng góp | report/bao_cao_robot.docx; report/bao_cao_robot.pdf; docs/changes_and_contributions.md | đã kiểm chứng | Đã kiểm tra 19 trang bản xuất, 9 bảng, 4 hình và 18 công thức; bổ sung thông tin cá nhân nếu mẫu học phần yêu cầu |
| C5 | Tái tạo và hồ sơ nguồn | README.md; scripts; docs/provided_manifest.json | đã kiểm chứng | MATLAB cần license hợp lệ; xuất PDF cần Microsoft Word trong môi trường hiện tại |

Chưa kết luận đã đủ bằng chứng hướng tới mức Xuất sắc cho mọi yêu cầu: còn giới hạn chứng nhận cận liên tục và bảo đảm lý thuyết trên mô hình thực thi. Kết quả mô phỏng và kiểm tra số có giá trị trong phạm vi công bố; điểm số do giảng viên đánh giá.
