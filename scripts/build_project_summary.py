"""Build a short illustrated guide from existing, recorded project evidence."""
from pathlib import Path
import csv, json, math
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'report'
ASSETS = ROOT / 'figures' / 'summary'
ASSETS.mkdir(parents=True, exist_ok=True)
rows = list(csv.DictReader((ROOT/'tables/summary.csv').open(encoding='utf-8-sig')))
byid = {r['run_id']: r for r in rows}
evidence = json.loads((ROOT/'results/report_evidence.json').read_text(encoding='utf-8-sig'))
baseline = json.loads((ROOT/'results/baseline_comparison.json').read_text(encoding='utf-8-sig'))

def diagram(name, expanded=False):
    im = Image.new('RGB', (1600, 560), 'white')
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype('C:/Windows/Fonts/times.ttf', 34)
    small = ImageFont.truetype('C:/Windows/Fonts/times.ttf', 29)
    def box(x,y,w,h,text,color='#eaf0f7'):
        dr.rounded_rectangle((x,y,x+w,y+h), radius=15, fill=color, outline='#25435c', width=3)
        dr.multiline_text((x+w/2,y+h/2),text,font=font,fill='#142b40',anchor='mm',align='center',spacing=7)
    def arrow(points):
        dr.line(points, fill='#25435c', width=4)
        x,y=points[-1]; px,py=points[-2]
        dx,dy=x-px,y-py; length=math.hypot(dx,dy); ux,uy=dx/length,dy/length
        dr.polygon([(x,y),(x-18*ux+8*uy,y-18*uy-8*ux),(x-18*ux-8*uy,y-18*uy+8*ux)], fill='#25435c')
    if not expanded:
        box(25,20,490,125,'OFFLINE\nMô hình và giới hạn bánh')
        box(625,20,950,125,'Dựng miền cuối T0 và các tập T1 … TN')
        arrow([(515,82),(625,82)])
        box(25,240,390,145,'Tham chiếu theo thời gian\nvà trạng thái đo')
        box(535,240,520,145,'ONLINE\nTìm tập → QCQP hoặc QP')
        box(1175,240,400,145,'Lệnh hai bánh\nRobot Khepera IV')
        arrow([(1100,145),(1100,200),(790,200),(790,240)])
        arrow([(415,312),(535,312)]); arrow([(1055,312),(1175,312)])
        arrow([(1370,385),(1370,480),(215,480),(215,385)])
        dr.text((790,490),'Phản hồi vị trí và hướng qua encoder / odometry',font=small,fill='#25435c',anchor='mt')
    else:
        box(25,20,470,125,'Cấu hình chung\n2 quỹ đạo × 3 đầu × 3 giới hạn')
        box(610,20,470,125,'T-ST-RHC kế thừa\nTính tập và giải tối ưu')
        box(610,200,470,125,'Đối chứng Blažič\nĐổi sang bánh và bão hòa','#edf4ea')
        box(1190,95,385,155,'Mô hình robot chung\nGiữ lệnh và ode45')
        arrow([(495,82),(610,82)]); arrow([(495,82),(550,82),(550,262),(610,262)])
        arrow([(1080,82),(1130,82),(1130,145),(1190,145)])
        arrow([(1080,262),(1130,262),(1130,200),(1190,200)])
        box(610,400,965,125,'Lưu dữ liệu và log → Tính chỉ số → Hình và bảng\nKiểm tra điều kiện, ca lỗi và chênh lệch mô hình','#edf4ea')
        arrow([(1380,250),(1380,400)])
        dr.text((55,350),'Trạng thái robot được phản hồi\nvề bộ điều khiển đang chạy',font=small,fill='#25435c',spacing=8)
        dr.text((55,445),'Hai nhánh chạy riêng từng ca',font=small,fill='#25435c')
    p=ASSETS/(name+'.png'); im.save(p); return p

original_diagram=diagram('so_do_bai_bao_goc')
expanded_diagram=diagram('so_do_nhom_phat_trien',True)
doc=Document(); sec=doc.sections[0]
sec.page_width=Cm(21); sec.page_height=Cm(29.7)
sec.top_margin=Cm(1.6); sec.bottom_margin=Cm(1.5)
sec.left_margin=Cm(1.8); sec.right_margin=Cm(1.8)
for sty in ['Normal','Title','Heading 1','Heading 2','Caption']:
    s=doc.styles[sty]; s.font.name='Times New Roman'; s.font.color.rgb=RGBColor(0,0,0)
    s.font.size=Pt(13 if sty=='Normal' else 11 if sty=='Caption' else 16 if sty=='Heading 1' else 14 if sty=='Heading 2' else 20)
    s.paragraph_format.space_after=Pt(5)
    rf=s.element.get_or_add_rPr().get_or_add_rFonts()
    for attr in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:
        rf.attrib.pop(qn('w:'+attr),None)
    for attr in ['ascii','hAnsi','eastAsia','cs']: rf.set(qn('w:'+attr),'Times New Roman')
    for border in list(s.element.iter(qn('w:pBdr'))): border.getparent().remove(border)
doc.styles['Caption'].font.bold=False
doc.styles['Caption'].font.italic=False
doc.styles['Normal'].paragraph_format.line_spacing=1.03
doc.styles['Title'].paragraph_format.space_after=Pt(8)
doc.core_properties.title='Tóm tắt đề tài robot và minh chứng'
doc.core_properties.author='Nhóm dự án Robot'

def p(text,style=None): return doc.add_paragraph(text,style)
def h(text): doc.add_heading(text,1)
def link(label,rel,para=None):
    para=para or doc.add_paragraph()
    target=(ROOT/rel).resolve().as_uri() if not rel.startswith('https:') else rel
    el=OxmlElement('w:hyperlink'); el.set(qn('r:id'),para.part.relate_to(target,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True))
    r=OxmlElement('w:r'); pr=OxmlElement('w:rPr'); color=OxmlElement('w:color'); color.set(qn('w:val'),'174B79'); pr.append(color); r.append(pr)
    t=OxmlElement('w:t'); t.text=label; r.append(t); el.append(r); para._p.append(el)
    return para
def paths(items):
    for rel in items: link(rel,rel)
def pic(path,width=6.65):
    par=doc.add_paragraph(); par.alignment=WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_after=Pt(2); par.add_run().add_picture(str(path),width=Inches(width))
def table(headers,data,widths=None):
    t=doc.add_table(rows=1,cols=len(headers)); t.style='Table Grid'
    for c,x in zip(t.rows[0].cells,headers): c.text=x
    for row in data:
        for c,x in zip(t.add_row().cells,row): c.text=str(x)
    for i,row in enumerate(t.rows):
        for c in row.cells:
            for par in c.paragraphs:
                par.paragraph_format.space_after=Pt(3); par.paragraph_format.space_before=Pt(2)
                for r in par.runs: r.font.size=Pt(11); r.bold=(i==0)
        trpr=row._tr.get_or_add_trPr(); trpr.append(OxmlElement('w:cantSplit'))
    return t
def page(): doc.add_page_break()

p('Tóm tắt đề tài robot\nvà minh chứng', 'Title')
p('Mô phỏng và đánh giá bám quỹ đạo theo thời gian cho robot hai bánh có giới hạn vận tốc bằng T-ST-RHC trên MATLAB.')
p('Ý chính: robot phải đến đúng vị trí vào đúng thời điểm mà không vượt tốc độ bánh. Nhóm kế thừa thuật toán của tác giả, xây dựng hệ thống mô phỏng và đối chứng để đánh giá khi đổi trạng thái đầu và giới hạn bánh. Giả thiết cơ bản: bánh không trượt, biết trạng thái; nhóm chỉ mô phỏng, chưa chế tạo robot.')
h('1 Nội dung bài báo gốc')
p('C. Tiriolo và W. Lucia, A Set-Theoretic Control Approach to the Trajectory Tracking Problem for Input–Output Linearized Wheeled Mobile Robots, IEEE Control Systems Letters, 2023.')
for text in [
    'Mô hình động học robot vi sai; dùng một điểm phía trước robot để tuyến tính hóa đầu vào–đầu ra. Ràng buộc bánh sau biến đổi phụ thuộc hướng robot.',
    'Tính trước miền cuối bất biến và các tập có thể điều khiển về miền cuối. Khi chạy: tìm tập chứa sai số, giải QCQP ở ngoài miền cuối hoặc QP trong miền cuối, rồi đổi thành lệnh hai bánh.',
    'Bảo đảm sai số bị chặn và tính khả thi với các giả thiết của mô hình thiết kế; không đồng nghĩa sai số luôn về đúng 0.',
    'Thực nghiệm với Khepera IV, quỹ đạo số 8, so sánh bốn phương pháp gồm RHC, Lyapunov Blažič, MPC tuyến tính và tuyến tính hóa phản hồi động; có đồ thị, IAE, ISE, ITAE và ITSE.'
]: p('• '+text)
h('2 Phần nhóm đã phát triển thêm')
table(['Phần thêm trong dự án','Giá trị và phạm vi đóng góp'],[
    ('Tái lập và tổ chức mã','Giữ bản gốc, sửa tương thích riêng; tách mô hình, điều khiển, cấu hình, lưu dữ liệu và kiểm thử.'),
    ('Đối chứng tự triển khai','Hiện thực Blažič (18), bão hòa bánh và hiệu chỉnh trên ca riêng. Bài báo gốc đã có đối chứng Lyapunov; đây không phải luật mới.'),
    ('Bộ đánh giá mở rộng','Thêm đường tròn; 2 quỹ đạo × 3 điều kiện đầu × 3 giới hạn bánh × 2 bộ điều khiển = 36 cấu hình.'),
    ('Đo lường và chẩn đoán','RMSE, IAE, vi phạm bánh, biến thiên lệnh, thời gian toàn bước, log nghiệm; lưu ca dừng và đối chiếu mô hình thiết kế với robot giữ lệnh.')
])
p('Các phần “thêm” nói trên là sản phẩm triển khai và đánh giá trong dự án; nhóm chưa đề xuất thuật toán T-ST-RHC mới hay định lý ổn định mới. Đường dẫn ở các trang sau tính từ D:\\RobotCK.', 'Caption')

page(); h('3 Sơ đồ gốc và sau khi nhóm phát triển')
pic(original_diagram,6.1); p('Hình 1. Luồng phương pháp và thực nghiệm bài báo gốc, nhóm vẽ lại theo Algorithm 1 và Mục IV. Khi tái lập trong dự án, robot thật được thay bằng mô phỏng theo mã repo.', 'Caption')
pic(expanded_diagram,6.1); p('Hình 2. Hệ thống nhóm phát triển. Hai nhánh điều khiển dùng chung điều kiện thử, mô hình robot và quy tắc đánh giá; mỗi nhánh chạy riêng.', 'Caption')
h('4 Địa chỉ tài liệu và mã nguồn')
table(['Cần tìm','Địa chỉ trong D:\\RobotCK'],[
    ('Bài báo và phần giải thích','STMPC_tracking_robot2023.pdf; docs/theory.md; docs/parameter_comparison.md'),
    ('Mã gốc được bảo toàn','original/provided/; bản chạy sau sửa tương thích: original/repaired/'),
    ('Mã nhóm phát triển','src/; config/default_config.m; scripts/; tests/test_robot_project.m'),
    ('Mô tả phần phát triển','docs/changes_and_contributions.md; docs/experiment_design.md; docs/results_analysis.md'),
    ('Nguồn và hồ sơ kiểm chứng','docs/references.md; docs/rubric_evidence.md; results/environment.json'),
    ('Sơ đồ trong bản tóm tắt','figures/summary/so_do_bai_bao_goc.png; figures/summary/so_do_nhom_phat_trien.png')
])
par=p('Nguồn trực tuyến: '); link('DOI bài báo','https://doi.org/10.1109/LCSYS.2023.3286774',par)
par=p('Mã tác giả tại phiên bản đã đối chiếu: '); link('GitHub commit c57e98262ff21d8bab711b892a14c7afc98e0c08','https://github.com/cristiri/T_ST_RHC_mobile_robots/tree/c57e98262ff21d8bab711b892a14c7afc98e0c08',par)

page(); h('5 Hình khi chạy lại mã tác giả')
pic(ROOT/'figures/baseline_report.png')
p('Hình 3. Lần tái lập mô phỏng từ mã tác giả sau khi bỏ duy nhất lệnh vẽ plot(ell_d) không tương thích. Bốn ô: quỹ đạo, sai số tâm, vận tốc bánh và chỉ số tập. Đây là dữ liệu nhóm chạy lại, không phải hình thực nghiệm robot thật trong bài báo.', 'Caption')
p('Thiết lập nền: số 8; q0 = (0.6 m, 0 m, π rad); giới hạn bánh 10 rad/s; chu kỳ 0.15 s. Môi trường được lưu: MATLAB R2023a. Kết quả nền có 293 lệnh; RMSE trên mẫu trước điều khiển là 0.07365 m, không có vi phạm vận tốc theo hồ sơ đã xuất.')
table(['Minh chứng','Địa chỉ'],[
    ('Hình tái lập','figures/baseline_report.png'),
    ('Dữ liệu và log nền','results/baseline/baseline.mat; results/baseline/'),
    ('Lỗi khi chạy bản chưa sửa','results/baseline_attempt01/; results/baseline_attempt02/'),
    ('Sai khác sau tái cấu trúc','results/baseline_comparison.json'),
    ('Số liệu dùng cho hình/báo cáo','results/report_evidence.json; scripts/export_report_evidence.m')
])
p(f"Đối chiếu với cùng thiết lập số của tác giả: sai khác trạng thái lớn nhất {baseline['maxStateDifference']:.3g} theo đơn vị từng thành phần; sai khác lệnh bánh {baseline['maxWheelDifference']:.3g} rad/s; kiểm tra đạt dung sai đã công bố.")
p('Cần phân biệt: cấu hình repo và thực nghiệm bài báo khác kích thước robot, số tập và hàm mục tiêu. Vì vậy đây là tái lập mô phỏng repo; không nhận là tái tạo chính xác số liệu thực nghiệm của bài báo. Bản đánh giá mở rộng còn dùng thiết lập số riêng, được công bố trong docs/experiment_design.md.')
par=p('Mở nhanh: '); link('hình nền','figures/baseline_report.png',par); par.add_run(' | '); link('dữ liệu nền','results/baseline/baseline.mat',par)

page(); h('6 Hình sau khi phát triển đối chứng')
pic(ROOT/'figures/eight_i1_w10_tstrhc.png',5.65)
p('Hình 4. T-ST-RHC trong hệ thống đánh giá của nhóm, quỹ đạo số 8, điều kiện đầu mức 1, giới hạn 10 rad/s.', 'Caption')
pic(ROOT/'figures/eight_i1_w10_lyapunov.png',5.65)
p('Hình 5. Đối chứng Blažič với cùng ca thử. Các ô biểu diễn quỹ đạo, sai số tâm, vận tốc bánh; ô cuối của đối chứng biểu diễn sai số hướng (rad).', 'Caption')
a=byid['eight_i1_w10_tstrhc']; b=byid['eight_i1_w10_lyapunov']
table(['Cùng điều kiện thử','T-ST-RHC','Lyapunov'],[
    ('RMSE tâm robot (m)',f"{float(a['rmse']):.5f}",f"{float(b['rmse']):.5f}"),
    ('IAE (m·s)',f"{float(a['iae']):.5f}",f"{float(b['iae']):.5f}")
])
p('Đầu chung q0 = (0.05 m, 0 m, 0.725447 rad), chạy 44.1 s. RMSE của T-ST-RHC nhỏ hơn trong ca này; kết quả này không suy rộng cho mọi cấu hình.', 'Caption')
p('Hình: figures/eight_i1_w10_tstrhc.png và figures/eight_i1_w10_lyapunov.png. Dữ liệu: results/eight_i1_w10_tstrhc/run.mat và results/eight_i1_w10_lyapunov/run.mat. Bảng: tables/summary.csv.', 'Caption')

page(); h('7 Ca bất lợi và minh chứng toàn bộ dự án')
pic(ROOT/'figures/circle_i3_w10_tstrhc.png',6.4)
p('Hình 6. Ca đường tròn, điều kiện đầu mức 3, giới hạn 10 rad/s: T-ST-RHC có sai số lớn và chỉ số tập tăng trở lại. Hình: figures/circle_i3_w10_tstrhc.png; dữ liệu: results/circle_i3_w10_tstrhc/run.mat.', 'Caption')
p('Kết quả toàn bộ: 36 cấu hình, 33 hoàn thành và 3 dừng. Ba ca số 8 của T-ST-RHC tại 8 rad/s không đạt điều kiện dựng tập; chỉ số toàn khoảng để NaN. Trong các cặp cùng hoàn thành, T-ST-RHC có RMSE nhỏ hơn Lyapunov ở 6/6 cặp số 8 và 7/9 cặp đường tròn.')
p('Ở ca Hình 6, RMSE ≈ 1.330 m; cùng trạng thái đầu tại 8 rad/s là ≈ 0.1265 m. Đối chiếu robot giữ lệnh, nghiệm tích phân chính xác và mô hình thiết kế cho thấy chênh lệch mô hình có vai trò lớn; tăng giới hạn bánh không tự bảo đảm bám tốt hơn. Đây chưa phải chứng minh định lý mới cho mô hình thực thi.')
table(['Kiểm chứng cần xem','Địa chỉ minh chứng'],[
    ('Toàn bộ ca và chỉ số','tables/summary.csv; tables/audit.csv; results/<run_id>/run.mat và summary.json'),
    ('Chẩn đoán ca bất lợi','tables/model_gap.csv; results/circle_i3_w10_tstrhc/diagnostic_summary.json; docs/results_analysis.md'),
    ('Kiểm tra kỹ thuật','results/test_summary.json: 8 đạt, 0 lỗi; tests/test_robot_project.m'),
    ('Toàn bộ hình phát triển','figures/circle_*.png; figures/eight_*.png; tên hình khớp thư mục results/<run_id>/'),
    ('Hướng dẫn tái tạo','README.md; scripts/run_original.m; scripts/run_suite.m; scripts/export_results.m')
])
p('Giới hạn kết luận: chưa kiểm chứng bằng robot thật; cận tham chiếu hiện kiểm tra trên lưới dày, chưa có chứng nhận giải tích liên tục; bảo đảm Lyapunov gốc không tự giữ sau bão hòa và lấy mẫu. Bản tóm tắt sử dụng kết quả đã lưu trong dự án, không tạo thêm lượt mô phỏng mới.')
doc.save(OUT/'tom_tat_de_tai_va_minh_chung.docx')
print(OUT/'tom_tat_de_tai_va_minh_chung.docx')
