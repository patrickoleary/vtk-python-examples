#!/usr/bin/env python

# Generate a structured grid from field data via a write/read round-trip
# using PLOT3D combustor data, then visualize with an isosurface and outline.

import os
import tempfile

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkDataObjectToDataSetFilter,
    vtkDataSetToDataObjectFilter,
    vtkFieldDataToAttributeDataFilter,
    vtkPolyDataNormals,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkIOLegacy import (
    vtkDataObjectReader,
    vtkDataObjectWriter,
    vtkStructuredGridReader,
    vtkStructuredGridWriter,
)
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
tmp_dir = tempfile.gettempdir()

# Inline color helper
named_colors = vtkNamedColors()
bisque_rgb = [0.0, 0.0, 0.0]
named_colors.GetColorRGB("bisque", bisque_rgb)

# Read PLOT3D data and write as structured grid
comb = vtkMultiBlockPLOT3DReader()
comb.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
comb.SetQFileName(os.path.join(data_dir, "combq.bin"))
comb.SetScalarFunctionNumber(100)
comb.Update()

output = comb.GetOutput().GetBlock(0)

tmp_sg = os.path.join(tmp_dir, "combsg.vtk")
wsg = vtkStructuredGridWriter()
wsg.SetInputData(output)
wsg.SetFileTypeToBinary()
wsg.SetFileName(tmp_sg)
wsg.Write()

# Read the structured grid back
pl3d = vtkStructuredGridReader()
pl3d.SetFileName(tmp_sg)

# Convert to field data
ds2do = vtkDataSetToDataObjectFilter()
ds2do.SetInputConnection(pl3d.GetOutputPort())

tmp_field = os.path.join(tmp_dir, "SGridField.vtk")
field_writer = vtkDataObjectWriter()
field_writer.SetInputConnection(ds2do.GetOutputPort())
field_writer.SetFileName(tmp_field)
field_writer.Write()

# Read the field back
dor = vtkDataObjectReader()
dor.SetFileName(tmp_field)

# Convert field to structured grid
do2ds = vtkDataObjectToDataSetFilter()
do2ds.SetInputConnection(dor.GetOutputPort())
do2ds.SetDataSetTypeToStructuredGrid()
do2ds.SetDimensionsComponent("Dimensions", 0)
do2ds.SetPointComponent(0, "Points", 0)
do2ds.SetPointComponent(1, "Points", 1)
do2ds.SetPointComponent(2, "Points", 2)
do2ds.Update()

# Assign vectors and scalars from the field
fd2ad = vtkFieldDataToAttributeDataFilter()
fd2ad.SetInputData(do2ds.GetStructuredGridOutput())
fd2ad.SetInputFieldToDataObjectField()
fd2ad.SetOutputAttributeDataToPointData()
fd2ad.SetVectorComponent(0, "Momentum", 0)
fd2ad.SetVectorComponent(1, "Momentum", 1)
fd2ad.SetVectorComponent(2, "Momentum", 2)
fd2ad.SetScalarComponent(0, "Density", 0)
fd2ad.Update()

# Isosurface at density = 0.38
iso = vtkContourFilter()
iso.SetInputConnection(fd2ad.GetOutputPort())
iso.SetValue(0, 0.38)

normals = vtkPolyDataNormals()
normals.SetInputConnection(iso.GetOutputPort())
normals.SetFeatureAngle(45)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(normals.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(bisque_rgb)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(fd2ad.GetStructuredGridOutput())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("field to sgrid")

# Scene
cam = renderer.GetActiveCamera()
cam.SetClippingRange(3.95297, 50)
cam.SetFocalPoint(9.71821, 0.458166, 29.3999)
cam.SetPosition(2.7439, -37.3196, 38.7167)
cam.SetViewUp(-0.16123, 0.264271, 0.950876)

# Cleanup temp files
for f in [tmp_sg, tmp_field]:
    try:
        os.remove(f)
    except OSError:
        pass

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
