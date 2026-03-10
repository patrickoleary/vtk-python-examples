#!/usr/bin/env python

# Read an STL mesh, write it to a Wavefront OBJ file, read it back,
# and render the result.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOGeometry import vtkOBJReader, vtkOBJWriter, vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
tomato_rgb = (1.0, 0.388, 0.278)
background_rgb = (0.200, 0.302, 0.400)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the STL mesh
stl_reader = vtkSTLReader()
stl_reader.SetFileName(str(data_dir / "headMesh.stl"))
stl_reader.Update()

# Writer: save to Wavefront OBJ format
obj_file = str(data_dir / "ReadSTLWriteOBJ.obj")
writer = vtkOBJWriter()
writer.SetFileName(obj_file)
writer.SetInputConnection(stl_reader.GetOutputPort())
writer.Write()

# Reader: read back the written OBJ file
obj_reader = vtkOBJReader()
obj_reader.SetFileName(obj_file)

# Mapper: map the read-back polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(obj_reader.GetOutputPort())

# Actor: assign the mapped geometry
back_face = vtkProperty()
back_face.SetColor(tomato_rgb)
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)
actor.SetBackfaceProperty(back_face)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadSTLWriteOBJ")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
