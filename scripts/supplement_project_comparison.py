"""Append the paper-versus-project comparison while preserving the existing summary."""
from pathlib import Path
from docx import Document
from docx.shared import Cm, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

root=Path(__file__).resolve().parents[1]
source=root/'report/tom_tat_de_tai_va_minh_chung.docx'
doc=Document(source)
if doc.paragraphs[0].text.startswith('cTóm tắt'):
    for run in doc.paragraphs[0].runs:
        if run.text:
            if run.text.startswith('c'):run.text=run.text[1:]
            break
doc.add_page_break()
doc.add_heading('8 So sánh bài báo gốc với dự án của nhóm',1)
doc.add_paragraph('Bài báo đề xuất và kiểm chứng T-ST-RHC. Dự án của nhóm kế thừa phương pháp và mã repo, mở rộng việc tái lập, khảo sát và phân tích. Cấu hình thực nghiệm trong bài báo và cấu hình mô phỏng repo là hai cấu hình khác nhau.')
comparison=[
('Mục tiêu','Đề xuất T-ST-RHC cho robot có giới hạn bánh; xây dựng cơ sở lý thuyết.','Tái lập có kiểm chứng và đánh giá ảnh hưởng của điều kiện đầu, giới hạn bánh; chưa đề xuất luật mới.'),
('Cách kiểm chứng','Thực nghiệm Khepera IV; encoder/odometry và truyền thông Wi-Fi TCP.','Mô phỏng MATLAB R2023a; robot tích phân ode45, lệnh bánh giữ hằng từng chu kỳ; biết trạng thái.'),
('Quỹ đạo và đầu vào','Thực nghiệm số 8, q0 = (0.6, 0, π), giới hạn 10 rad/s.','Thêm đường tròn; 3 mức sai lệch đầu; giới hạn 8/10/12 rad/s; tổng 36 cấu hình.'),
('Đối chứng','So với 4 phương pháp: RHC, Blažič, MPC tuyến tính và tuyến tính hóa phản hồi động.','Tập trung 1 đối chứng Blažič (18); tự triển khai, hiệu chỉnh riêng, thêm bão hòa bánh; dùng chung điều kiện thử.'),
('Thông số robot','Thực nghiệm R = 0.021 m; D = 0.1047 m; Ts = 0.15 s.','Giữ repo: r = 0.0205 m; d = 0.053 m; b = 0.1 m; Ts = 0.15 s. Không tự quy đổi D và d.'),
('Tập và mục tiêu tối ưu','Thực nghiệm: 396 tập ROSC; mục tiêu pha ngoài có phạt nỗ lực 0.5‖u‖².','Giữ repo: 700 tập ngoài miền cuối; không có hạng phạt nỗ lực đó. Đây là khác biệt cấu hình, không phải cải tiến do nhóm đề xuất.'),
('Chỉ số và thời gian','IAE, ISE, ITAE, ITSE; báo cáo thời gian các bài toán tối ưu.','RMSE, IAE, cực đại sai số, vi phạm bánh, biến thiên lệnh; đo toàn bước điều khiển sau warm-up, lặp 5 lần.'),
('Kết quả và ca khó','Báo cáo ưu thế T-ST-RHC trong thí nghiệm được công bố.','33/36 ca hoàn thành; 3 ca dừng do điều kiện dựng tập. RMSE nhỏ hơn đối chứng ở 6/6 cặp số 8 và 7/9 cặp tròn hoàn thành; giữ cả ca bất lợi.'),
('Phân tích bổ sung','Trình bày miền bất biến, miền thu hút và bảo đảm trên mô hình thiết kế.','Đối chiếu mô hình thiết kế với robot giữ lệnh và nghiệm tích phân chính xác; phân tích chỉ số tập tăng và sai số lớn.'),
('Sản phẩm và đóng góp','Bài báo, chứng minh, thực nghiệm và mã nguồn tác giả.','Hệ thống mô-đun, bộ đối chứng, ma trận thử, dữ liệu/log, kiểm thử và xuất hình/bảng; lưu dấu vết mã và cấu hình.')
]
table=doc.add_table(rows=1,cols=3); table.style='Table Grid'; table.autofit=False
widths=[2.8,7.2,7.4]
for cell,title in zip(table.rows[0].cells,['Tiêu chí','Bài báo gốc','Dự án của nhóm']):cell.text=title
for row in comparison:
    for cell,text in zip(table.add_row().cells,row):cell.text=text
for i,row in enumerate(table.rows):
    for cell,width in zip(row.cells,widths):
        cell.width=Cm(width)
        for par in cell.paragraphs:
            par.paragraph_format.space_after=Pt(3)
            par.paragraph_format.space_before=Pt(2)
            par.paragraph_format.line_spacing=1
            for run in par.runs:run.font.size=Pt(11); run.bold=(i==0)
    row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
table.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
doc.add_paragraph('Cách hiểu kết quả: nhóm mở rộng bằng chứng đánh giá, chưa chứng minh dự án tốt hơn kết quả của tác giả. Không so trực tiếp số đo giữa robot thật và mô phỏng khi khác thông số, hàm mục tiêu, trạng thái đầu hoặc khoảng lấy mẫu. Lyapunov đã có trong bài báo gốc; phần tự làm là triển khai và đánh giá đối chứng trong hệ thống của nhóm.')
par=doc.add_paragraph('Minh chứng: bài báo gốc Mục III–IV, Algorithm 1 và Bảng I; docs/parameter_comparison.md; docs/changes_and_contributions.md; docs/experiment_design.md; tables/summary.csv; tables/model_gap.csv. Các đường dẫn tính từ D:\\RobotCK.')
for run in par.runs:run.font.size=Pt(10)
target=root/'report/tom_tat_de_tai_va_minh_chung_so_sanh.docx'
doc.save(target)
print(target)
