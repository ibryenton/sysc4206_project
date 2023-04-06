#!/usr/bin/env python
"""
<Module Description>
"""
import numpy as np

import mecademicpy.robot as mdr

class Meca():
    """
    Test function which interfaces with mecademic robot
    """
    def __init__(self):
        self.robot = mdr.Robot()
        self.callbacks = mdr.RobotCallbacks()
        self.callbacks.on_connected = self.print_connected()
        self.robot.RegisterCallbacks(callbacks=self.callbacks, run_callbacks_in_separate_thread=True)
        self.robot.Connect(address='192.168.0.100', enable_synchronous_mode=True)
        self.reset_error()
        self.robot.ActivateAndHome()
        self.robot.SetJointVel(10)
        self.robot.MoveJoints(0, 0, 0, 0, 0, 0)
        #self.robot.MoveJoints(0, -60, 60, 0, 0, 0)

    # The returned robot position will be (0, -60, 60, 0, 0, 0), because this line will only be executed once MoveJoints(0, -60, 60, 0, 0, 0) has completed.
        #print(self.robot.GetJoints())

    def deactivate(self):
        """
        Deactivate and Disconnect from Meca500
        """
        robot.DeactivateRobot()
        robot.Disconnect()

    def print_connected(self):
        print('[bold aquamarine1] connected')


    def meca_coordinates(self, px, py, pz):
        # Pc is the vector which defines the BRF to the CRF
        Pc = [0, 320, 420, 1]
        P = [px, py, pz, 1]

        H = [[0, 1, 0, Pc[0]],
             [1, 0, 0, Pc[1]],
             [0, 0, -1, Pc[2]],
             [0, 0, 0, 1]]

        print(H)
        meca_coord = np.matmul(H,P)
        print(meca_coord)
        return meca_coord

    def get_joints(self):
        print(self.robot.GetJoints())

    def reset_error(self):
        self.robot.ResetError()

if __name__ == '__main__':
    main()

