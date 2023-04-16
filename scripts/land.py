from pymavlink import mavutil
connections = []
for i in range(12):
    connection = mavutil.mavlink_connection('udpin:localhost:{}'.format(14551 + 10*i))
    connections.append(connection)
for connection in connections:
    connection.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" %
            (connection.target_system, connection.target_component))
    mode = 'STABILIZE'
    mode_id = connection.mode_mapping()[mode]
    connection.mav.set_mode_send(connection.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,mode_id) 
