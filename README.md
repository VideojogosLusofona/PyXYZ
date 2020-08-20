# PyXYZ

PyXYZ (pronounced _pyxies_) is a a simple 3D wireframe engine for education, entirely programmed in Python.

![alt text](https://github.com/DiogoDeAndrade/PyXYZ/raw/master/screenshots/terrain.png "Sample terrain application")

This engine serves as a basis for the "Introdução à Matemática e Física Para Videojogos I" course, on the [Licenciatura em Videojogos][lv] da
[Universidade Lusófona de Humanidades e Tecnologias][ULHT] in Lisbon.

The engine was built using:
* Python 3.6
* Pygame (https://www.pygame.org/news)
* Numpy (https://numpy.org/devdocs/user/quickstart.html)
* Numpy-quaternion (https://pypi.org/project/numpy-quaternion/)

## Architecture

PyXYZ is an object-oriented engine, with the main design focus on simplicity and ease of learning and extension. 

It provides very little functionality out-of-the- box: it allows for the programmer to visualize a 3D scene using a virtual camera.

A scene is composed of 3D objects organized in an optional hierarchical fashion, and each object contains a polygonal mesh and a material that controls how the mesh is rendered. 

At the most basic level, it has a few elementary helper classes, like Color, which describes a color with separate red, green, blue and alpha channels, and Vector3, a straightforward 3D vector implementation.

The core of the engine is comprised of the Scene, Object3d, Camera and Mesh classes, which handle the rendering itself. 

An Object3d has the position, rotation and scaling (PRS properties), all of which are in local space. It also stores the reference for a mesh and a material, and contains a list of child Object3d, which enables the user to build the hierarchical scene graph. 

A Scene stores the scene graph with any number of Objects3d on the root level. It also contains a camera, that is used for the rendering. 

The Camera is derived from Object3d, so that it can be treated in the same way, and even parented to other objects, or vice-versa. It also provides a simple function to convert from screen space coordinates to a ray origin/position.

The Mesh contains a list of polygons, with each polygon being a list of vertex positions in local space. There are no indexing primitives as simplicity is the main driver of the engine. 

The Material class stores the rendering properties like line color and width. A single material can be used by multiple meshes for rendering.

The current implementation of PyXYZ uses Pygame for the actual render- ing. We chose Pygame for its simplicity, support for polygon rendering and full software implementation.

## Installation

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

## Basic Usage

First the programmer sets up Pygame, using something similar to:

~~~
pygame.init()
screen = pygame.display.set_mode((640, 480))
~~~

Then, a scene can be setup:

~~~
# Create a scene
scene = Scene("TestScene")
scene.camera = Camera(False , res_x , res_y)
# Moves the camera back 2 units
scene.camera.position -= vector3(0,0,2)
# Create a sphere and place it in a scene, at position (0,0,0) 
obj1 = Object3d("TestObject")
obj1.scale = vector3(1, 1, 1)
obj1.position = vector3(0, 0, 0)
# Set the material of the sphere, in this case it is red
obj1.mesh = Mesh.create_sphere((1, 1, 1), 12, 12) obj1.material = Material(color(1,0,0,1), "TestMaterial1") scene.add_object(obj1)
~~~

To render the scene, the programmer just has to use:

~~~
scene.render(screen)
~~~

## Sample applications

All the sample applications implement an application loop. A window is open, the content is displayed there, and the user can quit by pressing the ESC quit or closing the window.

### Sphere (sample_sphere.py)

![alt text](https://github.com/DiogoDeAndrade/PyXYZ/raw/master/screenshots/sphere.png "Sample sphere application")

The simplest sample, it just creates a red sphere on the center of the viewport and rotates it slowly.

### Hierachy (sample_hierarchy.py)

![alt text](https://github.com/DiogoDeAndrade/PyXYZ/raw/master/screenshots/hierarchy.png "Sample hierarchy application")

This application demonstrates the use of hierarchies. Hierarchies can be created by adding objects as children of other objects. The PRS of child objects will be considered to be in local space (the space of the parent).

### Cube fall (sample_cubefall.py)

![alt text](https://github.com/DiogoDeAndrade/PyXYZ/raw/master/screenshots/cubefall.png "Sample cube fall application")

In this application, cubes are spawned on top of the screen and fall
down with gravity. This demonstrates one way of creating/destroing objects through the life cycle of the application.

It also shows the use of creating classes derived from Object3d (use of hierarchy-based extension instead of component-based)

### Terrain (sample_terrain.py)

![alt text](https://github.com/DiogoDeAndrade/PyXYZ/raw/master/screenshots/terrain.png "Sample terrain application")

This application generates a terrain based on a 2-octave Perlin noise, colors the generated polygons based on height and slope, and rotates the terrain in front of the camera.

This makes use of a helper 2d perlin generator that's part of PyXYZ.

### Missile Game (sample_game.py)

![alt text](https://github.com/DiogoDeAndrade/PyXYZ/raw/master/screenshots/terrain.png "Sample terrain application")

This is a sort of incomplete game: the player can shoot some missiles using the mouse, and it demonstrates user input and a more complex application loop. It also shows functionality like creating a mesh from different parts, converting a mouse position into a ray, sphere/sphere collision detection, target tracking and a rudimentary screen flash effect. The game is not complete, since it doesn’t have win/lose condition

## Licenses

All code in this repo is made available through the [GPLv3] license.
The text and all the other files are made available through the 
[CC BY-NC-SA 4.0] license.

## Metadata

* Autor: [Diogo Andrade][]

[Diogo Andrade]:https://github.com/DiogoDeAndrade
[GPLv3]:https://www.gnu.org/licenses/gpl-3.0.en.html
[CC BY-NC-SA 4.0]:https://creativecommons.org/licenses/by-nc-sa/4.0/
[Bfxr]:https://www.bfxr.net/
[ULHT]:https://www.ulusofona.pt/
[lv]:https://www.ulusofona.pt/licenciatura/videojogos
