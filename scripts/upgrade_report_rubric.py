"""Evidence-based revision of the user's current report; never regenerates cover."""
from pathlib import Path
import csv,json,re,shutil
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'report/bao_cao_robot_cap_nhat.docx'
WORK=ROOT/'tmp/rubric_upgrade';WORK.mkdir(parents=True,exist_ok=True)
BACKUP=WORK/'before.docx'
if not BACKUP.exists():shutil.copy2(TARGET,BACKUP)
doc=Document(BACKUP)
def anchor(prefix):return next(p for p in doc.paragraphs if p.text.startswith(prefix) and not p.style.name.lower().startswith('toc'))
def add(a,text,style='Normal'):
 p=a.insert_paragraph_before(text,style);p.paragraph_format.line_spacing=1.3
 p.paragraph_format.space_after=Pt(6)
 if style=='Normal':p.alignment=3
 else:p.paragraph_format.keep_with_next=True
 for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(13)
 return p
def eq(a,text,label):
 p=add(a,'');p.alignment=1;p.paragraph_format.keep_together=True
 math=OxmlElement('m:oMath');run=OxmlElement('m:r');t=OxmlElement('m:t');t.text=text;run.append(t);math.append(run);p._p.append(math)
 p.add_run('    ('+label+')').font.size=Pt(13)
 return p
def table(a,caption,headers,rows):
 add(a,caption,'Caption')
 t=doc.add_table(rows=1,cols=len(headers));t.autofit=False
 for c,v in zip(t.rows[0].cells,headers):c.text=str(v)
 repeat=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(repeat)
 for row in rows:
  for c,v in zip(t.add_row().cells,row):c.text=str(v)
 for i,row in enumerate(t.rows):
  row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
  for c in row.cells:
   pr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');b.append(el)
   pr.append(b)
   if i==0:
    s=OxmlElement('w:shd');s.set(qn('w:fill'),'E7E6E6');pr.append(s)
   for p in c.paragraphs:
    p.paragraph_format.line_spacing=1.15;p.paragraph_format.space_after=Pt(4)
    for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(13);r.bold=i==0
 a._p.addprevious(t._tbl)
 return t

# Operational, measurable success, without inventing a tracking threshold.
a=anchor('1.3. Phạm vi')
add(a,'Tiêu chí xác nhận mục tiêu gồm: chạy hoàn chỉnh cấu hình nền; kiểm tra sai khác trước/sau tái cấu trúc trong dung sai công bố; áp dụng cùng mô hình, tham chiếu và giới hạn cho hai bộ điều khiển; lưu đầy đủ mọi cấu hình kể cả ca dừng; tái tạo bảng và hình từ dữ liệu. Một lượt “hoàn thành” chỉ nghĩa là đủ mẫu và không có lỗi bộ giải, không đồng nghĩa sai số bám đạt một ngưỡng chất lượng ứng dụng. Dự án chưa đặt ngưỡng sai số công nghiệp vì chưa có yêu cầu tải, độ chính xác và an toàn của một robot cụ thể.')

# Deeper theoretical explanation and all missing optimization interfaces.
a=anchor('2.5. Bộ điều khiển')
add(a,'2.4.1. Ý nghĩa hình học và điều kiện bảo đảm','Heading 3')
add(a,'Trong cận sai số tâm đã nêu, h(θ)=[cosθ,sinθ]ᵀ là vector hướng đơn vị, khác với vô hướng h=1+ec/a của luật Blažič. Ký hiệu N_s chỉ số tập mở rộng, còn N ở Mục 3.1.1 là số lệnh đánh giá; trong mã lần lượt là Nsets và N bước mô phỏng.')
add(a,'Với b>0, điểm z nằm cách tâm robot một khoảng b theo hướng tiến. Đạo hàm z bằng ma trận M(θ) nhân [v,ω]ᵀ, trong đó det M=b. Vì vậy phép đổi đầu vào khả nghịch. Điều này giải thích vì sao điều khiển hai tọa độ điểm phía trước thuận tiện hơn điều khiển trực tiếp đồng thời ba tọa độ tâm; hướng vẫn là động học nội và phải được theo dõi riêng. Công thức (2.6) là nghịch đảo M, không phải nghịch đảo mô hình động học ba trạng thái [1].')
add(a,'Các tập trong (2.9) là cầu đồng tâm trong không gian sai số điểm phía trước. Định nghĩa tường minh trong (2.19) cho phép kiểm tra tư cách thành viên mà không phụ thuộc cách lưu ma trận trong mã. Dùng chỉ số lý thuyết i=0 cho tập cuối; chỉ số mảng MATLAB tương ứng là i+1.')
eq(a,'T_i={e∈ℝ² : e^T Q_i^(−1)e≤1},  Q_i=r_i²I₂,  X_(N_s)=⋃_(i=0)^(N_s) T_i','2.19')
add(a,'Trong mô hình thiết kế, sai số một bước có nhiễu d_k=−T_s u_r,k. Nếu ‖u_r,k‖≤ρ thì ‖d_k‖≤T_sρ=r₀. Luật u=−e/T_s làm phần danh định bằng không; do đó trạng thái kế tiếp nằm trong T₀ khi đầu vào này hợp lệ. Điều kiện ρ<r_u cung cấp dư địa điều khiển để mở rộng các cầu, với độ tăng bán kính Δr=T_s(r_u−ρ). Đây là cơ sở của bất biến bền vững và các tập điều khiển về đích trong [1].')
add(a,'Với ‖e‖≤r_i, có thể chọn đầu vào trong cầu bảo thủ để phần danh định còn bán kính không lớn hơn r_(i−1)−r₀. Cộng mọi nhiễu trong D vẫn đưa sai số vào T_(i−1). Lặp lập luận cho thấy chỉ số tập có thể giảm về 0 trong hữu hạn bước trong mô hình và giả thiết của nguồn. Online tận dụng hướng hiện tại và u_r đã biết để bớt bảo thủ; không có nghĩa đây là MPC tuyến tính hóa cục bộ hoặc một bài toán dự báo dài N mẫu được giải lại ở mỗi bước.')
add(a,'Dự án kiểm tra ρ bằng lưới dày và biên số, chưa chứng nhận cận trên liên tục bằng giải tích. Ngoài ra, chuyển động dưới lệnh bánh giữ hằng làm θ thay đổi trong chu kỳ, nên cập nhật z thực không đúng tuyệt đối với hai bộ tích phân rời rạc dùng thiết kế. Hai điểm này giới hạn phạm vi viện dẫn bảo đảm của [1]; dữ liệu mô phỏng được dùng để đánh giá hành vi, không thay cho chứng minh tính khả thi đệ quy trên một mô hình khác.')
add(a,'2.4.2. Ràng buộc bánh và bài toán ở miền cuối','Heading 3')
add(a,'Trong (2.20), Ω là giới hạn đối xứng của từng bánh, H_d có kích thước 4×2 và 1₄ là vector bốn phần tử bằng 1. T có kích thước 2×2; H phụ thuộc θ hiện tại. Bởi vậy H u≤1₄ chính là bốn bất đẳng thức của vận tốc hai bánh sau chuyển đổi, không phải giới hạn độc lập tùy ý cho v và ω.')
eq(a,'H_d=(1/Ω)[−1,0;0,−1;1,0;0,1],  H(θ)=H_d T^(−1)T_FL(θ)','2.20')
add(a,'Ở miền cuối, u₀=−e/T_s được giữ và chỉ hiệu chỉnh phần bù tham chiếu. Phương trình (2.21) viết đầy đủ bài toán được gọi bằng quadprog. Chọn H_QP=I₂ và f_QP=−u_r cho hàm mục tiêu bằng một nửa bình phương khoảng cách, bỏ hằng số; nghiệm không đổi so với tối thiểu ‖û_r−u_r‖² [7].')
eq(a,'û_r=arg min_(ξ∈ℝ²) (1/2)‖ξ−u_r‖²,   H(u₀+ξ)≤1₄;   u=u₀+û_r','2.21')
add(a,'Ở miền ngoài, biến tối ưu û là phần hiệu chỉnh, còn lệnh áp dụng là u=û+u_r. Do đó (2.10) tối thiểu sai số dự đoán e+T_sû và (2.11) buộc phần dự đoán vào tập trước. Dự án giữ mục tiêu của mã repo, chưa thêm phạt nỗ lực hay biến thiên; khác biệt với mục tiêu thực nghiệm bài báo được công bố ở Phụ lục A.')
a=anchor('2.6. Phân tích')
add(a,'Bão hòa đối chứng được định nghĩa rõ trong (2.22), với j∈{R,L}. Từ lệnh [v,ω] của (2.15)–(2.16), trước tiên tính ω_req=T⁻¹[v,ω]ᵀ, sau đó giới hạn từng thành phần. Hai bánh có thể bị giới hạn khác nhau nên tỉ lệ v/ω và độ cong chuyển động có thể đổi; vì vậy không viện dẫn nguyên vẹn đạo hàm Lyapunov không bão hòa cho lệnh đã áp dụng.')
eq(a,'ω_(j,app)=max(−Ω,min(Ω,ω_(j,req))),  j∈{R,L}','2.22')
add(a,'Trong chứng minh liên tục của [2], V̇≤0 cho tính không tăng của V, nhưng hội tụ của sai số ngang còn cần điều kiện kích thích từ vận tốc tham chiếu và tính liên tục thích hợp. Sai số sin/cos hướng phải được xét trên quan hệ es²+(ec+1)²=1; không chỉ từ es→0 suy ra ngay θ−θ_r→0. Phần đối chứng trong dự án được xác nhận bằng đẳng thức đạo hàm trước bão hòa, kiểm tra riêng và dữ liệu vòng kín sau bão hòa, chứ không bằng tuyên bố ổn định toàn cục mới.')

# Reproducible metrics, numerically identical to compute_metrics.m.
a=anchor('3.2. Phương pháp')
add(a,'3.1.1. Định nghĩa chỉ số và khoảng đánh giá','Heading 3')
add(a,'Với N lệnh giữ hằng, có N+1 mẫu trạng thái tại t_k=kT_s, k=0,…,N. Các ca chính dùng N=294, t_N=44,1 s; lấy cả trạng thái đầu khi tính RMSE và sai số cực đại. Bảng 7 dùng các mẫu trạng thái này; Bảng 8 dùng N mẫu lệnh. Quy ước này tránh ghép trạng thái cuối với một lệnh không tồn tại.')
eq(a,'e_p(k)=√((x_k−x_r,k)²+(y_k−y_r,k)²)','3.1')
eq(a,'RMSE=√((1/(N+1))∑_(k=0)^N e_p(k)²),   E_max=max_(0≤k≤N)e_p(k)','3.2')
eq(a,'IAE=∑_(k=0)^(N−1) ((e_p(k)+e_p(k+1))/2)(t_(k+1)−t_k)','3.3')
add(a,'RMSE và E_max có đơn vị m; IAE có đơn vị m·s và được tính bằng quy tắc hình thang, tương ứng trapz(t_state,ep). Sai số điểm phía trước được lưu dạng vector e_z=z−z_r; RMSE phía trước tính bằng căn trung bình ‖e_z‖². Sai số hướng dùng atan2(sin(θ−θ_r),cos(θ−θ_r)), có đơn vị rad và nằm trong [−π,π].')
eq(a,'TV=∑_(k=1)^(N−1)‖ω_app(k)−ω_app(k−1)‖₂²','3.4')
add(a,'TV đo độ biến thiên vector lệnh hai bánh, đơn vị (rad/s)². Cùng T_s và khoảng đánh giá mới cho phép so trực tiếp; TV nhỏ biểu thị lệnh ít biến thiên hơn theo chỉ số này, không chứng minh gia tốc bánh nhỏ ở mọi thời điểm và không đại diện tiêu thụ năng lượng.')
eq(a,'n_j=∑_(k=0)^(N−1)1{|ω_(j,app)(k)|>Ω+ε_ω},   P_j=n_j/N','3.5')
eq(a,'δ_j=max_(0≤k<N)max(0,|ω_(j,app)(k)|−Ω),   ε_ω=10^(−7) rad/s','3.6')
add(a,'Trong (3.5)–(3.6), dung sai vận tốc εω=10⁻⁷ rad/s; 𝟙{điều kiện} bằng 1 khi điều kiện đúng và bằng 0 khi sai. Phép max trong δ_j lấy trên mọi mẫu lệnh của bánh j, không lấy trên mẫu trạng thái cuối.')
add(a,'n_j là số mẫu vi phạm của bánh j, P_j là tỉ lệ và δ_j là mức vượt lớn nhất. Bảng 8 gộp n_R+n_L nên một thời điểm có thể đóng góp hai mẫu bánh; bảng đầy đủ từng bánh nằm trong tables/summary.csv. Bão hòa khác vi phạm: saturationCount đếm thời điểm lệnh yêu cầu của đối chứng bị thay đổi bởi giới hạn, dù lệnh áp dụng vẫn hợp lệ. T-ST-RHC không bị cắt lệnh để che nghiệm sai ràng buộc.')
add(a,'Thời gian toàn bước đo từ trước tính sai số/ràng buộc, tìm tập và giải tối ưu đến sau chuyển sang lệnh bánh. Không đo tích phân robot, vẽ hình hoặc ghi tệp trong đoạn này. Mỗi cấu hình khởi động 10 bước rồi đo 5 lần. Các chỉ số mean, p95, max và số bước vượt T_s được gộp trên các mẫu hợp lệ của 5 lần; độ lệch chuẩn trung bình giữa 5 lần được lưu riêng. p95 dùng prctile(...,95) trên MATLAB R2023a, không thay bằng phần tử xếp hạng tùy ý. Nếu không có mẫu hợp lệ thì chỉ số là NaN, không phải thời gian bằng 0.')
add(a,'Mỗi nghiệm tối ưu phải có exitflag>0, giá trị hữu hạn và dư ràng buộc chuẩn hóa ≤10⁻⁷. Nếu không đạt, lượt chạy dừng và lưu lỗi; các chỉ số toàn khoảng để NaN, không tính trên đoạn ngắn rồi đem so với lượt đủ 44,1 s. Các lần lặp xác định dùng để mô tả thời gian, không phải mẫu thống kê độc lập về nhiễu.')
a=anchor('3.3. Triển khai')
add(a,'3.2.1. Thuật toán điều khiển và điều kiện dừng','Heading 3')
steps=[
'Offline: đọc cấu hình robot, T_s, b, Ω và luật thời gian tham chiếu; tạo vị trí, đạo hàm, hướng và u_r; kiểm tra tốc độ tham chiếu khác 0.',
'Tính ρ, r_u, T₀ và các T_i. Nếu ρ≥r_u hoặc e(0) ngoài X_N thì gắn nhãn ngoài điều kiện thiết kế và không gọi tối ưu với các tập không hợp lệ. Chỉ tái sử dụng tập khi mọi tham số ảnh hưởng được giữ nguyên.',
'Online tại k: đọc q_k và tham chiếu cùng t_k, tính e=z(q_k)−z_r,k, T_FL(θ_k) và H(θ_k). Tìm i nhỏ nhất sao cho ‖e‖≤r_i+10⁻⁹ m; nếu không tìm được thì dừng và ghi lỗi ngoài miền.',
'Nếu i>0, giải QCQP (2.10)–(2.11) bằng fmincon. Nếu i=0, tính u₀=−e/T_s và giải QP (2.21) bằng quadprog. Ghi chỉ số tập, exitflag, số vòng lặp và dư ràng buộc.',
'Kiểm tra nghiệm rồi đổi ω=T⁻¹T_FL u. Giữ ω trong một chu kỳ và tích phân động học bằng ode45. Lưu trạng thái ở t_(k+1), lệnh ở t_k và chuyển sang mẫu kế tiếp.',
'Với đối chứng, dùng cùng trạng thái/tham chiếu và bộ tích phân; thay bước tối ưu bằng (2.15)–(2.16), sau đó áp dụng (2.22). Lưu cả ω_req và ω_app để tách hiện tượng bão hòa khỏi vi phạm.']
for i,s in enumerate(steps,1):add(a,f'Bước {i}. {s}')
add(a,'Lựa chọn T-ST-RHC phù hợp vì ràng buộc bánh được đưa vào tối ưu thông qua H(θ), còn phần tính tập chuyển khỏi vòng online. Đối chứng tường minh có chi phí thấp, giúp đánh giá lợi ích của xử lý ràng buộc trong tối ưu. Hạn chế của lựa chọn này là cần miền khả thi, chuẩn bị lại tập khi đổi cấu hình và chịu ảnh hưởng của sai khác mô hình lấy mẫu. Các chức năng hình học ET/MPT3 được kiểm tra đúng lớp; dự án không yêu cầu hay xác nhận toàn bộ chức năng SDP của các toolbox [3]–[5].')
a=anchor('3.4. Công cụ')
env=json.loads((ROOT/'results/environment.json').read_text(encoding='utf-8-sig'))
add(a,f"Thông tin máy đo: {env['cpu']['Name']}, {env['cpu']['NumberOfCores']} nhân/{env['cpu']['NumberOfLogicalProcessors']} luồng, RAM hệ điều hành nhận {env['ramBytes']/2**30:.2f} GiB. MATLAB R2023a có Optimization Toolbox; hai bài toán tối ưu dùng fmincon và quadprog [6], [7], động học tích phân bằng ode45 [8]. Đây là máy đo mô phỏng, không phải bộ xử lý trên robot.")
add(a,'T_s=0,15 s, r=0,0205 m, d=0,053 m và b=0,1 m được giữ từ cấu hình repo để đối chiếu tái lập. b>0 bảo đảm khả nghịch nhưng cũng tạo sai khác giữa điểm điều khiển và tâm; dự án chưa khảo sát tối ưu b. N=700 là số tập mở rộng kế thừa để bao phủ miền đầu khảo sát, không được gọi là số tối thiểu hoặc tối ưu. Ba mức Ω=8/10/12 rad/s khảo sát thiếu, gần và dư khả năng điều khiển so với tham chiếu; không đồng thời giảm tốc tham chiếu khi đổi Ω.')
add(a,'Các mức đầu thay đồng thời sai lệch vị trí và hướng, vì vậy kết luận là ảnh hưởng của điều kiện đầu tổng hợp, chưa tách riêng ảnh hưởng x và θ. Lưới hiệu chỉnh đối chứng được chốt trên bốn ca riêng; góc π của mức lớn nằm ngoài góc π/6 dùng hiệu chỉnh. Do đó thông số là nghiệm tốt nhất trên lưới đã công bố, chưa bảo đảm tối ưu hoặc đại diện mọi miền góc. Tính công bằng ở đây là thống nhất mô hình và cách hiệu chỉnh minh bạch, không phải hai phương pháp phải có cùng số tham số.')

# Quantitative trade-off analysis, read from actual records.
rows=list(csv.DictReader((ROOT/'tables/summary.csv').open(encoding='utf-8-sig')))
byid={r['run_id']:r for r in rows}
a=anchor('Ca circle_i3_w10_tstrhc')
add(a,'4.2.1. Đánh đổi sai số độ mượt và thời gian tính','Heading 3')
for prefix in ['eight_i2_w10','circle_i3_w10']:
 st,ly=byid[prefix+'_tstrhc'],byid[prefix+'_lyapunov']
 ratio=lambda key:float(st[key])/float(ly[key])
 add(a,f"Với {prefix}, RMSE T-ST-RHC/Lyapunov lần lượt {float(st['rmse']):.5g}/{float(ly['rmse']):.5g} m; IAE {float(st['iae']):.5g}/{float(ly['iae']):.5g} m·s. Tỉ số ST/LY là {ratio('rmse'):.3g} cho RMSE, {ratio('commandVariation'):.3g} cho TV và {ratio('timingP955'):.3g} cho p95 thời gian. Cả hai không có mẫu bánh vi phạm trong cấu hình này. Các con số được tính từ dữ liệu Bảng 7–8 và tables/summary.csv, không đổi điều kiện thử.")
add(a,'Ở ca số 8 mức đầu vừa, RMSE giảm khoảng 48,2% nhưng TV tăng khoảng 34,1 lần và p95 tăng khoảng 122 lần. Vì mục tiêu hiện tại ưu tiên sai số dự đoán mà không phạt Δω, nghiệm có thể sửa sai mạnh hơn và tạo lệnh biến thiên lớn. Trên ca tròn mức đầu lớn, ST vừa có sai số cao hơn vừa có TV lớn hơn; đây là trường hợp đối chứng có lợi hơn theo các chỉ số đang xét, không nên che bằng kết luận trung bình toàn bộ quỹ đạo.')
add(a,'Ở số 8 mức đầu 3, tăng Ω từ 10 lên 12 rad/s làm RMSE tăng từ 0,09679 lên 0,1048 m và TV tăng từ 5627 lên khoảng 14740 (rad/s)². Việc nới miền lệnh chỉ mở rộng lựa chọn tức thời, không bảo đảm cải thiện vòng kín với cập nhật giữ lệnh. Bảng 7 cũng cho thấy RMSE mức đầu 1 gần như không đổi khi Ω từ 10 lên 12; khi giới hạn không chi phối mạnh, nới thêm không nhất thiết đem lại lợi ích.')
add(a,'Các chỉ số này chưa đủ để chọn một bộ điều khiển “tốt nhất” độc lập ứng dụng. Nếu ưu tiên sai số nhỏ và có ngân sách tính toán, ST có lợi trong nhiều cặp hoàn thành; nếu ưu tiên chi phí tính thấp và ít biến thiên lệnh thì Lyapunov có lợi ở nhiều ca. Chưa có mô hình công suất nên không quy TV thành mức tiêu hao năng lượng. Cần kiểm tra thêm giới hạn gia tốc bánh trước khi chuyển kết quả sang robot có cơ cấu chấp hành thực.')

# Improve ambiguous state-unit wording and completeness of references.
for p in doc.paragraphs:
 if p.text.startswith('Max sai khác') or 'Max sai khác thành phần trạng thái ode45' in p.text:
  p.text=p.text.replace('theo đơn vị m hoặc rad của thành phần tương ứng.','Giá trị này là cực đại thành phần của vector gồm cả m và rad, chỉ dùng chẩn đoán số; không diễn giải thành một chuẩn vật lý chung.')
ref=anchor('Tài liệu tham khảo')
following=[];found=False
for p in list(doc.paragraphs):
 if p._p is ref._p:found=True;continue
 if found and re.match(r'^\s*\d+\.',p.text):following.append(p)
references=[
'[1] C. Tiriolo and W. Lucia, “A Set-Theoretic Control Approach to the Trajectory Tracking Problem for Input–Output Linearized Wheeled Mobile Robots,” IEEE Control Systems Letters, vol. 7, pp. 2347–2352, 2023, doi: 10.1109/LCSYS.2023.3286774.',
'[2] S. Blažič, “A novel trajectory-tracking control law for wheeled mobile robots,” Robotics and Autonomous Systems, vol. 59, no. 11, pp. 1001–1007, 2011, doi: 10.1016/j.robot.2011.06.005.',
'[3] C. Tiriolo, “T_ST_RHC_mobile_robots,” mã MATLAB, commit c57e98262ff21d8bab711b892a14c7afc98e0c08, giấy phép Apache-2.0. [Trực tuyến]. https://github.com/cristiri/T_ST_RHC_mobile_robots/tree/c57e98262ff21d8bab711b892a14c7afc98e0c08. Truy cập: 16/11/2026.',
'[4] M. Herceg, M. Kvasnica, C. N. Jones, and M. Morari, “Multi-Parametric Toolbox 3.0,” in Proc. European Control Conference, Zurich, Switzerland, 2013, pp. 502–510. Mã sử dụng: https://github.com/kvasnica/mpt3/tree/76d28640251c0403f2c11deac9b0b2d7ee3759d0. Truy cập: 16/11/2026.',
'[5] System Analysis Department, CMC MSU, “Ellipsoidal Toolbox,” commit 715ed570b52fc4c04bb86994b0cbeaa7b5fa0b37. [Trực tuyến]. https://github.com/systemanalysisdpt-cmc-msu/ellipsoids/tree/715ed570b52fc4c04bb86994b0cbeaa7b5fa0b37. Truy cập: 16/11/2026.',
'[6] MathWorks, “fmincon — Solve constrained nonlinear multivariable minimization problem.” [Trực tuyến]. https://www.mathworks.com/help/optim/ug/fmincon.html. Truy cập: 16/11/2026.',
'[7] MathWorks, “quadprog — Quadratic programming.” [Trực tuyến]. https://www.mathworks.com/help/optim/ug/quadprog.html. Truy cập: 16/11/2026.',
'[8] MathWorks, “ode45 — Solve nonstiff differential equations.” [Trực tuyến]. https://www.mathworks.com/help/matlab/ref/ode45.html. Truy cập: 16/11/2026.']
for p in following:p._element.getparent().remove(p._element)
# A stable end anchor works even if the user removed the former appendix.
end=doc.add_paragraph('Phụ lục A. Ký hiệu và hồ sơ tái lập','Heading 1')
for text in references:add(end,text)
add(end,'Tài liệu [6]–[8] là trang trực tuyến hiện hành; mã được chạy trên R2023a và dùng các tùy chọn khả dụng trên phiên bản đó. Thông tin kết quả gốc được dẫn [1]; các bảng và hình mô phỏng trong báo cáo là dữ liệu tự chạy của dự án, không phải số liệu thực nghiệm sao chép từ bài báo.')

# Appendices keep long evidence tables out of the main argument.
a=doc.add_paragraph('Phụ lục B. Kết quả tái lập cấu hình nền','Heading 1')
add(a,'Bảng A.1 là bảng ký hiệu dùng trong (2.1)–(3.6). Quy ước bánh phải đứng trước bánh trái; T_i là tập, T là ma trận chuyển đổi, T_s là chu kỳ. Các ký hiệu có cùng chữ nhưng khác vai trò được phân biệt bằng chỉ số.')
table(a,'Bảng A.1. Ký hiệu chính và đơn vị',['Ký hiệu','Ý nghĩa','Đơn vị'],[
 ('q; q_r','Trạng thái thực và tham chiếu [x,y,θ]ᵀ','m, m, rad'),('r; d; b','Bán kính bánh; khoảng cách bánh; khoảng cách điểm điều khiển','m'),('ω_R; ω_L; Ω','Vận tốc bánh phải/trái; giới hạn từng bánh','rad/s'),('v; ω','Vận tốc tiến và quay của thân robot','m/s; rad/s'),('z; z_r; e','Điểm phía trước, tham chiếu và sai số z−z_r','m'),('u; u_r; û','Đầu vào tuyến tính hóa; tham chiếu; hiệu chỉnh','m/s'),('ρ; r_u','Cận chuẩn u_r; bán kính miền đầu vào bảo thủ','m/s'),('T_i; r_i; Q_i','Tập sai số; bán kính; ma trận dạng','m; m² cho Q_i'),('N; i','Số lệnh đánh giá; chỉ số tập','không thứ nguyên'),('e_x; e_y; e_s; e_c','Sai số cục bộ và sin/cos hướng theo [2]','m; m; 1; 1')])
add(a,'Bảng A.2 phân biệt cấu hình mô phỏng repo với thực nghiệm bài báo. Giá trị d và D được giữ đúng nguồn; chưa có căn cứ để tự ý nhân hoặc chia hai. Chọn lại hình học robot là thay đổi mô hình và đòi tính lại tập.')
table(a,'Bảng A.2. Cấu hình repo và thực nghiệm nguồn [1], [3]',['Thông số','Repo mô phỏng','Thực nghiệm bài báo'],[
 ('r hoặc R (m)','0,0205','0,021'),('d hoặc D (m)','0,053','0,1047'),('b (m)','0,1','Không nêu tường minh trong đoạn thiết lập'),('T_s (s); Ω (rad/s)','0,15; 10','0,15; 10'),('Quỹ đạo','0,6sin(t/3,5); 0,6sin(t/7)','Cùng luật số 8'),('q(0)','[0,6;0;π]ᵀ','[0,6;0;π]ᵀ'),('Tập mở rộng','700 + tập cuối','396 theo đoạn thực nghiệm'),('Mục tiêu ngoài miền cuối','Bình phương sai số dự đoán','Thêm 0,5‖u‖²'),('Mô hình thực thi','ode45, giữ lệnh bánh','Robot thật, odometry'),('Phiên bản MATLAB nguồn','README: R2022a','Mục IV: R2022b')])
add(a,'Mọi bảng và hình có thể truy lại từ results/<run_id>/run.mat. Mỗi lượt lưu cấu hình, trục thời gian, trạng thái/tham chiếu, lệnh yêu cầu/áp dụng, tập, trạng thái bộ giải, thời gian và SHA-256 mã. Dữ liệu nguyên bản ở results/baseline; hai lần lỗi môi trường ở baseline_attempt01/02; kiểm tra số ở baseline_comparison.json. Không coi file kiểm tra “đạt” là thay cho giải thích công thức hoặc dữ liệu gốc.')
end=doc.add_paragraph('Kết thúc phụ lục')
evidence=json.loads((ROOT/'results/report_evidence.json').read_text())
b=evidence['baseline'];comparison=evidence['comparison']
add(end,'Bản mã nguyên trạng được giữ ở original/provided và có giấy phép [3]. Hai lần chạy đầu bị chặn bởi việc nhận diện lớp ellipsoid và lỗi vẽ ET. Bản original/repaired bỏ duy nhất plot(ell_d); không sửa luật điều khiển. MPT3 dùng adapter chữ ký linprog, ET nạp cấu hình và Java hỗ trợ. Sửa môi trường được tách khỏi thay đổi thiết lập số của profile validated.')
add(end,f"Bảng B.1 và Hình 5 là kết quả tự tái lập trên MATLAB R2023a, không phải kết quả thực nghiệm tác giả. Có {b['samples']} lệnh; khoảng áp dụng lệnh là {b['controlDuration']:.2f} s. Để khớp phép đo eps gốc, các chỉ số nền dưới đây dùng trạng thái trước điều khiển từ t=0 đến {b['metricDuration']:.1f} s, không trộn với khoảng 44,1 s của 36 ca chính. eps gốc là MSE nên lấy căn để báo RMSE.")
table(end,'Bảng B.1. Chỉ số lần tái lập và sai khác sau tái cấu trúc',['Đại lượng','Giá trị','Nguồn'],[
 ('RMSE tâm trước điều khiển (m)',f"{b['rmsePrecontrol']:.6g}",'baseline.mat'),('IAE hình thang (m·s)',f"{b['iaePrecontrol']:.6g}",'baseline.mat'),('Sai số cực đại (m)',f"{b['maxErrorPrecontrol']:.6g}",'baseline.mat'),('Max |ω| (rad/s)',f"{b['maxWheel']:.8g}",'baseline.mat'),('Mẫu bánh vi phạm',str(b['violationCount']),'ε_ω=10⁻⁷ rad/s'),('Max sai khác thành phần vị trí (m)',f"{comparison['maxPositionComponent']:.6g}",'baseline_author so baseline'),('Max sai khác hướng (rad)',f"{comparison['maxHeadingDifference']:.6g}",'baseline_author so baseline')])
add(end,'Đối chiếu cấu trúc dùng cùng options bộ giải và lưới đầu ra ode45 của tác giả; dung sai vị trí 1 mm, hướng 0,001 rad và bánh 0,1 rad/s đã được công bố trước so sánh. Profile validated đổi thiết lập số nên có kết quả khác lớn hơn ngưỡng; báo cáo không dùng kết quả khớp của profile author để tuyên bố hai profile tương đương số.')
selected=['eight_i2_w10_tstrhc','eight_i2_w10_lyapunov','circle_i3_w10_tstrhc','circle_i3_w10_lyapunov']
add(end,'Bảng B.2 bổ sung biến thiên thời gian trên bốn ca đã vẽ ở Hình 1–4; đầy đủ 36 cấu hình nằm trong CSV. Mean, p95 và max gộp năm lần; SD là độ lệch chuẩn của năm thời gian trung bình. E2 là số 8 mức 2, T3 là tròn mức 3; cả bốn cùng Ω=10 rad/s.')
table(end,'Bảng B.2. Thời gian toàn bước của ca đại diện (ms)',['Ca','Mean','p95','Max','SD mean'],[(label,)+tuple(f"{float(byid[id][key])*1000:.5g}" for key in ['timingMean5','timingP955','timingMax5','timingStdMeans5']) for label,id in zip(['E2-ST','E2-LY','T3-ST','T3-LY'],selected)])
add(end,'Bảng B.3 phân biệt độ chính xác tại tâm và tại điểm điều khiển. Số bão hòa thuộc lần đánh giá đại diện thứ nhất; ST không cắt lệnh, nên giá trị 0 không có nghĩa bộ điều khiển chưa từng hoạt động sát biên. Mức vượt bánh của các lượt hoàn thành không vượt dung sai; dữ liệu từng bánh vẫn được giữ để kiểm tra.')
table(end,'Bảng B.3. Sai số cực đại và bão hòa trên ca đại diện',['Ca','E_max (m)','RMSE z (m)','Mẫu bão hòa'],[(label,f"{float(byid[id]['maxError']):.5g}",f"{float(byid[id]['frontRMSE']):.5g}",byid[id]['saturationCount']) for label,id in zip(['E2-ST','E2-LY','T3-ST','T3-LY'],selected)])
p=add(end,'Hình 5 cho phép đối chiếu trực quan quỹ đạo, sai số, vận tốc bánh và chỉ số tập của lượt nền. Nguồn: results/baseline/baseline.mat, hình được sinh bằng export_report_evidence.m.');p.paragraph_format.keep_with_next=True
p=add(end,'');r=p.add_run();r.add_picture(str(ROOT/'figures/baseline_report.png'),width=Cm(15));p.paragraph_format.keep_with_next=True
add(end,'Hình 5. Kết quả tự tái lập cấu hình nền của mã tác giả.','Caption')
end._element.getparent().remove(end._element)

# Turn original numbered mathematical paragraphs into native Office equations.
for p in list(doc.paragraphs):
 m=re.search(r'\s+\((2\.\d+)\)\s*$',p.text)
 if m and not p._p.xpath('.//m:oMath'):
  raw=p.text[:m.start()].strip();p.clear();math=OxmlElement('m:oMath');r=OxmlElement('m:r');t=OxmlElement('m:t');t.text=raw;r.append(t);math.append(r);p._p.append(math);p.add_run('    ('+m.group(1)+')');p.alignment=1

# Rebuild front lists with actual Word PAGEREF fields and stable bookmarks.
paras=list(doc.paragraphs)
start=next(p for p in paras if p.text=='DANH MỤC HÌNH VẼ' and p.style.name=='Heading 1')
finish=next(p for p in paras if p.text=='DANH MỤC TỪ VIẾT TẮT' and p.style.name=='Heading 1')
active=False
for p in list(doc.paragraphs):
 if p._p is start._p:active=True;continue
 if p._p is finish._p:break
 if active:p._element.getparent().remove(p._element)
plot_ids=['eight_i2_w10_tstrhc','eight_i2_w10_lyapunov','circle_i3_w10_tstrhc','circle_i3_w10_lyapunov']
for p in doc.paragraphs:
 if p.style.name=='Caption':
  match=re.match(r'^Hình\s+([1-4])\b',p.text)
  if match:
   index=int(match.group(1));p.text=f'Hình {index}. Quỹ đạo, sai số và lệnh điều khiển của {plot_ids[index-1]}. Nguồn: results/{plot_ids[index-1]}/run.mat (dữ liệu tự chạy).'
captions=[p for p in doc.paragraphs if p.style.name=='Caption' and re.match(r'^(Hình|Bảng)\s',p.text)]
for i,c in enumerate(captions,100):
 name=f'cap_{i}';bs=OxmlElement('w:bookmarkStart');bs.set(qn('w:id'),str(i));bs.set(qn('w:name'),name);be=OxmlElement('w:bookmarkEnd');be.set(qn('w:id'),str(i));c._p.insert(0,bs);c._p.append(be)
 if c.text.startswith('Hình'):
  number=re.match(r'Hình\s+(\d+)',c.text).group(1)
  titles={'1':'Số 8 mức 2 với T-ST-RHC','2':'Số 8 mức 2 với Lyapunov','3':'Đường tròn mức 3 với T-ST-RHC','4':'Đường tròn mức 3 với Lyapunov','5':'Kết quả tự tái lập cấu hình nền'}
  p=add(finish,f'Hình {number}. {titles[number]} … ');f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),f'PAGEREF {name} \\h');p._p.append(f)
add(finish,'DANH MỤC BẢNG BIỂU','Heading 1')
for i,c in enumerate(captions,100):
 if c.text.startswith('Bảng'):
  p=add(finish,c.text+' … ');f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),f'PAGEREF cap_{i} \\h');p._p.append(f)

# Consistent body typography while retaining the user's cover and images.
seen=False
for p in doc.paragraphs:
 if p.text=='Chương 1. GIỚI THIỆU':seen=True
 if not seen:continue
 if p.style.name=='Normal' and not p._p.xpath('.//m:oMath'):p.alignment=3;p.paragraph_format.line_spacing=1.3
 for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(13)
 if p.text.startswith('Chương ') and p.style.name=='Heading 1':p.paragraph_format.keep_with_next=True
doc.core_properties.title='Mô phỏng và đánh giá điều khiển bám quỹ đạo robot di động hai bánh có giới hạn vận tốc bằng phương pháp T-ST-RHC trên MATLAB.'
# Use structured OMML for RMSE rather than an overlong linear math string.
def mr(text):
 r=OxmlElement('m:r');t=OxmlElement('m:t');t.text=text;r.append(t);return r
def mel(tag,*children):
 e=OxmlElement('m:'+tag)
 for c in children:e.append(c)
 return e
for p in doc.paragraphs:
 if p._p.xpath('.//m:oMath') and p.text.strip().endswith('(3.2)'):
  p.clear();m=mel('oMath',mr('RMSE = '))
  term=mel('sSup',mel('e',mr('eₚ(k)')),mel('sup',mr('2')))
  summ=mel('nary',mel('naryPr'),mel('sub',mr('k=0')),mel('sup',mr('N')),mel('e',term))
  ratio=mel('f',mel('num',mr('1')),mel('den',mr('N+1')))
  radpr=mel('radPr');hide=OxmlElement('m:degHide');hide.set(qn('m:val'),'1');radpr.append(hide)
  m.append(mel('rad',radpr,mel('deg'),mel('e',ratio,summ)))
  p._p.append(m);p.add_run('    (3.2)')
  maxp=p.insert_paragraph_before('');maxp._p.addnext(p._p)
  # Move the added maximum formula after the RMSE paragraph.
  p._p.addnext(maxp._p);maxp.alignment=1
  maxp._p.append(mel('oMath',mr('E_max = max { eₚ(k) : k=0,…,N }')));maxp.add_run('    (3.2b)')
  break
# Build sums and fractions explicitly: Word's automatic linear conversion
# can mistakenly consume a norm exponent as an upper summation limit.
def sb(text,index):return mel('sSub',mel('e',mr(text)),mel('sub',mr(index)))
def sq(node):return mel('sSup',mel('e',node),mel('sup',mr('2')))
def fraction(num,den):return mel('f',mel('num',num),mel('den',den))
def sigma(lo,hi,*body):
 pr=mel('naryPr');char=OxmlElement('m:chr');char.set(qn('m:val'),'∑');pr.append(char)
 loc=OxmlElement('m:limLoc');loc.set(qn('m:val'),'undOvr');pr.append(loc)
 return mel('nary',pr,mel('sub',mr(lo)),mel('sup',mr(hi)),mel('e',*body))
def radical(*body):
 pr=mel('radPr');hide=OxmlElement('m:degHide');hide.set(qn('m:val'),'1');pr.append(hide)
 return mel('rad',pr,mel('deg'),mel('e',*body))
def matrix(rows):
 pr=mel('dPr')
 for tag,value in [('begChr','['),('endChr',']')]:
  el=OxmlElement('m:'+tag);el.set(qn('m:val'),value);pr.append(el)
 return mel('d',pr,mel('e',mel('m',*[mel('mr',*[mel('e',mr(v)) for v in row]) for row in rows])))
def seteq(label,*nodes):
 for p in doc.paragraphs:
  if p._p.xpath('.//m:oMath') and p.text.strip().endswith('('+label+')'):
   p.clear();p._p.append(mel('oMath',*nodes));p.add_run('    ('+label+')');p.alignment=1
   return
seteq('3.1',sb('e','p'),mr('(k) = '),radical(sq(mr('(xₖ−xᵣ,ₖ)')),mr(' + '),sq(mr('(yₖ−yᵣ,ₖ)'))))
seteq('3.2',mr('RMSE = '),radical(fraction(mr('1'),mr('N+1')),sigma('k=0','N',sq(mr('eₚ(k)')))))
seteq('3.2b',sb('E','max'),mr(' = max {eₚ(k) : k=0,…,N}'))
seteq('3.3',mr('IAE = '),sigma('k=0','N−1',fraction(mr('eₚ(k)+eₚ(k+1)'),mr('2')),mr('(tₖ₊₁−tₖ)')))
seteq('3.4',mr('TV = '),sigma('k=1','N−1',sq(mr('‖ωₐₚₚ(k)−ωₐₚₚ(k−1)‖₂'))))
seteq('3.5',sb('n','j'),mr(' = '),sigma('k=0','N−1',mr('𝟙{|ωⱼ,ₐₚₚ(k)|>Ω+εω}')),mr(',   '),sb('P','j'),mr(' = '),fraction(sb('n','j'),mr('N')))
seteq('3.6',sb('δ','j'),mr(' = max {max(0, |ωⱼ,ₐₚₚ(k)|−Ω) : k=0,…,N−1}'))
# The tolerance unit is explained in prose, avoiding a long second equation.
seteq('2.1',matrix([['v'],['ω']]),mr(' = T '),matrix([['ωR'],['ωL']]),mr(',   T = '),matrix([['r/2','r/2'],['r/d','−r/d']]))
seteq('2.6',matrix([['v'],['ω']]),mr(' = TFL u,   TFL = '),matrix([['cos θ','sin θ'],['−sin θ/b','cos θ/b']]))
seteq('2.20',sb('H','d'),mr(' = '),fraction(mr('1'),mr('Ω')),matrix([['−1','0'],['0','−1'],['1','0'],['0','1']]),mr(',   H(θ)=H_d T⁻¹TFL(θ)'))
seteq('2.19',mr('Tᵢ={e∈ℝ² : eᵀQᵢ⁻¹e≤1},  Qᵢ=rᵢ²I₂,  X={e : ‖e‖≤r_Nₛ}'))
seteq('2.21',mr('ûᵣ = arg min { ½‖ξ−uᵣ‖² : H(u₀+ξ)≤1₄ },  u=u₀+ûᵣ'))
seteq('2.22',mr('ωⱼ,ₐₚₚ = max(−Ω, min(Ω, ωⱼ,ᵣₑq)),   j∈{R,L}'))
front=False
for p in doc.paragraphs:
 if p.text=='DANH MỤC HÌNH VẼ' and p.style.name=='Heading 1':front=True
 if p.text=='Chương 1. GIỚI THIỆU':front=False
 if front and not p.style.name.startswith('Heading'):
  p.paragraph_format.line_spacing=1.0;p.paragraph_format.space_after=Pt(2)
for i,shape in enumerate(doc.inline_shapes):
 if i>=2:
  ratio=shape.height/shape.width;shape.width=Cm(14);shape.height=int(shape.width*ratio)
  from docx.text.paragraph import Paragraph
  para=Paragraph(shape._inline.getparent().getparent().getparent(),doc._body)
  para.alignment=1
for p in doc.paragraphs:
 if p.text in ('Tài liệu tham khảo','Phụ lục A. Ký hiệu và hồ sơ tái lập','Phụ lục B. Kết quả tái lập cấu hình nền') and not p.style.name.lower().startswith('toc'):
  p.paragraph_format.page_break_before=True
 if p.text.startswith('Bước 2. Tính ρ'):
  for r in p.runs:r.text=r.text.replace('X_N','X_(N_s)')
# Preserve the derivative mark explicitly instead of relying on math auto-format.
for p in doc.paragraphs:
 if p._p.xpath('.//m:oMath') and p.text.strip().endswith('(2.18)'):
  for t in p._p.xpath('.//m:t'):
   if t.text and t.text.lstrip().startswith('V'):
    t.text=t.text.replace('V','V̇',1);break
doc.save(TARGET)
print(TARGET)
