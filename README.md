# Simulating Sparks
Link to the video : https://youtu.be/Dcl4U-fsjF8

Author : Megha Shastry

Date   : Oct 6th 2016

This project builds a simple sparks simulation. The sparks can collide with obstacles in the scene. 
The sparks exist in the scene untill they collide with any of the obstacles. When a collision occours, 
the spark splits into smaller sparks which again follow the equations of motion.

Compilation Instructions :

* Pre-requisite installations to run the program :
	Python 2.7, OpenGL 2.0, PyopenGL, GLUT

* Command to Run :
	python Renderer.py

* Use the keys (o, shift+o), (i, shift+i), (u, shift+u), (y, shift+y) to toggle the appearace of the objects

* Use the keys (q, shift+q), (e, shift+e), (z, shift+z), (s, shift+s) to move the camera around in the scene

* Brief description of the classes :

	* glUtils class  : class with some generic openGL util functions for texture loading and camera manipulation.
	* globals class  : global variables used in other classes.
	* Renderer class : main entry point in the project. This class initialises the emitter, handles drawing of particles,
		               and handles keyboard interactions.
	* Emitter class  : This class adds particles with a initial velocity, to a global array, which is the emitter.
	* Particle class : This class uses contructs the particle and encapsulates all the methods needed to instantiate, 
					   move and display the particle.


