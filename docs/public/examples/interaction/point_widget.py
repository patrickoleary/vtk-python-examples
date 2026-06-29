#!/usr/bin/env python
# Demonstrate vtkPointWidget probing PLOT3D data with a cone glyph showing vector direction.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkProbeFilter,
    vtkStructuredGridOutlineFilter,
)
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionWidgets import vtkPointWidget
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

plot3d_reader = vtkMultiBlockPLOT3DReader()
plot3d_reader.SetXYZFileName(os.path.join(data_dir, "combxyz.bin"))
plot3d_reader.SetQFileName(os.path.join(data_dir, "combq.bin"))
plot3d_reader.SetScalarFunctionNumber(100)
plot3d_reader.SetVectorFunctionNumber(202)
plot3d_reader.Update()
plot3d_block0 = plot3d_reader.GetOutput().GetBlock(0)

point = vtkPolyData()

# Filter
probe = vtkProbeFilter()
probe.SetInputData(point)
probe.SetSourceData(plot3d_block0)

cone = vtkConeSource()
cone.SetResolution(16)

glyph = vtkGlyph3D()
glyph.SetInputConnection(probe.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseVector()
glyph.SetScaleModeToDataScalingOff()
glyph.SetScaleFactor(plot3d_block0.GetLength() * 0.1)

outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(plot3d_block0)

# Mapper + Actor (glyph)
glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.VisibilityOff()

# Mapper + Actor (outline)
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("point widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates probe point and makes glyph visible
def point_callback(caller, event_string):
    caller.GetPolyData(point)
    glyph_actor.VisibilityOn()


# Widget
point_widget = vtkPointWidget()
point_widget.SetInteractor(interactor)
point_widget.SetInputData(plot3d_block0)
point_widget.AllOff()
point_widget.PlaceWidget()
point_widget.AddObserver("InteractionEvent", point_callback)
point_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
