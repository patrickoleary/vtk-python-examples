#!/usr/bin/env python

# Read Exodus file with shared-face polyhedra, extract surface, and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkDataSetAttributes
from vtkmodules.vtkFiltersCore import vtkAssignAttribute
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Exodus file
exodus_reader = vtkExodusIIReader()
exodus_reader.SetFileName(os.path.join(data_dir, "shared_face_polyhedra.exo"))
exodus_reader.Update()

# Extract surface
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(exodus_reader.GetOutputPort())
surface_filter.Update()

# Assign ObjectId as scalars
assign_attribute = vtkAssignAttribute()
assign_attribute.SetInputConnection(surface_filter.GetOutputPort())
assign_attribute.Assign("ObjectId", vtkDataSetAttributes.SCALARS, vtkAssignAttribute.CELL_DATA)
assign_attribute.Update()

# Mapper
composite_mapper = vtkCompositePolyDataMapper()
composite_mapper.SetInputConnection(assign_attribute.GetOutputPort())
composite_mapper.SetScalarVisibility(True)
composite_mapper.SetScalarRange(10000, 20000)
composite_mapper.UseLookupTableScalarRangeOff()

# Actor
exodus_actor = vtkActor()
exodus_actor.SetMapper(composite_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(exodus_actor)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("exodus polyhedra again")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(4.45025631439989, -0.520617222824798, 1.08873910981941)
camera.SetFocalPoint(-0.441087924633898, 1.43633923685504, -1.32653110659694)
camera.SetViewUp(-0.424967955165741, 0.0530900205407349, 0.903650201572065)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
