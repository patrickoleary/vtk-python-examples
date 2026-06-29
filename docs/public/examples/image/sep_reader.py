#!/usr/bin/env python

# Read a SEP file, verify grid properties, and render with lookup table.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOImage import vtkSEPReader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read SEP file
sep_reader = vtkSEPReader()
sep_reader.SetFileName(os.path.join(data_dir, "small.H"))
sep_reader.SetFixedDimension1("DEPTH")
sep_reader.SetFixedDimensionValue1(0)
sep_reader.Update()

# Get scalar range for lookup table
scalar_range = sep_reader.GetOutput().GetScalarRange()

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetRampToLinear()
lookup_table.SetRange(scalar_range[0], scalar_range[1])
lookup_table.SetValueRange(0.0, 1.0)
lookup_table.SetSaturationRange(0.0, 0.0)
lookup_table.SetAlphaRange(1.0, 1.0)
lookup_table.Build()

# Map colors
colors = vtkImageMapToColors()
colors.SetInputConnection(sep_reader.GetOutputPort())
colors.SetLookupTable(lookup_table)

# Extract surface
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(colors.GetOutputPort())

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(surface.GetOutputPort())
poly_mapper.ScalarVisibilityOn()
poly_mapper.SelectColorArray("ImageScalars")
poly_mapper.SetColorModeToMapScalars()

# Actor
sep_actor = vtkActor()
sep_actor.SetMapper(poly_mapper)
sep_actor.GetProperty().EdgeVisibilityOn()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(sep_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("sep reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
z1 = renderer.GetActiveCamera().GetPosition()[2]
renderer.GetActiveCamera().SetPosition(0.25 * z1, 0.25 * z1, 0.5 * z1)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.0, 0.0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
