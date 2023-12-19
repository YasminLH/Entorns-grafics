import moderngl as mgl
import numpy as np
import glm
import pygame as pg
import vbo
import math
FOV = 100  # deg
NEAR = 0.1
FAR = 100
SPEED = 0.005
SENSITIVITY = 0.04

import struct

from pyquaternion import Quaternion
# Create a quaternion




class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.texture.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera


    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        
        m_model = glm.translate(m_model, (0,0,0))
        # rotate
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
 
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        # scale
        m_model = glm.scale(m_model, self.scale)
        # translate
        m_model = glm.translate(m_model, self.pos)
        return m_model

    def render(self):
        if self.tex_id == 'sea':
            self.time = pg.time.get_ticks() / 1000.0
            self.program['time'].value = self.time
        self.update()
        # if self.tex_id == 'sea':
            # self.vao.render(mgl.LINE_STRIP)
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self, light_properties):
        if self.tex_id != 'sea':
            self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)


     
        # # Actualizar propiedades de la luz
        self.program['light.position'].write(self.app.light.position)
        
    
    def on_init(self):
        # texture
        if self.tex_id != 'sea':
            self.texture = self.app.texture.textures[self.tex_id]
            self.program['u_texture_0'] = 0
            self.texture.use()
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        # self.program['light.Ia'].write(self.app.light.Ia)
        # self.program['light.Id'].write(self.app.light.Id)
        # self.program['light.Is'].write(self.app.light.Is)
       


    def render(self, light_properties):
        if self.tex_id == 'sea':
            self.time = pg.time.get_ticks() / 1000.0
            self.program['time'].value = self.time
        self.update(light_properties)
        # if self.tex_id == 'sea':
            # self.vao.render(mgl.LINE_STRIP)
        self.vao.render()



class Boat(ExtendedBaseModel):
    def __init__(self, app, vao_name='boat', tex_id='boat',
                 pos=(0, 0, 0), rot=(0,180, 10), scale=(0.4,0.4,0.4), yaw=-90, pitch=0, roll = 45):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.up = glm.vec3(0, 1, 0)
        #self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, 1) #glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        # view matrix
        self.m_view = self.get_view_matrix()
        self.left = True
        self.indice = rot[2]        
        self.velocity = 0.00
        
        #n
        self.position = glm.vec3(pos)
        
        self.rota = 0.0
        self.velocities = []

    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def get_position(self):
        return glm.vec3(self.pos)
    
    
    def get_rot_position(self):
        #print("rotation func: ", self.rota)
        return self.rota

    def update(self, light_properties):

        i = self.indice

        if i == 10:
            self.left = True
            i -= 0.125

        elif i == -10:
            self.left = False
            i += 0.125

        elif self.left == True and i < 10 and i > -10: 
            i -= 0.125

        elif self.left == False and i < 10 and i > -10:
            i += 0.125
        
        self.indice = i
        self.rot[2] = glm.radians(i)
        #self.rot[1] = glm.radians(180+i/2)

        #self.update_boat_vectors()
        self.move()
        self.velocities.append(self.velocity*24*3.6)
        #self.rotate()
        #self.update_boat_vectors()
        self.m_model = self.get_model_matrix()
        #self.update_model()
        self.program['m_model'].write(self.m_model)
        
        # # Actualizar propiedades de la luz
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(light_properties['Ia'])
        self.program['light.Id'].write(light_properties['Id'])
        self.program['light.Is'].write(light_properties['Is'])
      
    def update_model(self):
        m_model = self.m_model
        m_model = glm.translate(m_model, glm.vec3(0.0, 0.0, 0.0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        #self.move()
        m_model = glm.translate(m_model, self.pos)

    #    self.m_model = m_model

    def move(self):
        
        # velocity = SPEED * self.app.delta_time
        # print(velocity)
        keys = pg.key.get_pressed()
        # print("original value = " , glm.radians(180) , "actual value = ",  self.rot[1])
        if keys[pg.K_w]:
            self.velocity += 0.005
        if keys[pg.K_s]:
            self.velocity -= 0.005
       # self.velocity = glm.max(-0.05,glm.min(0.05,self.velocity))

        if keys[pg.K_a]:
            self.rot[1] += glm.radians(0.25)
            #self.pos +=  self.right *self.velocity #glm.radians(0.25)
            self.rota = self.rot[1]
            self.camera.update_rota(self.rota)

        if keys[pg.K_d]:
            #self.pos -=  self.right * self.velocity #glm.radians(0.25)
            self.rot[1] -= glm.radians(0.25)
            #n
            self.rota = self.rot[1]
            self.camera.update_rota(self.rota)


        forward = glm.vec3(glm.cos(-self.rot[1])*self.forward[0]-glm.sin(-self.rot[1])*self.forward[2],
                                0,glm.sin(-self.rot[1])*self.forward[0]+glm.cos(-self.rot[1])*self.forward[2])
        self.pos += forward * self.velocity

        #n
        self.camera.update_pos(self.pos)
        
        
    

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # scale
        m_model = glm.scale(m_model, self.scale)
        # rotate
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))

        return m_model
    
    def get_view_matrix(self):
        return glm.lookAt(self.pos, self.pos + self.forward, self.up)

class SkyBox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkyBox(BaseModel):
    def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        # texture
        self.texture = self.app.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        
class Sea(ExtendedBaseModel):
    def __init__(self, app, vao_name='sea', tex_id='sea',
                 pos=(-10, -10, -10), rot=(0, 0, 0), scale=(1.2, 0.7, 1.2)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        #self.on_init()    
         
 
    def on_init(self):
        super().on_init()
        sea_light_intensity_bytes = struct.pack('f', self.app.light.sea_light_intensity)
        
        # Write sea_light_intensity to the uniform buffer
        self.program['light.sea_light_intensity'].write(sea_light_intensity_bytes)
        self.program['light.Ia_mar'].write(self.app.light.Ia_mar)
        self.program['light.Id_mar'].write(self.app.light.Id_mar)
        self.program['light.Is_mar'].write(self.app.light.Is_mar)
       
    def update(self, light_properties):
        super().update(light_properties)
        sea_light_intensity_bytes = struct.pack('f', light_properties['sea_light_intensity'])

        # Write sea_light_intensity to the uniform buffer
        self.program['light.sea_light_intensity'].write(sea_light_intensity_bytes)
        self.program['light.Ia_mar'].write(light_properties['Ia_mar'])
        self.program['light.Id_mar'].write(light_properties['Id_mar'])
        self.program['light.Is_mar'].write(light_properties['Is_mar'])
        
        
        
    
        
   



class Boya(ExtendedBaseModel):
    def __init__(self, app, vao_name='boya', tex_id='boya',
                 pos=(0, 0, -10), rot=(0,1, -10), scale=(0.5,0.5,0.5), yaw=-90, pitch=0):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.left = True
        self.indice = rot[2]  

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # scale
        m_model = glm.scale(m_model, self.scale)
        # rotate
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))

        return m_model
    
    def update(self, light_properties):
        super().on_init()
        i = self.indice

        if i == 10:
            self.left = True
            i -= 0.125

        elif i == -10:
            self.left = False
            i += 0.125

        elif self.left == True and i < 10 and i > -10: 
            i -= 0.125

        elif self.left == False and i < 10 and i > -10:
            i += 0.125
        
        self.indice = i
        self.rot[2] = glm.radians(i)
        self.m_model = self.get_model_matrix()
        #self.update_model()
        self.program['m_model'].write(self.m_model)
        # # Actualizar propiedades de la luz
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(light_properties['Ia'])
        self.program['light.Id'].write(light_properties['Id'])
        self.program['light.Is'].write(light_properties['Is'])
      

    def on_init(self):
       
        super().on_init()
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
        















