import math
import numpy as np
np.set_printoptions(suppress=True)

from Kine_conts import *
from Kine_forward_inverse import *

from robodk.robolink import *
from robodk.robomath import *
from time import sleep

RDK = Robolink()

robot = RDK.ItemUserPick("UR5", ITEM_TYPE_ROBOT)

robot.Connect("169.254.141.138", 30000)
print("Robot connected")
robot.setSpeed(500)
robot.setAcceleration(500)
robot.setSpeedJoints(500)
robot.setJoints(robot.Joints())
sleep(1)

RDK = Robolink()

RDK.setSimulationSpeed(1)

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

def assemble_phone(bottom_color, fuse, top_color):
        fuse = int(fuse)
        window.withdraw()
        bot = get_bottom(bottom_color)
        fuse = get_fuse(fuse)
        top = get_top(top_color)
        print(bottom_color, fuse, top_color)


        #bot- and top assembly is always use in any phone assembly
        bot_assembly = [pre_assembly_bot, Assembly_bottom_air,Assembly_bottom_bottom,Assembly_release,Assembly_release_air]
        top_assembly = [collecet_pre_top, Assembly_top_air,Assembly_top_bottom,Assembly_release_lift,Assembly_release,Assembly_release_air, start_pos]
        
        if top == "Invalid choice" or bot == "Invalid choice" or fuse == "Invalid choice":
            return "Invalid choice"
        else:

            phone_assembly = [start_pos,bot, bot_assembly, fuse, top, top_assembly]
            
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

            phone_assembly = extract_theta_values(phone_assembly)
            
            for command in phone_assembly:
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
            window.deiconify()
            return command


import tkinter as tk
from tkinter import ttk

from main import *

###   Setup  ###

# Creates a window for GUI
window = tk.Tk()

# Set the window title
window.title("UR5 Robot Control Panel")

# Make the window non-resizable
window.resizable(False, False)

# Set the window size
window_width = 400
window_height = 500
window.geometry(f"{window_width}x{window_height}")

center_x = window_width/2

# Change the background color to blue
window.configure(bg="#B9C8D1")

##   Number of products   ##
# Initial value
num = tk.IntVar()
num.set(1)

# Displays the number of products selected
fuse_display = [1,2]
value_label = tk.Label(window, textvariable=num, height=fuse_display[0], width=fuse_display[1], font=("Supreme", 14))
value_label.place(x=center_x, y=65, anchor="center")

# Increase value button
fuse_increase = [1,7]
increase_button = tk.Button(window, text="Increase", command=lambda: num.set(num.get() + 1) if num.get() < 99 else None, height=fuse_increase[0], width=fuse_increase[1], font=("Supreme", 12))
increase_button.place(x = center_x + center_x/2.75, y=65, anchor="center")

# Decrease value button
fuse_decrease = [1,7]
decrease_button = tk.Button(window, text="Decrease", command=lambda: num.set(num.get() - 1) if num.get() > 1 else None, height=fuse_decrease[0], width=fuse_decrease[1], font=("Supreme", 12))
decrease_button.place(x = center_x - center_x/2.75, y=65, anchor="center")

# Create a title for selection of number of products
product_num_title = tk.Label(window, text="Products Orded:", font=("Supreme", 12),bg="#B9C8D1")
product_num_title.place(x=center_x, y= 30, anchor="center")


###   Fuse selection   ###
# Create a title for selection of number of products
fuse_num_title = tk.Label(window, text="Amount of fuses:", font=("Supreme", 12), justify="center")
fuse_num_title.place(x=center_x, y= 130, anchor="center")

# Create option to select the number of fuses in the product ##
fuse_num = ttk.Combobox(window, values=[0, 1, 2], state="readonly", width=15, font=("Supreme", 12), justify="center")
fuse_num.place(x=center_x, y=160, anchor="center")


## Type of top cover ##
# Create a title for the top_cover dropdown menu
top_cover_title = tk.Label(window, text="Top Cover Color:", font=("Supreme", 12), justify="center")
top_cover_title.place(x=center_x, y=230, anchor="center")

## Create a dropdown menu for selecting the top cover color ##
top_cover = ttk.Combobox(window, values=["blue", "red", "black"],state="readonly", font=("Supreme", 12), justify="center")
top_cover.place(x=center_x, y=260, anchor="center")


##   Type of bottom cover   ##
# Create a title for the dropdown menu
bottom_cover_title = tk.Label(window, text="Bottom Cover Color:", font=("Supreme", 12), justify="center")
bottom_cover_title.place(x=center_x, y=330, anchor="center")

## Create a dropdown menu for selecting the bottom cover color ##
bottom_cover = ttk.Combobox(window, values=["blue", "red", "black"],state="readonly", font=("Supreme", 12), justify="center")
bottom_cover.place(x=center_x, y=360, anchor="center")


## Creates the confirm button ##

products_in_queue = 0
queue_num = 0

def on_confirm():
    global products_in_queue
    global queue_num
    global queue
    if queue_num >= 10:
        print("Queue is full")
        return
    queue = [num.get(), bottom_cover.get(), int(fuse_num.get()), top_cover.get()]
    queue_num += 1
    print(queue)

    assemble_phone(queue[1],queue[2],queue[3])
    
    

confirm_button = tk.Button(window, text="Add to queue", command=on_confirm, font=("Supreme", 12), justify="center")
confirm_button.place(x=center_x, y=400, anchor="center")


##   Clear queue button   ##
def clear_queue():
    global products_in_queue
    global queue_num
    global queue
    queue = []
    products_in_queue = 0
    queue_num = 0
    products_in_queue_text.set(f"Total products in production: {products_in_queue}")

# Create a button to clear the queue
confirm_button = tk.Button(window, text="Clear queue", command=clear_queue, font=("Supreme", 10), justify="center")
confirm_button.place(x=center_x, y=480, anchor="center")


###   Fuse selection   ###
# Create a title for selection of number of products
product_in_progress = tk.Label(window, text="Amount of fuses:", font=("Supreme", 12), justify="center")
fuse_num_title.place(x=center_x, y= 130, anchor="center")


## Creates a label to display the total number of products in queue ##
# Create a StringVar to hold the text
products_in_queue_text = tk.StringVar()

# Create a label with the textvariable option set to products_in_queue_text
products_in_queue_label = tk.Label(window, textvariable=products_in_queue_text, font=("Supreme", 12), justify="center")
products_in_queue_label.place(x=center_x, y=450, anchor="center")

# Set the initial text
products_in_queue_text.set(f"Total products in production: {products_in_queue}")


def open_new_window():
    new_window = tk.Toplevel(window)
    new_window.title("Orders")
    new_window.resizable(False, False)

    # Display the data from queue[i,0]
    for i in range(len(queue)):
        order_label = tk.Label(new_window, text=f"Order {i+1}:", font=("Supreme", 12))  # Use a larger font size
        order_label.pack()
        data_label = tk.Label(new_window, text=f"Number of products: {queue[i][0]}\nNumber of fuses: {queue[i][1]}\nTop cover color: {queue[i][2]}\nBottom cover color: {queue[i][3]}\n", font=("Supreme", 10))  # Use a smaller font size
        data_label.pack()

        #data_label = tk.Label(new_window, text=f"Order {i+1}: \nNumber of products: {queue[i][0]} \nNumber of fuses: {queue[i][1]} \nTop cover color: {queue[i][2]} \nBottom cover color: {queue[i][3]}")
        #data_label.pack()
        y = (i+1) * 110
        new_window.geometry(f"200x{y}")


##   Order List   ##
dim_order_list = [1,6]
order_list = tk.Button(window, text="Orders", command=open_new_window, height=dim_order_list[0], width=dim_order_list[1], font=("Supreme", 12))
order_list.place(x = 360, y=20, anchor="center")

# Start the main event loop
window.mainloop()




    #assemble_phone("blue", "blue",0)