#!/usr/bin/env python

# Read EnSight RectGrid binary case with plane extraction, contour, streamlines, and tube filter.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkCommonExecutionModel import vtkCastToConcrete
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkCutter,
    vtkPolyDataNormals,
    vtkTriangleFilter,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersGeometry import vtkRectilinearGridGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOEnSight import vtkGenericEnSightReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
colors = vtkNamedColors()

VTK_VARY_RADIUS_BY_VECTOR = 2

# Read EnSight case file
ensight_reader = vtkGenericEnSightReader()
ensight_reader.SetCaseFileName(os.path.join(data_dir, "EnSight", "RectGrid_bin.case"))
ensight_reader.Update()

# Cast to rectilinear grid
cast_filter = vtkCastToConcrete()
cast_filter.SetInputData(ensight_reader.GetOutput().GetBlock(0))
cast_filter.Update()

# Plane extraction with warp
rect_grid_filter = vtkRectilinearGridGeometryFilter()
rect_grid_filter.SetInputData(cast_filter.GetRectilinearGridOutput())
rect_grid_filter.SetExtent(0, 100, 0, 100, 15, 15)

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(rect_grid_filter.GetOutputPort())

warp_vector = vtkWarpVector()
warp_vector.SetInputConnection(triangle_filter.GetOutputPort())
warp_vector.SetScaleFactor(0.05)

plane_mapper = vtkDataSetMapper()
plane_mapper.SetInputConnection(warp_vector.GetOutputPort())
plane_mapper.SetScalarRange(0.197813, 0.710419)

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Cut plane
cut_plane = vtkPlane()
cut_plane.SetOrigin(ensight_reader.GetOutput().GetBlock(0).GetCenter())
cut_plane.SetNormal(1, 0, 0)

plane_cut = vtkCutter()
plane_cut.SetInputData(cast_filter.GetRectilinearGridOutput())
plane_cut.SetCutFunction(cut_plane)

cut_mapper = vtkDataSetMapper()
cut_mapper.SetInputConnection(plane_cut.GetOutputPort())
cut_mapper.SetScalarRange(
    ensight_reader.GetOutput().GetBlock(0).GetPointData().GetScalars().GetRange())

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

# Isosurface
contour_filter = vtkContourFilter()
contour_filter.SetInputData(cast_filter.GetRectilinearGridOutput())
contour_filter.SetValue(0, 0.7)

normals_filter = vtkPolyDataNormals()
normals_filter.SetInputConnection(contour_filter.GetOutputPort())
normals_filter.SetFeatureAngle(45)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(normals_filter.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

bisque_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("bisque", bisque_rgb)

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(bisque_rgb)
iso_actor.GetProperty().SetRepresentationToWireframe()

# Stream tube
stream_tracer = vtkStreamTracer()
stream_tracer.SetInputData(ensight_reader.GetOutput().GetBlock(0))
stream_tracer.SetStartPosition(-1.2, -0.1, 1.3)
stream_tracer.SetMaximumPropagation(500)
stream_tracer.SetInitialIntegrationStep(0.05)
stream_tracer.SetIntegrationDirectionToBoth()

stream_tube = vtkTubeFilter()
stream_tube.SetInputConnection(stream_tracer.GetOutputPort())
stream_tube.SetRadius(0.025)
stream_tube.SetNumberOfSides(6)
stream_tube.SetVaryRadius(VTK_VARY_RADIUS_BY_VECTOR)

stream_tube_mapper = vtkPolyDataMapper()
stream_tube_mapper.SetInputConnection(stream_tube.GetOutputPort())
stream_tube_mapper.SetScalarRange(
    ensight_reader.GetOutput().GetBlock(0).GetPointData().GetScalars().GetRange())

stream_tube_actor = vtkActor()
stream_tube_actor.SetMapper(stream_tube_mapper)
stream_tube_actor.GetProperty().BackfaceCullingOn()

# Outline
outline_filter = vtkOutlineFilter()
outline_filter.SetInputData(cast_filter.GetRectilinearGridOutput())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

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

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ensight rect grid bin")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(3.76213, 10.712)
camera.SetFocalPoint(-0.0842503, -0.136905, 0.610234)
camera.SetPosition(2.53813, 2.2678, -5.22172)
camera.SetViewUp(-0.241047, 0.930635, 0.275343)

interactor.Initialize()
interactor.Start()
