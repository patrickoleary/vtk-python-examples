#!/usr/bin/env python

# Demonstrate vtkExtractRectilinearGrid extracting a subregion from
# a rectilinear grid with sample rate, rendered as a triangulated
# surface.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractRectilinearGrid
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOLegacy import vtkRectilinearGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read rectilinear grid
rgrid_reader = vtkRectilinearGridReader()
rgrid_reader.SetFileName(os.path.join(data_dir, "RectGrid2.vtk"))
rgrid_reader.Update()

# Extract subregion with sample rate
extract = vtkExtractRectilinearGrid()
extract.SetInputConnection(rgrid_reader.GetOutputPort())
extract.SetVOI(23, 40, 16, 30, 9, 9)
extract.SetSampleRate(2, 2, 1)
extract.IncludeBoundaryOn()
extract.Update()

# Convert to surface and triangulate
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(extract.GetOutputPort())

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(surface_filter.GetOutputPort())

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(triangle_filter.GetOutputPort())
mapper.SetScalarRange(extract.GetOutput().GetScalarRange())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(340, 400)
render_window.SetWindowName("extract rect grid")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
