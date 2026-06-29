#!/usr/bin/env python

# Generate a rectilinear grid from field data via a write/read round-trip,
# then visualize with a warped plane, cut plane, isosurface, and streamlines.

import os
import tempfile

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkCutter,
    vtkDataObjectToDataSetFilter,
    vtkDataSetToDataObjectFilter,
    vtkFieldDataToAttributeDataFilter,
    vtkPolyDataNormals,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersGeometry import vtkRectilinearGridGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOLegacy import (
    vtkDataObjectReader,
    vtkDataObjectWriter,
    vtkDataSetReader,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Inline color helper
named_colors = vtkNamedColors()

# Read the rectilinear grid dataset
reader = vtkDataSetReader()
reader.SetFileName(os.path.join(data_dir, "RectGrid2.vtk"))

# Convert to a data object (field)
ds2do = vtkDataSetToDataObjectFilter()
ds2do.SetInputConnection(reader.GetOutputPort())

# Write the field to a temporary file
tmp_file = os.path.join(tempfile.gettempdir(), "RGridField.vtk")

writer = vtkDataObjectWriter()
writer.SetInputConnection(ds2do.GetOutputPort())
writer.SetFileName(tmp_file)
writer.Write()

# Read the field back
dor = vtkDataObjectReader()
dor.SetFileName(tmp_file)

# Convert field back to rectilinear grid
do2ds = vtkDataObjectToDataSetFilter()
do2ds.SetInputConnection(dor.GetOutputPort())
do2ds.SetDataSetTypeToRectilinearGrid()
do2ds.SetDimensionsComponent("Dimensions", 0)
do2ds.SetPointComponent(0, "XCoordinates", 0)
do2ds.SetPointComponent(1, "YCoordinates", 0)
do2ds.SetPointComponent(2, "ZCoordinates", 0)
do2ds.Update()

# Assign vectors and scalars from the field
fd2ad = vtkFieldDataToAttributeDataFilter()
fd2ad.SetInputData(do2ds.GetRectilinearGridOutput())
fd2ad.SetInputFieldToDataObjectField()
fd2ad.SetOutputAttributeDataToPointData()
fd2ad.SetVectorComponent(0, "vectors", 0)
fd2ad.SetVectorComponent(1, "vectors", 1)
fd2ad.SetVectorComponent(2, "vectors", 2)
fd2ad.SetScalarComponent(0, "scalars", 0)
fd2ad.Update()

# Warped geometry plane at z=15
plane = vtkRectilinearGridGeometryFilter()
plane.SetInputData(fd2ad.GetRectilinearGridOutput())
plane.SetExtent(0, 100, 0, 100, 15, 15)

warper = vtkWarpVector()
warper.SetInputConnection(plane.GetOutputPort())
warper.SetScaleFactor(0.05)

plane_mapper = vtkDataSetMapper()
plane_mapper.SetInputConnection(warper.GetOutputPort())
plane_mapper.SetScalarRange(0.197813, 0.710419)

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Cut plane through the center
cut_plane = vtkPlane()
cut_plane.SetOrigin(fd2ad.GetOutput().GetCenter())
cut_plane.SetNormal(1, 0, 0)

plane_cut = vtkCutter()
plane_cut.SetInputData(fd2ad.GetRectilinearGridOutput())
plane_cut.SetCutFunction(cut_plane)

cut_mapper = vtkDataSetMapper()
cut_mapper.SetInputConnection(plane_cut.GetOutputPort())
cut_mapper.SetScalarRange(
    fd2ad.GetOutput().GetPointData().GetScalars().GetRange())

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

# Isosurface at 0.7
iso = vtkContourFilter()
iso.SetInputData(fd2ad.GetRectilinearGridOutput())
iso.SetValue(0, 0.7)

iso_normals = vtkPolyDataNormals()
iso_normals.SetInputConnection(iso.GetOutputPort())
iso_normals.SetFeatureAngle(45)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso_normals.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

bisque_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("bisque", bisque_rgb)

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(bisque_rgb)
iso_actor.GetProperty().SetRepresentationToWireframe()

# Streamlines
streamer = vtkStreamTracer()
streamer.SetInputConnection(fd2ad.GetOutputPort())
streamer.SetStartPosition(-1.2, -0.1, 1.3)
streamer.SetMaximumPropagation(500)
streamer.SetInitialIntegrationStep(0.05)
streamer.SetIntegrationDirectionToBoth()

stream_tube = vtkTubeFilter()
stream_tube.SetInputConnection(streamer.GetOutputPort())
stream_tube.SetRadius(0.025)
stream_tube.SetNumberOfSides(6)
stream_tube.SetVaryRadiusToVaryRadiusByVector()

stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(stream_tube.GetOutputPort())
stream_mapper.SetScalarRange(
    fd2ad.GetOutput().GetPointData().GetScalars().GetRange())

stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)
stream_actor.GetProperty().BackfaceCullingOn()

# Outline
outline = vtkOutlineFilter()
outline.SetInputData(fd2ad.GetRectilinearGridOutput())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

black_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("black", black_rgb)

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black_rgb)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(plane_actor)
renderer.AddActor(cut_actor)
renderer.AddActor(iso_actor)
renderer.AddActor(stream_actor)
renderer.SetBackground(1, 1, 1)
# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("field to rgrid")

# Scene
renderer.GetActiveCamera().SetPosition(0.0390893, 0.184813, -3.94026)
renderer.GetActiveCamera().SetFocalPoint(-0.00578326, 0, 0.701967)
renderer.GetActiveCamera().SetViewAngle(30)
renderer.GetActiveCamera().SetViewUp(0.00850257, 0.999169, 0.0398605)
renderer.GetActiveCamera().SetClippingRange(3.08127, 6.62716)

# Cleanup temp file
try:
    os.remove(tmp_file)
except OSError:
    pass

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
