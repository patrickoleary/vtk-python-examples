#!/usr/bin/env python

# Demonstrate vtkOctreeImageToPointSetFilter converting an octree
# image (generated from a sphere point set) back to a point set,
# colored by the max of sin(x).

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersGeometryPreview import (
    vtkOctreeImageToPointSetFilter,
    vtkPointSetToOctreeImageFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

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
point_set_to_image.SetNumberOfPointsPerCell(300)
point_set_to_image.ProcessInputPointArrayOn()
point_set_to_image.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "sin_x")
point_set_to_image.ComputeMaxOn()
point_set_to_image.ComputeCountOn()

# Convert octree image back to point set
image_to_point_set = vtkOctreeImageToPointSetFilter()
image_to_point_set.SetInputConnection(point_set_to_image.GetOutputPort())
image_to_point_set.ProcessInputCellArrayOn()
image_to_point_set.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_CELLS, "sin_x")
image_to_point_set.SetCellArrayComponent(1)

# Composite mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(image_to_point_set.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.5)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("octree image to pointset filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
