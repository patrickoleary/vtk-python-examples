#!/usr/bin/env python

# Extract isosurfaces from a wavelet dataset using FlyingEdges3D.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkFlyingEdges3D
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: wavelet dataset
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-63, 64, -63, 64, -63, 64)
wavelet.SetCenter(0.0, 0.0, 0.0)
wavelet.Update()

# Filter: extract multiple isosurfaces
flying_edges = vtkFlyingEdges3D()
flying_edges.SetInputConnection(wavelet.GetOutputPort())
flying_edges.GenerateValues(6, 128.0, 225.0)
flying_edges.ComputeNormalsOn()
flying_edges.ComputeGradientsOn()
flying_edges.ComputeScalarsOn()
flying_edges.SetArrayComponent(0)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(flying_edges.GetOutputPort())
mapper.SetScalarRange(128, 225)

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(399, 401)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("flying edges")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
