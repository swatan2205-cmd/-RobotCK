# Đưa dự án lên GitHub

Gói ZIP chứa mã MATLAB, cấu hình, kiểm tra, dữ liệu mô phỏng, hình, bảng, báo cáo, tài liệu và phụ thuộc được lưu trong dự án. Các tệp tạm và ZIP phát hành không nằm trong gói. Hướng dẫn môi trường và chạy mô phỏng nằm trong `README.md`.

1. Giải nén `robotck_project.zip` vào một thư mục riêng.
2. Tạo repository trống trên GitHub (không tạo sẵn README hoặc .gitignore).
3. Mở terminal tại thư mục vừa giải nén và chạy:

```powershell
git init
git add .
git commit -m "Initial project: robot trajectory tracking with T-ST-RHC and Lyapunov"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/RobotCK.git
git push -u origin main
```

Thay `YOUR_USERNAME/RobotCK` bằng địa chỉ repository thực tế. Đăng nhập GitHub khi Git yêu cầu. Không tải nguyên ZIP vào repository nếu muốn GitHub hiển thị mã và lịch sử sửa đổi.

`PACKAGE_MANIFEST.json` liệt kê SHA-256 của các tệp được đóng gói để kiểm tra tính toàn vẹn. Giữ thông tin tác giả và giấy phép của mã tái sử dụng trong `original/` và `external/`; không áp đặt một giấy phép chung mới lên các thành phần của bên thứ ba.
