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
		"""
		Generate particles and append to a global array of particles
		"""
		# args passed to particle -> deltaTime, velx, vely, velz, posx, posy, posz, size, texID
		particle = Particle(0.9, -0.22, 0.16, random.uniform(0.01, -0.1), globals.sawblade.getCentroidX()-0.33,
							globals.sawblade.getCentroidY()-0.33, globals.sawblade.getCentroidZ(), 0.13 ,self.texid)
		globals.all_particles = numpy.append(globals.all_particles, particle)
			
	
