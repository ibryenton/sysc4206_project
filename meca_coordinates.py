#!/usr/bin/env python
"""
<Module Description>
"""
import numpy as np
from rich import print
from rich.traceback import install; install()
import mecademicpy.robot as mdr

class Meca():
    """
    Test function which interfaces with mecademic robot
    """
    def __init__(self):
        self.robot = mdr.Robot()
        self.callbacks = mdr.RobotCallbacks()
        self.callbacks.on_connected = self.print_connected()
        self.robot.RegisterCallbacks(callbacks=self.callbacks, run_callbacks_in_separate_thread=False)
        self.robot.Connect(address='192.168.0.100', enable_synchronous_mode=True)
        self.reset_error()
        self.robot.ResumeMotion()
        self.robot.ActivateAndHome()
        self.robot.SetJointVel(10)
        self.robot.MoveJoints(0, 0, 0, 0, 0, 0)

    # The returned robot position will be (0, -60, 60, 0, 0, 0), because this line will only be executed once MoveJoints(0, -60, 60, 0, 0, 0) has completed.
        print(self.robot.GetJoints())

    def deactivate(self):
        """
        Deactivate and Disconnect from Meca500
        """
        robot.DeactivateRobot()
        robot.Disconnect()

    def print_connected(self):
        return print(f'[bold aquamarine1] connected')


    def meca_coordinates(self, px, py, pz):
        """
        Function which takes coordinates of point in Camera Reference Frame
        and returns the coordinates in Robot's Base Reference Frame

        Args:
            px (int): x coordinate of point in CRF
            py (int): y coordinate of point in CRF
            pz (int): z coordinate of point in CRF

        Returns:
            meca_coord (array): [x, y, z, 1] coordinates of point in BRF
        """
        # Pc is the vector which defines the BRF to the CRF
        Pc = [300, -30, 420]
        P = [px, -py, pz-25, 1]

        H = [[0, 1, 0, Pc[0]],
             [-1, 0, 0, Pc[1]],
             [0, 0, -1, Pc[2]],
             [0, 0, 0, 1]]

        meca_coord = np.matmul(H,P)
        return meca_coord

    def get_joints(self):
        print(self.robot.GetJoints())

    def reset_error(self):
        self.robot.ResetError()

if __name__ == '__main__':
    main()

