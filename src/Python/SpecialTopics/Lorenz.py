#!/usr/bin/env python

# Iso-surface of the Lorenz strange attractor computed by voxel visit counts.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkShortArray,
)
from vtkmodules.vtkCommonDataModel import vtkStructuredPoints
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dodger_blue_rgb = (0.118, 0.565, 1.0)
pale_goldenrod_rgb = (0.933, 0.910, 0.667)

# Lorenz system parameters
Pr = 10.0
b = 2.667
r = 28.0
h = 0.01
resolution = 200
iterations = 5000000
xmin, xmax = -30.0, 30.0
ymin, ymax = -30.0, 30.0
zmin, zmax = -10.0, 60.0

x_incr = resolution / (xmax - xmin)
y_incr = resolution / (ymax - ymin)
z_incr = resolution / (zmax - zmin)

# Random starting point
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(8775070)
x = rng.GetRangeValue(xmin, xmax)
rng.Next()
y = rng.GetRangeValue(ymin, ymax)
rng.Next()
z = rng.GetRangeValue(zmin, zmax)
rng.Next()

# Integrate the Lorenz equations, counting voxel visits
slice_size = resolution * resolution
num_pts = slice_size * resolution
scalars = vtkShortArray()
for i in range(num_pts):
    scalars.InsertTuple1(i, 0)

for _j in range(iterations):
    xx = x + h * Pr * (y - x)
    yy = y + h * (x * (r - z) - y)
    zz = z + h * (x * y - b * z)
    x, y, z = xx, yy, zz
    if xmin < x < xmax and ymin < y < ymax and zmin < z < zmax:
        ix = int((xx - xmin) * x_incr)
        iy = int((yy - ymin) * y_incr)
        iz = int((zz - zmin) * z_incr)
        idx = ix + iy * resolution + iz * slice_size
        scalars.SetTuple1(idx, scalars.GetTuple1(idx) + 1)

# StructuredPoints: voxel grid holding visit counts
volume = vtkStructuredPoints()
volume.GetPointData().SetScalars(scalars)
volume.SetDimensions(resolution, resolution, resolution)
volume.SetOrigin(xmin, ymin, zmin)
volume.SetSpacing(
    (xmax - xmin) / resolution,
    (ymax - ymin) / resolution,
    (zmax - zmin) / resolution,
)

# ContourFilter: extract iso-surface at visit count = 50
contour = vtkContourFilter()
contour.SetInputData(volume)
contour.SetValue(0, 50)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(contour.GetOutputPort())
mapper.ScalarVisibilityOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(dodger_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(pale_goldenrod_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("Lorenz")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

render_window.Render()

camera = renderer.GetActiveCamera()
camera.SetPosition(-67.645167, -25.714343, 63.483516)
camera.SetFocalPoint(3.224902, -4.398594, 29.552112)
camera.SetViewUp(-0.232264, 0.965078, 0.121151)
camera.SetDistance(81.414176)
camera.SetClippingRange(18.428905, 160.896031)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
