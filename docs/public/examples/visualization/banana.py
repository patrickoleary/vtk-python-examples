#!/usr/bin/env python

# Demonstrate vtkWeightedTransformFilter to create a banana-shaped deformation
# of a sphere using two interpolated transforms.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersHybrid import vtkWeightedTransformFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Use a sphere as a basis of the shape
sphere = vtkSphereSource()
sphere.SetPhiResolution(40)
sphere.SetThetaResolution(40)
sphere.Update()
sphere_data = sphere.GetOutput()

# Create a data array to hold the weighting coefficients
tf_array = vtkFloatArray()
npoints = sphere_data.GetNumberOfPoints()
tf_array.SetNumberOfComponents(2)
tf_array.SetNumberOfTuples(npoints)

# Parameterize the sphere along the z axis, fill weights with (1-a, a)
for i in range(npoints):
    pt = sphere_data.GetPoint(i)
    z = pt[2]
    zn = z + 0.5
    zn1 = 1.0 - zn
    if zn > 1.0:
        zn = 1.0
    if zn1 < 0.0:
        zn1 = 0.0
    tf_array.SetComponent(i, 0, zn1)
    tf_array.SetComponent(i, 1, zn)

# Bind the weights array to the sphere
tf_array.SetName("weights")
sphere_data.GetPointData().AddArray(tf_array)

# Stretch the shape
stretch = vtkTransform()
stretch.Scale(1, 1, 3.2)

stretch_filter = vtkTransformFilter()
stretch_filter.SetInputData(sphere_data)
stretch_filter.SetTransform(stretch)

# Create two transforms to interpolate between
identity = vtkTransform()
identity.Identity()

rotated_angle = 45
rotated = vtkTransform()
rotated.RotateX(rotated_angle)

# Apply weighted transform
weighted_trans = vtkWeightedTransformFilter()
weighted_trans.SetNumberOfTransforms(2)
weighted_trans.SetTransform(identity, 0)
weighted_trans.SetTransform(rotated, 1)
weighted_trans.SetWeightArray("weights")
weighted_trans.SetInputConnection(stretch_filter.GetOutputPort())

weighted_trans_mapper = vtkPolyDataMapper()
weighted_trans_mapper.SetInputConnection(weighted_trans.GetOutputPort())

weighted_trans_actor = vtkActor()
weighted_trans_actor.SetMapper(weighted_trans_mapper)
weighted_trans_actor.GetProperty().SetDiffuseColor(0.8, 0.8, 0.1)
weighted_trans_actor.GetProperty().SetRepresentationToSurface()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(weighted_trans_actor)
renderer.SetBackground(0.1, 0.2, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("banana")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(90)
renderer.GetActiveCamera().Dolly(1)

# Apply the rotation inline (was def cmd)
rotated.Identity()
rotated.RotateX(rotated_angle)

interactor.Initialize()
interactor.Start()
