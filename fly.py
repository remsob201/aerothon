from pymavlink import mavutil
import time

# Подключение к MAVLink
def connect_to_drone():
    connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')  # Подключаемся к PX4 через UDP
    connection.wait_heartbeat()  
    print("Connected to the drone!")
    return connection

def arm_and_takeoff(connection, altitude=10):
    print("Arming drone...")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,  # confirmation
        1,  # param1: 1 = ARM, 0 = DISARM
        0, 0, 0, 0, 0, 0  # параметры 2-7
    )
    connection.motors_armed_wait()  # Ждем, пока дрон будет заармирован

    print(f"Taking off to altitude {altitude} meters...")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,  # confirmatio
        0, 0, 0, 0, 0, 0, altitude  # параметры 2-7: последние два - высота
    )
    connection.mav.flightmode_custom = 'OFFBOARD'
    time.sleep(10)


def set_mode(connection, mode):
    if mode == 'OFFBOARD':
        print("Switching to OFFBOARD mode...")
        connection.mav.command_long_send(
            connection.target_system,
            connection.target_component,
            mavutil.mavlink.MAV_CMD_DO_SET_MODE,
            0,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
            6,  # Режим 6 = OFFBOARD
            0, 0, 0, 0, 0
        )
        connection.set_mode('OFFBOARD')

# Лететь вперед по прямой
def fly_straight(connection, velocity_x=5, duration=10):
    print(f"Flying straight with velocity {velocity_x} m/s for {duration} seconds...")

    set_mode(connection, 'OFFBOARD')

    for _ in range(duration * 10):  #
        connection.mav.set_position_target_local_ned_send(
            0,
            connection.target_system,
            connection.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b0000111111000111,  # Bitmask: используем только скорость
            0, 0, 0,
            velocity_x, 0, 0,  # vx, vy, vz (скорости)
            0, 0, 0,
            0, 0
        )
        time.sleep(0.1)  

def main():
    connection = connect_to_drone()


    arm_and_takeoff(connection, altitude=10)

    fly_straight(connection, velocity_x=5, duration=10)

if __name__ == "__main__":
    main()