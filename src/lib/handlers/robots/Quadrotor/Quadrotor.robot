RobotName: # Robot Name
Quadrotor

Type: # Robot type
Quadrotor

ActuatorHandler: # Robot default actuator handler with default argument values
QuadrotorActuator()

SensorHandler: # Robot default actuator handler with default argument values
QuadrotorSensor()

DriveHandler: # Robot default drive handler with default argument values
QuadrotorDrive()

InitHandler: # Robot default init handler with default argument values
QuadrotorInit(comPort='COM3')

LocomotionCommandHandler: # Robot locomotion command actuator handler with default argument values
QuadrotorLocomotionCommand()

MotionControlHandler: # Robot default motion control handler with default argument values
vectorController()

PoseHandler: # Robot default pose handler with default argument values
viconPose(host='10.0.0.102',port=800,x_VICON_name="Quadrotor01:Quadrotor01 <t-X>",y_VICON_name="Quadrotor01:Quadrotor01 <t-Y>",theta_VICON_name="Quadrotor01:Quadrotor01 <a-Z>", z_VICON_name="Quadrotor01:Quadrotor01 <t-Z>")

