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
import grafica.scene_graph as sg


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

    node_tpose_cuello = sg.SceneGraphNode('ojo')
    tpose_cuello_gpu = es.GPUShape().initBuffers()
    tpose_cuello_shape = bs.createColorCube(0.9, 1, 0.9)
    pipeline.setupVAO(tpose_cuello_gpu)
    tpose_cuello_gpu.fillBuffers(tpose_cuello_shape.vertices, tpose_cuello_shape.indices, GL_STATIC_DRAW)
    node_tpose_cuello.transform = tr.matmul([tr.translate(0.2, 0.2, 0), tr.scale(0.5, 0.3, 0.7)])
    node_tpose_cuello.childs += [tpose_cuello_gpu]

    node_tpose_cuerpo = sg.SceneGraphNode('cuerpo')
    tpose_cuerpo_gpu = es.GPUShape().initBuffers()
    tpose_cuerpo_shape = bs.createColorCube(0.9, 0.9, 0)
    pipeline.setupVAO(tpose_cuerpo_gpu)
    tpose_cuerpo_gpu.fillBuffers(tpose_cuerpo_shape.vertices, tpose_cuerpo_shape.indices, GL_STATIC_DRAW)
    node_tpose_cuerpo.transform = tr.matmul([tr.translate(0, -0.05, -0.), tr.scale(0.9, 0.8, 0.5)])
    node_tpose_cuerpo.childs += [tpose_cuerpo_gpu]


    node_tpose_pupil = sg.SceneGraphNode('pupil')
    tpose_brazos_gpu = es.GPUShape().initBuffers()
    tpose_brazos_shape = bs.createColorCube(0, 0, 0)
    pipeline.setupVAO(tpose_brazos_gpu)
    tpose_brazos_gpu.fillBuffers(tpose_brazos_shape.vertices, tpose_brazos_shape.indices, GL_STATIC_DRAW)
    node_tpose_pupil.transform = tr.matmul([tr.translate(0.3, 0.2, 0), tr.scale(0.1, 0.2, 1)])
    node_tpose_pupil.childs += [tpose_brazos_gpu]

    node_tpose_pierna_izq = sg.SceneGraphNode('ala')
    tpose_pierna_izq_gpu = es.GPUShape().initBuffers()
    tpose_pierna_izq_shape = bs.createColorCube(1, 1, 0)
    pipeline.setupVAO(tpose_pierna_izq_gpu)
    tpose_pierna_izq_gpu.fillBuffers(tpose_pierna_izq_shape.vertices, tpose_pierna_izq_shape.indices, GL_STATIC_DRAW)
    node_tpose_pierna_izq.transform = tr.matmul([tr.translate(-0.3, 0, 0), tr.scale(0.4, 0.4, 0.7)])
    node_tpose_pierna_izq.childs += [tpose_pierna_izq_gpu]

    node_tpose_pierna_der = sg.SceneGraphNode('Boca')
    tpose_pierna_der_gpu = es.GPUShape().initBuffers()
    tpose_pierna_der_shape = bs.createColorCube(1, 0.5, 0)
    pipeline.setupVAO(tpose_pierna_der_gpu)
    tpose_pierna_der_gpu.fillBuffers(tpose_pierna_der_shape.vertices, tpose_pierna_der_shape.indices, GL_STATIC_DRAW)
    node_tpose_pierna_der.transform = tr.matmul([tr.translate(0.3, -0.25, 0), tr.scale(0.5, 0.3, 0.7)])
    node_tpose_pierna_der.childs += [tpose_pierna_der_gpu]

    # Ensamblamos las piernas
    #node_piernas = sg.SceneGraphNode('piernas')
    #node_piernas.transform = tr.identity()
    #node_piernas.childs += [
     #   node_tpose_pierna_izq,
      #  node_tpose_pierna_der
    #]

    # Ensamblamos el cuerpo
    tpose = sg.SceneGraphNode('tpose')
    tpose.transform = tr.identity()
    tpose.childs += [
     
        node_tpose_cuello,
        node_tpose_cuerpo,
        node_tpose_pupil,
        node_tpose_pierna_der,
        node_tpose_pierna_izq
    ]

    # Almacenamos un ángulo para modificar tpose
    ang = 0

    while not glfw.window_should_close(window):
        # Iteramos eventos
        glfw.poll_events()

        # Borramos la pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Actualizamos la transformada de tpose
        ang += 0.0005
        #tpose.transform = tr.matmul([tr.rotationZ(ang)])

        # Dibujamos tpose
        sg.drawSceneGraphNode(tpose, pipeline, 'transform')

        # Intercambiamos buffer
        glfw.swap_buffers(window)

    # Borramos memoria y terminamos
    tpose.clear()
    glfw.terminate()
