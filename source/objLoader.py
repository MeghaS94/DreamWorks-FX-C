import numpy as np
import OpenGL
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math

"""
Class to read the obj model from a file.
The obj file will have vertices, faces, normals and texture coordinates.
"""
class ObjectLoader:

	def addTriangle(self, a, b, c):
		"""
		Add a triangle to the array of triangles.
		"""
		self.disp_tri_array = np.append(self.disp_tri_array, self.v_arr[a*3])
		self.disp_tri_array = np.append(self.disp_tri_array, self.v_arr[a*3+1])
		self.disp_tri_array = np.append(self.disp_tri_array, self.v_arr[a*3+2])
		self.disp_tri_array = np.append(self.disp_tri_array, self.v_arr[b*3])
		self.disp_tri_array = np.append(self.disp_tri_array, self.v_arr[b*3+1])
		self.disp_tri_array = np.append(self.disp_tri_array, self.v_arr[b*3+2])
		self.disp_tri_array = np.append(self.disp_tri_array, self.v_arr[c*3])
		self.disp_tri_array = np.append(self.disp_tri_array, self.v_arr[c*3+1])
		self.disp_tri_array = np.append(self.disp_tri_array, self.v_arr[c*3+2])

	def addTex(self, a, b, c):
		"""
		Add texture coordinates to the array of uvs.
		"""
		self.disp_tex_array = np.append(self.disp_tex_array, self.vt_arr[a*2])
		self.disp_tex_array = np.append(self.disp_tex_array, self.vt_arr[a*2+1])
		self.disp_tex_array = np.append(self.disp_tex_array, self.vt_arr[b*2])
		self.disp_tex_array = np.append(self.disp_tex_array, self.vt_arr[b*2+1])
		self.disp_tex_array = np.append(self.disp_tex_array, self.vt_arr[c*2])
		self.disp_tex_array = np.append(self.disp_tex_array, self.vt_arr[c*2+1])

	def addNormal(self, a, b, c):
		"""
		Add normals to the array of normals.
		"""
		self.disp_norm_array = np.append(self.disp_norm_array, self.vn_arr[a*3])
		self.disp_norm_array = np.append(self.disp_norm_array, self.vn_arr[a*3+1])
		self.disp_norm_array = np.append(self.disp_norm_array, self.vn_arr[a*3+2])
		self.disp_norm_array = np.append(self.disp_norm_array, self.vn_arr[b*3])
		self.disp_norm_array = np.append(self.disp_norm_array, self.vn_arr[b*3+1])
		self.disp_norm_array = np.append(self.disp_norm_array, self.vn_arr[b*3+2])
		self.disp_norm_array = np.append(self.disp_norm_array, self.vn_arr[c*3])
		self.disp_norm_array = np.append(self.disp_norm_array, self.vn_arr[c*3+1])
		self.disp_norm_array = np.append(self.disp_norm_array, self.vn_arr[c*3+2])

	def calulateNormal(self, a, b, c):
		"""
		From the given vertex information, compute the normal 
		by doing a cross product of the two sides of the face.
		"""
		# ath vertex -> self.v_arr[a*3], self.v_arr[a*3+1], self.v_arr[a*3+2]
		# bth vertex -> self.v_arr[b*3], self.v_arr[b*3+1], self.v_arr[b*3+2] 	
		# cth vertex -> self.v_arr[c*3], self.v_arr[c*3+1], self.v_arr[c*3+2]
		ab = np.array([self.v_arr[a*3] -self.v_arr[b*3], self.v_arr[a*3+1] -self.v_arr[b*3+1], self.v_arr[a*3+2] -self.v_arr[b*3+2] ])
		ac = np.array([self.v_arr[a*3] -self.v_arr[c*3], self.v_arr[a*3+1] -self.v_arr[c*3+1], self.v_arr[a*3+2] -self.v_arr[c*3+2] ])
		normal = np.cross(ab, ac)
		self.disp_norm_array = np.append(self.disp_norm_array, normal[0])
		self.disp_norm_array = np.append(self.disp_norm_array, normal[1])
		self.disp_norm_array = np.append(self.disp_norm_array, normal[2])
		self.disp_norm_array = np.append(self.disp_norm_array, normal[0])
		self.disp_norm_array = np.append(self.disp_norm_array, normal[1])
		self.disp_norm_array = np.append(self.disp_norm_array, normal[2])
		self.disp_norm_array = np.append(self.disp_norm_array, normal[0])
		self.disp_norm_array = np.append(self.disp_norm_array, normal[1])
		self.disp_norm_array = np.append(self.disp_norm_array, normal[2])

	def __init__(self, filename):
		f = open(filename, 'r')
		self.v_arr = np.array([])
		self.vt_arr = np.array([])
		self.vn_arr = np.array([])
		self.disp_tri_array = np.array([])
		self.disp_norm_array = np.array([])
		self.disp_tex_array = np.array([])
		self.cx = 0.0
		self.cy = 0.0
		self.cz = 0.0
		#limits for the bounding box
		self.minx = 100.0
		self.miny = 100.0
		self.minz = 100.0
		self.maxx = -100.0
		self.maxy = -100.0
		self.maxz = -100.0
		while(1):
			strg = f.readline()
			str_arr = strg.split()
			if (len(str_arr)==1 and str_arr[0]=='g'):
				break
		while(1):
			strg = f.readline()
			str_arr = strg.split()
			if (len(str_arr)==1 and str_arr[0]=='g'):
				break
			if str_arr[0]=='v':
				self.v_arr = np.append(self.v_arr, float(str_arr[1]))
				
				self.cx = self.cx + float(str_arr[1])
				if (float(str_arr[1]) > self.maxx):
					self.maxx = float(str_arr[1])
				elif (float(str_arr[1]) < self.minx) :
					self.minx = float(str_arr[1])	
				
				self.v_arr = np.append(self.v_arr, float(str_arr[2]))
				
				self.cy = self.cy + float(str_arr[2])
				if (float(str_arr[2]) > self.maxy):
					self.maxy = float(str_arr[2])
				elif (float(str_arr[2]) < self.miny) :
					self.miny = float(str_arr[2])
				
				self.v_arr = np.append(self.v_arr, float(str_arr[3]))
				self.cz = self.cz + float(str_arr[3])
				if (float(str_arr[3]) > self.maxz):
					self.maxz = float(str_arr[3])
				elif (float(str_arr[3]) < self.minz) :
					self.minz = float(str_arr[3])

			if str_arr[0]=='vt':
				self.vt_arr = np.append(self.vt_arr, float(str_arr[1]))
				self.vt_arr = np.append(self.vt_arr, float(str_arr[2]))
				#self.vt_arr.append(float(str_arr[3]))
			if str_arr[0]=='vn':
				self.vn_arr = np.append(self.vn_arr, float(str_arr[1]))
				self.vn_arr = np.append(self.vn_arr, float(str_arr[2]))
				self.vn_arr = np.append(self.vn_arr, float(str_arr[3]))
		self.cx = self.cx /float(len(self.v_arr)/3)
		self.cy = self.cy /float(len(self.v_arr)/3)
		self.cz = self.cz /float(len(self.v_arr)/3)
		while(1):
			strg = f.readline()
			str_arr = strg.split()
			if (len(str_arr)==0):
				break
			if str_arr[0]=='f':
				if(len(str_arr)==4): #case: TRIANGLES
					self.addTriangle(int(str_arr[1].split('/')[0])-1, int(str_arr[2].split('/')[0])-1, int(str_arr[3].split('/')[0])-1)
					if(len(str_arr[1].split('/'))>1 and str_arr[1].split('/')[1]!=''):
						self.addTex(int(str_arr[1].split('/')[1])-1, int(str_arr[2].split('/')[1])-1, int(str_arr[3].split('/')[1])-1)
					if(len(str_arr[1].split('/'))>2 and str_arr[1].split('/')[2]!=''):
						self.addNormal(int(str_arr[1].split('/')[2])-1, int(str_arr[2].split('/')[2])-1, int(str_arr[3].split('/')[2])-1)
					else : #compute and Add your own normal
						self.calulateNormal(int(str_arr[1].split('/')[0])-1, int(str_arr[2].split('/')[0])-1, int(str_arr[3].split('/')[0])-1)
				elif(len(str_arr)==5): #case: QUADS
					self.addTriangle(int(str_arr[1].split('/')[0])-1, int(str_arr[2].split('/')[0])-1, int(str_arr[4].split('/')[0])-1)
					self.addTriangle(int(str_arr[2].split('/')[0])-1, int(str_arr[3].split('/')[0])-1, int(str_arr[4].split('/')[0])-1)
					if(len(str_arr[1].split('/'))>1 and str_arr[1].split('/')[1]!=''):
						self.addTex(int(str_arr[1].split('/')[1])-1, int(str_arr[2].split('/')[1])-1, int(str_arr[4].split('/')[1])-1)
						self.addTex(int(str_arr[2].split('/')[1])-1, int(str_arr[3].split('/')[1])-1, int(str_arr[4].split('/')[1])-1)
					if(len(str_arr[1].split('/'))>2 and str_arr[1].split('/')[2]!=''):
						self.addNormal(int(str_arr[1].split('/')[2])-1, int(str_arr[2].split('/')[2])-1, int(str_arr[4].split('/')[2])-1)
						self.addNormal(int(str_arr[2].split('/')[2])-1, int(str_arr[3].split('/')[2])-1, int(str_arr[4].split('/')[2])-1)
					else :
						self.calulateNormal(int(str_arr[1].split('/')[0])-1, int(str_arr[2].split('/')[0])-1, int(str_arr[4].split('/')[0])-1)
						self.calulateNormal(int(str_arr[2].split('/')[0])-1, int(str_arr[3].split('/')[0])-1, int(str_arr[4].split('/')[0])-1)	
		#print "len of triangle array : ", len(self.disp_tri_array)
		#print disp_quad_array
		#print len(self.disp_tex_array)
		#print len(self.disp_norm_array)

	def getCentroidX(self):
		return self.cx

	def getCentroidY(self):
		return self.cy

	def getCentroidZ(self):
		return self.cz		

	def getTriangles(self):
		return self.disp_tri_array

	def getQuads(self):
		return self.disp_quad_array

	def getTexCoords(self):
		return self.disp_tex_array

	def getNormal(self):
		return self.disp_norm_array

	def getRadius(self):	
		return math.sqrt((self.cx - self.disp_tri_array[0])*(self.cx - self.disp_tri_array[0]) 
			+(self.cy - self.disp_tri_array[1])*(self.cy - self.disp_tri_array[1]) + (self.cz - self.disp_tri_array[2])*(self.cz - self.disp_tri_array[2]))

	def minX(self):
		return self.minx

	def minY(self):
		return self.miny
		
	def minZ(self):
		return self.minz			

	def maxX(self):
		return self.maxx

	def maxY(self):
		return self.maxy

	def maxZ(self):
		return self.maxz		

	def draw(self):
		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_NORMAL_ARRAY)
		glEnableClientState( GL_TEXTURE_COORD_ARRAY )
		#glPolygonMode(GL_FRONT, GL_LINES)
		if (len(self.disp_tri_array) > 0) :
			glVertexPointer(3,GL_FLOAT,	0, self.disp_tri_array)
		else :
			glVertexPointer(3,GL_FLOAT,	0, self.disp_quad_array)
		glNormalPointer(GL_FLOAT, 0, self.disp_norm_array)
		glTexCoordPointer( 2 , GL_FLOAT, 0, self.disp_tex_array )
		if (len(self.disp_tri_array) > 0) :
			glDrawArrays(GL_TRIANGLES, 0, len(self.disp_tri_array)/3)
		else :	
			glDrawArrays(GL_QUADS, 0, len(self.disp_quad_array)/3)
		glDisableClientState(GL_VERTEX_ARRAY)
		glDisableClientState(GL_NORMAL_ARRAY)
		glDisableClientState(GL_TEXTURE_COORD_ARRAY)

