#!/usr/bin/env python

# Demonstrate structured grid blanking using an image and scalar values
# on PLOT3D combustor data, displayed side by side.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import (
    vtkDataSetAttributes,
    vtkImageData,
    vtkStructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractGrid
from vtkmodules.vtkFiltersGeneral import (
    vtkBlankStructuredGrid,
    vtkBlankStructuredGridWithImage,
)
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

colors = vtkNamedColors()

# Read PLOT3D combustor data
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

output = pl3d.GetOutput().GetBlock(0)

# Extract a single plane from the grid
plane = vtkExtractGrid()
plane.SetInputData(output)
plane.SetVOI(0, 57, 0, 33, 0, 0)
plane.Update()

# Create blanking image data
VTK_UNSIGNED_CHAR = 3
blank_image = vtkImageData()
blank_image.SetDimensions(57, 33, 1)
blank_image.AllocateScalars(VTK_UNSIGNED_CHAR, 1)
blank_image.GetPointData().GetScalars().SetName("blankScalars")

blanking = blank_image.GetPointData().GetScalars()
num_blanks = 57 * 33
for i in range(num_blanks):
    blanking.SetComponent(i, 0, vtkDataSetAttributes.HIDDENPOINT)

# Manually blank out areas corresponding to dilution holes
blanking.SetComponent(318, 0, 0)
blanking.SetComponent(945, 0, 0)
blanking.SetComponent(1572, 0, 0)
blanking.SetComponent(641, 0, 0)
blanking.SetComponent(1553, 0, 0)

# Technique 1: blank using image
blank_it = vtkBlankStructuredGridWithImage()
blank_it.SetInputConnection(plane.GetOutputPort())
blank_it.SetBlankingInputData(blank_image)

blanked_plane = vtkStructuredGridGeometryFilter()
blanked_plane.SetInputConnection(blank_it.GetOutputPort())
blanked_plane.SetExtent(0, 100, 0, 100, 0, 0)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(blanked_plane.GetOutputPort())
plane_mapper.SetScalarRange(0.197813, 0.710419)

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Technique 2: blank using grid scalar values
another_grid = vtkStructuredGrid()
another_grid.CopyStructure(plane.GetOutput())
another_grid.GetPointData().SetScalars(blank_image.GetPointData().GetScalars())

blank_grid = vtkBlankStructuredGrid()
blank_grid.SetInputData(another_grid)
blank_grid.SetArrayName("blankScalars")
blank_grid.SetMinBlankingValue(-0.5)
blank_grid.SetMaxBlankingValue(0.5)

blanked_plane_2 = vtkStructuredGridGeometryFilter()
blanked_plane_2.SetInputConnection(blank_grid.GetOutputPort())
blanked_plane_2.SetExtent(0, 100, 0, 100, 0, 0)

plane_mapper_2 = vtkPolyDataMapper()
plane_mapper_2.SetInputConnection(blanked_plane_2.GetOutputPort())
plane_mapper_2.SetScalarRange(0.197813, 0.710419)

plane_actor_2 = vtkActor()
plane_actor_2.SetMapper(plane_mapper_2)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("black", rgb)
outline_actor.GetProperty().SetColor(rgb)

outline_mapper_2 = vtkPolyDataMapper()
outline_mapper_2.SetInputConnection(outline.GetOutputPort())

outline_actor_2 = vtkActor()
outline_actor_2.SetMapper(outline_mapper_2)
outline_actor_2.GetProperty().SetColor(rgb)

# Two renderers side by side
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)

renderer_0.AddActor(outline_actor)
renderer_0.AddActor(plane_actor)
renderer_0.SetBackground(1, 1, 1)

renderer_1.AddActor(outline_actor_2)
renderer_1.AddActor(plane_actor_2)
renderer_1.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(500, 250)
render_window.SetWindowName("blank grid")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer_0.GetActiveCamera()
cam.SetClippingRange(3.95297, 50)
cam.SetFocalPoint(8.88908, 0.595038, 29.3342)
cam.SetPosition(-12.3332, 31.7479, 41.2387)
cam.SetViewUp(0.060772, -0.319905, 0.945498)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

interactor.Initialize()
interactor.Start()
