function ref=make_reference(t,c)
switch c.trajectory
    case 'eight'
        x=c.eta*sin(t/c.alpha); y=c.eta*sin(t/(2*c.alpha));
        dx=c.eta/c.alpha*cos(t/c.alpha); dy=c.eta/(2*c.alpha)*cos(t/(2*c.alpha));
        ddx=-c.eta/c.alpha^2*sin(t/c.alpha); ddy=-c.eta/(4*c.alpha^2)*sin(t/(2*c.alpha));
    case 'circle'
        x=c.circleRadius*cos(c.circleOmega*t); y=c.circleRadius*sin(c.circleOmega*t);
        dx=-c.circleRadius*c.circleOmega*sin(c.circleOmega*t); dy=c.circleRadius*c.circleOmega*cos(c.circleOmega*t);
        ddx=-c.circleRadius*c.circleOmega^2*cos(c.circleOmega*t); ddy=-c.circleRadius*c.circleOmega^2*sin(c.circleOmega*t);
    otherwise, error('RobotCK:Reference','Unknown trajectory');
end
speed2=dx.^2+dy.^2;
assert(all(speed2>1e-14),'Reference is singular at zero speed');
theta=unwrap(atan2(dy,dx)); v=sqrt(speed2); omega=(dx.*ddy-dy.*ddx)./speed2;
b=c.robot.b;
ref=struct('t',t,'q',[x;y;theta],'v',v,'omega',omega,'dq',[dx;dy;omega],...
    'ddxy',[ddx;ddy],'z',[x+b*cos(theta);y+b*sin(theta)]);
ref.u=[dx-b*sin(theta).*omega;dy+b*cos(theta).*omega];
ref.wheel=body_to_wheel([v;omega],c.robot);
end
