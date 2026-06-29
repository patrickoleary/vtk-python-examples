#!/usr/bin/env python
# Demonstrate vtkScalarBarWidget with PLOT3D data and interactive scalar bar repositioning.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkInteractionWidgets import vtkScalarBarWidget
from vtkmodules.vtkIOParallel import vtkMultiBlockPLOT3DReader
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor  # noqa: F401
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
plot3d_block = plot3d_reader.GetOutput().GetBlock(0)

# Filter
geometry_filter = vtkStructuredGridGeometryFilter()
geometry_filter.SetInputData(plot3d_block)
geometry_filter.SetExtent(0, 100, 0, 100, 9, 9)

# Mapper + Actor
geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(geometry_filter.GetOutputPort())

geometry_actor = vtkActor()
geometry_actor.SetMapper(geometry_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(geometry_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("widgets scalar bar widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
scalar_bar_widget = vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(interactor)
scalar_bar_widget.GetScalarBarActor().SetTitle("Temperature")
scalar_bar_widget.GetScalarBarActor().SetLookupTable(geometry_mapper.GetLookupTable())
scalar_bar_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
