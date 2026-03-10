#!/usr/bin/env python

# Color the individual faces of an annotated cube and display it as an orientation widget.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkBandedPolyDataContourFilter
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
)
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import (
    vtkAnnotatedCubeActor,
    vtkAxesActor,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkPropAssembly,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
misty_rose = (1.000, 0.894, 0.882)
royal_blue = (0.255, 0.412, 0.882)
dim_gray = (0.412, 0.412, 0.412)
black = (0.000, 0.000, 0.000)
turquoise = (0.251, 0.878, 0.816)
mint = (0.741, 0.988, 0.788)
tomato = (1.000, 0.388, 0.278)

# Source: generate an elliptical cone
cone_source = vtkConeSource()
cone_source.SetCenter(0.0, 0.0, 0.0)
cone_source.SetRadius(5.0)
cone_source.SetHeight(15.0)
cone_source.SetDirection(0, 1, 0)
cone_source.SetResolution(60)

# Transform: scale the cone to create an elliptical base
transform = vtkTransform()
transform.Scale(1.0, 1.0, 0.75)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(cone_source.GetOutputPort())
transform_filter.SetTransform(transform)
transform_filter.Update()

bounds = transform_filter.GetOutput().GetBounds()

# Elevation: compute scalar values based on Y-height
elevation = vtkElevationFilter()
elevation.SetInputConnection(transform_filter.GetOutputPort())
elevation.SetLowPoint(0, bounds[2], 0)
elevation.SetHighPoint(0, bounds[3], 0)

# BandedContours: partition the elevation into bands
banded_contours = vtkBandedPolyDataContourFilter()
banded_contours.SetInputConnection(elevation.GetOutputPort())
banded_contours.SetScalarModeToValue()
banded_contours.GenerateContourEdgesOn()
banded_contours.GenerateValues(11, elevation.GetScalarRange())

# LookupTable: create a spectral color series for the bands
color_series = vtkColorSeries()
color_series.SetColorScheme(vtkColorSeries.BREWER_DIVERGING_SPECTRAL_11)

lut = vtkLookupTable()
color_series.BuildLookupTable(lut, vtkColorSeries.ORDINAL)

# Mapper: map banded contour data using the spectral lookup table
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(banded_contours.GetOutputPort())
cone_mapper.SetScalarRange(elevation.GetScalarRange())
cone_mapper.SetLookupTable(lut)

# Actor: assign the cone geometry
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)

# Mapper: map contour edge lines
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputData(banded_contours.GetContourEdgesOutput())
contour_mapper.SetScalarRange(elevation.GetScalarRange())
contour_mapper.SetResolveCoincidentTopologyToPolygonOffset()

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(dim_gray)

# AnnotatedCube: create a transparent cube with axis labels
annotated_cube = vtkAnnotatedCubeActor()
annotated_cube.SetFaceTextScale(0.366667)
annotated_cube.SetXPlusFaceText("X+")
annotated_cube.SetXMinusFaceText("X-")
annotated_cube.SetYPlusFaceText("Y+")
annotated_cube.SetYMinusFaceText("Y-")
annotated_cube.SetZPlusFaceText("Z+")
annotated_cube.SetZMinusFaceText("Z-")

annotated_cube.GetTextEdgesProperty().SetColor(black)
annotated_cube.GetTextEdgesProperty().SetLineWidth(1)
annotated_cube.GetXPlusFaceProperty().SetColor(turquoise)
annotated_cube.GetXMinusFaceProperty().SetColor(turquoise)
annotated_cube.GetYPlusFaceProperty().SetColor(mint)
annotated_cube.GetYMinusFaceProperty().SetColor(mint)
annotated_cube.GetZPlusFaceProperty().SetColor(tomato)
annotated_cube.GetZMinusFaceProperty().SetColor(tomato)
annotated_cube.SetXFaceTextRotation(90)
annotated_cube.SetYFaceTextRotation(180)
annotated_cube.SetZFaceTextRotation(-90)
annotated_cube.GetCubeProperty().SetOpacity(0)

# ColoredCube: create a unit cube with per-face colors
cube_source = vtkCubeSource()
cube_source.Update()

face_colors = vtkUnsignedCharArray()
face_colors.SetNumberOfComponents(3)
face_colors.InsertNextTuple3(0, 128, 0)    # X- Green
face_colors.InsertNextTuple3(255, 0, 0)    # X+ Red
face_colors.InsertNextTuple3(255, 255, 0)  # Y- Yellow
face_colors.InsertNextTuple3(0, 0, 255)    # Y+ Blue
face_colors.InsertNextTuple3(255, 0, 255)  # Z- Magenta
face_colors.InsertNextTuple3(0, 255, 255)  # Z+ Cyan

cube_source.GetOutput().GetCellData().SetScalars(face_colors)

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputData(cube_source.GetOutput())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)

# PropAssembly: combine the annotated cube text with the colored faces
prop_assembly = vtkPropAssembly()
prop_assembly.AddPart(annotated_cube)
prop_assembly.AddPart(cube_actor)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.AddActor(contour_actor)
renderer.SetBackground(misty_rose)
renderer.SetBackground2(royal_blue)
renderer.GradientBackgroundOn()
renderer.GetActiveCamera().Azimuth(45)
renderer.GetActiveCamera().Pitch(-22.5)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ColoredAnnotatedCube")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Widget 1: annotated cube orientation marker (lower left)
widget_cube = vtkOrientationMarkerWidget()
widget_cube.SetOrientationMarker(prop_assembly)
widget_cube.SetInteractor(render_window_interactor)
widget_cube.SetDefaultRenderer(renderer)
widget_cube.On()
widget_cube.InteractiveOn()

# Widget 2: labeled axes orientation marker (lower right)
axes = vtkAxesActor()
axes.SetShaftTypeToCylinder()
axes.SetXAxisLabelText("X")
axes.SetYAxisLabelText("Y")
axes.SetZAxisLabelText("Z")
axes.SetCylinderRadius(0.5 * axes.GetCylinderRadius())
axes.SetConeRadius(1.025 * axes.GetConeRadius())
axes.SetSphereRadius(1.5 * axes.GetSphereRadius())
tprop = axes.GetXAxisCaptionActor2D().GetCaptionTextProperty()
tprop.ItalicOn()
tprop.ShadowOn()
tprop.SetFontFamilyToTimes()
axes.GetYAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop)
axes.GetZAxisCaptionActor2D().GetCaptionTextProperty().ShallowCopy(tprop)

widget_axes = vtkOrientationMarkerWidget()
widget_axes.SetOrientationMarker(axes)
widget_axes.SetViewport(0.8, 0, 1.0, 0.2)
widget_axes.SetInteractor(render_window_interactor)
widget_axes.EnabledOn()
widget_axes.InteractiveOn()

# Launch the interactive visualization
render_window_interactor.Start()
