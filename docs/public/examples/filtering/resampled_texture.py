#!/usr/bin/env python

# Demonstrate automatic resampling of textures for non-power-of-two sizes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingCore import vtkExtractVOI
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Generate texture map (not power of two)
volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.GetOutput().SetOrigin(0.0, 0.0, 0.0)
volume_reader.SetDataByteOrderToLittleEndian()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

volume_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)

extract = vtkExtractVOI()
extract.SetInputConnection(volume_reader.GetOutputPort())
extract.SetVOI(32, 32, 0, 63, 0, 92)

texture = vtkTexture()
texture.SetInputConnection(extract.GetOutputPort())
texture.InterpolateOn()

# Generate plane to map texture onto
plane = vtkPlaneSource()
plane.SetXResolution(1)
plane.SetYResolution(1)

texture_mapper = vtkPolyDataMapper()
texture_mapper.SetInputConnection(plane.GetOutputPort())

texture_actor = vtkActor()
texture_actor.SetMapper(texture_mapper)
texture_actor.SetTexture(texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(texture_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("resampled texture")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
