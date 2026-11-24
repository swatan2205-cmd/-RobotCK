from pathlib import Path
import csv,json,hashlib,re,math,zipfile
from docx import Document

ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def jread(p):return json.loads(p.read_text(encoding='utf-8-sig'))
data=list(csv.DictReader((ROOT/'tables/summary.csv').open(encoding='utf-8-sig',newline='')))
assert len(data)==36 and len({r['run_id'] for r in data})==36
assert sum(r['status']=='completed' for r in data)==33
source_checks=[]
for row in data:
    id=row['run_id']; folder=ROOT/'results'/id
    assert (folder/'run.mat').exists()
    summary=jread(folder/'summary.json')
    assert summary['status']==row['status']
    for key in ['rmse','iae','maxError','commandVariation','frontRMSE']:
        a=float(row[key]);b=summary['metrics'][key]
        if b is None:assert math.isnan(a)
        else:assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-13)
    if row['status']=='completed':assert (ROOT/'figures'/f'{id}.png').exists()
    for entry in summary['source']:
        p=ROOT/entry['path']
        current=digest(p)
        match=current==entry['sha256']
        if entry['path'].startswith(('src/','config/')) or entry['path']=='setup_project.m':assert match,(id,entry['path'])
        source_checks.append({'run_id':id,'path':entry['path'],'matches_current':match,'recorded_sha256':entry['sha256'],'current_sha256':current})
with (ROOT/'tables/source_integrity.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(source_checks[0]));w.writeheader();w.writerows(source_checks)
for entry in jread(ROOT/'docs/provided_manifest.json'):
    p=ROOT/'original/provided'/entry['path'];assert digest(p)==entry['sha256']
    original_input=ROOT/'T_ST_RHC_mobile_robots-main'/entry['path']
    if original_input.exists():assert p.read_bytes()==original_input.read_bytes()
document=Document(ROOT/'report/bao_cao_robot.docx')
assert len(document.tables)==9
assert len(document.inline_shapes)==4
text='\n'.join(p.text for p in document.paragraphs)
assert all(f'(2.{i})' in text for i in range(1,19))
assert all(f'Bảng {i}' in text for i in range(1,10))
assert all(f'Hình {i}' in text for i in range(1,5))
assert 'placeholder' not in text.lower()
assert not document.element.xpath('.//w:pBdr')
report={'formal_cases':len(data),'completed_cases':33,'condition_stops':3,
        'matlab_tests':jread(ROOT/'results/test_summary.json'),
        'baseline':jread(ROOT/'results/baseline_comparison.json'),
        'core_source_integrity':True,'input_preserved':True,'csv_json_consistency':True,
        'report_tables':9,'report_figures':4,'numbered_equations':18,
        'render_engine':'Microsoft Word native export; Poppler rasterization',
        'packaged_render_docx_attempt':'Failed: LibreOffice is not bundled/available on this Windows runtime',
        'visual_qa':'pending final full-page inspection'}
report['report_pdf_sha256']=digest(ROOT/'report/bao_cao_robot.pdf')
previous=ROOT/'docs/delivery_audit.json'
if previous.exists():
    old=jread(previous)
    if old.get('report_pdf_sha256')==report['report_pdf_sha256']:
        for key in ['visual_qa','reviewed_pages','page_count','qa_image_manifest']:
            if key in old:report[key]=old[key]
(ROOT/'docs/delivery_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['matlab_tests','baseline']},ensure_ascii=False,indent=2))
