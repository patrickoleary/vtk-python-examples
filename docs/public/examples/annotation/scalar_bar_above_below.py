#!/usr/bin/env python

# Test vtkScalarBarActor with above/below range swatches on a plane source.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkLookupTable
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 3

# Plane source with cell data
plane = vtkPlaneSource()
plane.SetXResolution(resolution)
plane.SetYResolution(resolution)

cell_data = vtkDoubleArray()
for i in range(resolution * resolution):
    cell_data.InsertNextValue(i)

plane.Update()
plane.GetOutput().GetCellData().SetScalars(cell_data)

# Mapper
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())
plane_mapper.SetScalarRange(1, 7)

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Configure lookup table with above/below range colors
lut = vtkLookupTable.SafeDownCast(plane_mapper.GetLookupTable())
lut.SetUseBelowRangeColor(True)
lut.SetUseAboveRangeColor(True)
lut.SetNumberOfColors(7)

# Scalar bar 1 — vertical with both swatches
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(plane_mapper.GetLookupTable())
scalar_bar.SetDrawBelowRangeSwatch(True)
scalar_bar.SetDrawAboveRangeSwatch(True)

# Scalar bar 2 — horizontal with below swatch
scalar_bar_2 = vtkScalarBarActor()
scalar_bar_2.SetLookupTable(plane_mapper.GetLookupTable())
scalar_bar_2.SetDrawBelowRangeSwatch(True)
scalar_bar_2.SetOrientationToHorizontal()
scalar_bar_2.SetWidth(0.5)
scalar_bar_2.SetHeight(0.15)
scalar_bar_2.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_2.GetPositionCoordinate().SetValue(0.05, 0.8)

# Scalar bar 3 — horizontal with above swatch
scalar_bar_3 = vtkScalarBarActor()
scalar_bar_3.SetLookupTable(plane_mapper.GetLookupTable())
scalar_bar_3.SetDrawAboveRangeSwatch(True)
scalar_bar_3.SetOrientationToHorizontal()
scalar_bar_3.SetWidth(0.5)
scalar_bar_3.SetHeight(0.15)
scalar_bar_3.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_3.GetPositionCoordinate().SetValue(0.05, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(plane_actor)
renderer.AddActor(scalar_bar)
renderer.AddActor(scalar_bar_2)
renderer.AddActor(scalar_bar_3)
renderer.SetBackground(0.5, 0.5, 0.5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("scalar bar above below")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
