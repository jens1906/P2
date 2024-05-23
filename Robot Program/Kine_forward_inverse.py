import math
import numpy as np
np.set_printoptions(suppress=True)

from Kine_conts import *
from DH_paramter import*
from robodk.robolink import *
from robodk.robomath import *

RDK = Robolink()
robot = RDK.Item("UR5")

"""
Forward kinematics
"""
# Transformation matrix for the forward kinematics
def forward_kinematics(a,b,m): # n is the corresponding to the theta number
    F_theta = Joint_theta[m]
    TBW = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],])
    
    for n in range (a,b):
        transformation = np.array([
            [np.cos(F_theta[n]), -np.sin(F_theta[n]), 0, DH_a_mm[n]],
            [np.sin(F_theta[n]) * np.cos(DH_alpha_rad[n]), np.cos(F_theta[n]) * np.cos(DH_alpha_rad[n]), -np.sin(DH_alpha_rad[n]), -np.sin(DH_alpha_rad[n]) * DH_d_mm[n]],
            [np.sin(F_theta[n]) * np.sin(DH_alpha_rad[n]), np.cos(F_theta[n]) * np.sin(DH_alpha_rad[n]), np.cos(DH_alpha_rad[n]), np.cos(DH_alpha_rad[n]) * DH_d_mm[n]],
            [0, 0, 0, 1]])
        TBW = TBW@transformation
    return TBW

"""
Transformation matrix with position and rotation
"""
def rotXYZ_rad(Input_values):
    X = Input_values[0] 
    Y = Input_values[1] 
    Z = Input_values[2] 
    rotX = Input_values[3] 
    rotY = Input_values[4] 
    rotZ = Input_values[5]    
    T = np.array([
        [np.cos(rotZ)*np.cos(rotY), np.cos(rotZ)*np.sin(rotY)*np.sin(rotX)-np.sin(rotZ)*np.cos(rotX), np.cos(rotZ)*np.sin(rotY)*np.cos(rotX)+np.sin(rotZ)*np.sin(rotX), X],
        [np.sin(rotZ)*np.cos(rotY), np.sin(rotZ)*np.sin(rotY)*np.sin(rotX)+np.cos(rotZ)*np.cos(rotX), np.sin(rotZ)*np.sin(rotY)*np.cos(rotX)-np.cos(rotZ)*np.sin(rotX), Y],
        [-np.sin(rotY), np.cos(rotY)*np.sin(rotX), np.cos(rotY)*np.cos(rotX), Z],
        [0, 0, 0, 1]])
    return T

"""
Inverse kinematics
"""
def inverse_kinematics(Location):
    Location = np.linalg.inv(TB0)@Location@np.linalg.inv(T6W)
    """
    Theta 1
    """
    P05 = np.array(Location@np.array([0, 0, -DH_d_mm[5], 1]))
    phi_1 = math.atan2(P05[1], P05[0])
    phi_2 = math.acos(DH_d_mm[3] / math.sqrt(P05[0]**2 + P05[1]**2))
    Joint_theta[0:4,0]=phi_1 + phi_2 + math.pi/2
    Joint_theta[4:8,0]=phi_1 - phi_2 + math.pi/2

    """
    Theta 5
    """
    for i in {0,4}:
        P06 = [Location[0, 3], Location[1, 3], Location[2, 3]]
        Theta_5_cos = (P06[0] * np.sin(Joint_theta[i,0]) - P06[1] * np.cos(Joint_theta[i,0]) - DH_d_mm[3]) / DH_d_mm[5]
        if 1 >= Theta_5_cos >= -1:
            Theta_5 = np.arccos(Theta_5_cos)
        else:
            Theta_5 = 0        
        Joint_theta[i:i+2, 4] = Theta_5
        Joint_theta[i+2:i+4, 4] = -Theta_5        

    """
    Theta 6
    """    
    for i in {0, 2, 4, 6}:
        T60 = np.linalg.inv(Location)
        X_inv = np.array([T60[0,0],
                          T60[1,0],
                          T60[2,0]])
        Y_inv = np.array([T60[0,1],
                          T60[1,1],
                          T60[2,1]])
        phi_1 = (math.cos(Joint_theta[i,0]) * Y_inv[1] - math.sin((Joint_theta[i,0])) * X_inv[1]) / math.sin(Joint_theta[i,4])
        phi_2 = (math.sin((Joint_theta[i,0])) * X_inv[0]-math.cos(Joint_theta[i,0]) * Y_inv[0]) / math.sin(Joint_theta[i,4])
        Temp_theta = math.atan2(phi_1, phi_2)
        Joint_theta[i:i+2, 5] = Temp_theta
    
    for i in range(8):    
        """
        #Pre calculations for Theta 3
        """
        T01 = forward_kinematics(0, 1, i)     
        T45 = forward_kinematics(4, 5, i)
        T56 = forward_kinematics(5, 6, i)
        T14 = np.linalg.inv(T01)@Location@np.linalg.inv(T56)@np.linalg.inv(T45)   
        P14 = np.array([T14[0][3], T14[1][3], T14[2][3]])
        P14Length = math.sqrt(P14[0]**2 + P14[2]**2)
        
        """
        Theta 3
        """
        Joint_theta[i, 2] = (-1)**i*math.acos((P14Length**2-DH_a_mm[2]**2 - DH_a_mm[3]**2) / (2 * DH_a_mm[2] * DH_a_mm[3]))

        """
        Theta 2
        """
        phi_1 = math.atan2(-P14[2], -P14[0])
        phi_2 = math.asin((-DH_a_mm[3]*math.sin(Joint_theta[i,2])) / (P14Length))
        Joint_theta[i, 1] = (phi_1 - phi_2)
        
        """
        Theta 4
        """        
        T32 = np.linalg.inv(forward_kinematics(2, 3, i))
        T21 = np.linalg.inv(forward_kinematics(1, 2, i))
        T34 = T32@T21@T14                      
        Joint_theta[i, 3] = math.atan2(T34[1, 0], T34[0, 0])

    # Convert to degrees
    deg = np.array(np.round(np.rad2deg(Joint_theta), decimals=2))           
    return deg


"""
This is only here to test specific points
"""


"""pos0 = [300, 300, 300, math.radians(0), math.radians(0), math.radians(0)]
pos1 = [300, 300, 300, math.radians(90), math.radians(0), math.radians(0)]
pos2 = [300, 300, 300, math.radians(0), math.radians(90), math.radians(0)]
pos3 = [300, 300, 300, math.radians(90), math.radians(90), math.radians(0)]
pos4 = [300, 300, 300, math.radians(0), math.radians(0), math.radians(90)]
pos5 = [300, 300, 300, math.radians(90), math.radians(0), math.radians(90)]
pos6 = [300, 300, 300, math.radians(0), math.radians(90), math.radians(90)]
pos7 = [300, 300, 300, math.radians(90), math.radians(90), math.radians(90)]
testset = [pos0, pos1, pos2, pos3, pos4, pos5, pos6, pos7]
print(testset[0][0])

for n in range(8):
    loc = rotXYZ_rad(testset[n][0],testset[n][1],testset[n][2],testset[n][3],testset[n][4],testset[n][5])
    values = inverse_kinematics(loc)
    print(values)
    for i in range(8):
        Robotheta = np.array(values[i])
        robot.setJoints(Mat(Robotheta))
        time.sleep(0.5)"""

