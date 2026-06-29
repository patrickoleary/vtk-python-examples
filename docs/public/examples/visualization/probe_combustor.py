#!/usr/bin/env python

# Probe a combustor dataset with three planes and contour the resampled scalars.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkContourFilter,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gainsboro = (0.863, 0.863, 0.863)
black = (0.0, 0.0, 0.0)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load PLOT3D combustor dataset
pl3d = vtkMultiBlockPLOT3DReader()
pl3d.SetXYZFileName(str(data_dir / "combxyz.bin"))
pl3d.SetQFileName(str(data_dir / "combq.bin"))
pl3d.SetScalarFunctionNumber(100)
pl3d.SetVectorFunctionNumber(202)
pl3d.Update()

sg = pl3d.GetOutput().GetBlock(0)
scalar_range = sg.GetScalarRange()

# Source: shared plane geometry for probing
plane = vtkPlaneSource()
plane.SetResolution(50, 50)

# Transform/Filter: probe plane 0 at (3.7, 0.0, 28.37)
xform_0 = vtkTransform()
xform_0.Translate(3.7, 0.0, 28.37)
xform_0.Scale(5, 5, 5)
xform_0.RotateY(90)

tpd_0 = vtkTransformPolyDataFilter()
tpd_0.SetInputConnection(plane.GetOutputPort())
tpd_0.SetTransform(xform_0)

out_0 = vtkOutlineFilter()
out_0.SetInputConnection(tpd_0.GetOutputPort())

out_mapper_0 = vtkPolyDataMapper()
out_mapper_0.SetInputConnection(out_0.GetOutputPort())

out_actor_0 = vtkActor()
out_actor_0.SetMapper(out_mapper_0)
out_actor_0.GetProperty().SetColor(black)
out_actor_0.GetProperty().SetLineWidth(2.0)

# Transform/Filter: probe plane 1 at (9.2, 0.0, 31.20)
xform_1 = vtkTransform()
xform_1.Translate(9.2, 0.0, 31.20)
xform_1.Scale(5, 5, 5)
xform_1.RotateY(90)

tpd_1 = vtkTransformPolyDataFilter()
tpd_1.SetInputConnection(plane.GetOutputPort())
tpd_1.SetTransform(xform_1)

out_1 = vtkOutlineFilter()
out_1.SetInputConnection(tpd_1.GetOutputPort())

out_mapper_1 = vtkPolyDataMapper()
out_mapper_1.SetInputConnection(out_1.GetOutputPort())

out_actor_1 = vtkActor()
out_actor_1.SetMapper(out_mapper_1)
out_actor_1.GetProperty().SetColor(black)
out_actor_1.GetProperty().SetLineWidth(2.0)

# Transform/Filter: probe plane 2 at (13.27, 0.0, 33.30)
xform_2 = vtkTransform()
xform_2.Translate(13.27, 0.0, 33.30)
xform_2.Scale(5, 5, 5)
xform_2.RotateY(90)

tpd_2 = vtkTransformPolyDataFilter()
tpd_2.SetInputConnection(plane.GetOutputPort())
tpd_2.SetTransform(xform_2)

out_2 = vtkOutlineFilter()
out_2.SetInputConnection(tpd_2.GetOutputPort())

out_mapper_2 = vtkPolyDataMapper()
out_mapper_2.SetInputConnection(out_2.GetOutputPort())

out_actor_2 = vtkActor()
out_actor_2.SetMapper(out_mapper_2)
out_actor_2.GetProperty().SetColor(black)
out_actor_2.GetProperty().SetLineWidth(2.0)

# Filter: append the three transformed planes
append = vtkAppendPolyData()
append.AddInputConnection(tpd_0.GetOutputPort())
append.AddInputConnection(tpd_1.GetOutputPort())
append.AddInputConnection(tpd_2.GetOutputPort())

# Filter: probe the combustor with the three planes
probe = vtkProbeFilter()
probe.SetInputConnection(append.GetOutputPort())
probe.SetSourceData(sg)

# Filter: contour the probed data
contour = vtkContourFilter()
contour.SetInputConnection(probe.GetOutputPort())
contour.GenerateValues(50, scalar_range)

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.SetScalarRange(scalar_range)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Filter: outline around the structured grid
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(sg)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)
outline_actor.GetProperty().SetLineWidth(2.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(contour_actor)
renderer.AddActor(out_actor_0)
renderer.AddActor(out_actor_1)
renderer.AddActor(out_actor_2)
renderer.SetBackground(gainsboro)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("probe combustor")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Scene: configure camera
renderer.ResetCamera()
renderer.GetActiveCamera().SetClippingRange(3.95297, 50)
renderer.GetActiveCamera().SetFocalPoint(8.88908, 0.595038, 29.3342)
renderer.GetActiveCamera().SetPosition(-12.3332, 31.7479, 41.2387)
renderer.GetActiveCamera().SetViewUp(0.060772, -0.319905, 0.945498)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
