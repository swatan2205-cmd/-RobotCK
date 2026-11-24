# Rà soát bản báo cáo cập nhật

Bản được chỉnh trực tiếp: `report/bao_cao_robot_cap_nhat.docx`. Giữ bìa, thông tin cá nhân, các bảng số liệu và hình hiện có; bổ sung từ dữ liệu đã chạy trên MATLAB. Không thay đổi bộ điều khiển để làm đẹp kết quả.

| Tiêu chí | Phần bổ sung trong báo cáo | Trạng thái |
|---|---|---|
| C1 | Tiêu chí xác nhận mục tiêu, phạm vi và cách kiểm chứng; phân biệt hoàn thành lượt chạy với đạt chất lượng ứng dụng | đã kiểm chứng |
| C2 | Hình học tập, điều kiện bảo đảm, miền cuối, ràng buộc bánh, bảng ký hiệu, đối chiếu nguồn và cấu hình repo/bài báo | đã kiểm chứng |
| C3 | Giả mã hai chế độ, điều kiện dừng, lý do chọn tham số, hiệu chỉnh đối chứng, hồ sơ tái lập và sai khác trước/sau tái cấu trúc | đã kiểm chứng |
| C4 | Công thức chỉ số, quy ước mẫu, bảng thời gian và biến thiên, sai số cực đại/phía trước, đánh đổi định lượng và ca bất lợi | đã kiểm chứng |
| C5 | Trích dẫn số thống nhất, công thức Word, danh mục hình/bảng, phụ lục, chú thích truy xuất dữ liệu, kiểm tra bản xuất | đã kiểm chứng |

Minh chứng kiểm tra cấu trúc và bảo toàn: `docs/rubric_upgrade_audit.json`. Bằng chứng mô phỏng: `tables/summary.csv`, `tables/model_gap.csv`, `results/baseline_comparison.json`, `results/report_evidence.json`, các tệp `results/*/run.mat`. Hình tái lập được xuất bằng `scripts/export_report_evidence.m` từ dữ liệu nền đã lưu.

Giới hạn đã công bố trong báo cáo: cận tham chiếu bằng lưới và biên số chưa là chứng nhận liên tục giải tích; mô hình thiết kế không đồng nhất chính xác với robot giữ lệnh bánh; không kế thừa nguyên vẹn bảo đảm Lyapunov sau bão hòa; hiệu chỉnh trên lưới hữu hạn; thời gian đo phụ thuộc máy và tải hệ điều hành. Các giới hạn này không được chuyển thành tuyên bố bảo đảm mới. Báo cáo đã được củng cố theo C1–C5 để hướng tới mức Xuất sắc; điểm cuối cùng do giảng viên đánh giá.
