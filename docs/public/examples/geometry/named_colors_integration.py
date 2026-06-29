#!/usr/bin/env python

# Demonstrate vtkNamedColors integration with vtkBandedPolyDataContourFilter
# by creating a cone, computing elevation, generating banded contours, and
# rendering with a lookup table of primary additive/subtractive colors.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

named_colors = vtkNamedColors()

# Create a cone
cone = vtkConeSource()
cone.SetCenter(0.0, 0.0, 0.0)
cone.SetRadius(5.0)
cone.SetHeight(10)
cone.SetDirection(0, 1, 0)
cone.Update()

bounds = cone.GetOutput().GetBounds()

# Compute elevation
elevation = vtkElevationFilter()
elevation.SetInputConnection(cone.GetOutputPort())
elevation.SetLowPoint(0, bounds[2], 0)
elevation.SetHighPoint(0, bounds[3], 0)

# Banded contour filter
banded_contour = vtkBandedPolyDataContourFilter()
banded_contour.SetInputConnection(elevation.GetOutputPort())
banded_contour.SetScalarModeToValue()
banded_contour.GenerateContourEdgesOn()
banded_contour.GenerateValues(7, elevation.GetScalarRange())

# Lookup table with primary additive/subtractive colors
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(7)
lookup_table.SetTableValue(0, named_colors.GetColor4d("Red"))
lookup_table.SetTableValue(1, named_colors.GetColor4d("DarkGreen"))
lookup_table.SetTableValue(2, named_colors.GetColor4d("Blue"))
lookup_table.SetTableValue(3, named_colors.GetColor4d("Cyan"))
lookup_table.SetTableValue(4, named_colors.GetColor4d("Magenta"))
lookup_table.SetTableValue(5, named_colors.GetColor4d("Yellow"))
lookup_table.SetTableValue(6, named_colors.GetColor4d("White"))
lookup_table.SetTableRange(elevation.GetScalarRange())
lookup_table.Build()

# Surface mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(banded_contour.GetOutputPort())
mapper.SetScalarRange(elevation.GetScalarRange())
mapper.SetLookupTable(lookup_table)
mapper.SetScalarModeToUseCellData()

# Contour line mapper
contour_line_mapper = vtkPolyDataMapper()
contour_line_mapper.SetInputData(banded_contour.GetContourEdgesOutput())
contour_line_mapper.SetScalarRange(elevation.GetScalarRange())
contour_line_mapper.SetResolveCoincidentTopologyToPolygonOffset()

# Surface actor
actor = vtkActor()
actor.SetMapper(mapper)

# Contour line actor
contour_line_actor = vtkActor()
contour_line_actor.SetMapper(contour_line_mapper)
contour_line_actor.GetProperty().SetColor(named_colors.GetColor3d("Black"))

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(contour_line_actor)
renderer.SetBackground(named_colors.GetColor3d("SteelBlue"))

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("named colors integration")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
