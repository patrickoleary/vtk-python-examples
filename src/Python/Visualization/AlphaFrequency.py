#!/usr/bin/env python

# Linearly extrude letter glyphs to visualize character frequency in a text file.

import os
import re
from collections import Counter
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersModeling import vtkLinearExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Colors (normalized RGB)
peacock = (0.200, 0.631, 0.788)
silver = (0.753, 0.753, 0.753)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_path = data_dir / "Gettysburg.txt"

# Read the file and calculate the frequency of each letter
with open(file_path) as f:
    freq = Counter()
    for line in f:
        cleaned = re.sub(r"[\d_]", "", line.strip().lower())
        freq += Counter(re.findall(r"\w", cleaned, re.UNICODE))
max_freq = max(freq.values())
keys = list("abcdefghijklmnopqrstuvwxyz")

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.SetBackground(silver)

# Build one extruded letter actor per character
actors = []
for i, k in enumerate(keys):
    # ---- Source: generate vector text for the letter ----
    text = vtkVectorText()
    text.SetText(k.upper())

    # ---- Filter: linearly extrude by frequency ----
    extrude = vtkLinearExtrusionFilter()
    extrude.SetInputConnection(text.GetOutputPort())
    extrude.SetExtrusionTypeToVectorExtrusion()
    extrude.SetVector(0, 0, 1.0)
    extrude.SetScaleFactor(float(freq[k]) / max_freq * 2.50)

    # ---- Mapper: map polygon data to graphics primitives ----
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(extrude.GetOutputPort())
    mapper.ScalarVisibilityOff()

    # ---- Actor: assign the mapped geometry ----
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(peacock)
    if freq[k] <= 0:
        actor.VisibilityOff()

    renderer.AddActor(actor)
    actors.append(actor)

# Position the actors in two rows of 13
y = 0.0
for row in range(2):
    x = 0.0
    for col in range(13):
        actors[row * 13 + col].SetPosition(x, y, 0.0)
        x += 1.5
    y += -3.0

renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(30.0)
renderer.GetActiveCamera().Azimuth(-30.0)
renderer.GetActiveCamera().Dolly(1.25)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("AlphaFrequency")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
