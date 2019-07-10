def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
    
    #Taken from "Example of rewarding the agent to stay inside the two borders of the track"
    all_wheels_on_track = params['all_wheels_on_track']
    # Give a bonus if all the wheels are on the track and the agent is somewhere in between the track borders
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward *= 1.5
		
    #Taken from "Example of penalize steering, which helps mitigate zig-zag behaviors"
    steering = abs(params['steering_angle']) # Only need the absolute steering angle

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15

    # Penalize reward if the agent is steering too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8
			
    # Stuff from JP :)
    speed = params['speed']
    low_speed = 0.1
    high_speed = 5
	# penalize if the vehicle stops or goes backwards (if possible)?
    if speed < low_speed:
        reward *= 0.3
    elif speed > high_speed:
        reward *= 0.8
			
    return float(reward)