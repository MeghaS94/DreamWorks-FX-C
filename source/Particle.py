import OpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy, math, sys, os, random
from objLoader import ObjectLoader
import globals

class Particle :
	def __init__(self, deltaTime, velx, vely, velz, posx, posy, posz, size, texID):
		#Assests in the scene
		self.sphere = globals.sphere
		self.cube = globals.cube
		self.cone = globals.cone
		self.bunny = globals.bunny
		self.ground = globals.ground
		self.texid = texID
		
		#Initial velocity given to the particle
		self.Velx = velx 
		self.Vely = vely 
		self.Velz = velz 
		self.Posx = posx
		self.Posy = posy
		self.Posz = posz
		self.size = size
		#sphere obstacle's information
		self.sCX = self.sphere.getCentroidX()
		self.sCY = self.sphere.getCentroidY()
		self.sCZ = self.sphere.getCentroidZ()
		self.sCR = self.sphere.getRadius()
		#box obstacle information
		self.bxmin = self.cube.minX()
		self.bxmax = self.cube.maxX()
		self.bymin = self.cube.minY()
		self.bymax = self.cube.maxY()
		self.bzmin = self.cube.minZ()
		self.bzmax = self.cube.maxZ()
		#cone obstacle information
		self.cxmin = self.cone.minX()
		self.cxmax = self.cone.maxX()
		self.cymin = self.cone.minY()
		self.cymax = self.cone.maxY()
		self.czmin = self.cone.minZ()
		self.czmax = self.cone.maxZ()
		#bunny's obstacle information
		self.Bunxmin = self.bunny.minX()
		self.Bunxmax = self.bunny.maxX()
		self.Bunymin = self.bunny.minY()
		self.Bunymax = self.bunny.maxY()
		self.Bunzmin = self.bunny.minZ()
		self.Bunzmax = self.bunny.maxZ()
		#Time interval after which new velocity and new position are calculated
		self.deltaTime = deltaTime
		self.g = 0.0095 		#acceleration due to gravity
		self.done = False	#bool flag to check if a particle has collided or not, 
							#Particle is killed as soon as it collides and child particles are spawned.

	def newPos(self):
		#Calculate the new position of the particle
		# xnew = xold + velx * delta t -> since there is no acceleration in x
		# znew = zold + velz * delta t -> since there is no acceleration in z
		# ynew = yold + vely * delta t - (1/2)* g * (delta t)^2 -> to consider the effect of acceleration due to gravity in y direction
		self.Posx = self.Posx + (self.deltaTime) * self.Velx 
		self.Posy = self.Posy + self.Vely * self.deltaTime - (0.5)*(self.g)*self.deltaTime*self.deltaTime
		self.Posz = self.Posz + (self.deltaTime) * self.Velz

	def checkInsideTriangle(self, point, vertex1, vertex2, vertex3):
		#A - vertex1, B- vertex2, C-vertex3
		#compute basis vectors
		v0 = vertex3 - vertex1
		v1 = vertex2 - vertex1
		v2 = point - vertex1

		#compute dot products
		dot00 = numpy.dot(v0, v0)
		dot01 = numpy.dot(v0, v1)
		dot02 = numpy.dot(v0, v2)
		dot11 = numpy.dot(v1, v1)
		dot12 = numpy.dot(v1, v2)

		#Compute barycentric coordinates
		if ((dot00 * dot11 - dot01 * dot01) != 0):
			invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
		else :
			invDenom = 1 / (0.0001)	
		u = (dot11 * dot02 - dot01 * dot12) * invDenom
		v = (dot00 * dot12 - dot01 * dot02) * invDenom

		#Check if point is in triangle
		return (u >= 0) and (v >= 0) and (u + v <= 1)


	def calculateCollisionImpact(self, faces, normals, e):		
		for i in range(0,len(faces), 9):
			vertex1 = numpy.array([faces[i], faces[i+1], faces[i+2]])
			vertex2 = numpy.array([faces[i+3], faces[i+4], faces[i+5]])
			vertex3 = numpy.array([faces[i+6], faces[i+7], faces[i+8]])

			normal = numpy.array([ normals[i], normals[i+1], normals[i+2]])
			magnitude = float(numpy.linalg.norm(normal))

			UnitNormal = numpy.array([ normals[i]/ float(magnitude), normals[i+1]/ float(magnitude), normals[i+2]/ float(magnitude)])
			d = -(numpy.dot(vertex1, UnitNormal)) #check
			
			perpDist = (UnitNormal[0]*self.Posx + UnitNormal[1]*self.Posy + UnitNormal[2]*self.Posz + d)
			#perpDist = abs(normal[0]*self.Posx + normal[1]*self.Posy + normal[2]*self.Posz + d)/float(numpy.linalg.norm(normal))
			if ( perpDist < 0.001):
				position = numpy.array([self.Posx, self.Posy, self.Posz])
				pointOnPlane = position - perpDist*UnitNormal
				
				if (self.checkInsideTriangle(pointOnPlane , vertex1, vertex2, vertex3)):
					#print "DetectCollisionWithCone"
					#if (normal[0]*self.Posx + normal[1]*self.Posy + normal[2]*self.Posz + d > 0):
					ec = e
					n = normal 	#normal at the point of collision
					Velocity = numpy.array([self.Velx, self.Vely, self.Velz])
					t = numpy.cross(n,numpy.cross(Velocity,n))	 #tagent = nX(vXn)
					# resolve the velocity into components along the normal n and tangent t 
					Vxn = (numpy.dot(Velocity, n) / float(numpy.dot(n,n)) )* n[0]
					Vyn = (numpy.dot(Velocity, n) / float(numpy.dot(n,n)) )* n[1]
					Vzn = (numpy.dot(Velocity, n) / float(numpy.dot(n,n)) )* n[2]
					Vxt = (numpy.dot(Velocity, t) / float(numpy.dot(t,t)) )* t[0]
					Vyt = (numpy.dot(Velocity, t) / float(numpy.dot(t,t)) )* t[1]
					Vzt = (numpy.dot(Velocity, t) / float(numpy.dot(t,t)) )* t[2]
					#resultant velocity is -e*(vel along normal) + (vel along tangent)
					#self.Velx = -ec*Vxn + Vxt
					#self.Vely = -ec*Vyn + Vyt
					#self.Velz = -ec*Vzn + Vzt
					#set bool to kill particles
					self.done = True
					V = math.sqrt(self.Velx*self.Velx + self.Vely*self.Vely + self.Velz*self.Velz )
					normal_mag = math.sqrt(n[0]*n[0] +  n[1]*n[1] + n[2]*n[2])
					#unit vector of velocity in the direction of the normal
					Nx_unit = n[0]/ float(normal_mag)
					Ny_unit = n[1]/ float(normal_mag)
					Nz_unit = n[2]/ float(normal_mag)
					for i in range(3):
						#angle to project the child particles at
						ALPHA = random.randint(-30, 30)
						vRot = numpy.array([])
						vtangent = numpy.array([Vxt, Vyt , Vzt])
						normal = numpy.array([n[0], n[1], n[2]])
						#rotate the velocity along tangent about the normal by an angle ALPHA
						vRot =  vtangent * numpy.cos(numpy.deg2rad(ALPHA)) + numpy.cross(normal, vtangent) * numpy.sin(numpy.deg2rad(ALPHA)) + normal*(numpy.cross(normal, vtangent))*(1- numpy.cos(numpy.deg2rad(ALPHA)))	
						#the resultant velocity of the child particles is : -e*(v along normal) + (vtangent rotated by ALPHA)
						
						globals.all_particles = numpy.append(globals.all_particles, 
							Particle(self.deltaTime, -ec*Vxn + vRot[0] ,-ec*Vyn + vRot[1],-ec*Vzn + vRot[2] , self.Posx, self.Posy, self.Posz, 
								self.size*random.uniform(0.6, 0.8),self.texid))				

					break	
	
	def newVel(self):
		#Since the only acceleration considered in acceleration due to gravity, g, velocity changes due to acceleration only in the y direction
		# vely = vely - g * delta t
		self.Vely = self.Vely - self.g* self.deltaTime

		if(self.DetectCollisionWithPlane()):
			ep = 0.4 #e for plane
			n =  numpy.array([0,1,0 ] )   #normal to the ground
			Velocity = numpy.array([self.Velx, self.Vely, self.Velz])
			t = numpy.array([1,0,0])	  #numpy.cross(n,numpy.cross(Velocity,n))	 
			#print t						#tagent = n X v
			Vxn = (numpy.dot(Velocity, n) / float(numpy.dot(n,n)) )* n[0]
			Vyn = (numpy.dot(Velocity, n) / float(numpy.dot(n,n)) )* n[1]
			Vzn = (numpy.dot(Velocity, n) / float(numpy.dot(n,n)) )* n[2]
			Vxt = (numpy.dot(Velocity, t) / float(numpy.dot(t,t)) )* t[0]
			Vyt = (numpy.dot(Velocity, t) / float(numpy.dot(t,t)) )* t[1]
			Vzt = (numpy.dot(Velocity, t) / float(numpy.dot(t,t)) )* t[2]
			# resultant velocity is -e*(velocity along normal) + (velocity along tangent)
			self.Velx = -ep*Vxn + Vxt
			self.Vely = -ep*Vyn + Vyt
			self.Velz = -ep*Vzn + Vzt
			# set bool to kill particle
			self.done = True
			V = math.sqrt(self.Velx*self.Velx + self.Vely*self.Vely + self.Velz*self.Velz )
			normal_mag = math.sqrt(Vxn*Vxn +  Vyn*Vyn + Vyn*Vyn)
			#unit vector of the velocity in the direction of the normal
			Vxn_unit = Vxn/ float(normal_mag)
			Vyn_unit = Vyn/ float(normal_mag)
			Vzn_unit = Vzn/ float(normal_mag)
			for i in range(random.randint(2,5)):
				# angle to project the child particles at
				ALPHA = random.randint(1, 360)
				vRot = numpy.array([])
				vtangent = numpy.array([Vxt, Vyt , Vzt])
				normal = numpy.array([n[0], n[1], n[2]])
				#rotate the velocity along tangent about the normal by an angle ALPHA
				vRot =  vtangent * numpy.cos(numpy.deg2rad(ALPHA)) + numpy.cross(normal, vtangent) * numpy.sin(numpy.deg2rad(ALPHA)) + normal*(numpy.cross(normal, vtangent))*(1- numpy.cos(numpy.deg2rad(ALPHA)))	
				# the resultant velocity given to the child particles is : -e*(V along noraml) + (vtangent rotated by ALPHA)
				globals.all_particles = numpy.append(globals.all_particles, 
					Particle(self.deltaTime, -ep*Vxn + vRot[0] ,-ep*Vyn + vRot[1],-ep*Vzn + vRot[2] , self.Posx, self.Posy, self.Posz, 
						self.size*random.uniform(0.6, 0.9), self.texid))

		if (globals.obstacles_in_scene[3] == 1):			
			if (self.DetectCollisionWithBunny()):
				# get all triangles
				#iterate and check if collision occoured, 
				#give that normal and compute new vel
				Bunny_triangles = self.bunny.getTriangles()
				Bunny_normals = self.bunny.getNormal()
				self.calculateCollisionImpact(Bunny_triangles, Bunny_normals, 0.05)

		if (globals.obstacles_in_scene[1] == 1):		
			if (self.DetectCollisionWithCone()):
				# get all triangles
				#iterate and check if collision occoured, 
				#give that normal and compute new vel
				Cone_triangles = self.cone.getTriangles()
				Cone_normals = self.cone.getNormal()
				self.calculateCollisionImpact(Cone_triangles, Cone_normals, 0.5)				

		if (globals.obstacles_in_scene[0] == 1):		
			if (self.DetectCollisionWithSphere()):
				Sphere_triangles = self.sphere.getTriangles()
				Sphere_normals = self.sphere.getNormal()
				self.calculateCollisionImpact(Sphere_triangles, Sphere_normals, 0.5)
				
		if (globals.obstacles_in_scene[2] == 1):
			if (self.DetectCollisionWithCube()):
				#iterate and check if collision occoured, 
				#give that normal and compute new vel
				Cube_triangles = self.cube.getTriangles()
				Cube_normals = self.cube.getNormal()
				self.calculateCollisionImpact(Cube_triangles, Cube_normals, 0.07)
		


	def DetectCollisionWithPlane(self):
		#xz plane, check perpendicular distance to xz plane
		if self.Posy <= 0.1 :
			return True
		else :
			return False	

	
	def DetectCollisionWithSphere(self):
		#assume each particle has a center, if distance between the center of the sphere and the center of the particle < sum of the their radii, collision occours
		if (math.sqrt( (self.Posx - self.sCX)*(self.Posx - self.sCX) +(self.Posy - self.sCY)*(self.Posy - self.sCY)+(self.Posz - self.sCZ)*(self.Posz - self.sCZ) ) <=self.sCR+0.05):
			#print "detected collision with sphere"
			return True
		else :
			return False	

	def DetectCollisionWithCube(self):		
		if((self.Posx >= self.bxmin and self.Posx <= self.bxmax) and (self.Posy >= self.bymin and self.Posy<= self.bymax)  
			and (self.Posz >= self.bzmin and self.Posz<= self.bzmax) ):
			#print "collided with the cube" #entered the bounding box of the cube
			return True
		else :
			return False

	def DetectCollisionWithCone(self):		
		if((self.Posx >= self.cxmin and self.Posx <= self.cxmax) and (self.Posy >= self.cymin and self.Posy<= self.cymax)  
			and (self.Posz >= self.czmin and self.Posz<= self.czmax) ):
			#print "collided with the cone" #entered the bounding box of the cone
			return True
		else :
			return False

	def DetectCollisionWithBunny(self):		
		if((self.Posx >= self.Bunxmin and self.Posx <= self.Bunxmax) and (self.Posy >= self.Bunymin and self.Posy<= self.Bunymax)  
			and (self.Posz >= self.Bunzmin and self.Posz<= self.Bunzmax) ):
			#print "collided with the bunny" #entered the bounding box of the bunny
			return True
		else :
			return False		

	def beginBillboard(self):
		glPushMatrix()
		a = (GLfloat * 16)()
		mvm = glGetFloatv(GL_MODELVIEW_MATRIX, a)
		for i in range(0,3):
			for j in range(0,3):
				if (i == j):
					mvm[i*4+j] = 1
				else :
					mvm[i*4+j] = 0
		glLoadMatrixf(mvm)				

	def endBillboard(self):
		glPopMatrix()	

	def drawQuad(self, Size, px, py, pz):
		#calculate the position and orientation of the textured quad(spark)
		velocity = numpy.array([self.Velx, self.Vely, self.Velz ])
		X = numpy.array([1.0,0.0,0.0])
		Y = numpy.array([0.0,1.0,0.0])
		Z = numpy.array([0.0,0.0,1.0])
		thetax = numpy.degrees(numpy.arccos(numpy.dot(velocity, X)/numpy.linalg.norm(velocity)))
		thetay = numpy.degrees(numpy.arccos(numpy.dot(velocity, Y)/numpy.linalg.norm(velocity)))
		thetaz = numpy.degrees(numpy.arccos(numpy.dot(velocity, Z)/numpy.linalg.norm(velocity)))
		normal = numpy.cross( X,velocity)
		norm = numpy.linalg.norm(normal)
		#f (self.Vely < 0):
		#	thetax = - thetax 

		glPushMatrix()
		glTranslatef(px, py, pz)
		# rotate by thetax along the normal of the plane of the velocity vector and the x axis, to rotate the spark according to its direction of movement
		glRotatef(thetax, normal[0]/float(norm), normal[1]/float(norm), normal[2]/float(norm))
		glTranslatef(-px, -py, -pz)
		
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3f(-Size+px, -Size+py, pz)
		glTexCoord2f(1.0, 0.0)
		glVertex3f(-Size+px, Size+py, pz)
		glTexCoord2f(1.0, 1.0)
		glVertex3f(Size+px, Size+py, pz)
		glTexCoord2f(0.0, 1.0)
		glVertex3f(Size+px, -Size+py, pz)
		glEnd()
		
		glPopMatrix()
		

	def draw(self):
		i =0
		if self.done == True :
			return False
		elif (self.size <= 0.1):
			return False
		else :
			#self.beginBillboard()	
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)	
			glEnable(GL_BLEND)
			glBindTexture(GL_TEXTURE_2D, self.texid)
			self.drawQuad(self.size, self.Posx, self.Posy, self.Posz )
			glDisable(GL_BLEND)
			#self.endBillboard()		
		self.newPos()
		self.newVel()
		return True
