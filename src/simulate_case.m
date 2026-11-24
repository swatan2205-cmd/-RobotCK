function run=simulate_case(c,sets)
N=ceil(c.duration/c.Ts); t=(0:N)*c.Ts; ref=make_reference(t,c);
if nargin<2, sets=prepare_sets(c,ref); end
run=struct('config',c,'reference',ref,'sets',sets,'t_state',t,'t_control',t(1:end-1),...
    'q',nan(3,N+1),'wheel_requested',nan(2,N),'wheel_applied',nan(2,N),...
    'controlSeconds',nan(1,N),'diagnostics',[],'status','completed','error','',...
    'completedSteps',0);
run.q(:,1)=c.q0; memory=struct('u_previous',[0;0]);
for k=1:N
    rk=struct('q',ref.q(:,k),'z',ref.z(:,k),'u',ref.u(:,k),'v',ref.v(k),'omega',ref.omega(k));
    try
        clock=tic;
        [req,applied,memory,diagnostic]=controller_step(run.q(:,k),rk,c,sets,memory);
        run.controlSeconds(k)=toc(clock);
        run.diagnostics=[run.diagnostics diagnostic]; %#ok<AGROW>
        run.wheel_requested(:,k)=req; run.wheel_applied(:,k)=applied;
        run.q(:,k+1)=integrate_robot(run.q(:,k),applied,c);
        assert(all(isfinite(run.q(:,k+1))),'RobotCK:State','Non-finite state');
        run.completedSteps=k;
    catch ME
        run.status='failed'; run.error=getReport(ME,'extended','hyperlinks','off');
        run.failedStep=k; break
    end
end
run.errors.position=vecnorm(run.q(1:2,:)-ref.q(1:2,:));
run.errors.heading=atan2(sin(run.q(3,:)-ref.q(3,:)),cos(run.q(3,:)-ref.q(3,:)));
zactual=run.q(1:2,:)+c.robot.b*[cos(run.q(3,:));sin(run.q(3,:))];
run.errors.front=zactual-ref.z;
% Actual held-input evolution versus the nominal linear design step.
run.errors.linearizationResidual=nan(2,N);
for k=1:run.completedSteps
 vw=wheel_to_body(run.wheel_applied(:,k),c.robot);
 th=run.q(3,k); M=[cos(th) -c.robot.b*sin(th);sin(th) c.robot.b*cos(th)];
 run.errors.linearizationResidual(:,k)=zactual(:,k+1)-zactual(:,k)-c.Ts*M*vw;
end
run.metrics=compute_metrics(run);
end
