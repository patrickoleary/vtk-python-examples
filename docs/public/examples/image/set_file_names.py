#!/usr/bin/env python

# Read image slices using glob/sort file names and display with vtkImageActor.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCore import (
    vtkGlobFileNames,
    vtkSortFileNames,
)
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Glob and sort file names
glob_file_names = vtkGlobFileNames()
glob_file_names.AddFileNames(os.path.join(data_dir, "headsq", "quarter.*[0-9]"))

sort_file_names = vtkSortFileNames()
sort_file_names.SetInputFileNames(glob_file_names.GetFileNames())
sort_file_names.NumericSortOn()

# Read image slices
image_reader = vtkImageReader2()
image_reader.SetFileNames(sort_file_names.GetFileNames())
image_reader.SetDataExtent(0, 63, 0, 63, 1, 1)
image_reader.SetDataByteOrderToLittleEndian()

# Display slice 2 with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(image_reader.GetOutputPort())
image_actor.SetDisplayExtent(0, 63, 0, 63, 2, 2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("set file names")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
