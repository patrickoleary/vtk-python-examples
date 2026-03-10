#!/usr/bin/env python

# Demonstrate vtkInteractorStyleTrackballCamera, which allows the user to
# rotate, pan, and zoom the camera around the scene with the mouse.  A random
# point cloud is displayed as sphere glyphs.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersSources import (
    vtkPointSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
royal_blue_rgb = (0.255, 0.412, 0.882)

# Source: generate a random point cloud
point_source = vtkPointSource()
point_source.SetCenter(0, 0, 0)
point_source.SetNumberOfPoints(50)
point_source.SetRadius(5)
point_source.Update()

# GlyphSource: small sphere to place at each point
glyph_sphere = vtkSphereSource()
bounds = point_source.GetOutput().GetPoints().GetBounds()
max_len = max(bounds[i + 1] - bounds[i] for i in range(0, 5, 2))
glyph_sphere.SetRadius(0.05 * max_len)

# PointData: wrap the points in a vtkPolyData
point_data = vtkPolyData()
point_data.SetPoints(point_source.GetOutput().GetPoints())

# Mapper: glyph each point as a sphere
mapper = vtkGlyph3DMapper()
mapper.SetInputData(point_data)
mapper.SetSourceConnection(glyph_sphere.GetOutputPort())
mapper.ScalarVisibilityOff()
mapper.ScalingOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(gold_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(royal_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("InteractorStyleTrackballCamera")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Style: trackball-camera mode (mouse manipulates the camera)
style = vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
