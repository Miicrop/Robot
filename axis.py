import numpy as np

class Axis:
    def __init__(self, theta, d, a, alpha):
        self.theta = self.degrees_to_radians(theta)
        self.d = d
        self.a = a
        self.alpha = self.degrees_to_radians(alpha)
        
    def degrees_to_radians(self, degrees):
        return degrees * np.pi / 180
    
    def radians_to_degrees(self, radians):
        return radians * 180 / np.pi
    
    def dh_params(self):
        return (self.theta, self.d, self.a, self.alpha)
    
    def transformation_matrix(self):
        theta, d, a, alpha = self.dh_params()
        
        return np.array([
            [np.cos(theta), -np.sin(theta) * np.cos(alpha),  np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
            [np.sin(theta),  np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
            [            0,                  np.sin(alpha),                  np.cos(alpha),                 d],
            [            0,                              0,                              0,                 1]
        ])
    
    def set_theta(self, theta):
        self.theta = self.degrees_to_radians(theta)
    
    def get_theta(self):
        return self.radians_to_degrees(self.theta)