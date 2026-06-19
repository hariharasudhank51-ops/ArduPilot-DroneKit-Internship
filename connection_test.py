from dronekit import connect

# Connect to the Vehicle using the correct TCP port from your SITL log
print("Connecting to vehicle...")
vehicle = connect('127.0.0.1:14551', wait_ready=True)

# Print basic information requested by Task 1
print("\n--- Drone is connected! ---")
print("GPS:", vehicle.gps_0)
print("Battery:", vehicle.battery)
print("Last Heartbeat:", vehicle.last_heartbeat)

# Close vehicle object cleanly
vehicle.close()
print("Connection closed.")
