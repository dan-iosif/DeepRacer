def reward_function(params):
    '''
    Reward function iteration 1 (JP):
        changes: 
            1. combine all 3 examples (stay on center, keep all wheels on the track and mitigate zig-zag behaviors)
            2. add another modifier that discourages stopping and excessive speed 
        results: 
            success rate = 100% from 3 runs
            record = 1min10sec
    Reward function iteration 2 (JP)
        changes: 
            1. modify stay on center so that it allows the racer to venture a bit closer to the edge
            2. added more steering thresholds
            3. added example for waypoints
            4. added more speed tresholds
    '''

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    # Calculate 4 markers that are at varying distances away from the center line (e
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    marker_4 = 0.75 * track_width
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.6
    elif distance_from_center <= marker_3:
        reward = 0.3
    elif distance_from_center <= marker_4:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
		
#Taken from "Example of rewarding the agent to stay inside the two borders of the track" - adapted
    all_wheels_on_track = params['all_wheels_on_track']
    # Give a bonus if all the wheels are on the track and the agent is somewhere in between the track borders
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward *= 1.5
		
#Taken from "Example of penalize steering, which helps mitigate zig-zag behaviors" - adapted and modified
    steering = abs(params['steering_angle']) # Only need the absolute steering angle

    # Steering penality threshold, change the number based on your action space setting
    steering_threshold_1 = 30
    steering_threshold_2 = 20
    steering_threshold_3 = 10
    steering_threshold_4 = 5
    steering_threshold_5 = 1

    # Penalize reward if the agent is steering too much and reward if it goes straight
    if steering > steering_threshold_1:
        reward *= 0.7
    elif steering > steering_threshold_2:
        reward *= 0.8
    elif steering > steering_threshold_3:
        reward *= 0.9
    elif steering > steering_threshold_4:
        reward *= 1
    elif steering > steering_threshold_5:
        reward *= 1.1

#Taken from "Example of using waypoints and heading to make the car in the right direction" - adapted and modified

    import math

    # Read input variables
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5
        
# Stuff from JP :)
    speed = params['speed']
    speed_threshold_1 = 0.1
    speed_threshold_2 = 0.5
    speed_threshold_3 = 1
    speed_threshold_4 = 2
    speed_threshold_5 = 3
    speed_threshold_6 = 4
	# penalize if the vehicle stops or goes backwards (if possible)?
    if speed < speed_threshold_1:
        reward *= 0.3
    elif speed < speed_threshold_2:
        reward *= 0.8
    elif speed < speed_threshold_3:
        reward *= 0.9
    elif speed > speed_threshold_4:
        reward *= 1
    elif speed > speed_threshold_5:
        reward *= 0.8
    elif speed > speed_threshold_6:
        reward *= 0.5
    else:
        #speed is >= treshold_3 but <= than threshold 4
        reward *= 1.1
			
    return float(reward)