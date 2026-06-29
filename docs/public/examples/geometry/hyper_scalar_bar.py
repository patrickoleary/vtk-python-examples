#!/usr/bin/env python

# Demonstrate vtkHyperStreamline with a vtkScalarBarActor by generating
# a point-load tensor field, creating four hyperstreamlines, and rendering
# them with a logarithmic scalar bar, context plane, outline, and load cone.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkHyperStreamline
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkImagingHybrid import vtkPointLoad
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkLogLookupTable,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

VTK_INTEGRATE_BOTH_DIRECTIONS = 2

# Generate tensor field from point load
pt_load = vtkPointLoad()
pt_load.SetLoadValue(100.0)
pt_load.SetSampleDimensions(20, 20, 20)
pt_load.ComputeEffectiveStressOn()
pt_load.SetModelBounds(-10, 10, -10, 10, -10, 10)
pt_load.Update()

# Log lookup table
lookup_table = vtkLogLookupTable()
lookup_table.SetHueRange(0.6667, 0.0)

# Scalar bar
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(lookup_table)
scalar_bar.SetTitle("Stress")
scalar_bar.GetPositionCoordinate().SetCoordinateSystemToNormalizedViewport()
scalar_bar.GetPositionCoordinate().SetValue(0.1, 0.05)
scalar_bar.SetOrientationToVertical()
scalar_bar.SetWidth(0.1)
scalar_bar.SetHeight(0.9)
scalar_bar.SetPosition(0.01, 0.1)
scalar_bar.SetLabelFormat("{:<#6.3f}")
scalar_bar.GetLabelTextProperty().SetColor(1, 0, 0)
scalar_bar.GetTitleTextProperty().SetColor(1, 0, 0)

# Hyperstreamline 1
streamline_1 = vtkHyperStreamline()
streamline_1.SetInputConnection(pt_load.GetOutputPort())
streamline_1.SetStartPosition(9, 9, -9)
streamline_1.IntegrateMinorEigenvector()
streamline_1.SetMaximumPropagationDistance(18.0)
streamline_1.SetIntegrationStepLength(0.1)
streamline_1.SetStepLength(0.01)
streamline_1.SetRadius(0.25)
streamline_1.SetNumberOfSides(18)
streamline_1.SetIntegrationDirection(VTK_INTEGRATE_BOTH_DIRECTIONS)
streamline_1.Update()

streamline_1_mapper = vtkPolyDataMapper()
streamline_1_mapper.SetInputConnection(streamline_1.GetOutputPort())
streamline_1_mapper.SetLookupTable(lookup_table)
streamline_1_mapper.SetScalarRange(pt_load.GetOutput().GetScalarRange())

streamline_1_actor = vtkActor()
streamline_1_actor.SetMapper(streamline_1_mapper)

# Hyperstreamline 2
streamline_2 = vtkHyperStreamline()
streamline_2.SetInputConnection(pt_load.GetOutputPort())
streamline_2.SetStartPosition(-9, -9, -9)
streamline_2.IntegrateMinorEigenvector()
streamline_2.SetMaximumPropagationDistance(18.0)
streamline_2.SetIntegrationStepLength(0.1)
streamline_2.SetStepLength(0.01)
streamline_2.SetRadius(0.25)
streamline_2.SetNumberOfSides(18)
streamline_2.SetIntegrationDirection(VTK_INTEGRATE_BOTH_DIRECTIONS)
streamline_2.Update()

streamline_2_mapper = vtkPolyDataMapper()
streamline_2_mapper.SetInputConnection(streamline_2.GetOutputPort())
streamline_2_mapper.SetLookupTable(lookup_table)
streamline_2_mapper.SetScalarRange(pt_load.GetOutput().GetScalarRange())

streamline_2_actor = vtkActor()
streamline_2_actor.SetMapper(streamline_2_mapper)

# Hyperstreamline 3
streamline_3 = vtkHyperStreamline()
streamline_3.SetInputConnection(pt_load.GetOutputPort())
streamline_3.SetStartPosition(9, -9, -9)
streamline_3.IntegrateMinorEigenvector()
streamline_3.SetMaximumPropagationDistance(18.0)
streamline_3.SetIntegrationStepLength(0.1)
streamline_3.SetStepLength(0.01)
streamline_3.SetRadius(0.25)
streamline_3.SetNumberOfSides(18)
streamline_3.SetIntegrationDirection(VTK_INTEGRATE_BOTH_DIRECTIONS)
streamline_3.Update()

streamline_3_mapper = vtkPolyDataMapper()
streamline_3_mapper.SetInputConnection(streamline_3.GetOutputPort())
streamline_3_mapper.SetLookupTable(lookup_table)
streamline_3_mapper.SetScalarRange(pt_load.GetOutput().GetScalarRange())

streamline_3_actor = vtkActor()
streamline_3_actor.SetMapper(streamline_3_mapper)

# Hyperstreamline 4
streamline_4 = vtkHyperStreamline()
streamline_4.SetInputConnection(pt_load.GetOutputPort())
streamline_4.SetStartPosition(-9, 9, -9)
streamline_4.IntegrateMinorEigenvector()
streamline_4.SetMaximumPropagationDistance(18.0)
streamline_4.SetIntegrationStepLength(0.1)
streamline_4.SetStepLength(0.01)
streamline_4.SetRadius(0.25)
streamline_4.SetNumberOfSides(18)
streamline_4.SetIntegrationDirection(VTK_INTEGRATE_BOTH_DIRECTIONS)
streamline_4.Update()

streamline_4_mapper = vtkPolyDataMapper()
streamline_4_mapper.SetInputConnection(streamline_4.GetOutputPort())
streamline_4_mapper.SetLookupTable(lookup_table)
streamline_4_mapper.SetScalarRange(pt_load.GetOutput().GetScalarRange())

streamline_4_actor = vtkActor()
streamline_4_actor.SetMapper(streamline_4_mapper)

# Context plane
geometry = vtkImageDataGeometryFilter()
geometry.SetInputConnection(pt_load.GetOutputPort())
geometry.SetExtent(0, 100, 0, 100, 0, 0)
geometry.Update()

geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(geometry.GetOutputPort())
geometry_mapper.SetScalarRange(geometry.GetOutput().GetScalarRange())

geometry_actor = vtkActor()
geometry_actor.SetMapper(geometry_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(pt_load.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Cone indicating point of load application
cone_src = vtkConeSource()
cone_src.SetRadius(0.5)
cone_src.SetHeight(2)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_src.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetPosition(0, 0, 11)
cone_actor.RotateY(90)
cone_actor.GetProperty().SetColor(1, 0, 0)

# Camera
camera = vtkCamera()
camera.SetFocalPoint(0.113766, -1.13665, -1.01919)
camera.SetPosition(-29.4886, -63.1488, 26.5807)
camera.SetViewAngle(24.4617)
camera.SetViewUp(0.17138, 0.331163, 0.927879)
camera.SetClippingRange(1, 100)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(scalar_bar)
renderer.AddActor(streamline_1_actor)
renderer.AddActor(streamline_2_actor)
renderer.AddActor(streamline_3_actor)
renderer.AddActor(streamline_4_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(cone_actor)
renderer.AddActor(geometry_actor)
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.SetActiveCamera(camera)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("hyper scalar bar")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
