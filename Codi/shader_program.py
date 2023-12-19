

class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')
        self.programs['skybox'] = self.get_program('skybox')
        self.programs['advanced_skybox'] = self.get_program('advanced_skybox')
        self.programs['sea']=self.get_sea_program('sea')
    
    def get_sea_program(self,name):
        vertex_shader='''
                #version 330
                layout (location = 0) in vec3 in_position;
                out vec3 fragPos;
                out vec3 Normal;
                uniform mat4 m_proj;
                uniform mat4 m_view;
                uniform mat4 m_model;
                uniform float time;
                float D = 0.9999;
                vec3 a,b;
                float f[]={3,6,9,12,15,18,21};
                float j[]={1.2,2.0,1.8,4.0,3.0,5.0,7.0};
                int seed = 1;
                float lista[7];

                
                float my_rand() {
                    seed = (seed * 1103515245+ 12849689) & 0x7FFFFFFF;
                    return  float (seed / 0x7FFFFFFF +0.1);
                }
                
                
                
                void main() {
                    
                    
                    for (int i = 0; i < 7; ++i) {
                        lista[i] = my_rand();
                    }
                    
                    float offsetY=0.0;
                    float offsetYX=0.0;
                    float offsetYZ=0.0;
                    
                    for (int i = 0; i < 4; ++i) {
                        offsetY+=sin((in_position.x +lista[i]) * f[i] + time) * j[i];
                    }
                    
                    for (int i = 4; i < 7; ++i) {
                    offsetY+=sin((in_position.z + lista[i]) * f[i] + time) * j[i];
                    }
                
                    offsetY/=5.0;
                    
                    
                for (int i = 0; i < 4; ++i) {
                        offsetYX+= sin((in_position.x+D ) *my_rand()+ time) *j[i];
                    }
                    
                    for (int i = 4; i < 7; ++i) {
                    offsetYX+=sin((in_position.z)* my_rand()+ time) * j[i];
                    }
                
                    offsetYX/=5.0;
                    
                
                    for (int i = 0; i < 4; ++i) {
                        offsetYZ+= sin((in_position.x)* my_rand() + time) * j[i];
                    }
                    
                    for (int i = 4; i < 7; ++i) {
                    offsetYZ+=sin((in_position.z+D) * my_rand()+ time) *j[i];
                    }
                
                    offsetYZ/=5.0;
                
                    a = vec3(D,offsetYX,0)-vec3(0,offsetY,0);
                    b = vec3(0,offsetYZ,D)-vec3(0,offsetY,0);
                    Normal = vec3(a.y*b.z-a.z*b.y, a.z*b.x-a.x*b.z, a.x*b.y-a.y*b.x);
            
                    gl_Position = m_proj * m_view * m_model *  vec4(in_position.x, offsetY-0.9, in_position.z, 1.0);
                    
                    
                }
            '''
        fragment_shader='''
                #version 330
                layout (location = 0) out vec4 fragColor;
                in vec3 fragPos;
                in vec3 Normal;
                struct Light{
                    vec3 position;
                    vec3 Ia;
                    vec3 Id;
                    vec3 Is;
                    vec3 Ia_mar;
                    vec3 Id_mar;
                    vec3 Is_mar;
                    float sea_light_intensity;
                    
                    };
                uniform Light light;
                uniform vec3 camPos;
                vec3 nNormal;
               
                
                vec3 getLight(vec3 color){
                    nNormal = normalize(Normal);
                    
                    // ambient light
                    vec3 ambient = light.Ia_mar;
                    
                    // diffuse light
                    vec3 lightDir = normalize(light.position - fragPos);
                    float diff = max(0, dot(lightDir,nNormal));
                    vec3 diffuse = diff * light.Id_mar;
                    
                    // specular light
                    vec3 viewDir = normalize(camPos-fragPos);
                    vec3 reflectDir = reflect(-lightDir, nNormal);
                    float spec = pow(max(dot(viewDir,reflectDir),0),32);
                    vec3 specular = spec*light.Is_mar;
               
                    
                    return color*(ambient +diffuse+specular);
                    }
                void main() { 
                  
                    vec3 color = vec3(0.5, 1.2, 1.9);  

                    color = getLight(color) ; 
                    color *= light.sea_light_intensity;;
                    fragColor = vec4(color,1.0);
                }
            '''
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
    
    
    def get_program(self, shader_program_name):
        with open(f'shaders/{shader_program_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_program_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        [program.release() for program in self.programs.values()]
