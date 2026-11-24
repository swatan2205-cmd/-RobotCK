# Tư liệu mô phỏng RobotCK

[Xem hoặc tải video MP4](https://raw.githubusercontent.com/swatan2205-cmd/-RobotCK/main/output/simulation_media/robotck_simulation.mp4) · [Toàn bộ 34 ảnh kết quả](../../figures) · [Bảng số liệu](../../tables/summary.csv)

Video dựng lại từ trạng thái và tham chiếu đã lưu trong bốn lượt chạy ở giới hạn 10 rad/s. Hàng trên là quỹ đạo số 8 với sai lệch ban đầu vừa. Hàng dưới là đường tròn với sai lệch ban đầu lớn. Hai hình trong mỗi hàng dùng cùng tỉ lệ trục để tiện đối chiếu. Video phát nhanh khoảng 3 lần so với thời gian mô phỏng hiển thị trên hình.

| Quỹ đạo | T-ST-RHC | Lyapunov |
| --- | --- | --- |
| Số 8, mức vừa | [Xem hình](../../figures/eight_i2_w10_tstrhc.png) | [Xem hình](../../figures/eight_i2_w10_lyapunov.png) |
| Đường tròn, mức lớn | [Xem hình](../../figures/circle_i3_w10_tstrhc.png) | [Xem hình](../../figures/circle_i3_w10_lyapunov.png) |

[Kết quả tái lập cấu hình nền](../../figures/baseline_report.png) · [Mã dựng video](../../scripts/export_simulation_video.py) · [Mã gốc của Tiriolo và Lucia](https://github.com/cristiri/T_ST_RHC_mobile_robots)
