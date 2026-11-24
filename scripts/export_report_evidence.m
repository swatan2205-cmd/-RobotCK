function export_report_evidence()
root=setup_project(); a=load(fullfile(root,'results','baseline','baseline.mat')); b=a.result;
ep=vecnorm(b.q(1:2,1:numel(b.t))-[b.xr;b.yr]);
e.baseline=struct('samples',numel(b.t),'controlDuration',numel(b.t)*b.Ts,...
 'metricDuration',b.t(end),'rmsePrecontrol',sqrt(mean(ep.^2)),...
 'iaePrecontrol',trapz(b.t,ep),'maxErrorPrecontrol',max(ep),...
 'maxWheel',max(abs(b.wheel),[],'all'),'violationCount',sum(abs(b.wheel)>10+1e-7,'all'));
a=load(fullfile(root,'results','baseline_author','run.mat')); r=a.run;
e.comparison.maxPositionComponent=max(abs(r.q(1:2,:)-b.q(1:2,:)),[],'all');
e.comparison.maxHeadingDifference=max(abs(r.q(3,:)-b.q(3,:)));
f=figure('Visible','off','Color','w','Position',[100 100 1100 650]);
tiledlayout(2,2,'Padding','loose','TileSpacing','loose');
nexttile; plot(b.xr,b.yr,'r--',b.q(1,:),b.q(2,:),'b'); axis equal; grid on; xlabel('x (m)');ylabel('y (m)');legend('Reference','Baseline');
nexttile;plot(b.t,ep);grid on;xlabel('t (s)');ylabel('Position error (m)');
nexttile;plot(b.t,b.wheel);yline(10,'r--');yline(-10,'r--');grid on;xlabel('t (s)');ylabel('Wheel velocity (rad/s)');legend('Right','Left');
nexttile;stairs(b.t,b.index-1);grid on;xlabel('t (s)');ylabel('Set index (zero based)');
set(f,'PaperPositionMode','auto');print(f,fullfile(root,'figures','baseline_report.png'),'-dpng','-r180');close(f);
fid=fopen(fullfile(root,'results','report_evidence.json'),'w');fprintf(fid,'%s',jsonencode(e,PrettyPrint=true));fclose(fid);
disp(e);
end
