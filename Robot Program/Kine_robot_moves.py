"""import numpy as np
np.set_printoptions(suppress=True)

from Kine_forward_inverse import *

from robodk.robolink import *
from robodk.robomath import *

RDK = Robolink()

robot = RDK.Item("UR5")


def get_valid_Lmoves(joints):
    valid_moves = []
    cur_pos = robot.Joints()
    for i in joints:
        collison = robot.MoveL_Test(cur_pos, Mat(i.tolist()))
        if collison == 0:
            valid_moves.append(i.tolist())
            break
        else:
            continue
    if not valid_moves:
        print("No valid moves found")
    return valid_moves

def get_valid_Jmoves(joints, pos):
    print("Validating joint Jmoves")
    cur_pos = robot.Joints()
    for i in joints:
        collison = robot.MoveJ_Test(cur_pos, i.tolist())
        if collison == 0:
            print(i, "!Valid", "\n", "-"*50)
            robot.setJoints(cur_pos)
            return i.tolist()
        else:
            print(i, "Collision detected")
            continue
    robot.setJoints(cur_pos)
    return None
    print("!!!No valid moves found going to robodk IK solution!!!")
    Location_T06_deg = rotXYZ_rad(pos[0], pos[1], pos[2], np.degrees(pos[3]), np.degrees(pos[4]), np.degrees(pos[5]))
    valid_joints_list = Location_T06_deg.tolist()
    # Convert the list of lists to a pose object
    solve_pose = Mat(valid_joints_list)
    #solve_pose[0:3, 3] = [-pos[1], pos[0], pos[2]]
    print(solve_pose)
    valid_joints = robot.SolveIK_All(solve_pose)
    valid_joints = np.array([valid_joint[:-2] for valid_joint in valid_joints])

    return get_valid_Jmoves(valid_joints, pos)

def validate_joints(Joint_array, correct_pos):
    cur_pos = robot.Joints().tolist()
    print("Validating inverse kinematics solutions")
    valid_joints = []
    for i in Joint_array:
        robot.setJoints(i.tolist())
        print(i, np.round(robomath.Pose_2_TxyzRxyz(robot.Pose())[0:3]), np.round(np.degrees(robomath.Pose_2_TxyzRxyz(robot.Pose())[3:6])), np.round(correct_pos[0:3]), np.round(np.degrees(correct_pos[3:6])))
        if numpy.allclose(np.round(robomath.Pose_2_TxyzRxyz(robot.Pose())[0:3]),np.round(correct_pos[0:3]), atol=20):
            valid_joints.append(i)
    print("Valid joints:\n", np.array(valid_joints),"\n","-"*50)
    robot.setJoints(cur_pos)
    return np.array(valid_joints)

def move_to(pos):
    Location_T06 = rotXYZ_rad(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])
    joints = inverse_kinematics(Location_T06)
    print("Inverse kinematics solutions:\n", joints, "\n", "-"*50)
    Valid_move = get_valid_Jmoves(validate_joints(joints, pos), pos)
    print("Valid joint: ", Valid_move)
    return Valid_move

def get_valid_moves(start_joint, pos_array):
    RDK.setSimulationSpeed(40)
    valid_joints = []
    for pos in pos_array:
        print("="*50, "\nGetting valid joints from", robot.Pose().Pos(), "\nto: ", pos, "\n","-"*50)
        valid_joints.append(move_to(pos))
    robot.setJoints(start_joint)
    return valid_joints

def move_through_thetha_array(valid_pos_array, move_type):
    RDK.setSimulationSpeed(1)
    print(valid_pos_array)
    for i in valid_pos_array:
        if i is None:
            print("!!!No valid move for position:", valid_pos_array.index(i)+1,"Terminnating program!!!")
            exit()
        if move_type.upper() == "L":
            robot.MoveL(i)
        elif move_type.upper() == "J":
            robot.MoveJ(i)
        time.sleep(0)
    RDK.setSimulationSpeed(40)

    

"""