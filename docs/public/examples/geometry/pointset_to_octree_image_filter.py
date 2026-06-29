#!/usr/bin/env python

# Demonstrate vtkPointSetToOctreeImageFilter generating an octree
# image from a sphere point set, rendered with GPU volume ray casting
# using maximum intensity projection.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkPartitionedDataSet,
    vtkPiecewiseFunction,
)
from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersGeometryPreview import vtkPointSetToOctreeImageFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper

# High-resolution sphere
sphere = vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(0.5)
sphere.SetPhiResolution(2000)
sphere.SetThetaResolution(2000)

# Compute sin(x) as a point data array
calc = vtkArrayCalculator()
calc.SetInputConnection(sphere.GetOutputPort())
calc.SetAttributeTypeToPointData()
calc.AddCoordinateScalarVariable("coordsX", 0)
calc.SetFunction("sin(coordsX)")
calc.SetResultArrayName("sin_x")

# Generate octree image from the point set
point_set_to_image = vtkPointSetToOctreeImageFilter()
point_set_to_image.SetInputConnection(calc.GetOutputPort())
point_set_to_image.SetNumberOfPointsPerCell(10)
point_set_to_image.ProcessInputPointArrayOn()
point_set_to_image.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "sin_x")
point_set_to_image.ComputeMaxOff()
point_set_to_image.ComputeCountOn()
point_set_to_image.Update()

image = vtkPartitionedDataSet.SafeDownCast(
    point_set_to_image.GetOutput()).GetPartition(0)

# Opacity transfer function
opacity_tf = vtkPiecewiseFunction()
opacity_tf.AddPoint(20, 0.0)
opacity_tf.AddPoint(255, 0.2)

# Color transfer function
color_tf = vtkColorTransferFunction()
color_tf.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
color_tf.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
color_tf.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
color_tf.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
color_tf.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

# Volume property
volume_property = vtkVolumeProperty()
volume_property.SetColor(color_tf)
volume_property.SetScalarOpacity(opacity_tf)
volume_property.ShadeOn()
volume_property.SetInterpolationTypeToLinear()

# GPU volume mapper with maximum intensity blending
volume_mapper = vtkGPUVolumeRayCastMapper()
volume_mapper.SetInputData(image)
volume_mapper.SetBlendModeToMaximumIntensity()

volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.5)
renderer.AddViewProp(volume)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("pointset to octree image filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(45)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
