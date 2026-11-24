function result = run_original(repaired)
if nargin<1, repaired=false; end
root=setup_project();
outdir=fullfile(root,'results','baseline'); if ~isfolder(outdir), mkdir(outdir); end
diary(fullfile(outdir,'console.log')); cleanup=onCleanup(@()diary('off'));
oldvis=get(0,'DefaultFigureVisible'); set(0,'DefaultFigureVisible','off');
viscleanup=onCleanup(@()set(0,'DefaultFigureVisible',oldvis));
source='provided'; if repaired, source='repaired'; end
addpath(fullfile(root,'original',source));
try
    result=execute_author_script(source); result.status='completed';
catch ME
    result.status='failed'; result.error=getReport(ME,'extended','hyperlinks','off');
    fprintf(2,'%s\n',result.error);
end
result.timestamp=char(datetime('now','TimeZone','Asia/Bangkok'));
result.repaired=repaired;
save(fullfile(outdir,'baseline.mat'),'result');
figs=findall(0,'Type','figure');
for n=1:numel(figs), savefig(figs(n),fullfile(outdir,sprintf('author_%02d.fig',n))); end
close all;
rmpath(fullfile(root,'original',source));
disp(result.status);
end

function result=execute_author_script(source)
run(fullfile(fileparts(fileparts(mfilename('fullpath'))),'original',source,'ST_FL_Trajectory_Tracking_Differential_Drive_CDC23.m'));
result=struct('q',qseq,'wheel',wrwlseq,'t',tt,'index',index_seq,...
    'xr',xr,'yr',yr,'thetar',thetar,'Q_k',Q_k,'Ts',Ts,'r',r,'d',d,'b',b,...
    'wheelLimit',wrlmax,'mse_author',eps,'u',uk_seq);
end
