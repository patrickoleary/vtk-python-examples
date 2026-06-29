#!/usr/bin/env python

# Read an Exodus file with IOSS reader, select side sets, clip, and render PressureRMS.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
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
ioss_reader.AddFileName(os.path.join(data_dir, "Exodus", "biplane_rms_pressure_bs.exo"))
ioss_reader.UpdateInformation()
ioss_reader.GetElementBlockSelection().DisableAllArrays()
ioss_reader.GetSideSetSelection().EnableArray("surface_10")
ioss_reader.GetSideSetFieldSelection().EnableAllArrays()

# Clip with a plane
clip_plane = vtkPlane()
clip_plane.SetNormal(1, 0, 0)
clip_plane.SetOrigin(0, 0, 0)

clip_filter = vtkClipDataSet()
clip_filter.SetInputConnection(ioss_reader.GetOutputPort())
clip_filter.SetClipFunction(clip_plane)

# Extract surface
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputConnection(clip_filter.GetOutputPort())

# Mapper
surface_mapper = vtkCompositePolyDataMapper()
surface_mapper.SetInputConnection(surface_filter.GetOutputPort())
surface_mapper.SetScalarModeToUseCellFieldData()
surface_mapper.SelectColorArray("PressureRMS")
surface_mapper.ScalarVisibilityOn()
surface_mapper.UseLookupTableScalarRangeOff()
surface_mapper.SetScalarRange(0, 1)

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
render_window.SetWindowName("ioss exodus set arrays")
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
