#!/usr/bin/env python

# Orient a cylinder between two random points, marking each endpoint with a
# sphere.  The cylinder (whose height vector is +y by default) is rotated,
# scaled, and translated using a user matrix built from an orthonormal basis.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkMinimalStandardRandomSequence,
)
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import (
    vtkCylinderSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cyan_rgb = (0.0, 1.0, 1.0)
yellow_rgb = (1.0, 1.0, 0.0)
magenta_rgb = (1.0, 0.0, 1.0)
background_rgb = (0.102, 0.2, 0.302)

# Source: create a cylinder (height vector is +y, centered at origin)
cylinder_source = vtkCylinderSource()
cylinder_source.SetResolution(15)

# Generate a random start and end point (seeded for reproducibility)
start_point = [0.0] * 3
end_point = [0.0] * 3
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(8775070)
for i in range(0, 3):
    rng.Next()
    start_point[i] = rng.GetRangeValue(-10, 10)
    rng.Next()
    end_point[i] = rng.GetRangeValue(-10, 10)

# Build an orthonormal basis so the cylinder can be rotated to span from
# start_point to end_point.  The basis vectors form a rotation matrix that
# is combined with additional transforms to handle the cylinder's +y default.
#
# Step 1 — X axis: the direction from start to end.
normalized_x = [0.0] * 3
normalized_y = [0.0] * 3
normalized_z = [0.0] * 3

vtkMath.Subtract(end_point, start_point, normalized_x)
length = vtkMath.Norm(normalized_x)
vtkMath.Normalize(normalized_x)

# Step 2 — Z axis: pick a random vector not parallel to X, compute Z = X × arbitrary.
arbitrary = [0.0] * 3
for i in range(0, 3):
    rng.Next()
    arbitrary[i] = rng.GetRangeValue(-10, 10)
vtkMath.Cross(normalized_x, arbitrary, normalized_z)
vtkMath.Normalize(normalized_z)

# Step 3 — Y axis: complete the right-handed basis with Y = Z × X.
vtkMath.Cross(normalized_z, normalized_x, normalized_y)

# Direction cosine matrix from the orthonormal basis
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

# Transform: translate to start, rotate via direction cosines, then rotate
# -90° about z to align the cylinder's +y height axis with the +x direction,
# scale the height to match the distance, and shift so the base sits at start.
transform = vtkTransform()
transform.Translate(start_point)
transform.Concatenate(matrix)
transform.RotateZ(-90.0)
transform.Scale(1.0, length, 1.0)
transform.Translate(0, 0.5, 0)

# Mapper and actor: oriented cylinder (using SetUserMatrix for efficiency)
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder_source.GetOutputPort())

cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.SetUserMatrix(transform.GetMatrix())
cylinder_actor.GetProperty().SetColor(cyan_rgb)

# Mapper and actor: sphere at start point
start_sphere_source = vtkSphereSource()
start_sphere_source.SetCenter(start_point)
start_sphere_source.SetRadius(0.8)

start_sphere_mapper = vtkPolyDataMapper()
start_sphere_mapper.SetInputConnection(start_sphere_source.GetOutputPort())

start_sphere_actor = vtkActor()
start_sphere_actor.SetMapper(start_sphere_mapper)
start_sphere_actor.GetProperty().SetColor(yellow_rgb)

# Mapper and actor: sphere at end point
end_sphere_source = vtkSphereSource()
end_sphere_source.SetCenter(end_point)
end_sphere_source.SetRadius(0.8)

end_sphere_mapper = vtkPolyDataMapper()
end_sphere_mapper.SetInputConnection(end_sphere_source.GetOutputPort())

end_sphere_actor = vtkActor()
end_sphere_actor.SetMapper(end_sphere_mapper)
end_sphere_actor.GetProperty().SetColor(magenta_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(cylinder_actor)
renderer.AddActor(start_sphere_actor)
renderer.AddActor(end_sphere_actor)
renderer.SetBackground(background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("OrientedCylinder")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
