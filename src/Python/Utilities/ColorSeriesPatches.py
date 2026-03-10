#!/usr/bin/env python

# Visualize all VTK color series as rows of colored bars.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Enumerate all built-in color series schemes.
# vtkColorSeries provides indexed access to color schemes by integer ID.
series = vtkColorSeries()
num_schemes = series.GetNumberOfColorSchemes()

# Grid layout parameters
pad_x = 0.1
pad_y = 0.15
cell_w = 1.0
cell_h = 0.6

# Build a polydata with one quad per color in each series
points = vtkPoints()
cells = vtkCellArray()
cell_colors = vtkUnsignedCharArray()
cell_colors.SetNumberOfComponents(3)
cell_colors.SetName("Colors")

for scheme_idx in range(num_schemes):
    series.SetColorScheme(scheme_idx)
    num_colors = series.GetNumberOfColors()

    for color_idx in range(num_colors):
        x0 = color_idx * (cell_w + pad_x)
        y0 = (num_schemes - 1 - scheme_idx) * (cell_h + pad_y)
        x1 = x0 + cell_w
        y1 = y0 + cell_h

        pid = points.GetNumberOfPoints()
        points.InsertNextPoint(x0, y0, 0.0)
        points.InsertNextPoint(x1, y0, 0.0)
        points.InsertNextPoint(x1, y1, 0.0)
        points.InsertNextPoint(x0, y1, 0.0)

        cells.InsertNextCell(4)
        cells.InsertCellPoint(pid)
        cells.InsertCellPoint(pid + 1)
        cells.InsertCellPoint(pid + 2)
        cells.InsertCellPoint(pid + 3)

        c = series.GetColor(color_idx)
        cell_colors.InsertNextTuple3(c.GetRed(), c.GetGreen(), c.GetBlue())

poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetPolys(cells)
poly_data.GetCellData().SetScalars(cell_colors)

# Mapper: map the colored quads to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(poly_data)
mapper.SetScalarModeToUseCellData()

# Actor: display the color series grid
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.2, 0.2)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1200, 800)
render_window.SetWindowName("ColorSeriesPatches")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
