import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '192.168.100.13' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 270 # enter the value in degrees for the identification tower 
tall_tower_angle = 0 # enter the value in degrees for the classification tower
drop_tube_angle = 180#270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = -21.5 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.1 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin2_offset = 0.2
bin2_color = [0,1,0]
bin3_offset = 0.3
bin3_color = [0,0,1]
bin4_offset = 0.4
bin4_color = [0.63,0.23,0.78]

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

def dispense_container():
    n=input("Please enter a number between 1 and 6: ")
    while n<'1' or n>'6':
        print("You have entered an invalid number,please re-enter the number.")
        n=input("Please enter a number between 1 and 6")
    container_list=table.dispense_container(int(n),True)
    return container_list
 
def load_container(n):
    x,y,z=[0.644, 0.0, 0.273]
    arm.move_arm(x,y,z)
    time.sleep(2)
    arm.control_gripper(45)
    time.sleep(2)
    if n==0:
        x_4,y_4,z_4= [0,-0.597,0.571]
        arm.move_arm(x_4,y_4,z_4)
        time.sleep(2)
        arm.control_gripper(-45)
        time.sleep(2)
        arm.rotate_shoulder(-45)
        time.sleep(2)
        arm.home()
    elif n==1:
        x_3,y_3,z_3=(0.0, -0.522, 0.532)
        arm.move_arm(x_3,y_3,z_3)
        time.sleep(2)
        arm.control_gripper(-45)
        time.sleep(2)
        arm.rotate_shoulder(-45)
        time.sleep(2)
        arm.home()
    elif n==2:
        x_2,y_2,z_2=(0.0, -0.429, 0.524)
        arm.move_arm(x_2,y_2,z_2)
        time.sleep(2)
        arm.control_gripper(-45)
        time.sleep(2)
        arm.rotate_shoulder(-45)
        time.sleep(2)
        arm.home()


total_mass=0
container_count=0
conditions=True


while conditions==True:
    container_list=dispense_container()
    container_material=container_list[0]
    container_mass=container_list[1]
    print(container_mass)
    
    container_bin_location=container_list[2]
    print(container_bin_location)
    if container_count==0:
        total_mass=total_mass+container_mass
        load_container(container_count)
        container_count=container_count+1
    else:
        if container_count>0 and container_count<3:
            if container_bin_location==previous_bin_location:
                if (total_mass+container_mass)<90:
                    total_mass=total_mass+container_mass
                    print(total_mass)
                    print(container_count)
                    load_container(container_count)
                    container_count=container_count+1
                else:
                    conditions=False
            else:
                conditions=False
        else:
            conditions=False
    previous_bin_location=container_bin_location
    print(container_count)
    print(previous_bin_location)
    print(total_mass)

    
def transfer_container(bin_color):
    bot.activate_color_sensor()
    while True:
        wheels = bot.line_following_sensors()
        color = bot.read_color_sensor()
        print(color)
        if color[0] == bin_color:
            bot.forward_time(4)
            bot.stop()
            bot.deactivate_color_sensor()
            return

        if wheels[0] == 1 and wheels[1] == 1:
            bot.set_wheel_speed([0.1,0.1])

        elif wheels[0] == 1 and wheels[1] == 0:
            bot.set_wheel_speed([0,0.03])

        elif wheels[0] == 0 and wheels[1] == 1:
            bot.set_wheel_speed([0.03,0])

        else:
            bot.set_wheel_speed([0.5,0.2])

def deposit_container():
    bot.activate_linear_actuator()
    bot.dump()
    bot.deactivate_linear_actuator()
    
def main():
    if previous_bin_location == 'Bin01':
        transfer_container(bin01_color)

    if previous_bin_location == 'Bin02':
        transfer_container(bin02_color)

    if previous_bin_location == 'Bin02':
        transfer_container(bin03_color)

    if previous_bin_location == 'Bin04':
        transfer_container(bin04_color)
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
