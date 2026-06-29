#!/usr/bin/env python

# Split PLOT3D velocity vectors into components, contour each, merge
# them back, and trace a ribbon streamline using vtkSplitField and
# vtkMergeFields.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkAssignAttribute,
    vtkContourFilter,
    vtkMergeFields,
    vtkPolyDataNormals,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeneral import vtkSplitField
from vtkmodules.vtkFiltersModeling import vtkRibbonFilter
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

# Read PLOT3D combustor data
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
pl3d.SetQFileName(os.path.join(data_dir, "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

output = pl3d.GetOutput().GetBlock(0)

# Split vector field into components
sf = vtkSplitField()
sf.SetInputData(output)
sf.SetInputField("VECTORS", "POINT_DATA")
sf.Split(0, "vx")
sf.Split(1, "vy")
sf.Split(2, "vz")

# Iso-contour of vx component
aax = vtkAssignAttribute()
aax.SetInputConnection(sf.GetOutputPort())
aax.Assign("vx", "SCALARS", "POINT_DATA")

iso_vx = vtkContourFilter()
iso_vx.SetInputConnection(aax.GetOutputPort())
iso_vx.SetValue(0, 0.38)

normals_vx = vtkPolyDataNormals()
normals_vx.SetInputConnection(iso_vx.GetOutputPort())
normals_vx.SetFeatureAngle(45)

iso_vx_mapper = vtkPolyDataMapper()
iso_vx_mapper.SetInputConnection(normals_vx.GetOutputPort())
iso_vx_mapper.ScalarVisibilityOff()

iso_vx_actor = vtkActor()
iso_vx_actor.SetMapper(iso_vx_mapper)
iso_vx_actor.GetProperty().SetColor(1, 0.7, 0.6)

# Iso-contour of vy component
aay = vtkAssignAttribute()
aay.SetInputConnection(sf.GetOutputPort())
aay.Assign("vy", "SCALARS", "POINT_DATA")

iso_vy = vtkContourFilter()
iso_vy.SetInputConnection(aay.GetOutputPort())
iso_vy.SetValue(0, 0.38)

normals_vy = vtkPolyDataNormals()
normals_vy.SetInputConnection(iso_vy.GetOutputPort())
normals_vy.SetFeatureAngle(45)

iso_vy_mapper = vtkPolyDataMapper()
iso_vy_mapper.SetInputConnection(normals_vy.GetOutputPort())
iso_vy_mapper.ScalarVisibilityOff()

iso_vy_actor = vtkActor()
iso_vy_actor.SetMapper(iso_vy_mapper)
iso_vy_actor.GetProperty().SetColor(0.7, 1, 0.6)

# Iso-contour of vz component
aaz = vtkAssignAttribute()
aaz.SetInputConnection(sf.GetOutputPort())
aaz.Assign("vz", "SCALARS", "POINT_DATA")

iso_vz = vtkContourFilter()
iso_vz.SetInputConnection(aaz.GetOutputPort())
iso_vz.SetValue(0, 0.38)

normals_vz = vtkPolyDataNormals()
normals_vz.SetInputConnection(iso_vz.GetOutputPort())
normals_vz.SetFeatureAngle(45)

iso_vz_mapper = vtkPolyDataMapper()
iso_vz_mapper.SetInputConnection(normals_vz.GetOutputPort())
iso_vz_mapper.ScalarVisibilityOff()

iso_vz_actor = vtkActor()
iso_vz_actor.SetMapper(iso_vz_mapper)
iso_vz_actor.GetProperty().SetColor(0.4, 0.5, 1)

# Merge components back and stream-trace with ribbon
mf = vtkMergeFields()
mf.SetInputConnection(sf.GetOutputPort())
mf.SetOutputField("merged", "POINT_DATA")
mf.SetNumberOfComponents(3)
mf.Merge(0, "vy", 0)
mf.Merge(1, "vz", 0)
mf.Merge(2, "vx", 0)

aa = vtkAssignAttribute()
aa.SetInputConnection(mf.GetOutputPort())
aa.Assign("merged", "SCALARS", "POINT_DATA")

aa2 = vtkAssignAttribute()
aa2.SetInputConnection(aa.GetOutputPort())
aa2.Assign("SCALARS", "VECTORS", "POINT_DATA")

sl = vtkStreamTracer()
sl.SetInputConnection(aa2.GetOutputPort())
sl.SetStartPosition(2, -2, 26)
sl.SetMaximumPropagation(40)
sl.SetInitialIntegrationStep(0.2)
sl.SetIntegrationDirectionToForward()

rf = vtkRibbonFilter()
rf.SetInputConnection(sl.GetOutputPort())
rf.SetWidth(1.0)
rf.SetWidthFactor(5)

sl_mapper = vtkPolyDataMapper()
sl_mapper.SetInputConnection(rf.GetOutputPort())

sl_actor = vtkActor()
sl_actor.SetMapper(sl_mapper)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(iso_vx_actor)
iso_vx_actor.AddPosition(0, 12, 0)
renderer.AddActor(iso_vy_actor)
renderer.AddActor(iso_vz_actor)
iso_vz_actor.AddPosition(0, -12, 0)
renderer.AddActor(sl_actor)
sl_actor.AddPosition(0, 24, 0)
renderer.AddActor(outline_actor)
outline_actor.AddPosition(0, 24, 0)
renderer.SetBackground(0.8, 0.8, 0.8)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(320, 320)
render_window.SetWindowName("split vectors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(-20.3093, 20.55444, 64.3922)
renderer.GetActiveCamera().SetFocalPoint(8.255, 0.0499763, 29.7631)
renderer.GetActiveCamera().SetViewAngle(30)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.GetActiveCamera().Dolly(0.4)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
