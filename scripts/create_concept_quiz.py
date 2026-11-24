"""Generate a Vietnamese conceptual self-test with separate answer key."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/pdfdeps'))
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

for name,file in [('TimesVN','times.ttf'),('TimesVN-Bold','timesbd.ttf'),('TimesVN-Italic','timesi.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('TimesVN',normal='TimesVN',bold='TimesVN-Bold',italic='TimesVN-Italic')
styles={
 'title':ParagraphStyle('title',fontName='TimesVN-Bold',fontSize=18,leading=23,alignment=TA_CENTER,spaceAfter=10,textColor=HexColor('#173750')),
 'sub':ParagraphStyle('sub',fontName='TimesVN',fontSize=12,leading=16,alignment=TA_CENTER,spaceAfter=12),
 'h':ParagraphStyle('h',fontName='TimesVN-Bold',fontSize=13,leading=17,spaceBefore=11,spaceAfter=6,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='TimesVN',fontSize=12,leading=15,alignment=TA_JUSTIFY,spaceAfter=6),
 'small':ParagraphStyle('small',fontName='TimesVN',fontSize=10,leading=13,spaceAfter=5),
}
story=[]
def p(text,style='body'):story.append(Paragraph(text,styles[style]))
def answer(n,title,items):
 p(f'Câu {n}. {title} (2,0 điểm)','h')
 for i,t in enumerate(items,1):p(f'<b>Ý {i} - 0,5 điểm.</b> {t}')

p('KIỂM TRA TỰ LUẬN 30 PHÚT','title')
p('Hiểu tổng quát về T-ST-RHC và điều khiển Lyapunov<br/>Bối cảnh: robot di động hai bánh vi sai có giới hạn vận tốc','sub')
p('<b>Hình thức:</b> 5 câu, tổng 10 điểm. Không yêu cầu công thức, chứng minh toán học hay mã chương trình. Trả lời trên giấy riêng, mỗi câu khoảng 5-8 dòng. Tài liệu tự ôn tập, không phải đề thi chính thức.')
p('<b>Cách sử dụng:</b> Chỉ đọc trang này khi làm bài. Đặt đồng hồ 30 phút; sau khi hết giờ mới mở phần đáp án từ trang 2. Diễn đạt bằng lời của mình, có giải thích quan hệ nguyên nhân - kết quả.')
questions=[
 ('Bài toán và ý nghĩa của giới hạn vận tốc','5 phút','Thế nào là bám quỹ đạo theo thời gian? Vì sao đi đúng đường hình học vẫn có thể bám quỹ đạo sai? Giới hạn vận tốc hai bánh ảnh hưởng thế nào khi robot có sai lệch ban đầu lớn?'),
 ('Nguyên lý T-ST-RHC','7 phút','Trình bày vai trò của điểm điều khiển phía trước robot, giai đoạn chuẩn bị offline và tính toán online. Phân biệt cách xử lý khi sai số ở ngoài tập cuối và khi đã vào tập cuối. Vì sao không thể nói phương pháp luôn đưa mọi sai số về đúng không?'),
 ('Nguyên lý điều khiển Lyapunov','6 phút','Giải thích vai trò của hàm Lyapunov khi thiết kế luật bám quỹ đạo. Vì sao hàm này không tăng chưa đủ để kết luận tất cả sai số hội tụ về không? Điều gì cần xem xét lại khi thêm bão hòa vận tốc bánh?'),
 ('So sánh hai phương pháp','6 phút','So sánh T-ST-RHC với đối chứng Lyapunov có bão hòa của dự án về: cách xử lý giới hạn bánh, công việc tính toán và phạm vi bảo đảm. Có thể khẳng định một phương pháp luôn tốt hơn phương pháp còn lại không? Giải thích.'),
 ('Đánh giá một tình huống mô phỏng','6 phút','Một ca T-ST-RHC không vi phạm giới hạn bánh nhưng sai số bám vẫn lớn. Hãy giải thích vì sao hai hiện tượng này có thể cùng xảy ra, nêu những điều cần kiểm tra và đề xuất cách so sánh công bằng với đối chứng Lyapunov. Chỉ nhìn hình quỹ đạo có đủ kết luận không?'),
]
for i,(title,time,q) in enumerate(questions,1):
 p(f'Câu {i}. {title} (2,0 điểm; {time})','h');p(q)
story.append(PageBreak())
p('ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM','title')
p('Mỗi câu có 4 ý, mỗi ý tối đa 0,5 điểm. Chấp nhận cách diễn đạt tương đương, đúng bản chất. Có thể cho 0,25 điểm nếu ý đúng nhưng giải thích còn thiếu.','small')
answer(1,'Bài toán và giới hạn vận tốc',[
 'Bám quỹ đạo yêu cầu robot đến vị trí tham chiếu tại đúng thời điểm; trong bài toán này còn theo dõi hướng chuyển động tương ứng. Bám đường hình học chủ yếu yêu cầu đi theo hình dạng đường.',
 'Robot đi đúng đường nhưng chậm hơn hoặc nhanh hơn lịch tham chiếu vẫn có sai số tại cùng thời điểm. Vì vậy, hình quỹ đạo trùng nhau chưa chứng minh bám theo thời gian tốt.',
 'Giới hạn từng bánh hạn chế các chuyển động tiến và quay có thể thực hiện. Robot không thể tăng tùy ý tốc độ để sửa sai; một lệnh mong muốn có thể vượt khả năng cho phép.',
 'Sai lệch đầu lớn thường đòi hỏi hiệu chỉnh mạnh, có thể làm kéo dài quá độ hoặc gây khó khăn về khả thi. Khả năng bám phụ thuộc cả tham chiếu và miền điều khiển, không chỉ độ lớn sai số.'
])
answer(2,'Nguyên lý T-ST-RHC',[
 'Điểm phía trước giúp biến đổi mô hình động học sang dạng thuận lợi cho thiết kế điều khiển. Sai số của điểm này khác sai số tâm robot; bám tốt điểm phía trước chưa đủ kết luận tâm và hướng đều chính xác.',
 'Offline xây dựng tập cuối bất biến điều khiển bền vững và các tập có thể đưa sai số về tập trước. Các tập mô tả miền thu hút; tính bất biến có nghĩa tồn tại cách chọn điều khiển hợp lệ để giữ sai số trong tập, theo giả thiết thiết kế.',
 'Online dùng sai số và hướng hiện tại. Ngoài tập cuối, chọn lệnh thỏa giới hạn để đưa sai số về tập trước; trong tập cuối, dùng luật miền cuối để duy trì sai số trong miền cho phép và tận dụng tham chiếu.',
 'Bảo đảm có điều kiện về mô hình, tham chiếu, ràng buộc và miền khởi đầu. Mục tiêu bị chặn trong tập cuối không đồng nghĩa hội tụ chính xác về không, cũng không áp dụng cho mọi trạng thái đầu.'
])
answer(3,'Nguyên lý Lyapunov',[
 'Hàm Lyapunov là đại lượng vô hướng phản ánh mức sai lệch, tương tự một thước đo năng lượng toán học. Thiết kế luật để đại lượng này giảm hoặc không tăng nhằm phân tích ổn định; đó không nhất thiết là năng lượng điện của robot.',
 'Ổn định nghĩa là sai lệch ban đầu đủ nhỏ sẽ tiếp tục được giữ nhỏ; hội tụ còn yêu cầu sai lệch tiến về mục tiêu. Hai khái niệm liên quan nhưng không đồng nhất.',
 'Không tăng có thể vẫn cho phép một phần sai số tồn tại. Muốn kết luận toàn bộ sai số về không phải kiểm tra thêm điều kiện của định lý; với luật Blažič cần xét các điều kiện về tham chiếu và hướng.',
 'Bão hòa làm lệnh thực tế khác lệnh được dùng trong chứng minh gốc. Chặn lệnh giúp tuân giới hạn bánh nhưng không tự động bảo toàn ổn định hay hội tụ; cần phân tích lại hoặc giới hạn kết luận ở thử nghiệm đã thực hiện.'
])
story.append(PageBreak())
p('ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM','title')
answer(4,'So sánh hai phương pháp',[
 'T-ST-RHC đưa ràng buộc bánh vào bước chọn lệnh tối ưu. Đối chứng Lyapunov trong dự án tính lệnh theo luật tường minh, sau đó giới hạn từng bánh. Đây là so sánh với một triển khai cụ thể, không đại diện mọi phương pháp dựa trên Lyapunov.',
 'T-ST-RHC có chi phí chuẩn bị tập và tính toán online để tìm tập, giải tối ưu. Đối chứng thường ít tính toán hơn mỗi bước. Cần đo trên cùng môi trường để đánh giá chênh lệch thực tế.',
 'T-ST-RHC gắn bảo đảm với các tập và giả thiết mô hình. Luật Lyapunov gốc có bảo đảm theo điều kiện của chứng minh; sau lấy mẫu và bão hòa, không được mặc nhiên kế thừa đầy đủ bảo đảm đó.',
 'Không có ưu thế tuyệt đối: cần cân nhắc sai số bám, tuân ràng buộc, biến thiên lệnh và thời gian tính. Kết luận phải gắn với kịch bản và yêu cầu ứng dụng, thay vì chỉ chọn phương pháp có sai số nhỏ ở một ca.'
])
answer(5,'Phân tích tình huống và đánh giá công bằng',[
 'Tuân giới hạn là điều kiện về lệnh điều khiển, còn bám tốt là yêu cầu về trạng thái. Lệnh hợp lệ vẫn có thể không sửa sai kịp khi tham chiếu khó hoặc trạng thái đầu bất lợi; hai hiện tượng vì vậy không mâu thuẫn.',
 'Kiểm tra điều kiện dựng tập, sai số đầu trong miền thu hút, trạng thái bộ giải và dữ liệu lỗi. Đối chiếu sai số tâm, điểm phía trước và hướng; xem xét khác biệt giữa mô hình thiết kế và robot mô phỏng giữ lệnh bánh.',
 'Dùng cùng robot, tham chiếu theo thời gian, trạng thái đầu, giới hạn bánh, chu kỳ lấy mẫu, bộ tích phân và thời lượng. Chốt tham số đối chứng bằng hiệu chỉnh riêng trước đánh giá; giữ lại và báo rõ cả ca thất bại.',
 'Cần số liệu sai số trung bình/cực đại, sai số tích lũy, vi phạm bánh, biến thiên lệnh và thời gian tính, kèm đồ thị theo thời gian. Một hình đường đi không đủ chứng minh bám đúng thời điểm, ổn định hay ưu thế tổng quát.'
])
p('Tự kiểm tra sau khi chấm','h')
p('Với mỗi ý mất điểm, ghi lại: khái niệm mình nhầm, cách giải thích đúng và một ví dụ bằng lời. Không cộng điểm chỉ vì nêu đúng tên thuật toán; câu trả lời cần thể hiện quan hệ giữa nguyên lý, điều kiện áp dụng và giới hạn kết luận.','small')
p('Nguồn đối chiếu và phạm vi','h')
p('[1] C. Tiriolo, W. Lucia (2023), “A Set-Theoretic Control Approach to the Trajectory Tracking Problem for Input-Output Linearized Wheeled Mobile Robots”. DOI: 10.1109/LCSYS.2023.3286774. Bản tác giả: <link href="https://users.encs.concordia.ca/~wlucia/files/STMPC_tracking_robot2023.pdf" color="#173750">PDF tại Concordia</link>.','small')
p('[2] S. Blažič (2011), “A novel trajectory-tracking control law for wheeled mobile robots”, Robotics and Autonomous Systems, 59, 1001-1007. DOI: <link href="https://doi.org/10.1016/j.robot.2011.06.005" color="#173750">10.1016/j.robot.2011.06.005</link>.','small')
p('Câu 1-3: nguyên lý và điều kiện nền tảng; câu 4-5: vận dụng vào phạm vi dự án. Đối chứng được hiểu là luật Blažič với bão hòa từng bánh. Đề không yêu cầu nhớ kết quả số hoặc trình bày công thức. Biên soạn: 24/11/2026.','small')

out=ROOT/'output/pdf/kiem_tra_30_phut_T_ST_RHC_Lyapunov_dap_an.pdf';out.parent.mkdir(parents=True,exist_ok=True)
def footer(c,doc):
 c.setStrokeColor(HexColor('#c7d2db'));c.line(45,39,A4[0]-45,39)
 c.setFont('TimesVN',9);c.setFillColor(HexColor('#425466'))
 c.drawString(45,26,'TỰ ÔN TẬP | T-ST-RHC VÀ LYAPUNOV')
 c.drawRightString(A4[0]-45,26,f'Trang {doc.page}')
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=45,leftMargin=45,topMargin=38,bottomMargin=50,title='Kiểm tra tự luận 30 phút - T-ST-RHC và Lyapunov',author='Tài liệu tự ôn tập dự án Kỹ thuật Robot')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
r=PdfReader(out)
assert len(r.pages)==3,f'Unexpected pages: {len(r.pages)}'
assert 'Câu 5.' in r.pages[0].extract_text()
assert 'ĐÁP ÁN' in r.pages[1].extract_text()
print(f'{out}\nPages: {len(r.pages)}')
