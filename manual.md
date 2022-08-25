## How to use the system.

To program and retreive files form the Raspberry Pi Pico I used the Thonny IDE.

I worked with two interpreters : 

- The default Thonny interpreter, running on my computer.
- The MicroPython interpreter running on the Pico board.

The interface is the following :

![](Thonny_ide.jpg)

- `1` is the current directory on my computer.
- `2` is the current directory on the Pico.
- `3` shows which interpreter is in use (to change click on this item).

*Interpreter choice :*

![](choose_int.jpg)

For informations about installing MicroPython interpreter see [here](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html).

### Program installation.

Connect the Pico to your computer with PICO-UPS-A board switch in OFF position.

In your working directory install `acc_pt_log.py`, `icm20948_mod.py`, `lps22hb_mod.py` and `bin_to_csv.py`

icm20948_mod.py, lps22hb_mod.py are in the embedded-sensors repository : [Pico_IMU_10DOF](https://github.com/pcamus/embedded-sensors/tree/main/Pico_IMU_10DOF)

Rename acc_pt_log.py as `main.py` (MicroPython starts automatically main.py at reset).

With the MicroPython interpreter selected, copy `main.py`, `icm20948_mod.py` and `lps22hb_mod.py` to the Pico (right click on the files then Upload to /)

Disconnect your computer. The logging will start when you switch ON the PICO-UPS-A for a duration equal to the value of the LOG_TIME variable (in main.py).
