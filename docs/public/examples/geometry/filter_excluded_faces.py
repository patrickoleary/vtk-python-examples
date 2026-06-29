#!/usr/bin/env python

# Demonstrate vtkGeometryFilter with excluded faces on a hexahedral
# unstructured grid extracted from an image volume.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkImageData,
    vtkPolyData,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkSimpleElevationFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Control test resolution
res = 10

# Create a synthetic volume
vol = vtkImageData()
vol.SetDimensions(res, res, res)

# Extract as unstructured grid
sphere = vtkSphere()
sphere.SetRadius(10000)

grid = vtkExtractGeometry()
grid.SetInputData(vol)
grid.SetImplicitFunction(sphere)
grid.Update()

# Create elevation scalar field
ele = vtkSimpleElevationFilter()
ele.SetInputConnection(grid.GetOutputPort())

# Create excluded faces
face = [0, 1, 11, 10]
faces = vtkCellArray()
faces.InsertNextCell(4, face)

excluded_faces = vtkPolyData()
excluded_faces.SetPolys(faces)

# Extract surface with excluded faces
geom_filter = vtkGeometryFilter()
geom_filter.SetInputConnection(ele.GetOutputPort())
geom_filter.SetExcludedFacesData(excluded_faces)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geom_filter.GetOutputPort())
mapper.SetScalarRange(0, float(res - 1))

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("filter excluded faces")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(-1, -1, -1)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2)

interactor.Initialize()
interactor.Start()
