def map_range(input_list, new_min, new_max):
    # Find the minimum and maximum value in the input list
    old_min = min(input_list)
    old_max = max(input_list)
    
    # Map the values from the input list to a new range
    mapped_values = (input_list - old_min) / (old_max - old_min) * (new_max - new_min) + new_min 
    
    return mapped_values

def map_data(input_list, newMin, newMax, reverse=False):
    # Find the minimum and maximum value in the input list
    oldMin = min(input_list)
    oldMax = max(input_list)

    if reverse:
        newMin, newMax = newMax, newMin
    return [round((x - oldMin) / (oldMax - oldMin) * (newMax - newMin) + newMin) for x in input_list]
