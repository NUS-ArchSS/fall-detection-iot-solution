import math
from awsiot.mqtt_publish import publishData

class FallDetector:
    def __init__(self, threshold):
        self.threshold = threshold
    
    def detect_fall(self, data):
        # Check for accel in the data
        if data["name"] == "Accel":
            # Check if there are at least 3 values
            accel_data = data["data_values"]
            if len(accel_data) >= 3:
                x_str, y_str, z_str = accel_data[0], accel_data[1], accel_data[2]
                x, y, z = float(x_str), float(y_str), float(z_str)
                magnitude = math.sqrt(x**2 + y**2 + z**2)
                is_fall =  magnitude > self.threshold
                if is_fall:
                    print("Fall detected:", is_fall)
                    data_time=data["data_time"]
                    publishData(data_time)
