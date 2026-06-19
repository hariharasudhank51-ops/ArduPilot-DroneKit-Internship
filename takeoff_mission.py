from dronekit import connect, VehicleMode
import time

print("Connecting to vehicle...")
# Using port 14551 which we verified works perfectly on your setup
vehicle = connect('127.0.0.1:14551', wait_ready=True)

def arm_and_takeoff(target_altitude):
    print("Basic pre-arm checks...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Changing mode to GUIDED...")
    vehicle.mode = VehicleMode("GUIDED")
    
    print("Arming motors...")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print(f"Taking off! Target Altitude: {target_altitude}m")
    vehicle.simple_takeoff(target_altitude)

    while True:
        current_alt = vehicle.location.global_relative_frame.alt
        print(f" Altitude: {current_alt:.2f}m")
        
        # Check if the drone has reached 95% of target altitude
        if current_alt >= target_altitude * 0.95:
            print("Reached target altitude successfully!")
            break
        time.sleep(1)

# Takeoff to 18 meters as required by the task
arm_and_takeoff(18)

# Hold position for 5 seconds
print("Hovering...")
time.sleep(5)

# Land the drone safely
print("Setting mode to LAND...")
vehicle.mode = VehicleMode("LAND")

time.sleep(2)
vehicle.close()
print("Mission complete.")
