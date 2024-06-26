import tkinter
import customtkinter
from PIL import Image
import os, sys

from robot import Robot

robot = Robot()

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("960x700")
        
        self.grid_columnconfigure(0, weight=1)
        
        self.theta_constant = 5.0
        
        self.button_frame = customtkinter.CTkFrame(self)
        self.button_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.button_frame.grid_columnconfigure((0,1,2), weight=0)
        
        
        self.button_a1_decrease = customtkinter.CTkButton(self.button_frame, text="-", width=50, command=lambda:self.decrease_theta(0))
        self.button_a1_decrease.grid(row=0, column=0, padx=10, pady=30)
        
        self.button_a2_decrease = customtkinter.CTkButton(self.button_frame, text="-", width=50, command=lambda:self.decrease_theta(1))
        self.button_a2_decrease.grid(row=1, column=0, padx=10, pady=30)
        
        self.button_a3_decrease = customtkinter.CTkButton(self.button_frame, text="-", width=50, command=lambda:self.decrease_theta(2))
        self.button_a3_decrease.grid(row=2, column=0, padx=10, pady=30)
        
        self.button_a4_decrease = customtkinter.CTkButton(self.button_frame, text="-", width=50, command=lambda:self.decrease_theta(3))
        self.button_a4_decrease.grid(row=3, column=0, padx=10, pady=30)
        
        self.button_a5_decrease = customtkinter.CTkButton(self.button_frame, text="-", width=50, command=lambda:self.decrease_theta(4))
        self.button_a5_decrease.grid(row=4, column=0, padx=10, pady=30)
        
        self.button_a6_decrease = customtkinter.CTkButton(self.button_frame, text="-", width=50, command=lambda:self.decrease_theta(5))
        self.button_a6_decrease.grid(row=5, column=0, padx=10, pady=30)

        
        self.button_a1_increase = customtkinter.CTkButton(self.button_frame, text="+", width=50, command=lambda:self.increase_theta(0))
        self.button_a1_increase.grid(row=0, column=1, padx=10, pady=30)
        
        self.button_a2_increase = customtkinter.CTkButton(self.button_frame, text="+", width=50, command=lambda:self.increase_theta(1))
        self.button_a2_increase.grid(row=1, column=1, padx=10, pady=30)
        
        self.button_a3_increase = customtkinter.CTkButton(self.button_frame, text="+", width=50, command=lambda:self.increase_theta(2))
        self.button_a3_increase.grid(row=2, column=1, padx=10, pady=30)
        
        self.button_a4_increase = customtkinter.CTkButton(self.button_frame, text="+", width=50, command=lambda:self.increase_theta(3))
        self.button_a4_increase.grid(row=3, column=1, padx=10, pady=30)
        
        self.button_a5_increase = customtkinter.CTkButton(self.button_frame, text="+", width=50, command=lambda:self.increase_theta(4))
        self.button_a5_increase.grid(row=4, column=1, padx=10, pady=30)
        
        self.button_a6_increase = customtkinter.CTkButton(self.button_frame, text="+", width=50, command=lambda:self.increase_theta(5))
        self.button_a6_increase.grid(row=5, column=1, padx=10, pady=30)
      
        
        self.label_a1 = customtkinter.CTkLabel(self.button_frame, text="Axis 1")
        self.label_a1.grid(row=0, column=2, padx=10, pady=30)
        
        self.label_a2 = customtkinter.CTkLabel(self.button_frame, text="Axis 2")
        self.label_a2.grid(row=1, column=2, padx=10, pady=30)
        
        self.label_a3 = customtkinter.CTkLabel(self.button_frame, text="Axis 3")
        self.label_a3.grid(row=2, column=2, padx=10, pady=30)
        
        self.label_a4 = customtkinter.CTkLabel(self.button_frame, text="Axis 4")
        self.label_a4.grid(row=2, column=2, padx=10, pady=30)
        
        self.label_a5 = customtkinter.CTkLabel(self.button_frame, text="Axis 5")
        self.label_a5.grid(row=2, column=2, padx=10, pady=30)
        
        self.label_a6 = customtkinter.CTkLabel(self.button_frame, text="Axis 6")
        self.label_a6.grid(row=2, column=2, padx=10, pady=30)
        
        
        self.label_a1_theta = customtkinter.CTkLabel(self.button_frame, text="Theta 1")
        self.label_a1_theta.grid(row=0, column=7, padx=10, pady=30)
        
        self.label_a2_theta = customtkinter.CTkLabel(self.button_frame, text="Theta 2")
        self.label_a2_theta.grid(row=1, column=7, padx=10, pady=30)
        
        self.label_a3_theta = customtkinter.CTkLabel(self.button_frame, text="Theta 3")
        self.label_a3_theta.grid(row=2, column=7, padx=10, pady=30)
        
        self.label_a4_theta = customtkinter.CTkLabel(self.button_frame, text="Theta 4")
        self.label_a4_theta.grid(row=3, column=7, padx=10, pady=30)
        
        self.label_a5_theta = customtkinter.CTkLabel(self.button_frame, text="Theta 5")
        self.label_a5_theta.grid(row=4, column=7, padx=10, pady=30)
        
        self.label_a6_theta = customtkinter.CTkLabel(self.button_frame, text="Theta 6")
        self.label_a6_theta.grid(row=5, column=7, padx=10, pady=30)
        
        
        self.button_theta_1 = customtkinter.CTkButton(self.button_frame, text="1", width=50, command=lambda:self.change_theta_constant(1))
        self.button_theta_1.grid(row=6, column=0, padx=10, pady=(50,10))
        
        self.button_theta_5 = customtkinter.CTkButton(self.button_frame, text="5", width=50, command=lambda:self.change_theta_constant(5))
        self.button_theta_5.grid(row=6, column=1, padx=10, pady=(50,10))
        
        self.button_theta_10 = customtkinter.CTkButton(self.button_frame, text="10", width=50, command=lambda:self.change_theta_constant(10))
        self.button_theta_10.grid(row=6, column=2, padx=10, pady=(50,10))
        
        
        self.button_speed_decrease = customtkinter.CTkButton(self.button_frame, text="-", width=50, command=self.decrease_speed)
        self.button_speed_decrease.grid(row=0, column=3, padx=10, pady=30)
        
        self.button_speed_increase = customtkinter.CTkButton(self.button_frame, text="+", width=50, command=self.increase_speed)
        self.button_speed_increase.grid(row=0, column=4, padx=10, pady=30)
        
        self.label_speed = customtkinter.CTkLabel(self.button_frame, text="current Speed")
        self.label_speed.grid(row=0, column=5, padx=10, pady=30)
        
        
        self.button_save_current_position = customtkinter.CTkButton(self.button_frame, text="Save current Position", width=200, command=self.save_current_position)
        self.button_save_current_position.grid(row=0, column=6, padx=10, pady=30)
        
        self.button_run_programm = customtkinter.CTkButton(self.button_frame, text="Run Programm", width=200, command=self.run_programm)
        self.button_run_programm.grid(row=1, column=6, padx=10, pady=30)
        
        self.button_clear_programm = customtkinter.CTkButton(self.button_frame, text="Clear Programm", width=200, command=self.clear_programm)
        self.button_clear_programm.grid(row=2, column=6, padx=10, pady=30)
        
        self.update_all_on_startup()
        
    def update_all_on_startup(self):
        self.update_speed_label()
        self.update_thetas()
        
        
    def decrease_theta(self, axis_index):
        robot.set_theta(axis_index, robot.get_theta(axis_index) - self.theta_constant)
        self.update_thetas()
    
    def increase_theta(self, axis_index):
        robot.set_theta(axis_index, robot.get_theta(axis_index) + self.theta_constant)
        self.update_thetas()
    
    def update_thetas(self):
        self.label_a1_theta.configure(text=robot.get_theta(0))
        self.label_a2_theta.configure(text=robot.get_theta(1))
        self.label_a3_theta.configure(text=robot.get_theta(2))
        # self.label_a4_theta.configure(text=robot.get_theta(4))
        # self.label_a5_theta.configure(text=robot.get_theta(5))
        # self.label_a6_theta.configure(text=robot.get_theta(6))
        
    def change_theta_constant(self, new_theta_constant):
        self.theta_constant = new_theta_constant
    

    def decrease_speed(self):
        robot.decrease_speed()
        self.update_speed_label()
        
    def increase_speed(self):
        robot.increase_speed()
        self.update_speed_label()
        
    def update_speed_label(self):
        self.label_speed.configure(text=robot.currentSpeed)
 
        
    def save_current_position(self):
        robot.save_forward_kinematics()
        
    def run_programm(self):
        pass
    
    def clear_programm(self):
        robot.clear_forards_kinematics()
        

app = App()
app.mainloop()