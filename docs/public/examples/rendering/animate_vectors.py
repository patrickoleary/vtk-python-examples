#!/usr/bin/env python

# Animate vector field motion using texture map animation.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkGlyph3D,
    vtkThresholdPoints,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)
wheat_rgb = (0.961, 0.871, 0.702)

# Data: locate the carotid dataset and vector animation texture maps
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
carotid_file = str(data_dir / "carotid.vtk")

# Source: read the carotid artery structured points dataset
reader = vtkStructuredPointsReader()
reader.SetFileName(carotid_file)

# ThresholdPoints: keep only points with scalar value above 200
threshold = vtkThresholdPoints()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.SetUpperThreshold(200)
threshold.SetThresholdFunction(threshold.THRESHOLD_UPPER)

# LineSource: a single line segment used as the glyph shape
line = vtkLineSource()
line.SetResolution(1)

# Glyph3D: place line glyphs at each thresholded point, scaled by scalar
lines = vtkGlyph3D()
lines.SetInputConnection(threshold.GetOutputPort())
lines.SetSourceConnection(line.GetOutputPort())
lines.SetScaleFactor(0.005)
lines.SetScaleModeToScaleByScalar()
lines.Update()

# Mapper: map the glyphs
vector_mapper = vtkPolyDataMapper()
vector_mapper.SetInputConnection(lines.GetOutputPort())
vector_mapper.SetScalarRange(lines.GetOutput().GetScalarRange())

# Actor: display the vector glyphs
vector_actor = vtkActor()
vector_actor.SetMapper(vector_mapper)
vector_actor.GetProperty().SetOpacity(0.99)
vector_actor.GetProperty().SetLineWidth(1.5)

# Outline: wireframe bounding box for context
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(black_rgb)

# TextureMaps: load the 7 vector animation texture maps (vecAnim2-8).
# Each texture has an intensity gradient that, when cycled frame-by-frame,
# creates the illusion of motion along the vector field.
tmap_2 = vtkStructuredPointsReader()
tmap_2.SetFileName(str(data_dir / "VectorAnimation" / "vecAnim2.vtk"))
texture_2 = vtkTexture()
texture_2.SetInputConnection(tmap_2.GetOutputPort())
texture_2.InterpolateOff()
texture_2.RepeatOff()

tmap_3 = vtkStructuredPointsReader()
tmap_3.SetFileName(str(data_dir / "VectorAnimation" / "vecAnim3.vtk"))
texture_3 = vtkTexture()
texture_3.SetInputConnection(tmap_3.GetOutputPort())
texture_3.InterpolateOff()
texture_3.RepeatOff()

tmap_4 = vtkStructuredPointsReader()
tmap_4.SetFileName(str(data_dir / "VectorAnimation" / "vecAnim4.vtk"))
texture_4 = vtkTexture()
texture_4.SetInputConnection(tmap_4.GetOutputPort())
texture_4.InterpolateOff()
texture_4.RepeatOff()

tmap_5 = vtkStructuredPointsReader()
tmap_5.SetFileName(str(data_dir / "VectorAnimation" / "vecAnim5.vtk"))
texture_5 = vtkTexture()
texture_5.SetInputConnection(tmap_5.GetOutputPort())
texture_5.InterpolateOff()
texture_5.RepeatOff()

tmap_6 = vtkStructuredPointsReader()
tmap_6.SetFileName(str(data_dir / "VectorAnimation" / "vecAnim6.vtk"))
texture_6 = vtkTexture()
texture_6.SetInputConnection(tmap_6.GetOutputPort())
texture_6.InterpolateOff()
texture_6.RepeatOff()

tmap_7 = vtkStructuredPointsReader()
tmap_7.SetFileName(str(data_dir / "VectorAnimation" / "vecAnim7.vtk"))
texture_7 = vtkTexture()
texture_7.SetInputConnection(tmap_7.GetOutputPort())
texture_7.InterpolateOff()
texture_7.RepeatOff()

tmap_8 = vtkStructuredPointsReader()
tmap_8.SetFileName(str(data_dir / "VectorAnimation" / "vecAnim8.vtk"))
texture_8 = vtkTexture()
texture_8.SetInputConnection(tmap_8.GetOutputPort())
texture_8.InterpolateOff()
texture_8.RepeatOff()

texture_maps = [texture_2, texture_3, texture_4, texture_5, texture_6, texture_7, texture_8]
vector_actor.SetTexture(texture_2)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(vector_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(wheat_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("animate vectors")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Scene: position the camera
cam = vtkCamera()
cam.SetClippingRange(17.4043, 870.216)
cam.SetFocalPoint(136.71, 104.025, 23)
cam.SetPosition(204.747, 258.939, 63.7925)
cam.SetViewUp(-0.102647, -0.210897, 0.972104)
cam.Zoom(1.2)
renderer.SetActiveCamera(cam)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Animation: cycle through texture maps to simulate vector field motion
for j in range(100):
    for texture in texture_maps:
        vector_actor.SetTexture(texture)
        render_window.Render()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
