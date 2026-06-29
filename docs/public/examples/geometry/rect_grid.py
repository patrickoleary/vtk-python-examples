#!/usr/bin/env python

# Demonstrate vtkRectilinearGridGeometryFilter with warped plane,
# cut plane, contour, stream tubes, and outline on rectilinear grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkCommonExecutionModel import vtkCastToConcrete
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkCutter,
    vtkPolyDataNormals,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersGeometry import vtkRectilinearGridGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOLegacy import vtkDataSetReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

colors = vtkNamedColors()

VTK_VARY_RADIUS_BY_VECTOR = 2

# Read rectilinear grid
reader = vtkDataSetReader()
reader.SetFileName(os.path.join(data_dir, "RectGrid2.vtk"))
reader.Update()

to_rectilinear_grid = vtkCastToConcrete()
to_rectilinear_grid.SetInputConnection(reader.GetOutputPort())
to_rectilinear_grid.Update()

# Warped plane
plane = vtkRectilinearGridGeometryFilter()
plane.SetInputData(to_rectilinear_grid.GetRectilinearGridOutput())
plane.SetExtent(0, 100, 0, 100, 15, 15)

warper = vtkWarpVector()
warper.SetInputConnection(plane.GetOutputPort())
warper.SetScaleFactor(0.05)

plane_mapper = vtkDataSetMapper()
plane_mapper.SetInputConnection(warper.GetOutputPort())
plane_mapper.SetScalarRange(0.197813, 0.710419)

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Cut plane
cut_plane = vtkPlane()
cut_plane.SetOrigin(reader.GetOutput().GetCenter())
cut_plane.SetNormal(1, 0, 0)

plane_cut = vtkCutter()
plane_cut.SetInputData(to_rectilinear_grid.GetRectilinearGridOutput())
plane_cut.SetCutFunction(cut_plane)

cut_mapper = vtkDataSetMapper()
cut_mapper.SetInputConnection(plane_cut.GetOutputPort())
cut_mapper.SetScalarRange(
    reader.GetOutput().GetPointData().GetScalars().GetRange()
)

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

# Contour
iso = vtkContourFilter()
iso.SetInputData(to_rectilinear_grid.GetRectilinearGridOutput())
iso.SetValue(0, 0.7)

normals = vtkPolyDataNormals()
normals.SetInputConnection(iso.GetOutputPort())
normals.SetFeatureAngle(45)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(normals.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

bisque_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("bisque", bisque_rgb)

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(bisque_rgb)
iso_actor.GetProperty().SetRepresentationToWireframe()

# Stream tracer with tubes
streamer = vtkStreamTracer()
streamer.SetInputConnection(reader.GetOutputPort())
streamer.SetStartPosition(-1.2, -0.1, 1.3)
streamer.SetMaximumPropagation(500)
streamer.SetInitialIntegrationStep(0.05)
streamer.SetIntegrationDirectionToBoth()

stream_tube = vtkTubeFilter()
stream_tube.SetInputConnection(streamer.GetOutputPort())
stream_tube.SetRadius(0.025)
stream_tube.SetNumberOfSides(6)
stream_tube.SetVaryRadius(VTK_VARY_RADIUS_BY_VECTOR)

map_stream_tube = vtkPolyDataMapper()
map_stream_tube.SetInputConnection(stream_tube.GetOutputPort())
map_stream_tube.SetScalarRange(
    reader.GetOutput().GetPointData().GetScalars().GetRange()
)

stream_tube_actor = vtkActor()
stream_tube_actor.SetMapper(map_stream_tube)
stream_tube_actor.GetProperty().BackfaceCullingOn()

# Outline
outline = vtkOutlineFilter()
outline.SetInputData(to_rectilinear_grid.GetRectilinearGridOutput())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

black_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("black", black_rgb)

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black_rgb)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(plane_actor)
renderer.AddActor(cut_actor)
renderer.AddActor(iso_actor)
renderer.AddActor(stream_tube_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("rect grid")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

cam = renderer.GetActiveCamera()
cam.SetClippingRange(3.76213, 10.712)
cam.SetFocalPoint(-0.0842503, -0.136905, 0.610234)
cam.SetPosition(2.53813, 2.2678, -5.22172)
cam.SetViewUp(-0.241047, 0.930635, 0.275343)

render_window.Render()
interactor.Start()
