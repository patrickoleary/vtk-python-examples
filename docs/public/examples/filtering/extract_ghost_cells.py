#!/usr/bin/env python

# Demonstrate vtkExtractGhostCells by creating an image dataset with
# ghost cells marked in a sub-region, extracting them, and rendering
# the ghost cells alongside the original volume.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    vtkDataSetAttributes,
    vtkImageData,
)
from vtkmodules.vtkFiltersCore import vtkPointDataToCellData
from vtkmodules.vtkFiltersGeneral import vtkExtractGhostCells
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create wavelet image data
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-5, 5, -5, 5, -5, 5)

# Convert point data to cell data
point_to_cell = vtkPointDataToCellData()
point_to_cell.SetInputConnection(wavelet.GetOutputPort())
point_to_cell.Update()

# Copy output and add ghost cell array
image = vtkImageData()
image.ShallowCopy(point_to_cell.GetOutputDataObject(0))

ghosts = vtkUnsignedCharArray()
ghosts.SetNumberOfValues(image.GetNumberOfCells())
ghosts.Fill(0)
ghosts.SetName(vtkDataSetAttributes.GhostArrayName())

# Mark a sub-region as ghost cells
dims = [10, 10, 10]
for k in range(1, 6):
    for j in range(1, 5):
        for i in range(1, 3):
            cell_id = i + j * dims[0] + k * dims[0] * dims[1]
            ghosts.SetValue(cell_id, vtkDataSetAttributes.DUPLICATECELL)

image.GetCellData().AddArray(ghosts)

# Extract ghost cells
extract = vtkExtractGhostCells()
extract.SetInputData(image)

# Render original volume surface (transparent)
original_surface = vtkDataSetSurfaceFilter()
original_surface.SetInputData(image)

original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(original_surface.GetOutputPort())
original_mapper.ScalarVisibilityOff()

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetOpacity(0.2)
original_actor.GetProperty().SetColor(0.8, 0.8, 0.8)

# Render extracted ghost cells (opaque, colored)
ghost_surface = vtkDataSetSurfaceFilter()
ghost_surface.SetInputConnection(extract.GetOutputPort())

ghost_mapper = vtkPolyDataMapper()
ghost_mapper.SetInputConnection(ghost_surface.GetOutputPort())

ghost_actor = vtkActor()
ghost_actor.SetMapper(ghost_mapper)
ghost_actor.GetProperty().SetColor(1.0, 0.2, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(original_actor)
renderer.AddActor(ghost_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("extract ghost cells")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
