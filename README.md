# SYSC 4206 Final Project

Status: No

This repository contains the files used for the SYSC4206 Final design project aimed to implement a lactate testing protocol utilizing surgical robotics and video recognition.

The course covers controlling the Meca500 robot using MATLAB, but Python allows more flexibility in terms of designing complete aplications which can be released to the general public and don’t require MATLAB and other advanced toolboxes.

### Meca.py

This script creates a wrapper object for the MecademicPy library, implementing error catching and other useful messages when certain events are detected. This shows the simplicity of using Python for interfacing with the Meca500, accomplishing functions like connecting to the robot in much fewer lines than the MATLAB implementation. Additionally, it allows the connection to the Meca500 in just two lines of code (1 import and one to initiaize the object). You can use any of the functions described in the programming manual on the Meca.robot object. The code snippet below highlights this:

```python
#required lines of code to use Meca.py in python application
from meca import Meca

meca = Meca() #initializes meca object

#MovePose
meca.robot.MovePose(0,0,0,0,0,0)

#MoveLin
meca.robot.MoveLin(0,0,0,0,0,0)
```

To interface with the Meca500 using python, you can utililze the MecademicPy library directly or import this file into your desired python script. The [meca.py](http://meca.py) script aims to reduce the repetition of standard code required to connect to the robot, but the following code snippet highlights the lines of code to interface with the MecademicPy library directly.

```python
# Using Python for meca using MecademicPy library directly
import mecademicpy.robot as mdr

robot = mdr.Robot()
callbacks = mdr.RobotCallbacks()
callbacks.on_connected = self.print_connected()
robot.RegisterCallbacks(callbacks=self.callbacks, run_callbacks_in_separate_thread=False)
robot.Connect(address='192.168.0.100', enable_synchronous_mode=True)
robot.ActivateAndHome()
```

The code above is included in the init of the [meca.py](http://meca.py) Meca object allowing the meca object to be. initialized in one line only.

### testWithCamera.py

This script utilizes python’s OpenCV library to connect to a webcam and identify red circular markers within the webcams image field. The coordinates of the red market are determined using OpenCV find contour function, and the location in mm is returned by converting the pixel location to mm with the pixel/mm ratio calculated by finding the quantity of pixel in a known distance. The threshold for red values was determined in terms of RGB values and can be adjusted for identification of other colours of markers. The [testWithCamera.py](http://testWithCamera.py) script imports the [meca.py](http://meca.py) and uses the MovePose command on the Meca.robot object to navigate to the incision site
