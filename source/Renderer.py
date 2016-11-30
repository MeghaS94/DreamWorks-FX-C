import OpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy, math, sys, os, random
import glutils
import time
from objLoader import ObjectLoader
from Particle import Particle
from Emitter import Emitter
import globals
"""
The main Renderer class
"""

class Renderer :
	"""rendering the particle system """
	def __init__(self):
		self.t = 0.0
		self.t = 0
		self.x = 0.0
		self.y = 0
		self.z = 0
		self.scale = 1.0
		self.rz  = 0.0

		#initialise glut
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
		self.width = 1000
		self.height = 1000
		self.aspect = self.width/float(self.height)
		glutInitWindowSize(1000,1000)
		glutCreateWindow("The return of the Bunny")

		self.init()
		#initialize GL
		glutReshapeFunc(self.reshape)
		glutDisplayFunc(self.display)
		glutKeyboardFunc(self.keyboard)
		#glutSpecialFunc(self.glutSpecialKey)
		
		# load all the required textures here
		self.texid_sawblade = glutils.loadTexture('../assets/sawblade.jpg')
		self.texid_ground = glutils.loadTexture('../assets/ground_tile.jpg')
		self.texid_slab = glutils.loadTexture('../assets/slab.jpg')
		self.texid_star = glutils.loadTextureWithTransparency('../assets/new_spark2.png')
		
		self.texid_cube = glutils.loadTexture('../assets/wood.jpg')
		self.texid_cone = glutils.loadTexture('../assets/blue.jpg')
		self.texid_sphere = glutils.loadTextureWithTransparency('../assets/sphere.png')
		self.texid_bunny = glutils.loadTextureWithTransparency('../assets/bunny.png')
		
		#create an emitter for the particle system
		self.emitter = Emitter(self.texid_star)
		self.frame=0
		self.time= 0
		self.timebase=0
		glutMainLoop()


	def keyboard (self,key, x, y):
		if (key == 'Q'):
			self.x += 0.3
			glutPostRedisplay()
		elif (key == 'q'):
			self.x -= 0.3
			glutPostRedisplay()
		elif (key == 'E'):
			self.y += 0.3
			glutPostRedisplay()	
		elif (key == 'e'):
			self.y -= 0.3
			glutPostRedisplay()
		elif (key == 'Z'):
			self.z += 0.3
			glutPostRedisplay()
		elif (key == 'z'):
			self.z -= 0.3
			glutPostRedisplay()
		elif (key == 's'):
			self.scale -= 0.3
			glutPostRedisplay()
		elif (key == 'S'):
			self.scale += 0.3
			glutPostRedisplay()
		elif (key == 'y'):
			#add shpere to the scene
			globals.obstacles_in_scene[0] = 1
		elif (key == 'Y'):
			#remove shpere from the scene
			globals.obstacles_in_scene[0] = 0
		elif (key == 'u'):
			#add cone to the scene
			globals.obstacles_in_scene[1] = 1
		elif (key == 'U'):
			#remove cone from the scene
			globals.obstacles_in_scene[1] = 0
		elif (key == 'i'):
			#add cube to the scene
			globals.obstacles_in_scene[2] = 1
		elif (key == 'I'):
			#remove cube from the scene
			globals.obstacles_in_scene[2] = 0
		elif (key == 'o'):
			#add bunny to the scene
			globals.obstacles_in_scene[3] = 1
		elif (key == 'O'):
			#remove bunny from the scene
			globals.obstacles_in_scene[3] = 0				
		

	#handles window resize events		
	def reshape(self, w, h):
		self.width = w
		self.height = h
		self.aspect = w/float(h)
		glViewport(0,0, w, h)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()	
		glOrtho(-3.0, 10.0, -7, 7, -100.0, 100.0)
		#gluPerspective(45.0, float(self.width)/float(self.height), 0.1, 100.0)	
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	#set initial state	
	def init(self) :
		self.t = 0.0
		glClearColor(0,0,0,0)
		glEnable(GL_DEPTH_TEST)
		glShadeModel (GL_SMOOTH)
		lightAmb = [ 1.0, 1.0, 1.0, 1.0 ]
		lightAmb1 = [ 1.0, 1.0, 0.0, 1.0 ]
		lightDifAndSpec = [ 1.0, 1.0, 1.0, 1.0 ]
		globAmb = [2,2,2, 1.0]
		headlightDiffuse = [ 0.5,0.5,0, 1]
		glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmb)
		glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDifAndSpec)
		glLightfv(GL_LIGHT0, GL_SPECULAR, lightDifAndSpec)
		glEnable(GL_LIGHT0)

		self.sawblade = globals.sawblade
		self.ground = globals.ground	
		self.slab = globals.slab
		self.sphere = globals.sphere
		self.cube = globals.cube
		#print self.cube.getNormal()
		self.cone = globals.cone
		self.bunny = globals.bunny

		glEnable(GL_LIGHTING)
		glEnable(GL_TEXTURE_2D)
		


	def display(self):
		# timer to dictate the emission of particles
		self.t += 1
		if (self.t % 1 == 0):
			self.emitter.emit()
		self.frame +=1
		self.time=glutGet(GLUT_ELAPSED_TIME);
		if (self.time - self.timebase > 1000) :
			print "FPS:%4.2f", self.frame*1000.0/(self.time-self.timebase)
			self.timebase = self.time
			self.frame = 0	

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		#variable to rotate the saw blade
		self.rz += 2.0
		glClearColor(0,0,0,0) 
		
		glPushMatrix()
		glLoadIdentity()
		gluLookAt (0,0,-5.0, 0.0,0.0, 0.0, 0.0, 1.0 , 0.0)
		glRotatef(self.x, 1,0,0)
		glRotatef(self.y, 0,1,0)
		glRotatef(self.z, 0,0,1)
		glScalef(self.scale, self.scale, self.scale)

		glBindTexture(GL_TEXTURE_2D, self.texid_slab)
		self.slab.draw()

		glBindTexture(GL_TEXTURE_2D, self.texid_ground)
		self.ground.draw()

		glBindTexture(GL_TEXTURE_2D, self.texid_sawblade)
		glPushMatrix()
		glTranslatef(self.sawblade.getCentroidX(), self.sawblade.getCentroidY(), self.sawblade.getCentroidZ() )
		glRotatef(self.rz, 0,0,1)
		glTranslatef(-self.sawblade.getCentroidX(), -self.sawblade.getCentroidY(), -self.sawblade.getCentroidZ() )  
		self.sawblade.draw()
		glPopMatrix()

		if(globals.obstacles_in_scene[0] == 1 ):
			glBindTexture(GL_TEXTURE_2D, self.texid_sphere)
			self.sphere.draw()

		if(globals.obstacles_in_scene[2] == 1 ):
			glBindTexture(GL_TEXTURE_2D, self.texid_cube)
			self.cube.draw()

		if(globals.obstacles_in_scene[1] == 1 ):		
			glBindTexture(GL_TEXTURE_2D, self.texid_cone)
			self.cone.draw()

		if(globals.obstacles_in_scene[3] == 1 ):	
			glBindTexture(GL_TEXTURE_2D, self.texid_bunny)
			self.bunny.draw()
		
		glDisable(GL_LIGHTING)
		#Draw the particles 
		i = 0
		while(i < len(globals.all_particles)):
			status = globals.all_particles[i].draw()
			if (status == False):
				globals.all_particles = numpy.delete(globals.all_particles, i)
			else :
				i += 1
		glEnable(GL_LIGHTING)		

		glPopMatrix()
		glutSwapBuffers()
		time.sleep(0.00005)
		glutPostRedisplay()

def main():
    print("starting glut window")
    globals.init()
    rw = Renderer()
    rw.display()

if __name__ == '__main__' :
    main()    		
