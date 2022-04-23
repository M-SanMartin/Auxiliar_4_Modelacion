# coding=utf-8

# Importamos librerias
import glfw
from OpenGL.GL import *
import sys
import os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.transformations as tr


# Acepta eventos
class Controller:
    pass


# Creamos un objeto global de controlador
controller = Controller()


# noinspection PyShadowingNames,PyUnusedLocal
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    else:
        print('Unknown key')


if __name__ == "__main__":

    # Inicializa glfw
    if not glfw.init():
        # noinspection PyUnresolvedReferences,PyUnboundLocalVariable
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, 'TPOSE Modelo', None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Conectamos la función on_key para que lea entradas del teclado
    glfw.set_key_callback(window, on_key)

    # Creamos un shader
    pipeline = es.SimpleTransformShaderProgram()
    glUseProgram(pipeline.shaderProgram)

    # Borramos la pantalla
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Al estar en 3D, activamos la profundidad
    glEnable(GL_DEPTH_TEST)

    """
    Creamos las figuras
    """
    tpose_cabeza_gpu = es.GPUShape().initBuffers()
    tpose_cabeza_shape = bs.createColorCube(1, 1, 0)
    tpose_cabeza_tr = tr.matmul([tr.translate(0, 0.7, 0), tr.scale(0.5, 0.5, 1)])
    pipeline.setupVAO(tpose_cabeza_gpu)
    tpose_cabeza_gpu.fillBuffers(tpose_cabeza_shape.vertices, tpose_cabeza_shape.indices, GL_STATIC_DRAW)

    tpose_cuello_gpu = es.GPUShape().initBuffers()
    tpose_cuello_shape = bs.createColorCube(1, 1, 0)
    tpose_cuello_tr = tr.matmul([tr.translate(0, 0.5, 0), tr.scale(0.2, 0.4, 1)])
    pipeline.setupVAO(tpose_cuello_gpu)
    tpose_cuello_gpu.fillBuffers(tpose_cuello_shape.vertices, tpose_cuello_shape.indices, GL_STATIC_DRAW)

    while not glfw.window_should_close(window):
        # Iteramos eventos
        glfw.poll_events()

        # Borramos la pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujamos tpose
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'transform'), 1, GL_TRUE, tpose_cabeza_tr)
        pipeline.drawCall(tpose_cabeza_gpu)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, 'transform'), 1, GL_TRUE, tpose_cuello_tr)
        pipeline.drawCall(tpose_cuello_gpu)

        # Intercambiamos buffer
        glfw.swap_buffers(window)

    # Borramos memoria y terminamos
    tpose_cabeza_gpu.clear()
    tpose_cuello_gpu.clear()

    glfw.terminate()
