from model import *
import glm
import random

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.boyas_i = []
        self.boyas_f = []
        self.pos_boyas = []
        self.puntuacio = 0.0
        self.in_cami = False
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)

        self.timer_started = False
        self.start_time = 0.0
        self.c = 0
        self.elapsed_time = 0.0
        
    

    def add_object(self, obj):
        self.objects.append(obj)
    
    def check_collisions(self,pos_boat):
        new_pos = glm.vec3(int(pos_boat[0]),int(pos_boat[1]),int(pos_boat[2]))
        # print("barco:",new_pos)
        # print("lista:",self.pos_boyas)
        mas = (self.pos_boyas[0]+max(self.pos_boyas))/2
        mis = (self.pos_boyas[1]+min(self.pos_boyas))/2
        if new_pos[0]>mas or new_pos[0]<mis:
            self.puntuacio-=0.1
    
    def load(self):
        app = self.app
        add = self.add_object

        n, s = 30, 3
        add(Sea(app,pos=(-10,0,-10)))
        add(Boat(app, pos=(0, 0.5, -10)))
        cami = self.cami()

        for i in cami:
            x_primera, z_primera = i[0],i[1]
            add(Boya(app, pos=(x_primera+3, 2, 2*(z_primera-10)*5)))
            self.pos_boyas.append(x_primera+3)
            add(Boya(app, pos=(x_primera-13, 2, 2*(z_primera-10)*5)))
            self.pos_boyas.append(x_primera-13)
        self.boyas_i = self.objects[2:4]
        self.boyas_f = self.objects[-2:]
        self.puntuacio = len(self.pos_boyas)

    def cami(self,width=40, height=40):
        width = width-1
        matrix = [[0] * width for _ in range(height)]
        x, y = int(width/2), int((height-25)/2)
        matrix[y][x] = 1
        long_cami = random.randint(height/2, height - 2)
        directions = [(-3, 0), (-3, -3), (-3, 3), (3, 0), (3, -3), (3, 3)]
        c = 1 
        positions = [(x,y)]
        while c<long_cami:
            for i in range(long_cami):
                dx, dy = random.choice(directions)

                x += dx
                y -= 1

                if 2 <= x < width-1 and 1 <= y:
                    matrix[y][x] = 1

                elif x<width-1:
                    x = 2
                elif 2<=x:
                    x = width-2
                matrix[y][x] = 1
                c+=1
                positions.append((x,y))


        return positions


    def render(self, light_properties):
    
        self.app.texture.textures['skybox'].use(location=0)

        for obj in self.objects:
             obj.render(light_properties)
        
       
        self.skybox.render()
        if not self.timer_started and self.check_passed_buoys():
            self.in_cami = True
            self.timer_started = True
            self.start_time = pg.time.get_ticks() / 1000.0

        # Check if the boat has passed the last two buoys
        if self.timer_started and self.check_passed_last_buoys() and self.c == 0:
            self.elapsed_time = pg.time.get_ticks() / 1000.0 - self.start_time
            self.c=1
            self.in_cami = False
        if self.in_cami:
            self.check_collisions(self.objects[1].pos)
    def check_passed_buoys(self):
        boat_pos = self.objects[1].pos
        # print("bota_i ",self.boyas_i)
        buoy1 = self.boyas_i[0]
        buoy2 = self.boyas_i[1]
        if buoy2.pos[0] < boat_pos[0] < buoy1.pos[0] and buoy2.pos[2] > boat_pos[2]:
            return True
        else:
            return False

    def check_passed_last_buoys(self):
        boat_pos = self.objects[1].pos
        buoy1 = self.boyas_f[0]
        buoy2 = self.boyas_f[1]
        if buoy2.pos[0] < boat_pos[0] < buoy1.pos[0] and buoy2.pos[2] > boat_pos[2]:
            return True
        else:
            return False