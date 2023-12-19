import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from scene import Scene
from texture import Texture
import os
import numpy as np
import time
from prettytable import PrettyTable

from model import Boat
class GraphicsEngine:
    def __init__(self, win_size=(900, 900)):
        # init pygame modules
        pg.init()
        pg.mixer.init()
        path = os.getcwd()
        path = path.replace("\\", "/")
        path+="/audio2.mp3"
        pg.mixer.music.load(path)
        pg.mixer.music.play(-1)

        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        # self.ctx.front_face = 'cw'mww
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # create an object to help track time
        self.tiempo_inicio = time.time()
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.count = 0
        # light
        self.light = Light()
        # camera
        self.camera = Camera(self)
        
       
        # scene
        
        #skybox
        self.texture = Texture(self)
        self.scene = Scene(self)

        self.count_audio = 0
        
        

    def check_events(self):
        
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                vels = self.scene.objects[1].velocities
                if len(vels)==0:
                    vels.append(0.0)
                average_velocity = np.average(vels)
                min_velocity = min(vels) 
                max_velocity = max(vels) 
                temps_cursa = self.scene.elapsed_time
                temps_final= time.time()
                temps_total= temps_final- self.tiempo_inicio
                puntuacio = (self.scene.puntuacio/len(self.scene.pos_boyas))*100
                print(" \n        Resumen del Videojuego")
                table = PrettyTable()
                table.field_names = ["Métricas", "Valores"]
                table.add_row(["Velocidad media", f"{average_velocity:.2f} km/h"])
                table.add_row(["Velocidad mínima", f"{min_velocity:.2f} km/h"])
                table.add_row(["Velocidad máxima", f"{max_velocity:.2f} km/h"])
                table.add_row(["Tiempo de ejecución", f"{temps_total:.2f} segundos"])
                table.add_row(["Tiempo de carrera", f"{temps_cursa:.2f} segundos"])
                table.add_row(["Puntuación", f"{puntuacio:.2f} puntos"])
                
                # Imprimeix la taula
                print(table)
                self.texture.destroy()
                # pg.mixer.music.stop()
                pg.quit()
                sys.exit()
            elif event.type==pg.KEYDOWN and event.key == pg.K_4:  
                
                if self.count == 0:
                    self.light.dia_mode()
                    # self.scene.objects[0].sea_light_intensity = 3
                    self.count = (self.count+1)%4
                if self.count ==1:
                    self.texture.textures['skybox'] =  self.texture.get_texture_cube(dir_path='textures/dia2/', ext='png')
                    self.light.dia2_mode()
                    # self.scene.objects[0].sea_light_intensity = 0.6
                    self.count = (self.count+1)%4
                elif self.count ==2:
                    self.texture.textures['skybox'] =  self.texture.get_texture_cube(dir_path='textures/dia3/', ext='png')
                    self.light.dia3_mode()
                    # self.scene.objects[0].sea_light_intensity = 0.7
                    self.count = (self.count+1)%4
                elif self.count ==3:
                    self.texture.textures['skybox'] =  self.texture.get_texture_cube(dir_path='textures/dia4/', ext='png')
                    self.light.nit_mode()
                    # self.scene.objects[0].sea_light_intensity = 0.8 
                

            elif event.type==pg.KEYDOWN and event.key == pg.K_1:
              
                if self.count == 0:
                    self.light.dia_mode()
                    # self.scene.objects[0].sea_light_intensity = 3
                    self.texture.textures['skybox'] =  self.texture.get_texture_cube(dir_path='textures/dia1/', ext='png')
                elif self.count ==1:
                    self.light.dia2_mode()
                    # self.scene.objects[0].sea_light_intensity = 0.4
                    self.texture.textures['skybox'] =  self.texture.get_texture_cube(dir_path='textures/dia2/', ext='png')
                    self.count = (self.count-1)%4
                elif self.count ==2:
                    self.texture.textures['skybox'] =  self.texture.get_texture_cube(dir_path='textures/dia3/', ext='png')
                    self.light.dia3_mode()
                    # self.scene.objects[0].sea_light_intensity = 0.3
                    self.count = (self.count-1)%4
                elif self.count ==3:
                    self.texture.textures['skybox'] =  self.texture.get_texture_cube(dir_path='textures/dia4/', ext='png')
                    self.light.nit_mode()
                    # self.scene.objects[0].sea_light_intensity = 0.2
                    self.count = (self.count-1)%4
            
            elif event.type==pg.KEYDOWN and event.key == pg.K_m: 
                if self.count_audio==0:
                    pg.mixer.music.stop()
                    self.count_audio = (self.count_audio+1)%2
                else:
                    pg.mixer.music.play(-1)
                    self.count_audio = (self.count_audio+1)%2
                  
                
               

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        light_properties = self.light.get_light_properties()
        self.scene.render(light_properties)
        # swap buffers
        pg.display.flip()
        

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001 

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()




