#!/usr/bin/env python

# Read Exodus files with polyhedral cells and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter, vtkTransformFilter
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read dodecahedron
exodus_reader = vtkExodusIIReader()
exodus_reader.SetFileName(os.path.join(data_dir, "dodecahedron.exo"))
exodus_reader.Update()

# Transform dodecahedron
transform = vtkTransform()
transform.Translate(1.5, 0.5, 0.5)
transform.Scale(0.1, 0.1, 0.1)

transform_filter = vtkTransformFilter()
transform_filter.SetInputData(exodus_reader.GetOutput().GetBlock(0).GetBlock(0))
transform_filter.SetTransform(transform)
transform_filter.Update()

# Read cube
exodus_reader_2 = vtkExodusIIReader()
exodus_reader_2.SetFileName(os.path.join(data_dir, "cube-1.exo"))
exodus_reader_2.Update()

# Shrink cube
shrink_filter = vtkShrinkFilter()
shrink_filter.SetInputData(exodus_reader_2.GetOutput().GetBlock(0).GetBlock(0))
shrink_filter.Update()

# Verify polyhedral faces
print(f"{exodus_reader.GetOutput().GetBlock(0).GetBlock(0).GetCell(0).GetNumberOfFaces()} polyhedral faces")

# Dodecahedron actor
dodecahedron_mapper = vtkDataSetMapper()
dodecahedron_mapper.SetInputData(transform_filter.GetOutput())

dodecahedron_actor = vtkActor()
dodecahedron_actor.SetMapper(dodecahedron_mapper)

# Cube actor
cube_mapper = vtkDataSetMapper()
cube_mapper.SetInputData(shrink_filter.GetOutput())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dodecahedron_actor)
renderer.AddActor(cube_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("exodus polyhedra")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(2.09, 1.419, 3.32)
camera.SetFocalPoint(0.838, 0.431, 0.431)
camera.SetViewUp(0.0820, 0.934, -0.348)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
