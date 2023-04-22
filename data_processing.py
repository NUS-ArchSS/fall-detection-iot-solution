import queue

def process_data(data_bytearray, accl_queue: queue, mag_queue: queue):
    # Convert the bytearray to a string
    # bytearray(b'1681367616818.033203125,Accel,-0.20727539062,-0.73022460937,-0.71899414062,\n1681367616821.6953125,Mag,300,622,257,\n')
    line = data_bytearray.decode('utf-8')

    """ data:
    Accelerometer: x,y,z
    1681353316941.78198242187,Accel,0.02404785156,-0.06604003906,-1.12475585937,
    HRMraw: heart rate raw data, filt, vcPPG, vcPPGoffs 
    1681353316963.296875,HRMraw,5566,-32768,1751,1032,
    Magnetometer: x,y,z
    1681353317265.97021484375,Mag,296,661,257,
    HRM: bpm, confidence
    1681354187341.98950195312,HRM,58,0,
    """
    # Split the string into lines
    data_lines = line.strip().split('\n')

    # Process each line and store the resulting dictionaries in a list
    data_list = []
    for line in data_lines:
        # Remove the trailing comma
        line = line.rstrip(',')

        # Check if any data exist
        if any(keyword in line for keyword in ["Accel", "Mag"]):
            line_parts = line.split(",")
            # if data value not null
            if len(line_parts) > 1:
                data_time = line_parts[0]
                name = line_parts[1]
                data_values = line_parts[2:]
                # Store data in a dictionary
                data_dict = {
                    "data_time": data_time,
                    "name": name,
                    "data_values": data_values
                }
                if name == 'Accel':
                    accl_queue.put(data_dict)
                else:
                    mag_queue.put(data_dict)
                # data_list.append(data_dict)

    return data_list;
