#!/usr/bin/env python

# Warp a plane by random scalar values using vtkWarpScalar and
# visualize the deformed surface.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkMath,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a plane
res = 100
plane = vtkPlaneSource()
plane.SetResolution(res, res)
plane.Update()

output = plane.GetOutput()

# Assign random scalars
vtk_math = vtkMath()
vtk_math.RandomSeed(42)
n_pts = output.GetNumberOfPoints()
scalars = vtkDoubleArray()
scalars.SetNumberOfComponents(1)
scalars.SetNumberOfTuples(n_pts)

for i in range(n_pts):
    scalars.SetTuple1(i, vtk_math.Random(0, 10))

output.GetPointData().SetScalars(scalars)

# Warp the plane by scalar values
warp = vtkWarpScalar()
warp.SetInputData(output)
warp.SetScaleFactor(2.5)
warp.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(warp.GetOutputPort())
mapper.SetScalarRange(scalars.GetRange())

actor = vtkActor()
actor.SetMapper(mapper)

# Also show the original plane as wireframe
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputData(output)
original_mapper.ScalarVisibilityOff()

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetRepresentationToWireframe()
original_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
original_actor.GetProperty().SetOpacity(0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(original_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("warp scalar")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
