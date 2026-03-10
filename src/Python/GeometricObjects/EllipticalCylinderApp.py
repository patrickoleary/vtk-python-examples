#!/usr/bin/env python

# Extrude an elliptical cross-section into a cylinder, showing the base
# polyline (as a tube), the extrusion vector (as an oriented arrow), and
# the semi-transparent extruded surface.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkPolyLine,
)
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
peacock_rgb = (0.2, 0.631, 0.788)
banana_rgb = (0.890, 0.812, 0.341)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Extrusion vector (controls cylinder direction and height)
nx = 0.0
ny = 0.0
nz = 100.0

# Data: generate elliptical cross-section points
r1 = 50
r2 = 30
center_x = 10.0
center_y = 5.0

points = vtkPoints()
angle = 0.0
idx = 0
while angle <= 2.0 * vtkMath.Pi() + (vtkMath.Pi() / 60.0):
    points.InsertNextPoint(
        r1 * math.cos(angle) + center_x,
        r2 * math.sin(angle) + center_y,
        0.0,
    )
    angle = angle + (vtkMath.Pi() / 60.0)
    idx += 1

# Polyline: connect the ellipse points into a closed loop
poly_line = vtkPolyLine()
poly_line.GetPointIds().SetNumberOfIds(idx)
for i in range(0, idx):
    poly_line.GetPointIds().SetId(i, i)

lines = vtkCellArray()
lines.InsertNextCell(poly_line)

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetLines(lines)

# Filter: extrude the elliptical cross-section
extrude = vtkLinearExtrusionFilter()
extrude.SetInputData(poly_data)
extrude.SetExtrusionTypeToNormalExtrusion()
extrude.SetVector(nx, ny, nz)
extrude.Update()

# Oriented arrow: compute start/end points for the extrusion vector
start_point = [center_x, center_y, 0.0]
end_point = [
    start_point[0] + extrude.GetVector()[0],
    start_point[1] + extrude.GetVector()[1],
    start_point[2] + extrude.GetVector()[2],
]

# Build an orthonormal basis so the arrow glyph (which points along +x by
# default) can be rotated to align with the extrusion vector.  The basis
# vectors (normalized_x, normalized_y, normalized_z) form a rotation matrix
# that is later combined with translation and scaling to produce the full
# arrow transform.
#
# Step 1 — X axis: the direction from start to end (the extrusion vector).
normalized_x = [0.0] * 3
normalized_y = [0.0] * 3
normalized_z = [0.0] * 3

vtkMath.Subtract(end_point, start_point, normalized_x)
length = vtkMath.Norm(normalized_x)
vtkMath.Normalize(normalized_x)

# Step 2 — Z axis: pick a random vector that is not parallel to X, then
# compute Z = X × arbitrary.  A seeded random sequence guarantees the same
# "arbitrary" vector on every run, avoiding the degenerate case where the
# arbitrary vector is parallel to X.
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(8775070)
max_r = 10.0

arbitrary = [0.0] * 3
arbitrary[0] = rng.GetRangeValue(-max_r, max_r)
rng.Next()
arbitrary[1] = rng.GetRangeValue(-max_r, max_r)
rng.Next()
arbitrary[2] = rng.GetRangeValue(-max_r, max_r)
rng.Next()

vtkMath.Cross(normalized_x, arbitrary, normalized_z)
vtkMath.Normalize(normalized_z)

# Step 3 — Y axis: complete the right-handed basis with Y = Z × X.
vtkMath.Cross(normalized_z, normalized_x, normalized_y)

# Direction cosine matrix
matrix = vtkMatrix4x4()
matrix.Identity()
matrix.SetElement(0, 0, normalized_x[0])
matrix.SetElement(1, 0, normalized_x[1])
matrix.SetElement(2, 0, normalized_x[2])
matrix.SetElement(0, 1, normalized_y[0])
matrix.SetElement(1, 1, normalized_y[1])
matrix.SetElement(2, 1, normalized_y[2])
matrix.SetElement(0, 2, normalized_z[0])
matrix.SetElement(1, 2, normalized_z[1])
matrix.SetElement(2, 2, normalized_z[2])

# Transform for the arrow
transform = vtkTransform()
transform.Translate(start_point)
transform.Concatenate(matrix)
transform.Scale(length, length, length)

# Source and filter: oriented arrow
arrow_source = vtkArrowSource()
arrow_source.SetTipResolution(31)
arrow_source.SetShaftResolution(21)

transform_pd = vtkTransformPolyDataFilter()
transform_pd.SetTransform(transform)
transform_pd.SetInputConnection(arrow_source.GetOutputPort())

# Mapper and actor: arrow
arrow_mapper = vtkPolyDataMapper()
arrow_mapper.SetInputConnection(transform_pd.GetOutputPort())

arrow_actor = vtkActor()
arrow_actor.SetMapper(arrow_mapper)
arrow_actor.GetProperty().SetColor(tomato_rgb)

# Filter, mapper, and actor: elliptical outline as a tube
tubes = vtkTubeFilter()
tubes.SetInputData(poly_data)
tubes.SetRadius(2.0)
tubes.SetNumberOfSides(21)

line_mapper = vtkPolyDataMapper()
line_mapper.SetInputConnection(tubes.GetOutputPort())

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.GetProperty().SetColor(peacock_rgb)

# Mapper and actor: extruded cylinder (semi-transparent)
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(extrude.GetOutputPort())

cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.GetProperty().SetColor(banana_rgb)
cylinder_actor.GetProperty().SetOpacity(0.7)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(slate_gray_background_rgb)
renderer.AddActor(cylinder_actor)
renderer.AddActor(line_actor)
renderer.AddActor(arrow_actor)

# Camera: position for a 3D view
camera = vtkCamera()
camera.SetPosition(0, 1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0, 0, 1)
camera.Azimuth(30)
camera.Elevation(30)

renderer.SetActiveCamera(camera)
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 600)
render_window.SetWindowName("EllipticalCylinderApp")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
