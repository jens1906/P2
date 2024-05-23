import math
import numpy as np


"""
DH parameters
"""
DH_alpha_rad = [0, math.radians(90), 0, 0, math.radians(90), math.radians(-90)]
DH_a_mm = [0, 0, -425, -392, 0, 0]
DH_d_mm = [0, 0, 0, 109.3, 94.75, 82.5]
Joint_theta = np.zeros((8, 6))

base_rotation = math.radians(0)

TB0 = np.array([[np.cos(base_rotation), -np.sin(base_rotation), 0, 0],
                [np.sin(base_rotation), np.cos(base_rotation), 0, 0],
                [0, 0, 1, 89.2],
                [0, 0, 0, 1]])

T6W = np.array([[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])