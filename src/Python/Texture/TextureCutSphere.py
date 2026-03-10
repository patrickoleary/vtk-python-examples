#!/usr/bin/env python

# Cut an outer sphere with a boolean texture to reveal an inner sphere.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPlanes
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkFiltersTexture import vtkImplicitTextureCoords
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Colors (normalized RGB)
blanched_almond_rgb = (1.0, 0.922, 0.804)
light_salmon_rgb = (1.0, 0.627, 0.478)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Data: locate the boolean texture map
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "texThres.vtk")

# Inner sphere: a smaller sphere that is revealed through the texture cut
inner_sphere = vtkSphereSource()
inner_sphere.SetRadius(0.5)

inner_mapper = vtkPolyDataMapper()
inner_mapper.SetInputConnection(inner_sphere.GetOutputPort())

inner_actor = vtkActor()
inner_actor.SetMapper(inner_mapper)
inner_actor.GetProperty().SetColor(blanched_almond_rgb)

# Outer sphere: the sphere that will be cut by the boolean texture
outer_sphere = vtkSphereSource()
outer_sphere.SetRadius(1.0)
outer_sphere.SetPhiResolution(21)
outer_sphere.SetThetaResolution(21)

# ImplicitTextureCoords: generate texture coordinates using two implicit
# planes as the R and S functions. The planes define where the texture
# is "inside" vs "outside", producing the boolean cut effect.
pts = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
points = vtkPoints()
points.SetNumberOfPoints(2)
points.SetPoint(0, pts[:3])
points.SetPoint(1, pts[3:])

nrms = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
normals = vtkDoubleArray()
normals.SetNumberOfComponents(3)
normals.SetNumberOfTuples(2)
normals.SetTuple(0, nrms[:3])
normals.SetTuple(1, nrms[3:])

planes = vtkPlanes()
planes.SetPoints(points)
planes.SetNormals(normals)

tcoords = vtkImplicitTextureCoords()
tcoords.SetInputConnection(outer_sphere.GetOutputPort())
tcoords.SetRFunction(planes)

# Texture: load the boolean texture map
tmap = vtkStructuredPointsReader()
tmap.SetFileName(file_name)

texture = vtkTexture()
texture.SetInputConnection(tmap.GetOutputPort())
texture.InterpolateOff()
texture.RepeatOff()

# Mapper: map the outer sphere with texture coordinates
outer_mapper = vtkDataSetMapper()
outer_mapper.SetInputConnection(tcoords.GetOutputPort())

# Actor: outer sphere with the boolean texture applied
outer_actor = vtkActor()
outer_actor.SetMapper(outer_mapper)
outer_actor.SetTexture(texture)
outer_actor.GetProperty().SetColor(light_salmon_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(inner_actor)
renderer.AddActor(outer_actor)
renderer.SetBackground(slate_gray_rgb)
renderer.GetActiveCamera().Azimuth(-30)
renderer.GetActiveCamera().Elevation(-30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TextureCutSphere")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
