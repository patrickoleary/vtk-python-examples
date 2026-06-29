#!/usr/bin/env python

# Cut an unstructured grid with a plane and visualize interpolated cell data.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtk3DLinearGridPlaneCutter,
    vtkGenerateIds,
)
from vtkmodules.vtkFiltersGeneral import vtkPassArrays
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Reader: load the unstructured grid
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "slightlyRotated.vtu"))

# Cut plane definition
plane = vtkPlane()
plane.SetOrigin(0.0, 0.0, 0.0)
plane.SetNormal(0, 1.0, 0.5)

# Generate simple cell IDs as cell data
cell_array_name = "CellIds"
compute_ids = vtkGenerateIds()
compute_ids.SetInputConnection(reader.GetOutputPort())
compute_ids.SetPointIds(False)
compute_ids.SetCellIds(True)
compute_ids.SetCellIdsArrayName(cell_array_name)
compute_ids.Update()

# Pass arrays through (allows selective removal)
remove_arrays = vtkPassArrays()
remove_arrays.SetInputConnection(compute_ids.GetOutputPort())

# Filter: 3D linear grid plane cutter
slicer = vtk3DLinearGridPlaneCutter()
slicer.SetInputConnection(remove_arrays.GetOutputPort())
slicer.SetPlane(plane)
slicer.SetInterpolateAttributes(True)
slicer.SetMergePoints(False)
slicer.Update()

# Mapper: color by cell IDs
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(slicer.GetOutputPort())
mapper.SetScalarModeToUseCellData()
mapper.SetColorModeToMapScalars()
mapper.ScalarVisibilityOn()
mapper.SelectColorArray(cell_array_name)

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("3d lineargrid plane cutter cell data")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
