function export_results()
root=setup_project(); folders=dir(fullfile(root,'results','*_i*_w*'));
set(0,'DefaultFigureVisible','off');
for i=1:numel(folders)
 if isempty(regexp(folders(i).name,'^(eight|circle)_i[123]_w(8|10|12)_(tstrhc|lyapunov)$','once')), continue; end
 data=load(fullfile(folders(i).folder,folders(i).name,'run.mat'),'run'); r=data.run;
 n=r.completedSteps;
 if n==0, continue; end
 f=figure('Position',[100 100 1100 700],'Color','w');
 tiledlayout(2,2,'TileSpacing','loose','Padding','loose');
 nexttile; plot(r.reference.q(1,:),r.reference.q(2,:),'r--',r.q(1,1:n+1),r.q(2,1:n+1),'b-');
 axis equal; grid on; xlabel('x (m)'); ylabel('y (m)'); legend('Reference','Robot');
 nexttile; ep=vecnorm(r.q(1:2,1:n+1)-r.reference.q(1:2,1:n+1));
 plot(r.t_state(1:n+1),ep); xlabel('t (s)'); ylabel('Position error (m)'); grid on;
 nexttile; plot(r.t_control(1:n),r.wheel_applied(:,1:n));
 yline(r.config.wheelLimit,'r--'); yline(-r.config.wheelLimit,'r--');
 xlabel('t (s)'); ylabel('Wheel velocity (rad/s)'); legend('Right','Left'); grid on;
 nexttile;
 if strcmp(r.config.controller,'tstrhc'), stairs(r.t_control(1:n),[r.diagnostics.index]); ylabel('Set index (zero based)');
 else, plot(r.t_state(1:n+1),atan2(sin(r.q(3,1:n+1)-r.reference.q(3,1:n+1)),cos(r.q(3,1:n+1)-r.reference.q(3,1:n+1)))); ylabel('Heading error (rad)'); end
 xlabel('t (s)'); grid on; sgtitle(strrep(r.run_id,'_',' '));
 drawnow; set(f,'PaperPositionMode','auto');
 print(f,fullfile(root,'figures',[r.run_id '.png']),'-dpng','-r150'); close(f);
end
end
