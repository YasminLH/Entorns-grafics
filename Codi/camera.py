import glm
import pygame as pg
FOV = 100  # deg
NEAR = 0.1
FAR = 100
SPEED = 0.005
SENSITIVITY = 0.04

class Camera:
    def __init__(self, app, position=(0, 0, 0)):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.rota = 0.0
        self.velocity = 0.00
        
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()
        
    def update(self):
        self.m_view = self.get_view_matrix()
        
    #n
    def update_rota(self, new_rota):
        #actualizar la variable rota
        self.rota = new_rota
 
    def update_pos(self, new_pos):
        
        self.position = new_pos

    def get_view_matrix(self):
        #delta = glm.vec3(0, -14, -30)
        
        #funciona no tocar:
        #delta = -glm.vec3(0*glm.cos(-self.rota) + 30* glm.sin(-self.rota), 14, 0 * glm.sin(-self.rota) -30*glm.cos(-self.rota))
        
        delta = -glm.vec3(0*glm.cos(-self.rota) + 30 * glm.sin(-self.rota), 14, 0 * glm.sin(-self.rota) -30*glm.cos(-self.rota))

        return glm.lookAt(self.position - delta , self.position, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)




















