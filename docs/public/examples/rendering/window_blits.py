#!/usr/bin/env python

# Demonstrate framebuffer blit operations using VTK FBO and PyOpenGL with a PLY model.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import VTK_UNSIGNED_CHAR
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkOpenGLFramebufferObject,
    vtkOpenGLRenderWindow,
)

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_NEAREST,
    GL_TRUE,
    glClear,
    glClearColor,
    glClearDepth,
    glColorMask,
    glDepthMask,
    glScissor,
)

# Data path
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Dragon PLY model
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetAmbientColor(0.2, 0.2, 1.0)
actor.GetProperty().SetDiffuseColor(1.0, 0.65, 0.7)
actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
actor.GetProperty().SetSpecular(0.5)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetAmbient(0.5)
actor.GetProperty().SetSpecularPower(20.0)
actor.GetProperty().SetOpacity(1.0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetMultiSamples(8)
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("window blits")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()

# Pipeline exception: must render once to create the OpenGL context
render_window.Render()

ogl_ren_win = vtkOpenGLRenderWindow.SafeDownCast(render_window)

# Create the start-render FBO (full size, for left/right half color+depth injection)
start_fbo = vtkOpenGLFramebufferObject()
start_fbo.SetContext(ogl_ren_win)
ogl_ren_win.GetState().PushFramebufferBindings()
size = render_window.GetSize()
start_fbo.PopulateFramebuffer(
    size[0], size[1],
    True,               # textures
    1, VTK_UNSIGNED_CHAR,  # 1 color buffer uchar
    True, 32,           # depth buffer
    0, render_window.GetStencilCapable() != 0)
ogl_ren_win.GetState().PopFramebufferBindings()

# Create the end-render FBO (quarter size, for picture-in-picture)
end_fbo = vtkOpenGLFramebufferObject()
end_fbo.SetContext(ogl_ren_win)
ogl_ren_win.GetState().PushFramebufferBindings()
end_fbo.PopulateFramebuffer(
    size[0] // 4, size[1] // 4,
    True,
    1, VTK_UNSIGNED_CHAR,
    True, 32,
    0, render_window.GetStencilCapable() != 0)
ogl_ren_win.GetState().PopFramebufferBindings()

def start_render_callback(caller, event):
    """Before render: inject colored halves with depth clipping into the render FBO."""
    sz = render_window.GetSize()
    start_fbo.Resize(sz[0], sz[1])

    ostate = ogl_ren_win.GetState()
    ostate.PushFramebufferBindings()
    start_fbo.Bind()
    start_fbo.ActivateDrawBuffer(0)

    # Left half — green with depth 0.7 (clips some geometry)
    glScissor(0, 0, sz[0] // 2, sz[1])
    glClearColor(0.1, 0.3, 0.2, 1.0)
    glClearDepth(0.7)
    glDepthMask(GL_TRUE)
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glScissor(0, 0, sz[0], sz[1])

    start_fbo.ActivateReadBuffer(0)
    start_fbo.DeactivateDrawBuffers()

    ogl_ren_win.BlitToRenderFramebuffer(
        0, 0, sz[0] // 2, sz[1],
        0, 0, sz[0] // 2, sz[1],
        GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT, GL_NEAREST)

    start_fbo.ActivateDrawBuffer(0)

    # Right half — blue with depth 1.0
    glScissor(sz[0] // 2, 0, sz[0] // 2, sz[1])
    glClearColor(0.1, 0.2, 0.4, 1.0)
    glClearDepth(1.0)
    glDepthMask(GL_TRUE)
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glScissor(0, 0, sz[0], sz[1])

    start_fbo.ActivateReadBuffer(0)
    start_fbo.DeactivateDrawBuffers()

    ogl_ren_win.BlitToRenderFramebuffer(
        sz[0] // 2, 0, sz[0] // 2, sz[1],
        sz[0] // 2, 0, sz[0] // 2, sz[1],
        GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT, GL_NEAREST)

    ostate.PopFramebufferBindings()

def end_render_callback(caller, event):
    """After render: copy center of frame to lower-left corner (picture-in-picture)."""
    sz = render_window.GetSize()
    qsz = [sz[0] // 4, sz[1] // 4]
    end_fbo.Resize(qsz[0], qsz[1])

    ostate = ogl_ren_win.GetState()
    ostate.PushFramebufferBindings()
    end_fbo.Bind()
    end_fbo.ActivateDrawBuffer(0)

    # Copy the center of the display framebuffer into the quarter-size FBO
    ogl_ren_win.BlitDisplayFramebuffer(
        0,
        qsz[0], qsz[1],
        sz[0] // 2, sz[1] // 2,
        0, 0, qsz[0], qsz[1],
        GL_COLOR_BUFFER_BIT, GL_NEAREST)

    end_fbo.DeactivateDrawBuffers()
    end_fbo.ActivateReadBuffer(0)

    # Blit into lower-left corner of the render framebuffer
    ogl_ren_win.BlitToRenderFramebuffer(
        0, 0, qsz[0], qsz[1],
        0, 0, qsz[0], qsz[1],
        GL_COLOR_BUFFER_BIT, GL_NEAREST)

    ostate.PopFramebufferBindings()

# Attach observers
render_window.AddObserver("StartEvent", start_render_callback)
render_window.AddObserver("RenderEvent", end_render_callback)

# Render multiple camera angles with preserved buffers
renderer.GetActiveCamera().Azimuth(80)
renderer.ResetCameraClippingRange()
render_window.Render()

renderer.PreserveColorBufferOn()
renderer.PreserveDepthBufferOn()

renderer.GetActiveCamera().Azimuth(-20)
renderer.ResetCameraClippingRange()
render_window.Render()

renderer.GetActiveCamera().Azimuth(-20)
renderer.ResetCameraClippingRange()
render_window.Render()

interactor.Initialize()
interactor.Start()
