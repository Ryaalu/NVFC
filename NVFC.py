import os
import sys
import time

# Check if the script is run as root
if not os.geteuid() == 0:
    sys.exit("Script must be run as root")

try:
    import GPUtil
    from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetTemperature, nvmlDeviceSetFanSpeed
except ImportError:
    sys.exit("Please install the required modules using 'pip install gputil pynvml'")

# Initialize NVML for NVIDIA GPU management
nvmlInit()

# Get the first GPU device handle, assuming a single GPU system
device_handle = nvmlDeviceGetHandleByIndex(0)

def set_fan_speed(speed):
    """ Set the GPU fan speed to a value between 0 and 100 """
    if speed < 0 or speed > 100:
        raise ValueError("Speed must be between 0 and 100")
    nvmlDeviceSetFanSpeed(device_handle, int(speed))

def control_fan_based_on_temp():
    """ Control the fan speed based on the GPU temperature """
    while True:
        temp = nvmlDeviceGetTemperature(device_handle, 0)  # 0 for GPU temperature
        if temp > 80:
            set_fan_speed(100)  # Max speed
        elif temp > 70:
            set_fan_speed(80)
        elif temp > 60:
            set_fan_speed(60)
        elif temp > 50:
            set_fan_speed(40)
        else:
            set_fan_speed(20)  # Min speed
        time.sleep(10)  # Check every 10 seconds

if __name__ == "__main__":
    try:
        control_fan_based_on_temp()
    except KeyboardInterrupt:
        print("Fan control script terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
