#!/usr/bin/env python

# Dice a sphere into pieces using vtkOBBDicer, which partitions the
# mesh along oriented bounding box splits. Each piece is colored
# differently using the piece index scalar.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkOBBDicer
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: generate a high-resolution sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(40)
sphere.SetPhiResolution(40)

# OBBDicer: split the sphere into approximately 10 pieces
dicer = vtkOBBDicer()
dicer.SetInputConnection(sphere.GetOutputPort())
dicer.SetNumberOfPieces(10)
dicer.SetDiceModeToSpecifiedNumberOfPieces()
dicer.Update()

# Mapper: color each piece by its scalar index
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(dicer.GetOutputPort())
mapper.SetScalarRange(0, dicer.GetNumberOfActualPieces() - 1)

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("OBBDicer")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
