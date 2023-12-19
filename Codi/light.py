import glm


class Light:
    def __init__(self, position=(30, 30, 10), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        # intensities
        #sempre comneça de dia 
        
        #vaixell
        self.Ia = 0.2 * self.color  # ambient
        self.Id = 0.3 * self.color  # diffuse
        self.Is = 0.5 * self.color  # specular
        
        
        #mar
        self.Ia_mar = 0.2 * self.color  # ambient
        self.Id_mar = 0.3 * self.color  # diffuse
        self.Is_mar = 0.5 * self.color  # specular
        self.sea_light_intensity =1.65
        
    def nit_mode(self):
        #nit
        self.Ia = 0.0000006 * self.color  # ambient
        self.Id = 0.1 * self.color  # diffuse
        self.Is = 0.5 * self.color  # specular
        self.Ia_mar = 0.2 * self.color  # ambient
        self.Id_mar = 0.3 * self.color  # diffuse
        self.Is_mar = 0.5 * self.color  # specular
        self.sea_light_intensity=0.3
    
        
    def dia_mode(self):
        # dia
        self.Ia = 0.2 * self.color  # ambient
        self.Id = 0.3 * self.color  # diffuse
        self.Is = 0.5 * self.color  # specular
        
        self.Ia_mar = 0.2 * self.color  # ambient
        self.Id_mar = 0.3 * self.color  # diffuse
        self.Is_mar = 0.5 * self.color  # specular
        self.sea_light_intensity=1.65
        
        
    def dia2_mode(self):
        self.Ia = 0.0001 * self.color  # ambient
        self.Id = 0.2 * self.color  # diffuse
        self.Is = 0.5 * self.color  # specular
        self.Ia_mar = 0.2 * self.color  # ambient
        self.Id_mar = 0.3 * self.color  # diffuse
        self.Is_mar = 0.5 * self.color  # specular
        self.sea_light_intensity=1.0
        
        
    def dia3_mode(self):
        self.Ia = 0.0000005 * self.color  # ambient
        self.Id = 0.105 * self.color  # diffuse
        self.Is = 0.5 * self.color  # specular
        self.Ia_mar = 0.2 * self.color  # ambient
        self.Id_mar = 0.3 * self.color  # diffuse
        self.Is_mar = 0.5 * self.color  # specular
        self.sea_light_intensity=0.5
        
    def get_light_properties(self):
        return {
            'Ia': self.Ia,
            'Id': self.Id,
            'Is': self.Is,
            'sea_light_intensity':self.sea_light_intensity,
            'Ia_mar':self.Ia_mar,
            'Id_mar':self.Id_mar,
            'Is_mar':self.Ia_mar
            
        }
    
    