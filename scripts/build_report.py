"""Build report only from recorded evidence. Run with Codex bundled Python."""
from pathlib import Path
import csv,json,math,re
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
def read_json(p): return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def rows(p):
    with (ROOT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def num(x):
    try:return float(x)
    except (ValueError,TypeError):return math.nan
def fmt(x,d=4):
    x=num(x)
    return f'{x:.{d}g}' if math.isfinite(x) else '—'

data=rows('tables/summary.csv'); sens=rows('tables/sensitivity.csv')
completed=[r for r in data if r['status']=='completed']; failed=[r for r in data if r['status']!='completed']
env=read_json('results/environment.json')
baseline=read_json('results/baseline_comparison.json')
test=read_json('results/test_summary.json')
cal=rows('tables/calibration.csv'); best=min(cal,key=lambda r:num(r['sumRMSE']))
runinfo={r['run_id']:read_json(f"results/{r['run_id']}/summary.json") for r in data}

analysis=[]
analysis.append(f"Chiến dịch gồm {len(data)} cấu hình, {len(completed)} lượt hoàn thành và {len(failed)} lượt dừng do kiểm tra điều kiện. Mỗi cấu hình được đo năm lần sau warm-up; đây là các lần chạy xác định phục vụ đo thời gian.")
for traj in ['eight','circle']:
    pair=[]
    for r in completed:
        if r['trajectory']==traj and r['controller']=='tstrhc':
            other=next((x for x in completed if x['trajectory']==traj and x['initial']==r['initial'] and x['wheelLimit']==r['wheelLimit'] and x['controller']=='lyapunov'),None)
            if other:pair.append((r,other))
    wins=sum(num(a['rmse'])<num(b['rmse']) for a,b in pair)
    analysis.append(f"Với quỹ đạo {traj}, T-ST-RHC có RMSE nhỏ hơn đối chứng trong {wins}/{len(pair)} cặp hoàn thành. Kết luận chỉ áp dụng cho cấu hình, hàm mục tiêu repo và lưới hiệu chỉnh đã công bố; các ca không chạy được không được tính thành chiến thắng cho phương pháp nào.")

hard=next(r for r in data if r['run_id']=='circle_i3_w10_tstrhc')
low=next(r for r in data if r['run_id']=='circle_i3_w8_tstrhc')
analysis.append(f"Ca circle_i3_w10_tstrhc có RMSE {fmt(hard['rmse'])} m, trong khi cùng trạng thái đầu tại 8 rad/s là {fmt(low['rmse'])} m. Tăng giới hạn vận tốc không bảo đảm giảm sai số. Việc tăng miền lệnh thay đổi nghiệm và chuyển động quay trong một chu kỳ; cần đọc đồng thời sai số phía trước, chỉ số tập và phần dư mô hình trước khi suy luận nguyên nhân.")
for id in ['circle_i3_w8_tstrhc','circle_i3_w10_tstrhc','circle_i3_w12_tstrhc']:
    detail=read_json(f'results/{id}/diagnostic_summary.json')
    analysis.append(f"{id}: sai số phía trước lớn nhất {fmt(detail['maxFrontError'])} m; phần dư tuyến tính hóa lớn nhất {fmt(detail['maxLinearizationResidual'])} m/bước; số lần chỉ số tập tăng {detail['indexIncreases']}. Đây là chẩn đoán trên mô hình giữ lệnh thực thi, không phải bằng chứng định lý của mô hình thiết kế đã được áp dụng chính xác.")
modelgap=rows('tables/model_gap.csv')
for row in modelgap:
    analysis.append(f"Phép đối chiếu {row['run_id']}: RMSE robot ode45 {fmt(row['physicalRMSE'])} m, nghiệm giữ lệnh chính xác {fmt(row['physicalExactRMSE'])} m, còn mô hình z tuyến tính kèm cập nhật hướng cho {fmt(row['designRMSE'])} m. Chỉ số tập tăng {row['physicalIndexIncreases']} lần ở robot và {row['designIndexIncreases']} lần ở mô hình thiết kế. Phần dư lấy mẫu tham chiếu tối đa {fmt(row['maxReferenceResidual'])} m/bước. Max sai khác thành phần trạng thái ode45 so nghiệm chính xác là {fmt(row['physicalExactMaxStateDifference'])}, theo đơn vị m hoặc rad của thành phần tương ứng.")
analysis.append("Phép đối chiếu thay riêng cập nhật robot bằng cập nhật z của mô hình thiết kế, giữ cấu hình và bộ điều khiển. Kết quả hỗ trợ giải thích rằng chênh lệch mô hình giữ lệnh có vai trò lớn trong ca bất lợi; mô hình chẩn đoán này không thay thế robot trong 36 ca chính và không phải cải tiến thuật toán. Sai khác ode45 so nghiệm chính xác ở cùng ca giúp phân biệt lỗi tích phân với chênh lệch cấu trúc mô hình. Không giảm tốc tham chiếu hoặc loại ca bất lợi.")
analysis.append("Ở ca đầu lớn, RMSE gần nhau giữa ode45 và nghiệm chính xác nhưng sai khác trạng thái tức thời có thể đáng kể, cho thấy tính nhạy của vòng kín với sai khác số. Vì vậy không kết luận hai diễn biến từng mẫu tương đương trên các ca này; kết quả kiểm tra rất nhỏ ở mức đầu vừa chỉ có phạm vi riêng.")
analysis.append("Với số 8 ở 8 rad/s, bán kính miền điều khiển bảo thủ nhỏ hơn cận tham chiếu. T-ST-RHC chủ động dừng trước bước điều khiển; đây là không đáp ứng điều kiện của cách dựng tập đang dùng, không kết luận mọi bộ điều khiển đều không thể bám quỹ đạo này.")
for ctrl in ['tstrhc','lyapunov']:
    subset=[r for r in completed if r['controller']==ctrl]
    mean_ms=sum(num(r['timingMean5']) for r in subset)/len(subset)*1000
    maximum=max(num(r['timingMax5']) for r in subset)*1000
    misses=sum(num(r['deadlineMisses5']) for r in subset)
    analysis.append(f"{ctrl}: trung bình thời gian theo cấu hình hoàn thành {mean_ms:.4g} ms, cực đại mọi lần đo {maximum:.4g} ms; tổng bước vượt Ts là {int(misses)}. Mức trung bình giữa cấu hình chỉ là mô tả chiến dịch; p95 và biến thiên từng cấu hình ở bảng thời gian. Không suy ra đáp ứng thời gian thực trên robot.")

text='# Phân tích kết quả tự chạy\n\n'+'\n\n'.join(analysis)+'\n'
(ROOT/'docs/results_analysis.md').write_text(text,encoding='utf-8')

doc=Document(); sec=doc.sections[0]
sec.page_width=Inches(8.5); sec.page_height=Inches(11)
sec.top_margin=sec.bottom_margin=Inches(.8); sec.left_margin=sec.right_margin=Inches(.85)
for style in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption']:
    s=doc.styles[style]; s.font.name='Times New Roman'; s.font.color.rgb=RGBColor(0,0,0)
    s.font.size=Pt(13 if style in ['Normal','Caption'] else 16)
    s.element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman')
doc.styles['Title'].font.size=Pt(22)
normal=doc.styles['Normal'].paragraph_format
normal.line_spacing=1.15; normal.space_after=Pt(7)
for style in doc.styles:
    if style.type==1:
        fonts=style.element.get_or_add_rPr().get_or_add_rFonts()
        for key in list(fonts.attrib):
            if 'Theme' in key or 'theme' in key:del fonts.attrib[key]
        for key in ['ascii','hAnsi','eastAsia','cs']:fonts.set(qn('w:'+key),'Times New Roman')
        for border in list(style.element.iter(qn('w:pBdr'))):border.getparent().remove(border)
doc.styles['Caption'].font.bold=False
footer=sec.footer.paragraphs[0];footer.alignment=1
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
table_count=0
equation_count=0

def p(text,style=None):
    para=doc.add_paragraph(text,style)
    return para
def heading(text,level=1):doc.add_heading(text,level)
def table(headers,body,title=''):
    global table_count
    table_count+=1
    if not title:
        title={'Mục tiêu':'Ma trận mục tiêu và bằng chứng','Nội dung':'Đối chiếu hai phương pháp',
            'Công thức':'Liên hệ công thức mã và kiểm tra','Hạng mục':'Kế thừa thay đổi và kiểm chứng',
            'Mức':'Điều kiện đầu theo mức sai lệch'}.get(headers[0],'Thông tin kỹ thuật')
        p(f'Các nội dung tương ứng được đối chiếu trong Bảng {table_count}.')
    caption=p(f'Bảng {table_count} {title}','Caption');caption.paragraph_format.keep_with_next=True
    t=doc.add_table(rows=1,cols=len(headers)); t.autofit=False
    for cell,h in zip(t.rows[0].cells,headers):cell.text=str(h)
    header=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(header)
    for vals in body:
        cells=t.add_row().cells
        for cell,val in zip(cells,vals):cell.text=str(val)
    for ri,row in enumerate(t.rows):
        no_split=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(no_split)
        for cell in row.cells:
            cell.vertical_alignment=1
            tcPr=cell._tc.get_or_add_tcPr(); borders=OxmlElement('w:tcBorders')
            for edge in ['top','left','bottom','right']:
                el=OxmlElement('w:'+edge); el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
            tcPr.append(borders)
            if ri==0:
                shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E7E6E6');tcPr.append(shade)
            for para in cell.paragraphs:
                para.paragraph_format.space_after=Pt(4);para.paragraph_format.space_before=Pt(4)
                for run in para.runs:run.font.name='Times New Roman';run.font.size=Pt(13);run.bold=(ri==0)
    return t

def equation(text):
    global equation_count
    equation_count+=1
    para=p(f'{text}    (2.{equation_count})');para.alignment=1
    para.paragraph_format.keep_together=True

def formula_line(line):
    if line.startswith('T='):
        p('Theo mô hình robot [1], quan hệ vận tốc hai bánh và vận tốc robot là')
        equation('[v; ω] = T[ωR; ωL],  T = [r/2, r/2; r/d, −r/d]')
        p('d là khoảng cách hai bánh theo công thức mã. Hai bánh cùng tốc độ tạo chuyển động thẳng; bánh phải nhanh hơn tạo quay dương. Giá trị d=0.053 m của repo được giữ riêng với D=0.1047 m của thực nghiệm bài báo.')
    elif line.startswith('dx/dt='):
        equation('ẋ = v cos θ,  ẏ = v sin θ,  θ̇ = ω')
        p('Vị trí và kích thước có đơn vị m; góc là rad; v là m/s; ω và vận tốc góc bánh là rad/s.')
    elif line.startswith('v_r='):
        equation('vr = √(ẋr² + ẏr²),  ωr = (ẋr ÿr − ẏr ẍr)/(ẋr² + ẏr²)')
        equation('θr = unwrap(atan2(ẏr, ẋr))')
        p('Kiểm tra tốc độ khác không trước khi tính tham chiếu. Sai số hướng dùng atan2(sin(θ−θr), cos(θ−θr)) để tránh trừ góc thô qua biên ±π.')
    elif line.startswith('z=['):
        equation('z = [x + b cos θ; y + b sin θ],  b > 0')
        equation('[v; ω] = TFL u,  TFL = [cos θ, sin θ; −sin θ/b, cos θ/b]')
        equation('e = z − zr,  e(k+1) = e(k) + Ts(u − ur)')
        p('ur=TFL(θr)⁻¹[vr;ωr]. b=0 làm phép biến đổi suy biến. Sai số T-ST-RHC là điểm phía trước trong tọa độ toàn cục; đối chứng dùng dấu và hệ tọa độ khác.')
    elif line.startswith('Đặt rho='):
        equation('ρ = max ‖ur‖,  ru = 2Ωrb / √(4b² + d²),  ρ < ru')
        equation('r0 = Tsρ,  ri = ri−1 + Ts(ru − ρ),  Qi = ri²I')
        p('Theo [1], D là tập nhiễu −Ts ur và T0 là tập cuối bán kính r0. Công thức mở rộng chỉ áp dụng cho A=I, B=Ts I và tập cầu đồng tâm; không tổng quát hóa phép căn phần tử sang ellipsoid bất kỳ.')
    elif line.startswith('Online chọn'):
        p('Online tìm chỉ số i nhỏ nhất chứa e. Với i>0, giải bài toán theo biến û và áp dụng u=û+ur:')
        equation('min ‖e + Tsû‖²;  H(û + ur) ≤ 1')
        equation('(e + Tsû)ᵀ Qi−1⁻¹ (e + Tsû) ≤ 1')
        p('Với i=0, u0=−e/Ts và QP chọn ûr gần ur nhất sao cho H(u0+ûr)≤1. H=Hd T⁻¹TFL(θ); lệnh bánh bằng T⁻¹TFLu. Bài toán QP dùng quy ước 0.5xᵀHx+fᵀx của quadprog [7].')
    elif line.startswith('Theo [2], phương trình'):
        p('Theo Blažič [2], các sai số cục bộ và biến hướng được định nghĩa như sau:')
        equation('ex = cos θ(xr−x) + sin θ(yr−y)')
        equation('ey = −sin θ(xr−x) + cos θ(yr−y)')
        equation('es = sin(θr−θ),  ec = cos(θr−θ)−1,  h = 1 + ec/a')
    elif line.startswith('v=v_r'):
        p('Luật (18) của nguồn [2], với k,kx,ks>0, a>2 và n nguyên:')
        equation('v = vr cos(θr−θ) + kx ex')
        equation('ω = ωr + k vr ey h² + ks es h²ⁿ')
        equation('V = k(ex²+ey²)/2 + (es²+ec²)/(2h)')
        equation('V̇ = −k kx ex² − ks es² h²ⁿ⁻² ≤ 0')
        p('Các biểu thức (2.12)–(2.18) liên hệ trực tiếp với controller_step và phép kiểm tra đạo hàm Lyapunov. Giả thiết kích thích của vr hoặc ωr, tính liên tục và điều kiện hướng trong chứng minh phải được kiểm tra khi diễn giải hội tụ; V̇≤0 riêng lẻ chưa đủ kết luận toàn bộ sai số hội tụ.')
    else:return False
    return True

def markdown_file(name,include_title=False):
    lines=(ROOT/name).read_text(encoding='utf-8').splitlines(); pending=[]
    def flush():
        nonlocal pending
        if pending:
            head=pending[0]; body=pending[2:]
            table(head,body);pending=[]
    for line in lines:
        if line.startswith('|'):
            pending.append([s.strip() for s in line.strip('|').split('|')]);continue
        flush()
        if line.startswith('# '):
            if include_title:heading(line[2:])
        elif line.startswith('## '):heading(line[3:],2)
        elif line.strip():
            if str(name).endswith('theory.md') and formula_line(line):continue
            p(line)
    flush()

PROJECT_TITLE='Mô phỏng và đánh giá điều khiển bám quỹ đạo robot di động hai bánh có giới hạn vận tốc bằng phương pháp T-ST-RHC trên MATLAB.'
p(PROJECT_TITLE,'Title')
p('Phương pháp T-ST-RHC dưới giới hạn vận tốc bánh và đối chứng Lyapunov')
p('Báo cáo kỹ thuật học phần Kỹ thuật Robot')
p('Ngày lập 16 tháng 11 năm 2026')
p(analysis[0])
p('Kết quả cho thấy lợi ích và giới hạn phụ thuộc cấu hình. Một số ca sai lệch đầu lớn có sai số cao dù vượt qua kiểm tra thiết kế số; báo cáo giữ các ca này để thảo luận sự khác biệt mô hình và phạm vi kết luận.')
p('Nội dung: bài toán và mục tiêu; cơ sở lý thuyết; triển khai và tái lập; thiết kế thử nghiệm; kết quả và thảo luận; kết luận; tài liệu tham khảo và phụ lục dữ liệu.')

heading('1 Bài toán và mục tiêu')
markdown_file('docs/problem_statement.md')
heading('2 Cơ sở lý thuyết và đối chiếu phương pháp')
markdown_file('docs/theory.md')
heading('3 Triển khai và tái lập')
p(f"Môi trường chạy là {env['matlab']}, {env['os']}. Thông tin CPU và bộ nhớ được ghi nguyên bản trong results/environment.json. ET và MPT3 được nạp trong phiên MATLAB, không thay đổi startup toàn cục.")
p('Cấu hình gốc: r=0.0205 m, d=0.053 m, b=0.1 m, Ts=0.15 s, Omega=10 rad/s, 700 tập mở rộng. Thực nghiệm bài báo dùng R=0.021 m, D=0.1047 m, Ts=0.15 s, Omega=10 rad/s và báo cáo 396 tập; hàm mục tiêu có thêm 0.5||u||². Bài báo ghi MATLAB R2022b cho thực nghiệm, README repo ghi R2022a. Các khác biệt này được công bố và không ép đồng nhất.')
p('Luồng chạy: kiểm tra môi trường → tạo tham chiếu → dựng tập và kiểm tra điều kiện → warm-up → lặp đo → tính sai số và tìm tập → giải tối ưu hoặc luật Lyapunov → đổi lệnh bánh → kiểm tra → tích phân robot → lưu dữ liệu → xuất bảng và hình. Lỗi ở bước nào đều giữ cấu hình và nguyên nhân.')
p(f"Đối chiếu tái cấu trúc với cùng options và lưới ode45 tác giả: sai khác trạng thái lớn nhất {baseline['maxStateDifference']:.6g}, vận tốc bánh {baseline['maxWheelDifference']:.6g} rad/s; kiểm tra đạt={baseline['pass']}. Ngưỡng công bố là 1 mm cho thành phần vị trí và 0.1 rad/s cho bánh; thành phần góc được so với cùng ngưỡng số 0.001 rad. Các ngưỡng là mức kiểm tra số, không phải mục tiêu chất lượng điều khiển.")
p('Lần so sánh ban đầu với thiết lập bộ giải siết chặt và ode45 mới có sai khác trạng thái khoảng 0.0031 và bánh 0.1044 rad/s, vượt ngưỡng. Vì vậy phép kiểm tra tương đương cấu trúc dùng lại thiết lập tác giả; đánh giá chính dùng profile validated, và khác biệt thiết lập số được công bố thay vì nới ngưỡng để báo đạt.')
p(f"Bộ kiểm tra MATLAB có {test['passed']} ca đạt, {test['failed']} ca lỗi. Kiểm tra bao gồm dấu quay, đạo hàm, góc tuần hoàn, tập cầu, tích phân, đẳng thức đạo hàm Lyapunov, nghiệm tối ưu, bão hòa và chỉ số trên sai số 3–4–5 biết trước.")
markdown_file('docs/changes_and_contributions.md')
heading('4 Thiết kế thử nghiệm')
markdown_file('docs/experiment_design.md')
p(f'Bảng {table_count+1} trình bày thông số đối chứng được chọn trước đánh giá chính từ toàn bộ lưới hiệu chỉnh.')
table(['k','kx','ks','a và n'],[[best['k'],best['kx'],best['ks'],f"a={best['a']}; n={best['n']}"]],title='Thông số Blažič sau hiệu chỉnh trên ca riêng [2]')

heading('5 Kết quả và thảo luận')
for s in analysis:p(s)
p(f'Bảng {table_count+1} giữ toàn bộ 36 lượt, không tính chỉ số toàn khoảng cho ca bị dừng. E/T là quỹ đạo số 8/tròn; ST/LY là T-ST-RHC/Blažič. Mã hàng có dạng quỹ đạo–mức đầu–giới hạn–bộ điều khiển; run_id đầy đủ nằm trong CSV và dữ liệu nguồn.')
table(['Ca','RMSE m','IAE m s','Trạng thái'],[[f"{'E' if r['trajectory']=='eight' else 'T'}-{r['initial']}-{r['wheelLimit']}-{'ST' if r['controller']=='tstrhc' else 'LY'}",fmt(r['rmse']),fmt(r['iae']),'Đạt lượt chạy' if r['status']=='completed' else 'Dừng điều kiện'] for r in data],title='Chỉ số toàn khoảng của 36 cấu hình từ tables/summary.csv')
p(f'Bảng {table_count+1} bổ sung đánh đổi lệnh và thời gian theo cấu hình hoàn thành. TV là tổng bình phương biến thiên lệnh, không phải năng lượng; p95 được gộp từ năm lần đo. Vi phạm là tổng số mẫu của hai bánh vượt dung sai.')
table(['Ca','TV rad² s⁻²','p95 ms','Vi phạm'],[[f"{'E' if r['trajectory']=='eight' else 'T'}-{r['initial']}-{r['wheelLimit']}-{'ST' if r['controller']=='tstrhc' else 'LY'}",fmt(r['commandVariation']),fmt(num(r['timingP955'])*1000),str(int(num(r['violationCountR'])+num(r['violationCountL'])))] for r in completed],title='Biến thiên lệnh thời gian và vi phạm từ tables/summary.csv')

for i,id in enumerate(['eight_i2_w10_tstrhc','eight_i2_w10_lyapunov','circle_i3_w10_tstrhc','circle_i3_w10_lyapunov'],1):
    image=ROOT/'figures'/f'{id}.png'
    if image.exists():
        para=p(f'Hình {i} trình bày dữ liệu của {id}; so sánh các Hình 1–2 và 3–4 dùng cùng điều kiện tương ứng.');para.paragraph_format.keep_with_next=True
        doc.add_picture(str(image),width=Inches(6.7))
        doc.paragraphs[-1].paragraph_format.keep_with_next=True
        p(f'Hình {i} Quỹ đạo sai số lệnh bánh và chỉ số tập hoặc sai số hướng Nguồn results/{id}/run.mat','Caption')

p(f'Bảng {table_count+1} kiểm tra độ nhạy tích phân với cùng điều khiển và cấu hình mức đầu vừa. Sai khác nhỏ cho thấy bộ tích phân không tạo khác biệt đáng kể trong các ca được kiểm tra; các ca lớn được kiểm tra riêng trong phép đối chiếu mô hình ở phần thảo luận.')
table(['Quỹ đạo','Điều khiển','Max sai khác trạng thái','Sai khác RMSE m'],[[r['trajectory'],r['controller'],fmt(r['maxStateDifference']),fmt(r['rmseDifference'])] for r in sens],title='ode45 so với nghiệm chính xác từ tables/sensitivity.csv')

heading('6 Kết luận và giới hạn')
p('Mục tiêu tái lập và xây dựng hệ thống đánh giá đã có mã, dữ liệu, log và kiểm tra trên MATLAB. Hệ thống tạo bảng và hình trực tiếp từ run.mat; đối chứng có nguồn và hiệu chỉnh riêng. Các kết quả thất bại được giữ để phân biệt điều kiện thiết kế với hành vi mô phỏng.')
p('Kết luận so sánh phải gắn từng cấu hình: T-ST-RHC đưa ràng buộc vào tối ưu và có chi phí tính toán cao hơn luật tường minh; độ chính xác không tăng đơn điệu khi nới giới hạn bánh. Phân tích phần dư mô hình hỗ trợ nhận diện giới hạn, nhưng chưa tạo chứng minh mới cho robot tích phân liên tục dưới lệnh giữ hằng.')
p('Giới hạn còn lại gồm cận tham chiếu kiểm tra số, thiếu mô hình động cơ và nhiễu, phạm vi hiệu chỉnh hữu hạn, phép đo thời gian phụ thuộc tải máy và chưa có xác nhận robot thật. Trước khi nộp, người học cần rà soát lập luận và thông tin cá nhân theo mẫu của giảng viên; báo cáo không cam kết điểm số.')

heading('Tài liệu tham khảo')
markdown_file('docs/references.md')
heading('Phụ lục cách tái tạo')
p('Tại thư mục gốc MATLAB: setup_project; check_environment; run_checks; run_original(true); compare_baseline; tune_lyapunov; run_suite; check_sensitivity; export_results. Chiến dịch chính lưu 36 run_id và năm dãy thời gian mỗi ca. Không chạy tác vụ MATLAB khác đồng thời khi đo lại thời gian.')
p('Sau khi có dữ liệu: chạy scripts/build_report.py bằng Python của runtime tài liệu để sinh Word; scripts/render_report.ps1 xuất PDF bằng Word. Các bước tạo báo cáo chỉ đọc dữ liệu mô phỏng; không thay dữ liệu để phù hợp nhận xét.')

doc.core_properties.title=PROJECT_TITLE
doc.core_properties.subject='Kỹ thuật Robot'
doc.core_properties.author=''
for para in doc.paragraphs:
    for border in list(para._p.iter(qn('w:pBdr'))):border.getparent().remove(border)
from format_report import format_document
format_document(doc)
out=ROOT/'report/bao_cao_robot_cap_nhat.docx';doc.save(out)
print(out)
