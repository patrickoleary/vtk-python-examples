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

# Three probe plane positions: (translate_x, translate_y, translate_z)
plane_positions = [
    (3.7, 0.0, 28.37),
    (9.2, 0.0, 31.20),
    (13.27, 0.0, 33.30),
]

append = vtkAppendPolyData()
plane_outline_actors = []

for tx, ty, tz in plane_positions:
    xform = vtkTransform()
    xform.Translate(tx, ty, tz)
    xform.Scale(5, 5, 5)
    xform.RotateY(90)

    tpd = vtkTransformPolyDataFilter()
    tpd.SetInputConnection(plane.GetOutputPort())
    tpd.SetTransform(xform)

    append.AddInputConnection(tpd.GetOutputPort())

    # Outline of each probe plane
    out = vtkOutlineFilter()
    out.SetInputConnection(tpd.GetOutputPort())

    out_mapper = vtkPolyDataMapper()
    out_mapper.SetInputConnection(out.GetOutputPort())

    out_actor = vtkActor()
    out_actor.SetMapper(out_mapper)
    out_actor.GetProperty().SetColor(black)
    out_actor.GetProperty().SetLineWidth(2.0)
    plane_outline_actors.append(out_actor)

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
for a in plane_outline_actors:
    renderer.AddActor(a)
renderer.SetBackground(gainsboro)
renderer.ResetCamera()
renderer.GetActiveCamera().SetClippingRange(3.95297, 50)
renderer.GetActiveCamera().SetFocalPoint(8.88908, 0.595038, 29.3342)
renderer.GetActiveCamera().SetPosition(-12.3332, 31.7479, 41.2387)
renderer.GetActiveCamera().SetViewUp(0.060772, -0.319905, 0.945498)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ProbeCombustor")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
