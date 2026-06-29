#!/usr/bin/env python

# Demonstrate vtkMergeArrays by merging point data arrays from multiple
# cube sources into a single output, and rendering the result colored
# by the merged normals.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkMergeArrays
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a cube with normals and tcoords
cube = vtkCubeSource()
cube.Update()

# Merge arrays from the same cube three times (testing suffix handling)
merge = vtkMergeArrays()
merge.AddInputData(cube.GetOutput())
merge.AddInputData(cube.GetOutput())
merge.AddInputData(cube.GetOutput())
merge.Update()

# Render the merged output
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(merge.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0.4, 0.7, 0.3)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("merge arrays")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
