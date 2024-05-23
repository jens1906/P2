import math
import numpy.matlib 
import numpy as np
np.set_printoptions(suppress=True)

from robodk.robolink import *
from robodk.robomath import *
from time import sleep

RDK = Robolink()

robot = RDK.ItemUserPick("UR5", ITEM_TYPE_ROBOT)

robot.Connect("169.254.141.138", 30000)
print("Robot connected")
robot.setSpeed(5)
robot.setSpeedJoints(5)
robot.setAcceleration(5)
robot.setJoints(robot.Joints())
sleep(1)

def get_position_array(i):
    switcher = {
        1: Collect_2_fuses_pre,
        2: Collect_2_fuses,
        3: Collect_1_fuse_pre,
        4: Collect_1_fuse,
        5: Collect_1_fuse_rel_pos,
        6: Collect_PCB_0_fuse_pre,
        7: Collect_PCB_0_fuse_bot,
        8: Collect_PCB_1_fuse_pre,
        9: Collect_PCB_1_fuse_top_bot,
        10: Collect_PCB_2_fuse_pre,
        11: Collect_PCB_2_fuse_bot,
        12: Collect_Blue_top_pre,
        13: Collect_Blue_top,
        14: Collect_Red_top_pre,
        15: Collect_Red_top,
        16: Collect_Black_top_pre,
        17: Collect_Black_top,
        18: Collect_Blue_bottom_pre,
        19: Collect_Blue_bottom,
        20: Collect_Red_bottom_pre,
        21: Collect_Red_bottom,
        22: Collect_Black_bottom_pre,
        23: Collect_Black_bottom,
        24: Assembly_release,
        25: Assembly_release_air,
        26: Assembly_bottom_bottom,
        27: Assembly_bottom_air,
        28: Assembly_top_bottom,
        29: Assembly_top_air,
        30: Assembly_0_fuse_bottom,
        31: Assembly_0_fuse_air,
        32: Assembly_0_fuse_release,
        33: Assembly_0_fuse_mid_release,
        34: Assembly_0_fuse_release_air,
        35: Assembly_1_fuse_bottom,
        36: Assembly_1_fuse_air,
        37: Assembly_1_fuse_release,
        38: Assembly_1_fuse_mid_release,
        39: Assembly_1_fuse_release_air,
        40: Assembly_2_fuse_bottom,
        41: Assembly_2_fuse_air,
        42: Assembly_2_fuse_release,
        43: Assembly_2_fuse_release_air
    }
    return switcher.get(i, "Invalid choice")

titles = ["Collect_2_fuses_pre", "Collect_2_fuses", "Collect_1_fuse_pre", "Collect_1_fuse", "Collect_1_fuse_rel_pos", "Collect_PCB_0_fuse_pre", "Collect_PCB_0_fuse_bot", "Collect_PCB_1_fuse_pre", "Collect_PCB_1_fuse_top_bot", "Collect_PCB_2_fuse_pre", "Collect_PCB_2_fuse_bot", "Collect_Blue_top_pre", "Collect_Blue_top", "Collect_Red_top_pre", "Collect_Red_top", "Collect_Black_top_pre", "Collect_Black_top", "Collect_Blue_bottom_pre", "Collect_Blue_bottom", "Collect_Red_bottom_pre", "Collect_Red_bottom", "Collect_Black_bottom_pre", "Collect_Black_bottom", "Assembly_release", "Assembly_release_air", "Assembly_bottom_bottom", "Assembly_bottom_air", "Assembly_top_bottom", "Assembly_top_air", "Assembly_0_fuse_bottom", "Assembly_0_fuse_air", "Assembly_0_fuse_release", "Assembly_0_fuse_mid_release", "Assembly_0_fuse_release_air", "Assembly_1_fuse_bottom", "Assembly_1_fuse_air", "Assembly_1_fuse_release", "Assembly_1_fuse_mid_release", "Assembly_1_fuse_release_air", "Assembly_2_fuse_bottom", "Assembly_2_fuse_air", "Assembly_2_fuse_release", "Assembly_2_fuse_release_air"]

#All points array
start_pos = [[64.30, -97.95, 132.19, -124.52, -89.99, 19.41]]
collecet_pre_top = [69.59, -92.82, 129.03, -139.75, -63.02, 28.03]
pre_assembly_bot = [59.56, -84.73, 142.5, -156.56, -60.7, 16.64]
Collect_PCB_1_fuse_pre_via = [53.61, -75.43, 126.02, -125.62, 31.15, 145.14]
Assembly_release_lift = [38.14, -71.23, 132.06, -151.03, -89.94, -5.39]
Collect_2_fuses_pre = [60.02, -70.99, 114.39, -108.85, 33.33, 151.44]
Collect_2_fuses = [61.42, -68.12, 114.08, -109.5, 33.93, 149.14]
Collect_2_fuse_release = [61.42, -74.12, 110.79, -100.27, 33.92, 149.22]
Collect_1_fuse_pre = [61.39, -75.01, 119.85, -108.42, 33.91, 131.64]
Collect_1_fuse = [62.57, -71.15, 118.49, -109.36, 34.44, 129.76]
Collect_1_fuse_rel_pos = [61.6, -73.01, 118.57, -108.87, 34, 131.3]
Collect_PCB_0_fuse_pre = [68.51, -73.49, 111.65, -38.07, 113.73, 120.04]
Collect_PCB_0_fuse_bot = [69.88, -70.02, 112.35, -43.14, 115.41, 119.75]
Collect_PCB_0_fuse_release = [69.92, -72.66, 110.85, -38.95, 115.57, 119.75]
Collect_PCB_1_fuse_pre = [67.11, -73.71, 113.16, -39.37, 112.33, 120.04]
Collect_PCB_1_fuse_release = [68.35, -74.15, 111.41, -37.18, 113.56, 121.05]
Collect_PCB_1_fuse_top_bot = [68.35, -70.3, 113.68, -43.29, 113.59, 121.05]
Collect_PCB_2_fuse_pre = [65.67, -73.87, 114.62, -40.68, 110.88, 120.04]
Collect_PCB_2_fuse_bot = [67.24, -70.26, 114.85, -44.51, 112.48, 120.02]
Collect_PCB_2_fuse_release = [67.5, -75.01, 112.48, -37.38, 112.7, 120.03]
Collect_Blue_top_pre = [84.45, -87.93, 130.94, -153.08, -67.35, 43.75]
Collect_Blue_top = [85.62, -84.3, 130.92, -157.15, -67.76, 44.96]
Collect_Red_top_pre = [78.48, -82.65, 124.25, -149.23, -65.41, 37.57]
Collect_Red_top = [79.61, -79.48, 124.23, -152.89, -65.77, 38.78]
Collect_Black_top_pre = [73.73, -76.82, 116.13, -144.83, -64.06, 32.53]
Collect_Black_top = [74.78, -74.21, 116.21, -147.89, -64.14, 34.04]
Collect_Blue_bottom_pre = [63.45, -85.85, 152.42, -167.48, -61.38, 21.07]
Collect_Blue_bottom = [65.49, -79.56, 152.09, -174.54, -61.81, 23.35]
Collect_Red_bottom_pre = [59.56, -80.11, 143.56, -162.26, -60.71, 16.67]
Collect_Red_bottom = [61.28, -75.35, 143.27, -167.69, -61, 18.63]
Collect_Black_bottom_pre = [56.78, -74.35, 133.89, -156.79, -60.3, 13.49]
Collect_Black_bottom = [58.25, -70.59, 133.64, -161.14, -60.51, 15.18]
Assembly_release = [27.43, -71.73, 132.85, -151.19, -89.93, -16.11]
Assembly_release_air = [27.44,-79.5, 130.82, -141.4, -89.91, -16.15]
Assembly_bottom_bottom = [38.14, -71, 132.1, -151.28, -89.94, -5.39]
Assembly_bottom_air = [38.15, -74.6, 131.33, -146.76, -89.92, -5.4]
Assembly_top_bottom = [38.14, -71.01, 132.11, -151.34, -89.95, -5.39]
Assembly_top_air = [38.15, -74.6, 131.33, -146.76, -89.92, -5.4]
Assembly_0_fuse_bottom = [47.93, -75.75, 127.27, -48.59, 94.4, 90]
Assembly_0_fuse_air = [47.96, -78.73, 127.3, -48.62, 94.4, 90]
Assembly_0_fuse_release = [48.18, -71.4, 113.82, -13.17, 95.74, 91.14]
Assembly_0_fuse_mid_release = [48.6, -73.52, 120.1, -31.09, 96.97, 90]
Assembly_0_fuse_release_air = [48.18, -73.4, 112.68, -10.03, 95.72, 91.13]
Assembly_1_fuse_bottom = [45.75, -76.38, 129.74, -53.71, 92.65, 90]
Assembly_1_fuse_air = [45.75, -79.42, 128.66, -49.6, 92.64, 90]
Assembly_1_fuse_release = [45.45, -71.46, 112.88, -6.76, 91.92, 91.34]
Assembly_1_fuse_mid_release = [45.62, -74.79, 122.46, -32.98, 92.43, 90.65]
Assembly_1_fuse_release_air = [45.44, -76.21, 109.51, 1.35, 91.88, 91.32]
Assembly_2_fuse_bottom = [43.73, -76.83, 130.09, -53.3, 91.42, 90]
Assembly_2_fuse_air = [43.73, -79.94, 128.97, -49.08, 91.4, 90]
Assembly_2_fuse_mid_release = [43.61, -72.92, 118.03, -20.14, 91.18, 90.55]
Assembly_2_fuse_release = [43.53, -69.82, 110.27, -0.49, 90.94, 90.78]
Assembly_2_fuse_release_air = [43.52, -72.75, 108.34, 4.36, 90.90, 90.77]


def Change_theta_to_Motoman():
    for i in range(1,len(titles)+1):
        print(get_position_array(i))
        #globals()[titles[i - 1]] = [0,0,0,0,0,0]
        globals()[titles[i - 1]] = Pose_2_Motoman(robot.SolveFK(get_position_array(i)))        
        print(f"{titles[i - 1]}:{get_position_array(i)}")        

"""
Phone assembly
"""
def get_bottom(color):
    bot_collect = {
        # works
        "blue": [Collect_Blue_bottom_pre, Collect_Blue_bottom, Collect_Blue_bottom_pre],
        "red": [Collect_Red_bottom_pre, Collect_Red_bottom, Collect_Red_bottom_pre],
        "black": [Collect_Black_bottom_pre, Collect_Black_bottom, Collect_Black_bottom_pre]
    }
    return bot_collect.get(color, "Invalid choice")

def get_fuse(fuse):
    fuse_collect = {
        # There are some missing via points
        # 0 works
        0: [Collect_PCB_0_fuse_pre, Collect_PCB_0_fuse_bot, Collect_PCB_0_fuse_release, Assembly_0_fuse_air,Assembly_0_fuse_bottom,Assembly_0_fuse_mid_release,Assembly_0_fuse_release,Assembly_0_fuse_release_air],
        1: [Collect_1_fuse_pre, Collect_1_fuse,Collect_1_fuse_rel_pos, Collect_PCB_1_fuse_pre_via, Collect_PCB_1_fuse_pre,Collect_PCB_1_fuse_top_bot, Collect_PCB_1_fuse_pre,Assembly_1_fuse_air,Assembly_1_fuse_bottom,Assembly_1_fuse_mid_release, Assembly_1_fuse_release, Assembly_1_fuse_release_air],
        2: [Collect_2_fuses_pre, Collect_2_fuses, Collect_2_fuse_release, Collect_PCB_2_fuse_pre, Collect_PCB_2_fuse_bot, Collect_PCB_2_fuse_release, Assembly_2_fuse_air, Assembly_2_fuse_bottom, Assembly_2_fuse_mid_release, Assembly_2_fuse_release, Assembly_2_fuse_release_air]
    }
    #Collect_PCB_2_fuse_pre
    return fuse_collect.get(fuse, "Invalid choice")

def get_top(color):
    top_collect = {
        # There are some missing via points
        "blue": [collecet_pre_top, Collect_Blue_top_pre, Collect_Blue_top, Collect_Blue_top_pre],
        "red": [collecet_pre_top, Collect_Red_top_pre, Collect_Red_top, Collect_Red_top_pre],
        "black": [collecet_pre_top, Collect_Black_top_pre, Collect_Black_top, Collect_Black_top_pre]
    }
    return top_collect.get(color, "Invalid choice")

def extract_theta_values(nested_list):    
    theta_values = []
    def recursive_search(lst):
        for item in lst:
            if isinstance(item, list):
                if len(item) == 6 and all(isinstance(i, (int, float)) for i in item):
                    theta_values.append(item)
                else:
                    recursive_search(item)
    recursive_search(nested_list)
    return theta_values

def assemble_phone(top_color,bottom_color, fuse):
    bot = get_bottom(bottom_color)
    fuse = get_fuse(fuse)
    top = get_top(top_color)

    #bot- and top assembly is always use in any phone assembly
    bot_assembly = [pre_assembly_bot, Assembly_bottom_air,Assembly_bottom_bottom,Assembly_release,Assembly_release_air]
    top_assembly = [collecet_pre_top, Assembly_top_air,Assembly_top_bottom,Assembly_release_lift,Assembly_release,Assembly_release_air, start_pos]
    
    if top == "Invalid choice" or bot == "Invalid choice" or fuse == "Invalid choice":
        return "Invalid choice"
    else:
        phone_assembly = [start_pos,bot, bot_assembly, fuse, top, top_assembly]
        
        commands = extract_theta_values(phone_assembly)

        for command in commands:
            print("Commands sent")
            while True:
                robot.MoveJ(command)
                pos = np.round(robot.Joints().tolist(), 2)
                sleep(0.1)
                if np.allclose(command, pos, atol=0.3):
                    #print("Position reached")
                    break
                else:
                    continue

        
        return command
    

#create a for loop to send the commands to the UR robot
#GUI to select the phone assembly
