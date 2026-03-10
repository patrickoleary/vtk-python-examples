#!/usr/bin/env python

# Visualize carotid artery blood flow using cone glyphs oriented by velocity.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkGlyph3D,
    vtkMaskPoints,
    vtkThresholdPoints,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
wheat = (0.961, 0.871, 0.702)
black = (0.0, 0.0, 0.0)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load carotid artery structured points
reader = vtkStructuredPointsReader()
reader.SetFileName(str(data_dir / "carotid.vtk"))

# Filter: threshold to keep only high-speed points
threshold = vtkThresholdPoints()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.SetUpperThreshold(200)
threshold.SetThresholdFunction(threshold.THRESHOLD_UPPER)

# Filter: subsample points for glyph placement
mask = vtkMaskPoints()
mask.SetInputConnection(threshold.GetOutputPort())
mask.SetOnRatio(5)

# Source: cone geometry for the glyphs
cone = vtkConeSource()
cone.SetResolution(11)
cone.SetHeight(1)
cone.SetRadius(0.25)

# Filter: place cone glyphs oriented and scaled by velocity
cones = vtkGlyph3D()
cones.SetInputConnection(mask.GetOutputPort())
cones.SetSourceConnection(cone.GetOutputPort())
cones.SetScaleFactor(0.4)
cones.SetScaleModeToScaleByVector()
cones.Update()

scalar_range = cones.GetOutput().GetPointData().GetScalars().GetRange()

# Lookup table: hue-based color mapping
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)
lut.Build()

# Mapper: color cone glyphs by scalar
vector_mapper = vtkPolyDataMapper()
vector_mapper.SetInputConnection(cones.GetOutputPort())
vector_mapper.SetScalarRange(scalar_range)
vector_mapper.SetLookupTable(lut)

# Actor: display the cone glyphs
vector_actor = vtkActor()
vector_actor.SetMapper(vector_mapper)

# Filter: speed contour for context
iso = vtkContourFilter()
iso.SetInputConnection(reader.GetOutputPort())
iso.SetValue(0, 175)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetRepresentationToWireframe()
iso_actor.GetProperty().SetOpacity(0.25)

# Filter: outline around the data
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black)

# Camera: configure the viewpoint
camera = vtkCamera()
camera.SetClippingRange(17.4043, 870.216)
camera.SetFocalPoint(136.71, 104.025, 23)
camera.SetPosition(204.747, 258.939, 63.7925)
camera.SetViewUp(-0.102647, -0.210897, 0.972104)
camera.Zoom(1.2)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(vector_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(wheat)
renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("CarotidFlowGlyphs")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
