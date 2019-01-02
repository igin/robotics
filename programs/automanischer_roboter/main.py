#!/usr/bin/env python3
import os
import sys
sys.path.append('/home/robot')

from programs.automanischer_roboter.automanischer_roboter.robot import Robot

os.chdir('/home/robot')

automanischer_roboter = Robot()
automanischer_roboter.start()
