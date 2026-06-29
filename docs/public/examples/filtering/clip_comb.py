#!/usr/bin/env python

# Clip PLOT3D combustor data using a boolean combination of two spheres
# via vtkClipDataSet.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkImplicitBoolean,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkStructuredGridOutlineFilter
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
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

# Create a boolean implicit function from two spheres
center = output.GetCenter()

sphere = vtkSphere()
sphere.SetCenter(center)
sphere.SetRadius(2.0)

sphere_2 = vtkSphere()
sphere_2.SetCenter(center[0] + 4.0, center[1], center[2])
sphere_2.SetRadius(4.0)

bool_op = vtkImplicitBoolean()
bool_op.SetOperationTypeToUnion()
bool_op.AddFunction(sphere)
bool_op.AddFunction(sphere_2)

# Clip the structured grid
clip = vtkClipDataSet()
clip.SetInputData(output)
clip.SetClipFunction(bool_op)
clip.InsideOutOn()

gf = vtkGeometryFilter()
gf.SetInputConnection(clip.GetOutputPort())

clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(gf.GetOutputPort())

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)

# Outline
outline = vtkStructuredGridOutlineFilter()
outline.SetInputData(output)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("clip comb")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetClippingRange(3.95297, 50)
cam.SetFocalPoint(8.88908, 0.595038, 29.3342)
cam.SetPosition(-12.3332, 31.7479, 41.2387)
cam.SetViewUp(0.060772, -0.319905, 0.945498)

interactor.Initialize()
interactor.Start()
