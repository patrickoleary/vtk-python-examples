#!/usr/bin/env python

# Test vtkCheckerboardSplatter on random 3D points with marching contour surface.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkMarchingContourFilter
from vtkmodules.vtkImagingHybrid import vtkCheckerboardSplatter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Splat random points into a cube
vtk_math = vtkMath()
points = vtkPoints()
for i in range(100000):
    points.InsertPoint(i, vtk_math.Random(0, 1), vtk_math.Random(0, 1), vtk_math.Random(0, 1))

profile = vtkPolyData()
profile.SetPoints(points)

# Checkerboard splatter
cbd_splatter = vtkCheckerboardSplatter()
cbd_splatter.SetInputData(profile)
cbd_splatter.SetSampleDimensions(100, 100, 100)
cbd_splatter.ScalarWarpingOff()
cbd_splatter.SetFootprint(2)
cbd_splatter.SetParallelSplatCrossover(2)

# Extract isosurface
cbd_surface = vtkMarchingContourFilter()
cbd_surface.SetInputConnection(cbd_splatter.GetOutputPort())
cbd_surface.SetValue(0, 0.01)

cbd_mapper = vtkPolyDataMapper()
cbd_mapper.SetInputConnection(cbd_surface.GetOutputPort())
cbd_mapper.ScalarVisibilityOff()

cbd_actor = vtkActor()
cbd_actor.SetMapper(cbd_mapper)
cbd_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Rendering
renderer = vtkRenderer()
renderer.AddActor(cbd_actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("checkerboard splatter")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 1, 1)
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
