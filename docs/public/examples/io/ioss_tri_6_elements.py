#!/usr/bin/env python

# Read an Exodus file with Tri6 elements, hide blocks, enable sets, and render with edges.

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

# Read the Exodus file
ioss_reader = vtkIOSSReader()
ioss_reader.SetFileName(os.path.join(data_dir, "Exodus", "SAND2020-4077_O-tri6sWFace2.exo"))
ioss_reader.UpdateInformation()

# Hide blocks and enable sets
for cc in range(vtkIOSSReader.ENTITY_START, vtkIOSSReader.ENTITY_END):
    sel = ioss_reader.GetEntitySelection(cc)
    if vtkIOSSReader.GetEntityTypeIsBlock(cc):
        sel.DisableAllArrays()
    elif vtkIOSSReader.GetEntityTypeIsSet(cc):
        sel.EnableAllArrays()

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
render_window.SetWindowName("ioss tri 6 elements")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
