#!/usr/bin/env python

# Read a CGNS file with IOSS reader, enable IDs and side sets, and render with edges.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOIOSS import vtkIOSSReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the CGNS file
ioss_reader = vtkIOSSReader()
ioss_reader.ReadIdsOn()
ioss_reader.AddFileName(os.path.join(data_dir, "CGNS", "fluid.cgns.4.0"))
ioss_reader.GenerateFileIdOn()
ioss_reader.UpdateInformation()
ioss_reader.GetSideSetSelection().EnableAllArrays()
ioss_reader.Update()

# Extract surface
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(ioss_reader.GetOutputPort())

# Mapper
surface_mapper = vtkCompositePolyDataMapper()
surface_mapper.SetInputConnection(surface_filter.GetOutputPort())

# Actor with edge visibility
actor = vtkActor()
actor.SetMapper(surface_mapper)
actor.GetProperty().EdgeVisibilityOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("iosscgns")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(10.0, 10.0, 5.0)
camera.SetViewUp(0.0, 0.4, 1.0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
