from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

print("Connecting to vehicle for Square Mission...")
vehicle = connect('127.0.0.1:14551', wait_ready=True)

def arm_and_takeoff(target_altitude):
    print("Pre-arm checks...")
    while not vehicle.is_armable:
        time.sleep(1)
    
    print("Changing to GUIDED mode...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print(f"Taking off to {target_altitude}m...")
    vehicle.simple_takeoff(target_altitude)

    while True:
        current_alt = vehicle.location.global_relative_frame.alt
        print(f" Altitude: {current_alt:.2f}m")
        if current_alt >= target_altitude * 0.95:
            print("Target altitude reached!")
            break
        time.sleep(1)

def send_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Moves the drone by sending ground velocity components (m/s).
    velocity_x = North/South (+ is North, - is South)
    velocity_y = East/West (+ is East, - is West)
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # bitmask (only enable velocities)
        0, 0, 0, # x, y, z positions
        velocity_x, velocity_y, velocity_z, # x, y, z velocities
        0, 0, 0, # x, y, z acceleration
        0, 0)    # yaw, yaw_rate
    
    # Send command to vehicle repeatedly over the specified duration
    for x in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

# ---- START THE SQUARE MISSION ----

# 1. Takeoff to 10 meters
arm_and_takeoff(10)
print("Hovering for 3 seconds...")
time.sleep(3)

# 2. Fly the Square Path (Moving at 5 meters per second for 4 seconds = 20-meter sides)
print("👉 Side 1: Flying NORTH")
send_velocity(5, 0, 0, 4)

print("👉 Side 2: Flying EAST")
send_velocity(0, 5, 0, 4)

print("👉 Side 3: Flying SOUTH")
send_velocity(-5, 0, 0, 4)

print("👉 Side 4: Flying WEST (Returning back near home)")
send_velocity(0, -5, 0, 4)

# 3. Return to Launch and Land automatically
print("🛬 Mission completed! Changing mode to RTL (Return to Launch)...")
vehicle.mode = VehicleMode("RTL")

# Close connection cleanly
time.sleep(2)
vehicle.close()
print("Square flight script finished.")
