function tests=test_robot_project
tests=functiontests(localfunctions);
end
function testWheelKnownCases(t)
c=default_config(); r=c.robot;
verifyEqual(t,wheel_to_body([1;1],r),[r.r;0],'AbsTol',1e-14);
verifyEqual(t,wheel_to_body([1;-1],r),[0;2*r.r/r.d],'AbsTol',1e-14);
w=[-3 2;4 -1]; verifyEqual(t,body_to_wheel(wheel_to_body(w,r),r),w,'AbsTol',1e-13);
end
function testReferenceDerivative(t)
c=default_config(); ts=linspace(1,3,20001); h=ts(2)-ts(1);
for trajectory={'eight','circle'}
 c.trajectory=trajectory{1}; r=make_reference(ts,c);
 derivative=diff(r.q(1:2,:),1,2)/h; mid=make_reference(ts(1:end-1)+h/2,c);
 verifyLessThan(t,max(abs(derivative-mid.dq(1:2,:)),[],'all'),1e-8);
 verifyLessThan(t,max(abs(diff(r.q(3,:)))),0.01);
end
end
function testReachSets(t)
c=default_config(); ref=make_reference(0:.01:44,c); s=prepare_sets(c,ref);
verifyTrue(t,s.assumptionOK);
verifyGreaterThan(t,min(eig(s.Q(:,:,1))),0);
verifyEqual(t,diff(s.radii),repmat(s.growth,1,c.Nsets),'AbsTol',1e-13);
% Worst direction: ||z+Ts*u||+Ts*bound <= previous radius.
radius=s.radii(40); nextRadius=s.radii(41);
verifyEqual(t,nextRadius-c.Ts*s.ru+c.Ts*s.referenceBound,radius,'AbsTol',1e-13);
end
function testAngleWrapAndDomainFailure(t)
c=default_config(); ref=make_reference(0:.01:44,c);
verifyLessThan(t,max(abs(diff(ref.q(3,:)))),0.1);
verifyEqual(t,[cos(ref.q(3,:));sin(ref.q(3,:))],...
    ref.dq(1:2,:)./ref.v,'AbsTol',1e-12);
c.wheelLimit=8; c.duration=.3; r=simulate_case(c);
verifyEqual(t,r.status,'failed'); verifyEqual(t,r.completedSteps,0);
verifyTrue(t,isnan(r.metrics.rmse));
c.wheelLimit=10; c.q0=[100;0;0]; r=simulate_case(c);
verifyEqual(t,r.status,'failed'); verifyTrue(t,contains(r.error,'outside computed domain'));
end
function testExactIntegration(t)
c=default_config(); q=[.1;.2;.9]; w=[4;-2];
c.integrator='exact'; exact=integrate_robot(q,w,c);
c.integrator='ode45'; numerical=integrate_robot(q,w,c);
verifyEqual(t,numerical,exact,'AbsTol',1e-8);
end
function testLyapunovDerivative(t)
c=default_config(); c.controller='lyapunov'; ref=make_reference(0,c);
rk=struct('q',ref.q,'z',ref.z,'u',ref.u,'v',ref.v,'omega',ref.omega);
for angle=[-pi -1 0 1 pi]
 q=ref.q+[.2;-.1;angle]; [req,~,~,~]=controller_step(q,rk,c,[],struct());
 vw=wheel_to_body(req,c.robot); delta=ref.q(1:2)-q(1:2);
 ex=[cos(q(3)) sin(q(3))]*delta; ey=[-sin(q(3)) cos(q(3))]*delta;
 es=sin(ref.q(3)-q(3)); ec=cos(ref.q(3)-q(3))-1; h=1+ec/c.lyap.a;
 vb=vw(1)-ref.v*cos(ref.q(3)-q(3)); wb=vw(2)-ref.omega;
 actual=-c.lyap.k*ex*vb+es*(c.lyap.k*ref.v*ey-wb/h^2);
 expected=-c.lyap.k*c.lyap.kx*ex^2-c.lyap.ks*es^2*h^(2*c.lyap.n-2);
 verifyEqual(t,actual,expected,'AbsTol',1e-12); verifyLessThanOrEqual(t,actual,1e-12);
end
end
function testSolverAndSaturation(t)
c=default_config(); c.duration=1.5; r=simulate_case(c);
verifyEqual(t,r.status,'completed'); verifyTrue(t,all([r.diagnostics.exitflag]>0));
verifyLessThanOrEqual(t,max(abs(r.wheel_applied),[],'all'),c.wheelLimit+1e-6);
c.controller='lyapunov'; c.q0=[10;10;pi]; r=simulate_case(c);
verifyGreaterThan(t,r.metrics.saturationCount,0); verifyEqual(t,r.metrics.violationCountR,0);
end
function testMetricsKnownConstant(t)
c=default_config(); r=simulate_case(setfield(c,'duration',.3)); %#ok<SFLD>
r.q=r.reference.q; r.q(1,:)=r.q(1,:)+3; r.q(2,:)=r.q(2,:)+4;
m=compute_metrics(r); verifyEqual(t,m.rmse,5,'AbsTol',1e-12);
verifyEqual(t,m.iae,5*r.t_state(end),'AbsTol',1e-12);
end
