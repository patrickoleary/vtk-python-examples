#!/usr/bin/env python

# Create a 3D cursor with shadows over PLOT3D combustor data, probing
# the velocity field and displaying a cone glyph at the focal point.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkCursor3D
from vtkmodules.vtkFiltersSources import vtkConeSource
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
reader = vtkMultiBlockPLOT3DReader()
reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
reader.SetScalarFunctionNumber(110)
reader.Update()

output = reader.GetOutput().GetBlock(0)

# Outline
outline_filter = vtkStructuredGridOutlineFilter()
outline_filter.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# 3D cursor with axes, outline, and shadows
cursor = vtkCursor3D()
cursor.SetModelBounds(output.GetBounds())
cursor.SetFocalPoint(output.GetCenter())
cursor.AllOff()
cursor.AxesOn()
cursor.OutlineOn()
cursor.XShadowsOn()
cursor.YShadowsOn()
cursor.ZShadowsOn()

cursor_mapper = vtkPolyDataMapper()
cursor_mapper.SetInputConnection(cursor.GetOutputPort())

cursor_actor = vtkActor()
cursor_actor.SetMapper(cursor_mapper)
cursor_actor.GetProperty().SetColor(1, 0, 0)

# Probe the data at the cursor focus
probe = vtkProbeFilter()
probe.SetInputData(cursor.GetFocus())
probe.SetSourceData(output)

# Cone glyph at the probe point
cone = vtkConeSource()
cone.SetResolution(16)
cone.SetRadius(0.25)

glyph = vtkGlyph3D()
glyph.SetInputConnection(probe.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseVector()
glyph.SetScaleModeToScaleByScalar()
glyph.SetScaleFactor(0.0002)

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(cursor_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(200, 200)
render_window.SetWindowName("general cursor3d")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(60)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
