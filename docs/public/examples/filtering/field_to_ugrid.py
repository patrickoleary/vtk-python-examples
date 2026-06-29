#!/usr/bin/env python

# Read a field representing an unstructured grid via a write/read round-trip,
# then visualize a blow-molding simulation with mold wireframe, parison
# surface, and thickness contours.

import os
import tempfile

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkConnectivityFilter,
    vtkContourFilter,
    vtkDataObjectToDataSetFilter,
    vtkDataSetToDataObjectFilter,
    vtkFieldDataToAttributeDataFilter,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpVector
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOLegacy import (
    vtkDataObjectReader,
    vtkDataObjectWriter,
    vtkUnstructuredGridReader,
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

# Read unstructured grid
reader = vtkUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "blow.vtk"))
reader.SetScalarsName("thickness9")
reader.SetVectorsName("displacement9")

# Convert to field data
ds2do = vtkDataSetToDataObjectFilter()
ds2do.SetInputConnection(reader.GetOutputPort())

# Write field to temp file
tmp_file = os.path.join(tempfile.gettempdir(), "UGridField.vtk")

field_writer = vtkDataObjectWriter()
field_writer.SetInputConnection(ds2do.GetOutputPort())
field_writer.SetFileName(tmp_file)
field_writer.Write()

# Read the field back
dor = vtkDataObjectReader()
dor.SetFileName(tmp_file)

# Convert field to unstructured grid
do2ds = vtkDataObjectToDataSetFilter()
do2ds.SetInputConnection(dor.GetOutputPort())
do2ds.SetDataSetTypeToUnstructuredGrid()
do2ds.SetPointComponent(0, "Points", 0)
do2ds.SetPointComponent(1, "Points", 1)
do2ds.SetPointComponent(2, "Points", 2)
do2ds.SetCellTypeComponent("CellTypes", 0)
do2ds.SetCellConnectivityComponent("Cells", 0)
do2ds.Update()

# Assign vectors and scalars from the field
fd2ad = vtkFieldDataToAttributeDataFilter()
fd2ad.SetInputData(do2ds.GetUnstructuredGridOutput())
fd2ad.SetInputFieldToDataObjectField()
fd2ad.SetOutputAttributeDataToPointData()
fd2ad.SetVectorComponent(0, "displacement9", 0)
fd2ad.SetVectorComponent(1, "displacement9", 1)
fd2ad.SetVectorComponent(2, "displacement9", 2)
fd2ad.SetScalarComponent(0, "thickness9", 0)
fd2ad.Update()

# Warp by displacement
warp = vtkWarpVector()
warp.SetInputData(fd2ad.GetUnstructuredGridOutput())

# Extract mold (regions 0 and 1) as wireframe
connect = vtkConnectivityFilter()
connect.SetInputConnection(warp.GetOutputPort())
connect.SetExtractionModeToSpecifiedRegions()
connect.AddSpecifiedRegion(0)
connect.AddSpecifiedRegion(1)

mold_mapper = vtkDataSetMapper()
mold_mapper.SetInputConnection(connect.GetOutputPort())
mold_mapper.ScalarVisibilityOff()

mold_actor = vtkActor()
mold_actor.SetMapper(mold_mapper)
mold_actor.GetProperty().SetColor(0.2, 0.2, 0.2)
mold_actor.GetProperty().SetRepresentationToWireframe()

# Extract parison (region 2) with normals and color by thickness
connect_2 = vtkConnectivityFilter()
connect_2.SetInputConnection(warp.GetOutputPort())
connect_2.SetExtractionModeToSpecifiedRegions()
connect_2.AddSpecifiedRegion(2)

parison = vtkGeometryFilter()
parison.SetInputConnection(connect_2.GetOutputPort())

normals = vtkPolyDataNormals()
normals.SetInputConnection(parison.GetOutputPort())
normals.SetFeatureAngle(60)

lut = vtkLookupTable()
lut.SetHueRange(0.0, 0.66667)

parison_mapper = vtkPolyDataMapper()
parison_mapper.SetInputConnection(normals.GetOutputPort())
parison_mapper.SetLookupTable(lut)
parison_mapper.SetScalarRange(0.12, 1.0)

parison_actor = vtkActor()
parison_actor.SetMapper(parison_mapper)

# Contour at thickness = 0.5
cf = vtkContourFilter()
cf.SetInputConnection(connect_2.GetOutputPort())
cf.SetValue(0, 0.5)

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(cf.GetOutputPort())

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mold_actor)
renderer.AddActor(parison_actor)
renderer.AddActor(contour_actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(380, 200)
render_window.SetMultiSamples(0)
render_window.SetWindowName("field to ugrid")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(60)
renderer.GetActiveCamera().Roll(-90)
renderer.GetActiveCamera().Dolly(2)
renderer.ResetCameraClippingRange()

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
