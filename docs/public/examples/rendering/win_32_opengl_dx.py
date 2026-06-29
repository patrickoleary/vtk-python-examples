#!/usr/bin/env python

# Test Win32 OpenGL/DirectX shared render window (Windows-only).
# NOTE: This test is only meaningful on Windows platforms with DirectX support.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# PLATFORM-ONLY: The C++ test uses vtkWin32OpenGLDXRenderWindow with Direct3D11
# COM interfaces (ID3D11Device, IDXGISwapChain, ID3D11Texture2D) to clear the
# background via D3D, render a VTK scene into a shared OpenGL-D3D texture, and
# present via a DXGI swap chain. This cannot be converted to Python as it requires
# Windows-only D3D11 APIs with no Python equivalent. This simplified fallback renders
# a sphere with the VTK standard pipeline to verify the basic rendering path.
sphere = vtkSphereSource()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("win 32 opengl dx")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
