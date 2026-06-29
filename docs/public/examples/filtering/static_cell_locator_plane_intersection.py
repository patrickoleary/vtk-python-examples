#!/usr/bin/env python

# Use vtkStaticCellLocator to find cells intersecting a plane on a
# wavelet isosurface, then extract and display those cells.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIdList
from vtkmodules.vtkCommonDataModel import vtkStaticCellLocator
from vtkmodules.vtkFiltersCore import (
    vtkExtractCells,
    vtkFlyingEdges3D,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

res = 15

# Create wavelet data
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-res, res, -res, res, -res, res)
wavelet.Update()

# Isocontour at two values
contour = vtkFlyingEdges3D()
contour.SetInputConnection(wavelet.GetOutputPort())
contour.SetValue(0, 100)
contour.SetValue(1, 200)
contour.Update()

# Build the locator on the contour
locator = vtkStaticCellLocator()
locator.SetDataSet(contour.GetOutput())
locator.AutomaticOn()
locator.SetNumberOfCellsPerNode(20)
locator.CacheCellBoundsOn()
locator.BuildLocator()

# Find cells along a diagonal plane
origin = [0, 0, 0]
normal = [1, 1, 1]
cell_ids = vtkIdList()
locator.FindCellsAlongPlane(origin, normal, 0.0, cell_ids)

# Split extracted cell ids into two halves for the ExtractCells API
number_of_ids = cell_ids.GetNumberOfIds()
first_half = int(number_of_ids / 2)
second_half = number_of_ids - first_half

cell_ids_first_half = vtkIdList()
for i in range(first_half):
    cell_ids_first_half.InsertNextId(cell_ids.GetId(i))

cell_ids_second_half = vtkIdList()
for i in range(second_half):
    cell_ids_second_half.InsertNextId(cell_ids.GetId(i + first_half))

# Extract the intersected cells
extract = vtkExtractCells()
extract.SetInputConnection(contour.GetOutputPort())
extract.AddCellList(cell_ids_first_half)
extract.AddCellList(cell_ids_second_half)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(extract.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Outline around the entire dataset
outline = vtkOutlineFilter()
outline.SetInputConnection(wavelet.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("static cell locator plane intersection")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
