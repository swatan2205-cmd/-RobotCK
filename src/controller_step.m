function [requested,applied,memory,diag]=controller_step(q,ref,c,sets,memory)
diag=struct('index',NaN,'exitflag',NaN,'constraintResidual',NaN,'iterations',0,...
    'saturated',false,'mode','');
if strcmp(c.controller,'lyapunov')
    delta=ref.q(1:2)-q(1:2);
    ex=[cos(q(3)) sin(q(3))]*delta;
    ey=[-sin(q(3)) cos(q(3))]*delta;
    es=sin(ref.q(3)-q(3)); ec=cos(ref.q(3)-q(3))-1;
    p=c.lyap; h=1+ec/p.a;
    vb=p.kx*ex; wb=p.k*ref.v*ey*h^2+p.ks*es*h^(2*p.n);
    requested=body_to_wheel([ref.v*cos(ref.q(3)-q(3))+vb;ref.omega+wb],c.robot);
    applied=max(-c.wheelLimit,min(c.wheelLimit,requested));
    diag.saturated=any(abs(applied-requested)>c.constraintTolerance);
    diag.mode='blazic18'; diag.constraintResidual=max(abs(applied)/c.wheelLimit-1);
    return
end
assert(sets.assumptionOK,'RobotCK:InfeasibleSets','Reference bound exceeds robust input radius');
b=c.robot.b; Ts=c.Ts;
z=q(1:2)+b*[cos(q(3));sin(q(3))]-ref.z;
j=find(norm(z)<=sets.radii+c.membershipTolerance,1);
assert(~isempty(j),'RobotCK:OutsideDomain','Error outside computed domain');
diag.index=j-1;
Tfl=[cos(q(3)) sin(q(3));-sin(q(3))/b cos(q(3))/b];
T=[c.robot.r/2 c.robot.r/2;c.robot.r/c.robot.d -c.robot.r/c.robot.d];
Hd=[-1 0;0 -1;1 0;0 1]/c.wheelLimit;
H=Hd*(T\Tfl); g=ones(4,1); ur=ref.u;
if j>1
    diag.mode='reaching'; Qpre=sets.Q(:,:,j-1);
    objective=@(u)sum((z+Ts*u).^2);
    constr=@(u)reach_constraint(u,z,Ts,Qpre,H,g,ur);
    options=optimoptions('fmincon','Display','off','ConstraintTolerance',1e-9,...
        'OptimalityTolerance',1e-9,'StepTolerance',1e-12,'MaxFunctionEvaluations',2000);
    if strcmp(c.solverProfile,'author'), options=optimoptions('fmincon','Display','off'); end
    [uhat,~,flag,output]=fmincon(objective,[0;0],[],[],[],[],[],[],constr,options);
    if isempty(uhat), error('RobotCK:Solver','Empty fmincon result'); end
    residual=constr(uhat); diag.constraintResidual=max(residual);
    u=uhat+ur;
else
    diag.mode='terminal'; uhat=-z/Ts;
    options=optimoptions('quadprog','Algorithm','interior-point-convex','Display','off',...
        'ConstraintTolerance',1e-9,'OptimalityTolerance',1e-9);
    if strcmp(c.solverProfile,'author'), options=optimoptions('quadprog','Algorithm','interior-point-convex','Display','off'); end
    [urhat,~,flag,output]=quadprog(eye(2),-ur,H,g-H*uhat,[],[],[],[],[],options);
    if isempty(urhat), error('RobotCK:Solver','Empty quadprog result'); end
    u=uhat+urhat; diag.constraintResidual=max(H*u-g);
end
diag.exitflag=flag; diag.iterations=output.iterations;
assert(flag>0 && all(isfinite(u)) && diag.constraintResidual<=c.constraintTolerance,...
    'RobotCK:Solver','Solver failed or violated constraints');
requested=T\(Tfl*u); applied=requested; memory.u_previous=uhat;
end

function [ineq,eq]=reach_constraint(u,z,Ts,Q,H,g,ur)
pred=z+Ts*u;
ineq=[H*(u+ur)-g;pred'*(Q\pred)-1]; eq=[];
end
