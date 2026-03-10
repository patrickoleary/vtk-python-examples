#!/usr/bin/env python

# Glyph cone spikes along surface normals of a face mesh.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkMaskPoints,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
flesh = (1.000, 0.490, 0.250)
emerald_green = (0.000, 0.789, 0.340)
slate_gray = (0.439, 0.502, 0.565)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "fran_cut.vtk")

# Reader: load the face mesh from a Cyberware laser digitizer scan
fran = vtkPolyDataReader()
fran.SetFileName(file_name)

# Filter: compute and flip surface normals to point outward
fran_normals = vtkPolyDataNormals()
fran_normals.SetInputConnection(fran.GetOutputPort())
fran_normals.FlipNormalsOn()

# Mapper: map the face surface to graphics primitives
fran_mapper = vtkPolyDataMapper()
fran_mapper.SetInputConnection(fran_normals.GetOutputPort())

# Actor: display the face surface
fran_actor = vtkActor()
fran_actor.SetMapper(fran_mapper)
fran_actor.GetProperty().SetColor(flesh)

# Filter: subsample every 10th point for glyphing
mask = vtkMaskPoints()
mask.SetInputConnection(fran_normals.GetOutputPort())
mask.SetOnRatio(10)
mask.RandomModeOn()

# Source: cone glyph translated so the base is at the origin
cone = vtkConeSource()
cone.SetResolution(6)

cone_transform = vtkTransform()
cone_transform.Translate(0.5, 0.0, 0.0)

cone_transformed = vtkTransformPolyDataFilter()
cone_transformed.SetInputConnection(cone.GetOutputPort())
cone_transformed.SetTransform(cone_transform)

# Filter: place oriented cone glyphs at subsampled surface points
glyph = vtkGlyph3D()
glyph.SetInputConnection(mask.GetOutputPort())
glyph.SetSourceConnection(cone_transformed.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.004)

# Mapper: map the glyphs to graphics primitives
spike_mapper = vtkPolyDataMapper()
spike_mapper.SetInputConnection(glyph.GetOutputPort())

# Actor: display the spike glyphs
spike_actor = vtkActor()
spike_actor.SetMapper(spike_mapper)
spike_actor.GetProperty().SetColor(emerald_green)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(fran_actor)
renderer.AddActor(spike_actor)
renderer.SetBackground(slate_gray)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.4)
renderer.GetActiveCamera().Azimuth(110)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("SpikeFran")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
