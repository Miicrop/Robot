import numpy as np
import serial, time
from axis import Axis

try:
    arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
    time.sleep(2)
except:
    print("no arduino connection possible")

class Robot:
    def __init__(self):
        self.axes_params = [    # insert DH-Params
            (0,  84, 0, -90),   # axis 4
            (0,   0, 0,  90),   # axis 5 
            (0, 141, 0,   0),   # axis 6
        #     (0,   0, 0,   0)    # axis flange
        ]
        self.axes = [Axis(*params) for params in self.axes_params]
        self.thetas = []
        self.read_thetas()
        
        self.max_speed = 2000
        self.current_speed = self.max_speed
        self.current_speed_percentage = 100
        self.valid_speeds = [3, 5, 10, 30, 50, 100]
        
    def forward_kinematics(self):
        T = np.eye(4)
        for axis in self.axes:
            T = np.dot(T, axis.transformation_matrix())
        T = np.round(T, decimals=5)
        return T
    
    def save_forward_kinematics(self):
        T = self.forward_kinematics()
        with open("config/currentProgram.txt", "a+") as f:
            np.savetxt(f, T, fmt='%.5f')
            f.write("\n")
            
    def load_forward_kinematics(self):
        with open("config/currentProgram.txt", "r") as f:
            content = f.read().strip().split("\n\n")
            matrices = [np.fromstring(matrix_str, sep=" ").reshape((4, 4)) for matrix_str in content]
        return matrices
    
    def clear_forards_kinematics(self):
        open('config/currentProgram.txt', 'w').close()
    
    def get_position(self):
        return self.forward_kinematics()[:3, 3]
    
    def get_orientation(self):
        return self.forward_kinematics()[:3, :3]
    
    def print_parameters(self):
        print(f"Forward-Kinematics: \n {self.forward_kinematics()} \n -------")
        print(f"Position: {self.get_position()} \n -------")
        print(f"Orientation: \n {self.get_orientation()}")
        
    def set_theta(self, axis_index, theta):
        self.axes[axis_index].set_theta(theta)
        self.update_thetas()
    
    def get_theta(self, axis_index):
        return self.axes[axis_index].get_theta()
    
    def update_thetas(self):
        self.thetas = [axis.get_theta() for axis in self.axes]
        with open("config/currentAngles.txt", "w") as f:
            for theta in self.thetas:
                f.write(f"{theta}\n")
    
    def read_thetas(self):
        try:
            with open("config/currentAngles.txt", "r") as f:
                [axis.set_theta(float(f.readline())) for axis in self.axes]
        except:
            self.update_thetas()
            
    def set_speed(self, speed_percentage):
        if speed_percentage in self.valid_speeds:
            self.current_speed_percentage = speed_percentage
            self.current_speed = self.current_speed_percentage * self.max_speed / 100
        else:
            raise ValueError("Invalid speed percentage")
        
    def increase_speed(self):
        currentIndex = self.valid_speeds.index(self.current_speed_percentage)
        if currentIndex < len(self.valid_speeds) - 1:
            self.current_speed_percentage = self.valid_speeds[currentIndex + 1]
        self.set_speed(self.current_speed_percentage)
            
    def decrease_speed(self):
        currentIndex = self.valid_speeds.index(self.current_speed_percentage)
        if currentIndex > 0:
            self.current_speed_percentage = self.valid_speeds[currentIndex - 1]
        self.set_speed(self.current_speed_percentage)
            
    def calculate_steps(self, target_angle):
        standard_degrees_per_step = 1.8
        step_mode = 4
        gear_transmission = 96
        degrees = standard_degrees_per_step / step_mode
        
        return int((target_angle / degrees) * gear_transmission)
    
    def send_string_over_serial(self):
        array_to_send = []
        for axis in self.axes:
            theta = axis.get_theta()
            steps = self.calculate_steps(theta)
            array_to_send.append(str(steps))

        array_to_send.append(str(self.current_speed))
        string_to_send = ",".join(array_to_send)
        
        arduino.write(bytes(string_to_send, 'utf-8'))
        
        # for i in range(4):
        #     data = arduino.readline().decode('utf-8').strip()
        #     print(data)

            
    # def inverse_kinematics(self, target_transforms, max_iterations=1000, threshold=1e-6, alpha=0.1):
    #     """
    #     Numerical Inverse Kinematics using Jacobian Transpose Method for multiple targets.

    #     :param target_transforms: List of 4x4 arrays of target transformation matrices
    #     :param max_iterations: Maximum number of iterations per target
    #     :param threshold: Convergence threshold
    #     :param alpha: Learning rate
    #     :return: List of thetas for each target if converged, else None
    #     """
    #     thetas_list = []
        
    #     for target_transform in target_transforms:
    #         for i in range(max_iterations):
    #             current_fk = self.forward_kinematics()
    #             current_transform = current_fk  # Assuming forward_kinematics returns 4x4 matrix
    #             current_position = current_transform[:3, 3]
    #             current_orientation = current_transform[:3, :3]
                
    #             target_position = target_transform[:3, 3]
    #             target_orientation = target_transform[:3, :3]
                
    #             position_error = target_position - current_position
    #             orientation_error = 0.5 * (np.cross(current_orientation[:, 0], target_orientation[:, 0]) +
    #                                        np.cross(current_orientation[:, 1], target_orientation[:, 1]) +
    #                                        np.cross(current_orientation[:, 2], target_orientation[:, 2]))
    #             error = np.hstack((position_error, orientation_error))
                
    #             if np.linalg.norm(error) < threshold:
    #                 thetas_list.append([axis.get_theta() for axis in self.axes])
    #                 break  # Exit inner loop if converged
                
    #             J = self.compute_jacobian()
                
    #             self.update_thetas_with_jacobian(J, error, alpha)
            
    #         else:
    #             # If inner loop did not break (reached max_iterations), return None for this target
    #             thetas_list.append(None)
        
    #     return thetas_list
            
    # def compute_jacobian(self):
    #     """
    #     Compute the Jacobian matrix for the robot.

    #     :return: 6xN Jacobian matrix
    #     """
    #     num_axes = len(self.axes)
    #     J = np.zeros((6, num_axes))
        
    #     T = np.eye(4)
    #     positions = [T[:3, 3]]
        
    #     for i, axis in enumerate(self.axes):
    #         T = np.dot(T, axis.transformation_matrix())
    #         positions.append(T[:3, 3])
        
    #     # Compute the Jacobian matrix
    #     for i in range(num_axes):
    #         z = T[:3, 2]  # z-axis of the current frame
    #         p = positions[-1]  # position of the end effector
    #         J[:3, i] = np.cross(z, (p - positions[i]))
    #         J[3:, i] = z
        
    #     return J
    
    # def update_thetas_with_jacobian(self, J, error, alpha):
    #     """
    #     Update the joint angles using the Jacobian Transpose method.

    #     :param J: Jacobian matrix
    #     :param error: Error vector
    #     :param alpha: Learning rate
    #     """
    #     d_theta = alpha * J.T.dot(error)
    #     for i in range(len(self.axes)):
    #         current_theta = self.axes[i].get_theta()
    #         new_theta = current_theta + d_theta[i]
    #         self.axes[i].set_theta(new_theta)
            

# DIE HIER GEHT SO HALBWEGS!!            
    def inverse_kinematics_from_matrices(self, matrices):
        # Liste für Gelenkwinkel
        thetas_list = []

        for T_desired in matrices:
            # Initiale Transformation initialisieren
            T_current = np.eye(4)
            thetas = []

            # Iteration über die Achsen in umgekehrter Reihenfolge
            for axis in reversed(self.axes):
                T_current = np.dot(np.linalg.inv(axis.transformation_matrix()), T_current)
                
                # Berechnung der gewünschten Transformation relativ zur Basis
                T_desired_base = np.dot(T_current, T_desired)
                
                # Extrahieren der Rotation und Position
                R_desired = T_desired_base[:3, :3]
                p_desired = T_desired_base[:3, 3]
                
                # Berechnung der Gelenkwinkel für die aktuelle Achse
                theta = np.arctan2(R_desired[1, 0], R_desired[0, 0])
                d = p_desired[2]
                a = np.sqrt(p_desired[0]**2 + p_desired[1]**2)
                alpha = np.arctan2(R_desired[2, 1], R_desired[2, 2])
                
                # Umwandlung von theta in Grad
                theta_deg = axis.radians_to_degrees(theta)
                
                # Theta setzen und speichern
                axis.set_theta(theta_deg)
                thetas.append(theta_deg)
            
            # Die Gelenkwinkel für die aktuelle Transformation speichern
            thetas_list.append(thetas[::-1])  # In umgekehrter Reihenfolge hinzufügen
        
        # Die Liste der Gelenkwinkel zurückgeben
        return thetas_list