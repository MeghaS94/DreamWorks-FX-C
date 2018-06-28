import numpy
import OpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy, math, sys, os, random
import glutils
import time
from objLoader import ObjectLoader

"""
This class contains variables, assests used accross files
"""

def init():
	global all_particles
	global obstacles_in_scene
	global sawblade, ground, slab, sphere, cube, cone, bunny
	all_particles = numpy.array([])
	sawblade = ObjectLoader("../assets/sawblade.obj")
	ground = ObjectLoader("../assets/ground.obj")	
	slab = ObjectLoader("../assets/slab.obj")
	sphere = ObjectLoader("../assets/sphere.obj")
	cube = ObjectLoader("../assets/cube.obj")
	cone = ObjectLoader("../assets/cone.obj")
	bunny = ObjectLoader("../assets/bunny.obj")
	#sphere, cone, cube, bunny
	obstacles_in_scene = numpy.array([ 1,1,1,1 ])
