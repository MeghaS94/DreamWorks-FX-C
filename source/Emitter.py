from Particle import Particle
import globals
import numpy, random

"""
This class takes care of the emission of particles.
tex id : texture ID (texture mapped to the emitted particles)
emit   : creates and adds particles with random velocities in x,y,z directions, to the global array all_particles.
"""

class Emitter :
	def __init__(self, texid):
		self.texid = texid

	def emit(self):	
		#particle = Particle(1.0, -random.uniform(0.1, 0.27), random.uniform(0.08, 0.2), 
		#	random.uniform(-0.1, 0.07), globals.sawblade.getCentroidX()-0.33,
		#	globals.sawblade.getCentroidY()-0.33, globals.sawblade.getCentroidZ(), 0.17 ,self.texid)
		particle = Particle(0.9, -0.22,
		 	0.16, random.uniform(0.01, -0.1), globals.sawblade.getCentroidX()-0.33,
			globals.sawblade.getCentroidY()-0.33, globals.sawblade.getCentroidZ(), 0.13 ,self.texid)
		globals.all_particles = numpy.append(globals.all_particles, particle)
			
	
