function m=compute_metrics(run)
n=run.completedSteps; c=run.config;
% Primary metrics require the complete common evaluation interval.
m=struct('rmse',NaN,'iae',NaN,'maxError',NaN,'commandVariation',NaN,...
    'violationCountR',NaN,'violationCountL',NaN,'violationRateR',NaN,'violationRateL',NaN,...
    'maxExcessR',NaN,'maxExcessL',NaN,'meanControlSeconds',NaN,'p95ControlSeconds',NaN,...
    'maxControlSeconds',NaN,'deadlineMisses',NaN,'saturationCount',NaN,'frontRMSE',NaN);
if n==0, return; end
times=run.controlSeconds(1:n);
m.meanControlSeconds=mean(times); m.p95ControlSeconds=prctile(times,95);
m.maxControlSeconds=max(times); m.deadlineMisses=sum(times>c.Ts);
m.saturationCount=sum([run.diagnostics.saturated]);
if ~strcmp(run.status,'completed'), return; end
err=run.q(1:2,:)-run.reference.q(1:2,:); ep=vecnorm(err);
m.rmse=sqrt(mean(ep.^2)); m.iae=trapz(run.t_state,ep); m.maxError=max(ep);
w=run.wheel_applied;
excess=max(abs(w)-c.wheelLimit,0); violation=excess>c.constraintTolerance;
m.violationCountR=sum(violation(1,:)); m.violationCountL=sum(violation(2,:));
m.violationRateR=mean(violation(1,:)); m.violationRateL=mean(violation(2,:));
m.maxExcessR=max(excess(1,:)); m.maxExcessL=max(excess(2,:));
m.commandVariation=sum(sum(diff(w,1,2).^2));
front=run.q(1:2,:)+c.robot.b*[cos(run.q(3,:));sin(run.q(3,:))];
m.frontRMSE=sqrt(mean(sum((front-run.reference.z).^2,1)));
end
