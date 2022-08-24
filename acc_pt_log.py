# File : acc_pt_log.py
#
# Log acceleration, pressure and temperarure 
# Takes 10 X,Y,Z acceleration samples per second during 10 sec (6 bytes for a X,Y,Z sample) 
# Then one pressure and one temperature sample (4 bytes).
# Repeat the process during a specified time
#
# Append the result to binary files : 10 s = 600 bytes for acceleration
# and 4 bytes for pressure and temperature.
#
# Chip ICM20948 : https://www.waveshare.com/w/upload/5/57/ICM-20948-v1.3.pdf
# Chip LPS22HB : https://www.waveshare.com/w/upload/2/20/Lps22hb.pdf
# Pico 10-DOF IMU module : https://www.waveshare.com/wiki/Pico-10DOF-IMU
#
# info@pcamus.be
# 22/8/2022

from icm20948_mod import *
from lps22hb_mod import *
from machine import Pin
import utime
import uos

LOG_TIME = 1800 # Logging time in seconds

# Calibration values to add to temperature and pressure (for my LPS22HB sensor).
temp_cal = -2.3
pres_cal = 40

# Creates sensors instances
icm20948=ICM20948()
lps22hb=LPS22HB()

# Heart beat and status LED
hb = Pin(25, machine.Pin.OUT)

file_buf_acc= bytearray(600) # 100 x 2 bytes x 3 axis
file_buf_PT= bytearray(4) # pressure = 2 bytes, temperature 2 bytes

filn_acc="acc.bin"
filn_PT="Press_Temp.bin"

# In this version I don't remove the file automatically at reset.
# The files must be removed manually when we start an new log.
# Otherwise the new log is appended to the previous one.

# 6 x 0x00 is written in the acc.bin indicating the begining of a new record.
f = open(filn_acc, "ab")
f.write(bytearray(6)) # bytearray with 6 elements initialized to 0
f.close()

# and 4 x 0x00 is written in the Press_Temp.bin.
f = open(filn_PT, "ab")
f.write(bytearray(4)) # bytearray with 4 elements initialized to 0
f.close()

# # Removes old copy of files if they exist
# try:
#     uos.remove(filn_acc) 
# except:
#     pass
# 
# try:
#     uos.remove(filn_PT) 
# except:
#     pass

# Two blinks means initialization success
hb.on() 
utime.sleep_ms(100)
hb.off()
utime.sleep_ms(100)
hb.on() 
utime.sleep_ms(100)
hb.off()

log_start=utime.time() # Start time of logging
pressure, temperature = lps22hb.LPS22HB_READ_P_T() # reads once before to remove false values

while(True):
       
    for i in range(100): # Takes 100 acceleration samples
        
        start=utime.ticks_ms()
       
        Accel=icm20948.icm20948_Accel_Read().copy()
        
        # Stores in a bytearray buffer after converting in the bytearray element format
        buf_index=i*6
        file_buf_acc[buf_index]=Accel[0] // 256   # Acc X MSB
        file_buf_acc[buf_index+1]=Accel[0] % 256  # Acc X LSB
        file_buf_acc[buf_index+2]=Accel[1] // 256 # Acc Y MSB 
        file_buf_acc[buf_index+3]=Accel[1] % 256  # Acc Y LSB
        file_buf_acc[buf_index+4]=Accel[2] // 256 # Acc Z MSB
        file_buf_acc[buf_index+5]=Accel[2] % 256  # Acc Z LSB
        
        while utime.ticks_diff(utime.ticks_ms(), start)<100:  # Takes a sample each 100 ms
            pass     
        
        hb.toggle() # toggle a led to have a heart beat

    pressure, temperature = lps22hb.LPS22HB_READ_P_T() # and takes one pressure and temperature
                                                       # measurement each 10 sec
 
    # Writes acceleration samples to a binary file
    f = open(filn_acc, "ab")
    f.write(file_buf_acc)
    f.close()
    
    # Convert pressure and temperature data to bytearray
    int_pressure=int(pressure + pres_cal)
    int_temperature=int((temperature + temp_cal)*10) # scales temperature to keep tenth of degree
                 
    file_buf_PT[0]=int_pressure // 256
    file_buf_PT[1]=int_pressure % 256
    file_buf_PT[2]=int_temperature // 256                 
    file_buf_PT[3]=int_temperature % 256
    
    # Writes to a binary file
    f = open(filn_PT, "ab")
    f.write(file_buf_PT)
    f.close()
       
    # Check for end of logging.
    if (utime.time()-log_start) > LOG_TIME :
        hb.off()
        sys.exit()
    
