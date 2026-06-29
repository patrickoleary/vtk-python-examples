#!/usr/bin/env python

# Demonstrate vtkRandomAttributeGenerator on a HyperTreeGrid by generating
# random cell scalars and vectors on a random HTG source, and rendering
# the HTG surface colored by the random scalars.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersHyperTree import vtkHyperTreeGridGeometry
from vtkmodules.vtkFiltersSources import vtkRandomHyperTreeGridSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a random HyperTreeGrid source
htg_source = vtkRandomHyperTreeGridSource()
htg_source.SetSeed(42)
htg_source.SetMaxDepth(3)
htg_source.SetDimensions(3, 3, 3)
htg_source.SetSplitFraction(0.5)

# Generate random cell scalars and vectors
random_gen = vtkRandomAttributeGenerator()
random_gen.SetInputConnection(htg_source.GetOutputPort())
random_gen.SetDataTypeToUnsignedChar()
random_gen.SetComponentRange(0, 255)
random_gen.SetGenerateCellScalars(True)
random_gen.SetGenerateCellVectors(True)
random_gen.Update()

# Extract geometry from HTG for rendering
geometry = vtkHyperTreeGridGeometry()
geometry.SetInputConnection(random_gen.GetOutputPort())

# Render colored by random cell scalars
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("RandomCellScalars")
mapper.SetScalarRange(0, 255)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("random attribute generator htg")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Azimuth(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
