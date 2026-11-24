function c=default_config()
c.robot=struct('r',0.0205,'d',0.053,'b',0.1);
c.Ts=0.15; c.duration=44; c.wheelLimit=10; c.Nsets=700;
c.trajectory='eight'; c.eta=0.6; c.alpha=3.5;
c.circleRadius=0.6; c.circleOmega=1/7;
c.q0=[0.6;0;pi]; c.controller='tstrhc'; c.integrator='ode45';
c.solverProfile='validated';
c.RelTol=1e-8; c.AbsTol=1e-10;
c.constraintTolerance=1e-7; c.membershipTolerance=1e-9;
c.lyap=struct('k',1,'kx',1,'ks',1,'a',2.1,'n',1);
c.timingRepeats=5; c.warmupSteps=10;
end
