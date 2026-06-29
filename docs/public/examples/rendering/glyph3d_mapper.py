#!/usr/bin/env python
# Demonstrate vtkGlyph3DMapper with superquadric glyphs on a plane.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPlaneSource, vtkSuperquadricSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Glyph source.
superquadric = vtkSuperquadricSource()

# Points source.
plane = vtkPlaneSource()
plane.SetResolution(6, 6)

# Glyph3D mapper.
mapper = vtkGlyph3DMapper()
mapper.SetInputConnection(plane.GetOutputPort())
mapper.SetSourceConnection(superquadric.GetOutputPort())

# Actor.
actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("glyph3d mapper")
render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
