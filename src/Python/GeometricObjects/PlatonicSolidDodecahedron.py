#!/usr/bin/env python

# Render a dodecahedron Platonic solid with each face colored using a
# lookup table so adjacent faces are visually distinct.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersSources import vtkPlatonicSolidSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Lookup table: map cell scalars to distinct face colors
lut = vtkLookupTable()
lut.SetNumberOfTableValues(20)
lut.SetTableRange(0.0, 19.0)
lut.Build()
lut.SetTableValue(0, 0.1, 0.1, 0.1)
lut.SetTableValue(1, 0, 0, 1)
lut.SetTableValue(2, 0, 1, 0)
lut.SetTableValue(3, 0, 1, 1)
lut.SetTableValue(4, 1, 0, 0)
lut.SetTableValue(5, 1, 0, 1)
lut.SetTableValue(6, 1, 1, 0)
lut.SetTableValue(7, 0.9, 0.7, 0.9)
lut.SetTableValue(8, 0.5, 0.5, 0.5)
lut.SetTableValue(9, 0.0, 0.0, 0.7)
lut.SetTableValue(10, 0.5, 0.7, 0.5)
lut.SetTableValue(11, 0, 0.7, 0.7)
lut.SetTableValue(12, 0.7, 0, 0)
lut.SetTableValue(13, 0.7, 0, 0.7)
lut.SetTableValue(14, 0.7, 0.7, 0)
lut.SetTableValue(15, 0, 0, 0.4)
lut.SetTableValue(16, 0, 0.4, 0)
lut.SetTableValue(17, 0, 0.4, 0.4)
lut.SetTableValue(18, 0.4, 0, 0)
lut.SetTableValue(19, 0.4, 0, 0.4)

# Source: generate dodecahedron polygon data (solid type 4)
source = vtkPlatonicSolidSource()
source.SetSolidType(4)

# Mapper: map polygon data to graphics primitives with face coloring
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())
mapper.SetLookupTable(lut)
mapper.SetScalarRange(0, 19)

# Actor: assign the mapped geometry and rotate for a 3D view
actor = vtkActor()
actor.SetMapper(mapper)
actor.RotateX(20)
actor.RotateY(30)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("PlatonicSolidDodecahedron")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
