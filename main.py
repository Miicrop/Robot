from robot import Robot

robot = Robot()
# robot.print_parameters()

# robot.set_theta(0, 90)
# robot.save_forward_kinematics()
robot.set_theta(1, 90)
robot.save_forward_kinematics()

[print(f"{i}\n") for i in robot.load_forward_kinematics()]

# robot.pretty_print_matrices(robot.load_forward_kinematics())

thetas_list = robot.inverse_kinematics_from_matrices(robot.load_forward_kinematics())

# Ausgabe der berechneten Gelenkwinkel
for idx, thetas in enumerate(thetas_list):
    print(f"Gelenkwinkel für Transformation {idx}: {thetas}")