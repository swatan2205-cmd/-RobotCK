function w=body_to_wheel(vw,robot)
w=[1/robot.r robot.d/(2*robot.r);1/robot.r -robot.d/(2*robot.r)]*vw;
end
