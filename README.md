# PyXYZ

PyXYZ (pronounced _pyxies_) is a a simple 3D wireframe engine for education, entirely programmed in Python, using only 
PyGame, NumPy and NumPy-Quaternion.

It is an object-oriented engine, with the main design focus on simplicity and ease of learning and extension, and has
very little functionality out-of-the-box: it allows for the programmer to visualize a 3D scene using a virtual camera.

![alt text](https://github.com/VideojogosLusofona/PyXYZ/raw/master/screenshots/terrain.png "Sample terrain application")

The engine was built using:
* Python 3.6 
* Pygame (https://www.pygame.org/news)
* Numpy (https://numpy.org/devdocs/user/quickstart.html)
* Numpy-quaternion (https://pypi.org/project/numpy-quaternion/)

This engine was tested with Python 3.6, 3.7, 3.8 and 3.9.

## Installation

### Dependencies

To use PyXYZ, you'll have to install all the used modules:

* `pip install pygame`
* `pip install numpy`
* `pip install numpy-quaternion`

Although not needed, to avoid some warnings on application startup, you can install two additional modules:

* `pip install numba`
* `pip install scipy`

If pip is not available on the command line, you can try to invoke it through the module interface on Python:

* `python -m pip install <name of package>`

There might be some issues with installing numpy and numpy-quaternion, due to a C compiler not being available in the path.
If that happens, you can try download a binary version of the library (called a wheel) and install it manually.

You can download the wheels for Numpy from `https://pypi.org/project/numpy/#files`. Choose the appropriate version for your OS and Python version (cp36 for Python 3.6, cp37 for Python 3.7, etc). For example, 64-bit Windows 10 for Python 3.6 is the file `numpy-1.17.4-cp35-cp35m-win_amd64.whl`.

For numpy-quaternion, you can get the files from `https://www.lfd.uci.edu/~gohlke/pythonlibs/`. Same naming scheme is used, so the file for 64-bit Windows 10 for Python 3.6 is the file `numpy_quaternion‑2019.12.12‑cp36‑cp36m‑win_amd64.whl`.

To install a wheel manually, you just have to run the command: `pip install <wheel name>` or `python -m pip install <wheel name>` from the directory where the wheel was downloaded to.

### PyXYZ

Because of its educational purpose, PyXYZ is not meant to be installed as a Python module.

As such, to create a program that uses PyXYZ, just copy the pyxyz directory from this repository to your new project.
You can then use

```python
import pyxyz
```

or 

```python
from pyxyz import *
```

to use PyXYZ.

## Documentation

Documentation is available at https://videojogoslusofona.github.io/PyXYZ/.

## Basic Usage

First the programmer sets up Pygame, using something similar to:

```python
pygame.init()
screen = pygame.display.set_mode((640, 480))
```

Then, a scene can be setup:

```python
# Create a scene
scene = Scene("TestScene")
scene.camera = Camera(False , res_x , res_y)
# Moves the camera back 2 units
scene.camera.position -= Vector3(0,0,2)
# Create a sphere and place it in a scene, at position (0,0,0) 
obj1 = Object3d("TestObject")
obj1.scale = Vector3(1, 1, 1)
obj1.position = Vector3(0, 0, 0)
# Set the material of the sphere, in this case it is red
obj1.mesh = Mesh.create_sphere((1, 1, 1), 12, 12) 
obj1.material = Material(Color(1,0,0,1), "TestMaterial1") 
scene.add_object(obj1)
```

To render the scene, the programmer just has to use:

```python
scene.render(screen)
```

## Sample applications

All the sample application are in the repository https://github.com/VideojogosLusofona/PyXYZ-Samples.

To use the samples, clone the repository and copy the pyxyz directory to that cloned repository.

All the sample applications implement an application loop. A window is open, the content is displayed there, and the user can quit by pressing the ESC quit or closing the window.

See the samples repository for more information on the samples.

## Licenses

All code in this repo is made available through the [MIT license].

[MIT license]:(LICENSE)
