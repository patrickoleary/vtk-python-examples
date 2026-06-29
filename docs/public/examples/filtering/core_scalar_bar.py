#!/usr/bin/env python

# Test vtkScalarBarActor with random cell colors on a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkFiltersProgrammable import vtkProgrammableAttributeDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(40)

# Fixed color values for 760 cells (20 theta * 38 phi strips)
fixed_cell_values = [
    0.12, 0.87, 0.34, 0.56, 0.78, 0.23, 0.91, 0.45, 0.67, 0.09,
    0.82, 0.38, 0.54, 0.71, 0.16, 0.93, 0.41, 0.63, 0.05, 0.88,
    0.29, 0.52, 0.74, 0.18, 0.96, 0.43, 0.65, 0.07, 0.81, 0.36,
    0.58, 0.73, 0.14, 0.92, 0.47, 0.69, 0.03, 0.85, 0.31, 0.53,
]

# Programmable filter callback to assign fixed colors
def color_cells(obj=None, event=""):
    input_data = random_colors.GetInput()
    output_data = random_colors.GetOutput()
    num_cells = input_data.GetNumberOfCells()
    colors = vtkFloatArray()
    colors.SetNumberOfTuples(num_cells)
    for i in range(num_cells):
        colors.SetValue(i, fixed_cell_values[i % len(fixed_cell_values)])
    output_data.GetCellData().CopyScalarsOff()
    output_data.GetCellData().PassData(input_data.GetCellData())
    output_data.GetCellData().SetScalars(colors)

random_colors = vtkProgrammableAttributeDataFilter()
random_colors.SetInputConnection(sphere.GetOutputPort())
random_colors.SetExecuteMethod(color_cells)

# Mapper and actor
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(random_colors.GetOutputPort())
sphere_mapper.SetScalarRange(random_colors.GetPolyDataOutput().GetScalarRange())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Scalar bar
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(sphere_mapper.GetLookupTable())
scalar_bar.SetTitle("Temperature")
scalar_bar.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar.GetPositionCoordinate().SetValue(0.1, 0.01)
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetWidth(0.8)
scalar_bar.SetHeight(0.17)
scalar_bar.SetPosition(scalar_bar.GetPosition())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddViewProp(scalar_bar)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("core scalar bar")
render_window.SetMultiSamples(0)
render_window.SetSize(350, 350)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# First render computes scalar bar layout, then update label count
render_window.Render()
scalar_bar.SetNumberOfLabels(8)

interactor.Initialize()
interactor.Start()
