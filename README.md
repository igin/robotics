# EV3 Lego Robotic Experiments

# Setup

Steps to run code on the EV3:

* Install EV3dev on your EV3 (see https://www.ev3dev.org/)
* Make a tethering bluetooth connection to your EV3 (see https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/)
* Copy your files to the robot using `scp ./myfile.py robot@ev3dev.local:`
* Connect to the EV3 using ssh: (default password `maker`)
    * `ssh robot@ev3dev.local`
    * Execute the program: `python3 myfile.py`
    * press `Ctrl+c` to stop the program