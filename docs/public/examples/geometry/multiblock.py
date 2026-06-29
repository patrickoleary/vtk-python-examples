#!/usr/bin/env python

# Demonstrate multi-block PLOT3D data processing with shrink, outline
# corner, and contour filters rendered together.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractBlock
from vtkmodules.vtkFiltersGeneral import (
    vtkShrinkPolyData,
)
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersSources import vtkOutlineCornerFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read multi-block PLOT3D data
reader = vtkMultiBlockPLOT3DReader()
reader.SetXYZFileName(os.path.join(data_dir, "mbwavelet_ascii.xyz"))
reader.SetQFileName(os.path.join(data_dir, "mbwavelet_ascii.q"))
reader.SetMultiGrid(1)
reader.SetBinaryFile(0)

# Geometry filter on full dataset
geometry_filter = vtkCompositeDataGeometryFilter()
geometry_filter.SetInputConnection(reader.GetOutputPort())

# Shrink
shrink = vtkShrinkPolyData()
shrink.SetShrinkFactor(0.2)
shrink.SetInputConnection(geometry_filter.GetOutputPort())

shrink_mapper = vtkPolyDataMapper()
shrink_mapper.SetInputConnection(shrink.GetOutputPort())

shrink_actor = vtkActor()
shrink_actor.SetMapper(shrink_mapper)
shrink_actor.GetProperty().SetColor(0, 0, 1)

# Outline corners
outline_corner_filter = vtkOutlineCornerFilter()
outline_corner_filter.SetInputConnection(reader.GetOutputPort())

geometry_filter_2 = vtkCompositeDataGeometryFilter()
geometry_filter_2.SetInputConnection(outline_corner_filter.GetOutputPort())

outline_corner_mapper = vtkPolyDataMapper()
outline_corner_mapper.SetInputConnection(geometry_filter_2.GetOutputPort())

outline_corner_actor = vtkActor()
outline_corner_actor.SetMapper(outline_corner_mapper)
outline_corner_actor.GetProperty().SetColor(1, 0, 0)

# Extract block 2 and contour
extract_block = vtkExtractBlock()
extract_block.SetInputConnection(reader.GetOutputPort())
extract_block.AddIndex(2)

contour = vtkContourFilter()
contour.SetInputConnection(extract_block.GetOutputPort())
contour.SetValue(0, 149)

geometry_filter_3 = vtkCompositeDataGeometryFilter()
geometry_filter_3.SetInputConnection(contour.GetOutputPort())

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(geometry_filter_3.GetOutputPort())

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(shrink_actor)
renderer.AddActor(outline_corner_actor)
renderer.AddActor(contour_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("multiblock")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-5.1828, 5.89733, 8.97969)
camera.SetFocalPoint(14.6491, -2.08677, -8.92362)
camera.SetViewUp(0.210794, 0.95813, -0.193784)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
