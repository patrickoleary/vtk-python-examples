#!/usr/bin/env python

# Demonstrate vtkDataSetSurfaceFilter on a blanked wavelet image
# data, checking that ghost/hidden cells are respected.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    vtkDataSetAttributes,
    vtkImageData,
    vtkStructuredData,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Wavelet source
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)
wavelet.Update()

# Shallow copy and blank cells
image = vtkImageData()
image.ShallowCopy(wavelet.GetOutputDataObject(0))

extent = image.GetExtent()
ghost_cells = vtkUnsignedCharArray()
ghost_cells.SetNumberOfComponents(1)
ghost_cells.SetNumberOfTuples(image.GetNumberOfCells())
ghost_cells.Fill(0)
ghost_cells.SetName(vtkDataSetAttributes.GhostArrayName())
image.GetCellData().AddArray(ghost_cells)

# Blank cells in a triangular pattern
ijk = [0, 0, 0]
for ijk[0] in range(extent[0], extent[1]):
    for ijk[1] in range(ijk[0], extent[3]):
        for ijk[2] in range(ijk[0], extent[5]):
            cell_id = vtkStructuredData.ComputeCellIdForExtent(extent, ijk)
            ghost_cells.SetValue(cell_id, vtkDataSetAttributes.HIDDENCELL)

# Surface filter
surface = vtkDataSetSurfaceFilter()
surface.SetInputData(image)

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetColorModeToMapScalars()
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("RTData")
mapper.SetScalarRange(37, 280)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(478, 392)
render_window.AddRenderer(renderer)
render_window.SetWindowName("regular grid dataset surface filter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
