import numpy as np
import serial, time, threading
from axis import Axis


class Robot:
    def __init__(self):
        self.axes_params = [
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
        
        self.standard_degrees_per_step = 1.8
        self.step_mode = 4
        self.gear_transmission = 96
        
        try:
            self.arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
            time.sleep(2)
            self.serial_thread = threading.Thread(target=self.read_serial)
            self.serial_thread.daemon = True
            self.serial_thread.start()
        except:
            print("no arduino connection possible")
        
    def read_serial(self):
        while True:
            try:
                line = self.arduino.readline().decode('utf-8').strip()
                if line:
                    self.current_positions = line
                    print(f"{line}")
            except serial.SerialException as e:
                print(f"Error reading serial: {e}")
                break

    def forward_kinematics(self):
        T = np.eye(4)
        for axis in self.axes:
            T = np.dot(T, axis.transformation_matrix())
        T = np.round(T, decimals=5)
        return T
    
    # def save_forward_kinematics(self):
    #     T = self.forward_kinematics()
    #     with open("config/currentProgram.txt", "a+") as f:
    #         np.savetxt(f, T, fmt='%.5f')
    #         f.write("\n")
            
    # def load_forward_kinematics(self):
    #     with open("config/currentProgram.txt", "r") as f:
    #         content = f.read().strip().split("\n\n")
    #         matrices = [np.fromstring(matrix_str, sep=" ").reshape((4, 4)) for matrix_str in content]
    #     return matrices
    
    # def clear_forards_kinematics(self):
    #     open('config/currentProgram.txt', 'w').close()
    
    # def get_position(self):
    #     return self.forward_kinematics()[:3, 3]
    
    # def get_orientation(self):
    #     return self.forward_kinematics()[:3, :3]
    
    # def print_parameters(self):
    #     print(f"Forward-Kinematics: \n {self.forward_kinematics()} \n -------")
    #     print(f"Position: {self.get_position()} \n -------")
    #     print(f"Orientation: \n {self.get_orientation()}")
        
    def set_theta(self, axis_index, theta):
        self.axes[axis_index].set_theta(theta)
        self.update_thetas()
    
    def get_theta(self, axis_index):
        return self.axes[axis_index].get_theta()
    
    def update_thetas(self):
        self.thetas = [axis.get_theta() for axis in self.axes]
        with open("config/currentThetas.txt", "w") as f:
            for theta in self.thetas:
                f.write(f"{theta}\n")
    
    def read_thetas(self):
        try:
            with open("config/currentThetas.txt", "r") as f:
                [axis.set_theta(float(f.readline())) for axis in self.axes]
        except:
            self.update_thetas()
            
    def save_thetas(self):
        self.thetas = [axis.get_theta() for axis in self.axes]
        with open("config/currentThetasProgram.txt", "a+") as f:
            for theta in self.thetas:
                f.write(f"{theta}\n")
            f.write("\n")
            
    def clear_thetas(self):
        open('config/currentThetasProgram.txt', 'w').close()
            
    def set_speed(self, speed_percentage):
        if speed_percentage in self.valid_speeds:
            self.current_speed_percentage = speed_percentage
            self.current_speed = self.current_speed_percentage * self.max_speed / 100
            self.send_string_over_serial("s", self.current_speed)
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
        degrees = self.standard_degrees_per_step / self.step_mode
        return int((target_angle / degrees) * self.gear_transmission)
    
    def calculate_theta_from_position(self, position):
        return int(position) / self.gear_transmission * self.standard_degrees_per_step / self.step_mode
    
    def get_current_positions(self):
        command_positions = self.current_positions.strip(",").split(",")
        for positions in command_positions:
            axis_index, position = positions.split(":")
            axis_index = int(axis_index)
            position = int(position)
            theta = self.calculate_theta_from_position(position)
            # ToDo: write 2 Theta Files and read on startup to add the start value on top of theta.
            # ToDo: on Robot Start transfer the last saved thetas from the second file to the "start" file with new values to calculate from 0
            self.set_theta(axis_index, theta)
    
    def send_string_over_serial(self, prefix, value):
        string_to_send = f"{prefix}{value}\n"
        self.arduino.write(bytes(string_to_send, 'utf-8'))
        
     
    def run_programm(self):
        with open("config/currentThetasProgram.txt", "r") as f:
            content = f.read().strip().split("\n\n")
            matrices = [np.fromstring(matrix_str, sep=" ") for matrix_str in content]
            for matrix in matrices:
                index = 0
                result_strings = []
                for value in matrix:
                    steps = self.calculate_steps(value)
                    result_strings.append(f"{index}:{steps}")
                    index += 1
                string_to_send = ",".join(result_strings)
                # self.arduino.write(bytes(string_to_send, "utf-8"))