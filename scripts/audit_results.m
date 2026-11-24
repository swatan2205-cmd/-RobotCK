function audit=audit_results()
root=setup_project(); files=dir(fullfile(root,'results','*_i*_w*','run.mat'));
% Exclude diagnostic runs sharing the formal run-id prefix.
keep=false(size(files));
for k=1:numel(files)
 [~,foldername]=fileparts(files(k).folder);
 keep(k)=~isempty(regexp(foldername,'^(eight|circle)_i[123]_w(8|10|12)_(tstrhc|lyapunov)$','once'));
end
files=files(keep);
rows=[];
for k=1:numel(files)
 a=load(fullfile(files(k).folder,files(k).name),'run'); r=a.run;
 assert(size(r.q,2)==size(r.wheel_applied,2)+1,'Sample shape mismatch');
 assert(numel(r.t_state)==size(r.q,2),'State time mismatch');
 assert(numel(r.t_control)==size(r.wheel_applied,2),'Control time mismatch');
 d=struct('maxFrontError',NaN,'maxLinearizationResidual',NaN,'indexIncreases',0,...
     'maxConstraintResidual',NaN,'nonPositiveExitflags',0,'repeatAgreement',true);
 n=r.completedSteps;
 if n>0
  d.maxFrontError=max(vecnorm(r.errors.front(:,1:n+1)));
  d.maxLinearizationResidual=max(vecnorm(r.errors.linearizationResidual(:,1:n)));
  if strcmp(r.config.controller,'tstrhc')
   d.indexIncreases=sum(diff([r.diagnostics.index])>0);
   d.nonPositiveExitflags=sum([r.diagnostics.exitflag]<=0);
  end
  d.maxConstraintResidual=max([r.diagnostics.constraintResidual]);
 end
 for j=2:numel(r.repeatMetrics)
  d.repeatAgreement=d.repeatAgreement && isequaln(r.repeatMetrics{j}.rmse,r.metrics.rmse) && strcmp(r.repeatStatus{j},r.status);
 end
 fid=fopen(fullfile(files(k).folder,'diagnostic_summary.json'),'w'); fprintf(fid,'%s',jsonencode(d,PrettyPrint=true)); fclose(fid);
 row=struct('run_id',r.run_id,'status',r.status,'shapeOK',true,'repeatAgreement',d.repeatAgreement,...
     'solverFlagsOK',d.nonPositiveExitflags==0);
 rows=[rows row]; %#ok<AGROW>
end
audit=struct2table(rows); writetable(audit,fullfile(root,'tables','audit.csv'));
assert(height(audit)==36,'Expected 36 formal cases');
assert(all(audit.shapeOK & audit.repeatAgreement & audit.solverFlagsOK),'Data audit failed');
disp(audit);
end
