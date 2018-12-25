# EV3 Lego Robotic Experiments

# Setup

Steps to run code on the EV3:

* Install EV3dev on your EV3 (see https://www.ev3dev.org/)
* Make a tethering bluetooth connection to your EV3 (see https://www.ev3dev.org/docs/tutorials/connecting-to-the-internet-via-bluetooth/)

# Running programs

This repository enables easy running of programs on the ev3 using the run_program script. 

```bash
./run_program.sh random_drive
```

This will copy all your python files to the ev3 and execute the `random_drive/main.py`.
