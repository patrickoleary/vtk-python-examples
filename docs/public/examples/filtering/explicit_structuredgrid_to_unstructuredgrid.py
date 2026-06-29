#!/usr/bin/env python

# Convert a wavelet image data to explicit structured grid and then
# back to unstructured grid, verifying block index arrays are preserved.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkExplicitStructuredGridToUnstructuredGrid,
    vtkImageDataToExplicitStructuredGrid,
)
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: wavelet dataset
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)
wavelet.SetCenter(0.0, 0.0, 0.0)
wavelet.Update()

# Filter: convert image data to explicit structured grid
esg_converter = vtkImageDataToExplicitStructuredGrid()
esg_converter.SetInputConnection(wavelet.GetOutputPort())
esg_converter.Update()

# Filter: convert explicit structured grid to unstructured grid
ug_converter = vtkExplicitStructuredGridToUnstructuredGrid()
ug_converter.SetInputData(esg_converter.GetOutput())
ug_converter.Update()

# Verify block index arrays exist
cell_data = ug_converter.GetOutput().GetCellData()
for name in ("BLOCK_I", "BLOCK_J", "BLOCK_K"):
    if cell_data.GetArray(name) is None:
        print(f"Missing expected array: {name}")

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(ug_converter.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("explicit structuredgrid to unstructuredgrid")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
