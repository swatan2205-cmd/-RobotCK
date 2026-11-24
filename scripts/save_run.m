function save_run(run,runid)
root=fileparts(fileparts(mfilename('fullpath'))); folder=fullfile(root,'results',runid);
if ~isfolder(folder), mkdir(folder); end
run.run_id=runid; run.source=source_manifest();
run.timestamp=char(datetime('now','TimeZone','Asia/Bangkok','Format','yyyy-MM-dd HH:mm:ss Z'));
save(fullfile(folder,'run.mat'),'run','-v7');
summary=rmfield(run,{'q','reference','wheel_requested','wheel_applied','diagnostics','controlSeconds','errors'});
summary.sets=rmfield(summary.sets,{'Q','radii'});
fid=fopen(fullfile(folder,'summary.json'),'w','n','UTF-8');
fprintf(fid,'%s',jsonencode(summary,PrettyPrint=true)); fclose(fid);
fid=fopen(fullfile(folder,'console.log'),'w','n','UTF-8'); fprintf(fid,'%s\n%s',run.status,run.error); fclose(fid);
end
