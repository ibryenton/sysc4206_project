#!/usr/bin/env python
"""
Script which interfaces with Mecademic Meca500 R3 6-DOF robot arm
using Mecademic's MecademicPy library
"""
import mecademicpy.robot as mdr
from rich import print



def main():
    """
    Test function which interfaces with mecademic robot
    """
    robot = mdr.Robot()
    robot.Connect(address='192.168.0.100', enable_synchronous_mode=True)
    robot.ActivateAndHome()

    robot.MoveJoints(0, 0, 0, 0, 0, 0)
    robot.MoveJoints(0, -60, 60, 0, 0, 0)

    # The returned robot position will be (0, -60, 60, 0, 0, 0), because this line will only be executed once MoveJoints(0, -60, 60, 0, 0, 0) has completed.
    print(robot.GetJoints())

    robot.DeactivateRobot()
    robot.Disconnect()

if __name__ == '__main__':
    main()


