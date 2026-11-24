"""Apply the supplied course guide to the existing report, preserving results."""
from pathlib import Path
from copy import deepcopy
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1]
TITLE='Mô phỏng và đánh giá điều khiển bám quỹ đạo robot di động hai bánh có giới hạn vận tốc bằng phương pháp T-ST-RHC trên MATLAB.'

def before(anchor,text,style='Normal'):
    return anchor.insert_paragraph_before(text,style)
def field(p,instruction):
    f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),instruction);p._p.append(f)

def format_document(doc):
    if any(p.text=='Chương 1. GIỚI THIỆU' for p in doc.paragraphs):return tidy_document(doc)
    for sec in doc.sections:
        sec.page_width=Cm(21);sec.page_height=Cm(29.7)
        sec.top_margin=Cm(2.2);sec.bottom_margin=Cm(2);sec.left_margin=Cm(2.65);sec.right_margin=Cm(2.15)
    for s in doc.styles:
        if s.type in (1,2):
            s.font.name='Times New Roman';s.font.size=Pt(13);s.font.color.rgb=RGBColor(0,0,0)
            fonts=s.element.get_or_add_rPr().get_or_add_rFonts()
            for k in list(fonts.attrib):
                if 'theme' in k.lower():del fonts.attrib[k]
            for k in ['ascii','hAnsi','eastAsia','cs']:fonts.set(qn('w:'+k),'Times New Roman')
    doc.styles['Title'].font.size=Pt(18)
    normal=doc.styles['Normal'].paragraph_format
    normal.line_spacing=1.3;normal.space_after=Pt(6);normal.alignment=3
    replacements={
      '1 Bài toán và mục tiêu':'Chương 1. GIỚI THIỆU',
      '2 Cơ sở lý thuyết và đối chiếu phương pháp':'Chương 2. CƠ SỞ LÝ THUYẾT',
      '3 Triển khai và tái lập':'Chương 3. NỘI DUNG NGHIÊN CỨU VÀ THỰC HIỆN',
      '4 Thiết kế thử nghiệm':'3.4. Công cụ và thiết lập thử nghiệm',
      '5 Kết quả và thảo luận':'Chương 4. KẾT QUẢ VÀ THẢO LUẬN',
      '6 Kết luận và giới hạn':'Chương 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN',
      'Động học và dấu':'2.2. Mô hình động học và quy ước dấu',
      'Tham chiếu':'2.3. Quỹ đạo tham chiếu theo thời gian',
      'Điểm phía trước và T-ST-RHC':'2.4. Tuyến tính hóa phản hồi và nguyên lý T-ST-RHC',
      'Đối chứng Blažič':'2.5. Bộ điều khiển đối chứng Lyapunov',
      'Đối chiếu':'2.6. Phân tích và đối chiếu hai phương pháp'}
    for p in list(doc.paragraphs):
        old=p.text
        if old in replacements:
            p.text=replacements[old];p.style='Heading 2' if old=='4 Thiết kế thử nghiệm' else p.style
            if p.text.startswith('Chương '):p.paragraph_format.page_break_before=True
    pars=doc.paragraphs
    ch1=next(p for p in pars if p.text=='Chương 1. GIỚI THIỆU')
    # Replace the former introductory block with front matter.
    for p in list(doc.paragraphs):
        if p._p is ch1._p:break
        p._element.getparent().remove(p._element)
    before(ch1,'ĐẠI HỌC ĐÀ NẴNG – TRƯỜNG ĐẠI HỌC BÁCH KHOA')
    before(ch1,'KHOA ĐIỆN TỬ VÀ TRÍ TUỆ NHÂN TẠO')
    before(ch1,'BÁO CÁO CUỐI KỲ HỌC PHẦN KỸ THUẬT ROBOT','Title')
    before(ch1,TITLE,'Title')
    before(ch1,'Sinh viên thực hiện: Nguyễn Đức Phúc; Đặng Văn Anh Nguyên')
    before(ch1,'Mã số sinh viên: .................................. Lớp: ........................')
    before(ch1,'Giảng viên hướng dẫn: PGS.TS Nguyễn Đăng Khoa')
    before(ch1,'Ngày lập báo cáo: 16 tháng 11 năm 2026')
    t=before(ch1,'MỤC LỤC','Heading 1');t.paragraph_format.page_break_before=True
    field(before(ch1,''),'TOC \\o "1-2" \\h \\z \\u')
    before(ch1,'DANH MỤC HÌNH VẼ','Heading 1')
    for i,id in enumerate(['eight_i2_w10_tstrhc','eight_i2_w10_lyapunov','circle_i3_w10_tstrhc','circle_i3_w10_lyapunov'],1):before(ch1,f'Hình {i}. Kết quả mô phỏng {id}.')
    before(ch1,'DANH MỤC BẢNG BIỂU','Heading 1')
    for p in list(doc.paragraphs):
        if p.style.name=='Caption' and p.text.startswith('Bảng '):before(ch1,p.text)
    before(ch1,'DANH MỤC TỪ VIẾT TẮT','Heading 1')
    for text in ['T-ST-RHC: Trajectory Tracking Set-Theoretic Receding Horizon Control.','RMSE: căn trung bình bình phương sai số.','IAE: tích phân trị tuyệt đối sai số.','QP: quy hoạch toàn phương; QCQP: quy hoạch toàn phương có ràng buộc toàn phương.','ET: Ellipsoidal Toolbox; MPT3: Multi-Parametric Toolbox 3.']:before(ch1,text)
    first=next(p for p in doc.paragraphs if p.text.startswith('Xét một robot hai bánh'))
    before(first,'1.1. Bối cảnh và ý nghĩa của đề tài','Heading 2')
    before(first,'Robot di động hai bánh vi sai có thể thực hiện nhiệm vụ vận chuyển trên nền phẳng theo lịch chuyển động đã định. Bám đúng đường hình học chưa đủ khi robot cần đến vị trí tại đúng thời điểm. Giới hạn vận tốc bánh làm giảm khả năng sửa sai lệch đầu, đặc biệt khi tham chiếu đổi hướng hoặc có độ cong lớn. Đề tài nghiên cứu vấn đề này bằng mô phỏng MATLAB, không khẳng định đã triển khai trên hệ thống vận chuyển thực tế.')
    target=next(p for p in doc.paragraphs if p.text.startswith('Các nội dung tương ứng') )
    before(target,'1.2. Mục tiêu chung và mục tiêu cụ thể','Heading 2')
    before(target,'Mục tiêu chung là tái lập và đánh giá T-ST-RHC trong bài toán bám quỹ đạo có giới hạn vận tốc bánh. Các mục tiêu cụ thể gồm kiểm chứng mô hình và mã kế thừa; xây dựng đối chứng Lyapunov có bão hòa; tổ chức thử nghiệm thống nhất; định lượng sai số, độ mượt và chi phí tính toán; giải thích các ca bất lợi.')
    ch2=next(p for p in doc.paragraphs if p.text.startswith('Chương 2.'))
    before(ch2,'1.3. Phạm vi thực hiện','Heading 2')
    before(ch2,'Nghiên cứu mô hình động học một robot hai bánh trên mặt phẳng, không trượt và biết trạng thái. Hai quỹ đạo là số 8 và đường tròn; khảo sát ba mức sai lệch đầu và ba giới hạn vận tốc. Chưa xét động cơ, nhiễu, sai số cảm biến hoặc chế tạo phần cứng.')
    before(ch2,'1.4. Cấu trúc báo cáo','Heading 2')
    before(ch2,'Chương 2 trình bày cơ sở lý thuyết. Chương 3 mô tả bài toán, phương pháp triển khai và thiết lập. Chương 4 trình bày kết quả, đánh giá và hạn chế. Chương 5 đối chiếu mục tiêu và đề xuất hướng phát triển.')
    theory=next(p for p in doc.paragraphs if p.text.startswith('2.2.'))
    before(theory,'2.1. Tổng quan bài toán và các nghiên cứu liên quan','Heading 2')
    before(theory,'Tiriolo và Lucia [1] khai thác tuyến tính hóa đầu ra và các tập điều khiển về đích để xử lý ràng buộc vận tốc. Blažič [2] xây dựng luật tường minh dựa trên hàm Lyapunov cho mô hình động học; bản đối chứng của dự án thêm bão hòa bánh và không kế thừa nguyên vẹn bảo đảm ổn định của luật gốc. Việc so sánh tập trung vào đánh đổi giữa chất lượng bám, ràng buộc và chi phí tính toán, thay vì giả định phương pháp tối ưu luôn tốt hơn.')
    anchors=[('Môi trường chạy là','3.1. Phát biểu bài toán và tiêu chí kiểm chứng'),('Luồng chạy:','3.2. Phương pháp tiếp cận và quy trình thực hiện'),('Đối chiếu tái cấu trúc','3.3. Triển khai và kiểm chứng kỹ thuật'),('Chiến dịch gồm','4.1. Kết quả mô phỏng'),('Với quỹ đạo eight','4.2. Phân tích và đánh giá'),('Mục tiêu tái lập','5.1. Kết luận theo mục tiêu')]
    for prefix,label in anchors:
        a=next(p for p in doc.paragraphs if p.text.startswith(prefix));before(a,label,'Heading 2')
    a=next(p for p in doc.paragraphs if p.text.startswith('Môi trường chạy là'))
    before(a,'Đầu vào gồm trạng thái q=[x,y,θ]ᵀ, tham chiếu vị trí và đạo hàm theo thời gian, cấu hình robot và giới hạn từng bánh. Đầu ra là vận tốc góc bánh phải và trái. Yêu cầu là bám tham chiếu trong giới hạn lệnh; đánh giá bằng RMSE, IAE, sai số cực đại, vi phạm bánh, biến thiên lệnh và thời gian toàn bước. Các ca ngoài điều kiện dựng tập phải được ghi nhận và không dùng để bác bỏ định lý gốc.')
    a=next(p for p in doc.paragraphs if p.text.startswith('Chương 5.'))
    before(a,'4.3. Hạn chế và nguyên nhân','Heading 2')
    before(a,'Ba ca số 8 ở 8 rad/s dừng do không đạt điều kiện tập. Một số ca tròn sai lệch đầu lớn có sai số cao và dao động lệnh, dù không vi phạm giới hạn bánh. Phép đối chiếu mô hình cho thấy khoảng cách giữa cập nhật tuyến tính và robot giữ lệnh có vai trò đáng kể. Cận tham chiếu hiện dựa trên lưới số; kết quả chưa bao gồm nhiễu, động cơ và robot thật.')
    a=next(p for p in doc.paragraphs if p.text=='Tài liệu tham khảo')
    before(a,'5.2. Hướng phát triển','Heading 2')
    for text in [
      'Ưu tiên khảo sát chu kỳ lấy mẫu nhỏ hơn và đánh giá lại phần dư giữa mô hình thiết kế và robot giữ lệnh. Mỗi thay đổi Ts phải tính lại tập và giữ cùng điều kiện giữa hai bộ điều khiển; không chỉ giảm Ts rồi quy kết toàn bộ cải thiện cho bộ giải.',
      'Khảo sát bổ sung thành phần phạt biến thiên lệnh trong mục tiêu T-ST-RHC để giảm dao động bánh. Cần quét trọng số trên bộ hiệu chỉnh riêng, sau đó so sánh RMSE, IAE, biến thiên lệnh và thời gian tính trên bộ đánh giá đã khóa. Đây là hướng đề xuất, chưa phải cải tiến đã được xác nhận.',
      'Mở rộng đối chứng sang cách xử lý bão hòa có cơ sở ổn định; sau khi hoàn tất đánh giá cơ bản mới thêm nhiễu và sai số mô hình với seed, mức nhiễu và số lần lặp công bố. Chưa suy ra khả năng thời gian thực hoặc hiệu quả trên robot thật từ số liệu máy mô phỏng.']:before(a,text)
    for p in doc.paragraphs:
        if p.style.name=='Normal':p.alignment=3;p.paragraph_format.line_spacing=1.3
        if p.style.name.startswith('Heading'):p.paragraph_format.keep_with_next=True
        for r in p.runs:
            r.font.name='Times New Roman'
            if p.style.name!='Title':r.font.size=Pt(13)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing=1.3
                    for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(13)
    for shape in doc.inline_shapes:
        ratio=shape.height/shape.width;shape.width=Cm(16);shape.height=int(shape.width*ratio)
    return tidy_document(doc)

def tidy_document(doc):
    for p in doc.paragraphs:
        if p.text.startswith('Chương '):p.paragraph_format.page_break_before=p.style.name=='Heading 1' and p.text.startswith('Chương 1.')
        if p.text.startswith('Ba ca số 8 ở 8 rad/s'):p.paragraph_format.keep_together=True
    for p in doc.paragraphs:
        if p.text=='MỤC LỤC':break
        p.alignment=1
    doc.sections[0].different_first_page_header_footer=True
    for shape in doc.inline_shapes:
        ratio=shape.height/shape.width;shape.width=Cm(15);shape.height=int(shape.width*ratio)
    return doc

if __name__=='__main__':
    target=ROOT/'report/bao_cao_robot_cap_nhat.docx'
    format_document(Document(target)).save(target)
