from vbo import VBO
from shader_program import ShaderProgram




class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # # cube vao
        # self.vaos['cube'] = self.get_vao(
        #     program=self.program.programs['default'],
        #     vbo = self.vbo.vbos['cube'])

        # cat vao
        self.vaos['boat'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['boat'])

        # skybox vao
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        # advanced_skybox vao
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])
        
        self.vaos['sea'] = self.get_vao(
            program=self.program.programs['sea'],
            vbo=self.vbo.vbos['sea'])
        
        self.vaos['boya'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['boya'])


    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()