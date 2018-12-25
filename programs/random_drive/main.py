#!/usr/bin/env python3
import sys

sys.path.append('/home/robot')

from programs.random_drive.random_drive.drive import drive

print("Let's drive!")
sys.stdout.flush()

drive()
