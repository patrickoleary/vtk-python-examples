#!/usr/bin/env python

# Demonstrate vtkLinearExtrusionFilter with cell data preservation by
# extruding vector text with random cell colors, and also testing
# vtkArrowSource with different resolutions.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath, vtkUnsignedCharArray
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkStripper
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Create vector text "o"
disk = vtkVectorText()
disk.SetText("o")

# Transform to offset
transform = vtkTransform()
transform.Translate(1.1, 0, 0)

transform_filter = vtkTransformFilter()
transform_filter.SetTransform(transform)
transform_filter.SetInputConnection(disk.GetOutputPort())

# Strip the transformed text
strips = vtkStripper()
strips.SetInputConnection(transform_filter.GetOutputPort())
strips.Update()

# Append original and stripped text
append_filter = vtkAppendPolyData()
append_filter.AddInputData(disk.GetOutput())
append_filter.AddInputData(strips.GetOutput())
append_filter.Update()
model = append_filter.GetOutput()

# Extrude the combined model
extrude = vtkLinearExtrusionFilter()
extrude.SetInputData(model)

# Create random cell scalars
vtk_math = vtkMath()
vtk_math.RandomSeed(1230)

cell_colors = vtkUnsignedCharArray()
cell_colors.SetNumberOfComponents(3)
cell_colors.SetNumberOfTuples(model.GetNumberOfCells())
for i in range(model.GetNumberOfCells()):
    cell_colors.InsertComponent(i, 0, vtk_math.Random(100, 255))
    cell_colors.InsertComponent(i, 1, vtk_math.Random(100, 255))
    cell_colors.InsertComponent(i, 2, vtk_math.Random(100, 255))

model.GetCellData().SetScalars(cell_colors)

# Arrow sources
arrow_1 = vtkArrowSource()

arrow_2 = vtkArrowSource()
arrow_2.SetShaftResolution(2)
arrow_2.SetTipResolution(1)

# Mapper and actor pairs
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(extrude.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(arrow_1.GetOutputPort())
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.SetPosition(0, -0.2, 1)

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(arrow_2.GetOutputPort())
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.SetPosition(1, -0.2, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("extrude copy cd")

# Scene
camera = renderer.GetActiveCamera()
camera.Azimuth(20)
camera.Elevation(40)
renderer.ResetCamera()
camera.Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
