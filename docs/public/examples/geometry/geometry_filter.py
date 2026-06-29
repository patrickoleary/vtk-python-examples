#!/usr/bin/env python

# Demonstrate vtkGeometryFilter in fast mode with merging on
# tetrahedral data extracted from an image volume, compared
# against vtkDataSetSurfaceFilter.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkSimpleElevationFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersGeneral import vtkDataSetTriangleFilter
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Control test resolution
res = 50

# Create a synthetic volume
vol = vtkImageData()
vol.SetDimensions(res, res, res)

# Triangulate to tetrahedra
tetras = vtkDataSetTriangleFilter()
tetras.SetInputData(vol)
tetras.Update()

# Create elevation scalar field
ele = vtkSimpleElevationFilter()
ele.SetInputConnection(tetras.GetOutputPort())
ele.Update()

# Extract surface with vtkGeometryFilter (fast mode)
geom_filter = vtkGeometryFilter()
geom_filter.SetInputConnection(ele.GetOutputPort())
geom_filter.FastModeOn()
geom_filter.MergingOn()
geom_filter.Update()

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
render_window.SetWindowName("geometry filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(1, 0, 0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
