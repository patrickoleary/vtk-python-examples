#!/usr/bin/env python

# Demonstrate vtkAMRSliceFilter on Enzo AMR data, slicing along the
# Y-normal at a given offset, validating cell count, and rendering
# the surface colored by TotalEnergy.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersAMR import vtkAMRSliceFilter
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOAMR import vtkAMREnzoReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Count total cells across all levels and blocks
datafield_name = "TotalEnergy"

# Read Enzo AMR hierarchy
reader = vtkAMREnzoReader()
reader.SetFileName(os.path.join(data_dir, "AMR", "Enzo", "DD0010", "moving7_0010.hierarchy"))
reader.SetMaxLevel(10)
reader.SetCellArrayStatus(datafield_name, 1)

# Slice along Y-normal
amr_filter = vtkAMRSliceFilter()
amr_filter.SetInputConnection(reader.GetOutputPort())
amr_filter.SetNormal(1)
amr_filter.SetOffsetFromOrigin(0.86)
amr_filter.SetMaxResolution(7)
amr_filter.Update()
amr_output = amr_filter.GetOutputDataObject(0)

# Validate output
if not amr_output.CheckValidity():
    print("Output is not valid")
    exit(1)

total_cells = 0
for i in range(amr_output.GetNumberOfLevels()):
    for j in range(amr_output.GetNumberOfBlocks(i)):
        block_cells = amr_output.GetDataSetAsImageData(i, j).GetNumberOfCells()
        total_cells = total_cells + block_cells
if total_cells != 800:
    print("Wrong number of cells in the output")
    exit(1)

# Extract surface geometry
surface = vtkGeometryFilter()
surface.SetInputData(amr_output)

# Composite mapper colored by TotalEnergy
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray(datafield_name)
mapper.SetScalarRange(1.2e-7, 1.5e-3)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("amr slice filter")

# Scene
renderer.GetActiveCamera().SetPosition(1, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
