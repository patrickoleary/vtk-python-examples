#!/usr/bin/env python

# Demonstrate reading a field and converting it to PolyData via a
# write/read round-trip with vtkDataObjectToDataSetFilter.

import os
import tempfile

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkDataObjectToDataSetFilter,
    vtkDataSetToDataObjectFilter,
    vtkFieldDataToAttributeDataFilter,
)
from vtkmodules.vtkIOLegacy import (
    vtkDataObjectReader,
    vtkDataObjectWriter,
    vtkPolyDataReader,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read polydata and convert to a data object (field)
reader = vtkPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "polyEx.vtk"))

ds2do = vtkDataSetToDataObjectFilter()
ds2do.SetInputConnection(reader.GetOutputPort())

# Write the field to a temporary file
tmp_file = os.path.join(tempfile.gettempdir(), "PolyField.vtk")

writer = vtkDataObjectWriter()
writer.SetInputConnection(ds2do.GetOutputPort())
writer.SetFileName(tmp_file)
writer.Write()

# Read the field back
dor = vtkDataObjectReader()
dor.SetFileName(tmp_file)

# Convert field back to polydata
do2ds = vtkDataObjectToDataSetFilter()
do2ds.SetInputConnection(dor.GetOutputPort())
do2ds.SetDataSetTypeToPolyData()
do2ds.SetPointComponent(0, "Points", 0)
do2ds.SetPointComponent(1, "Points", 1)
do2ds.SetPointComponent(2, "Points", 2)
do2ds.SetPolysComponent("Polys", 0)

# Assign scalars from the field
fd2ad = vtkFieldDataToAttributeDataFilter()
fd2ad.SetInputConnection(do2ds.GetOutputPort())
fd2ad.SetInputFieldToDataObjectField()
fd2ad.SetOutputAttributeDataToPointData()
fd2ad.SetScalarComponent(0, "my_scalars", 0)

# Map the result
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(fd2ad.GetOutputPort())
mapper.SetScalarRange(fd2ad.GetOutput().GetScalarRange())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)
# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("field to polydata")

# Scene
renderer.ResetCamera()
cam = renderer.GetActiveCamera()
cam.SetClippingRange(0.348, 17.43)
cam.SetPosition(2.92, 2.62, -0.836)
cam.SetViewUp(-0.436, -0.067, -0.897)
cam.Azimuth(90)

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
