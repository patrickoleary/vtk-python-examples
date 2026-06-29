#!/usr/bin/env python

# Test vtkScalarBarActor with multiple configurations including annotations, opacity, and custom labels.

import math
import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Source
plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()

# Filter
grid_geometry_filter = vtkStructuredGridGeometryFilter()
grid_geometry_filter.SetInputData(plot3d_reader.GetOutput().GetBlock(0))
grid_geometry_filter.SetExtent(0, 100, 0, 100, 9, 9)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(grid_geometry_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Scalar bar 1 — vertical with annotations
lut = outline_mapper.GetLookupTable()
lut.SetAnnotation(0.0, "Zed")
lut.SetAnnotation(1.0, "Uno")
lut.SetAnnotation(0.1, "$\\frac{1}{10}$")
lut.SetAnnotation(0.125, "$\\frac{1}{8}$")
lut.SetAnnotation(0.5, "Half")

scalar_bar_1 = vtkScalarBarActor()
scalar_bar_1.SetTitle("Density")
scalar_bar_1.SetLookupTable(lut)
scalar_bar_1.DrawAnnotationsOn()
scalar_bar_1.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_1.GetPositionCoordinate().SetValue(0.6, 0.05)
scalar_bar_1.SetWidth(0.15)
scalar_bar_1.SetHeight(0.5)
scalar_bar_1.SetTextPositionToPrecedeScalarBar()
scalar_bar_1.GetTitleTextProperty().SetColor(0.0, 0.0, 1.0)
scalar_bar_1.GetLabelTextProperty().SetColor(0.0, 0.0, 1.0)
scalar_bar_1.GetAnnotationTextProperty().SetColor(0.0, 0.0, 1.0)
scalar_bar_1.SetDrawFrame(1)
scalar_bar_1.GetFrameProperty().SetColor(0.0, 0.0, 0.0)
scalar_bar_1.SetDrawBackground(1)
scalar_bar_1.GetBackgroundProperty().SetColor(1.0, 1.0, 1.0)

# Scalar bar 2 — horizontal, no annotations
scalar_bar_2 = vtkScalarBarActor()
scalar_bar_2.SetTitle("Density")
scalar_bar_2.SetLookupTable(lut)
scalar_bar_2.DrawAnnotationsOff()
scalar_bar_2.SetOrientationToHorizontal()
scalar_bar_2.SetWidth(0.5)
scalar_bar_2.SetHeight(0.15)
scalar_bar_2.SetVerticalTitleSeparation(10)
scalar_bar_2.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_2.GetPositionCoordinate().SetValue(0.05, 0.05)
scalar_bar_2.SetTextPositionToPrecedeScalarBar()
scalar_bar_2.GetTitleTextProperty().SetColor(1.0, 0.0, 0.0)
scalar_bar_2.GetLabelTextProperty().SetColor(0.8, 0.0, 0.0)
scalar_bar_2.SetDrawFrame(1)
scalar_bar_2.GetFrameProperty().SetColor(1.0, 0.0, 0.0)
scalar_bar_2.SetDrawBackground(1)
scalar_bar_2.GetBackgroundProperty().SetColor(0.5, 0.5, 0.5)

# Scalar bar 3 — vertical, text succeeds bar
scalar_bar_3 = vtkScalarBarActor()
scalar_bar_3.SetTitle("Density")
scalar_bar_3.SetLookupTable(lut)
scalar_bar_3.DrawAnnotationsOff()
scalar_bar_3.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_3.GetPositionCoordinate().SetValue(0.8, 0.05)
scalar_bar_3.SetWidth(0.15)
scalar_bar_3.SetHeight(0.5)
scalar_bar_3.SetTextPositionToSucceedScalarBar()
scalar_bar_3.SetVerticalTitleSeparation(15)
scalar_bar_3.GetTitleTextProperty().SetColor(0.0, 0.0, 1.0)
scalar_bar_3.GetLabelTextProperty().SetColor(0.0, 0.0, 1.0)
scalar_bar_3.SetDrawFrame(1)
scalar_bar_3.GetFrameProperty().SetColor(0.0, 0.0, 0.0)
scalar_bar_3.SetDrawBackground(0)

# Scalar bar 4 — horizontal, text succeeds bar
scalar_bar_4 = vtkScalarBarActor()
scalar_bar_4.SetTitle("Density")
scalar_bar_4.SetLookupTable(lut)
scalar_bar_4.DrawAnnotationsOff()
scalar_bar_4.SetOrientationToHorizontal()
scalar_bar_4.SetWidth(0.5)
scalar_bar_4.SetHeight(0.15)
scalar_bar_4.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_4.GetPositionCoordinate().SetValue(0.05, 0.8)
scalar_bar_4.SetTextPositionToSucceedScalarBar()
scalar_bar_4.GetTitleTextProperty().SetColor(0.0, 0.0, 1.0)
scalar_bar_4.GetLabelTextProperty().SetColor(0.0, 0.0, 1.0)
scalar_bar_4.SetDrawFrame(1)
scalar_bar_4.GetFrameProperty().SetColor(1.0, 1.0, 1.0)
scalar_bar_4.SetDrawBackground(0)

# Scalar bar 5 — horizontal with custom labels
scalar_bar_5 = vtkScalarBarActor()
scalar_bar_5.SetTitle("Density")
scalar_bar_5.SetLookupTable(lut)
scalar_bar_5.DrawAnnotationsOff()
scalar_bar_5.SetOrientationToHorizontal()
scalar_bar_5.SetWidth(0.5)
scalar_bar_5.SetHeight(0.15)
scalar_bar_5.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_5.GetPositionCoordinate().SetValue(0.05, 0.6)
scalar_bar_5.SetDrawFrame(1)
scalar_bar_5.SetDrawBackground(0)

custom_labels = vtkDoubleArray()
custom_labels.SetNumberOfComponents(1)
custom_labels.SetNumberOfTuples(4)
custom_labels.SetValue(0, -1)
custom_labels.SetValue(1, 0.2)
custom_labels.SetValue(2, 0.6)
custom_labels.SetValue(3, 1.1)
scalar_bar_5.SetCustomLabels(custom_labels)
scalar_bar_5.SetUseCustomLabels(True)

# Scalar bar 6 — horizontal with opacity function
opacity_func = vtkPiecewiseFunction()
opacity_func.AddPoint(0.0, 1.0)
opacity_func.AddPoint(1.0, 0.1)

scalar_bar_6 = vtkScalarBarActor()
scalar_bar_6.SetTitle("DensityWithOpacity")
scalar_bar_6.SetLookupTable(lut)
scalar_bar_6.SetOpacityFunction(opacity_func)
scalar_bar_6.SetUseOpacity(True)
scalar_bar_6.DrawAnnotationsOff()
scalar_bar_6.SetOrientationToHorizontal()
scalar_bar_6.SetWidth(0.5)
scalar_bar_6.SetHeight(0.15)
scalar_bar_6.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_6.GetPositionCoordinate().SetValue(0.05, 0.4)
scalar_bar_6.GetTitleTextProperty().SetColor(0.5, 0.0, 1.0)
scalar_bar_6.GetLabelTextProperty().SetColor(0.5, 0.0, 1.0)
scalar_bar_6.SetDrawFrame(1)
scalar_bar_6.SetTextureGridWidth(20)

# Scalar bar 7 — distinct linear LUT
range_min = 1.0
range_max = 6.019831813928703

lut2 = vtkLookupTable()
lut2.SetRange(range_min, range_max)
lut2.SetNumberOfColors(4)
lut2.Build()

scalar_bar_7 = vtkScalarBarActor()
scalar_bar_7.SetTitle("distinct linear")
scalar_bar_7.SetLookupTable(lut2)
scalar_bar_7.SetWidth(0.15)
scalar_bar_7.SetHeight(0.4)
scalar_bar_7.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_7.GetPositionCoordinate().SetValue(0.6, 0.6)
scalar_bar_7.SetMaximumNumberOfColors(4)

# Scalar bar 8 — distinct log LUT
range_max_log = math.pow(10.0, range_max)

lut3 = vtkLookupTable()
lut3.SetRange(range_min, range_max_log)
lut3.SetNumberOfColors(4)
lut3.SetScaleToLog10()
lut3.Build()

scalar_bar_8 = vtkScalarBarActor()
scalar_bar_8.SetTitle("distinct log")
scalar_bar_8.SetLookupTable(lut3)
scalar_bar_8.SetWidth(0.15)
scalar_bar_8.SetHeight(0.4)
scalar_bar_8.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar_8.GetPositionCoordinate().SetValue(0.8, 0.6)
scalar_bar_8.SetMaximumNumberOfColors(4)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(scalar_bar_1)
renderer.AddActor(scalar_bar_2)
renderer.AddActor(scalar_bar_3)
renderer.AddActor(scalar_bar_4)
renderer.AddActor(scalar_bar_5)
renderer.AddActor(scalar_bar_6)
renderer.AddActor(scalar_bar_7)
renderer.AddActor(scalar_bar_8)
renderer.GradientBackgroundOn()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.SetBackground2(0.0, 0.0, 0.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("scalar bar")
render_window.SetMultiSamples(0)
render_window.SetSize(700, 500)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetFocalPoint(8, 0, 30)
renderer.GetActiveCamera().SetPosition(6, 0, 50)

interactor.Initialize()
interactor.Start()
