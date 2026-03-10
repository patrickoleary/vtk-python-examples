#!/usr/bin/env python

# Subdivide an icosahedron using vtkLoopSubdivisionFilter. Side-by-side
# viewports show the original coarse mesh (left) and the subdivided
# smooth mesh (right).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersModeling import vtkLoopSubdivisionFilter
from vtkmodules.vtkFiltersSources import vtkPlatonicSolidSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
cornflower_blue_background_rgb = (0.392, 0.584, 0.929)
alice_blue_rgb = (0.941, 0.973, 1.000)
steel_blue_rgb = (0.275, 0.510, 0.706)

# Source: generate an icosahedron (platonic solid index 4)
icosahedron = vtkPlatonicSolidSource()
icosahedron.SetSolidTypeToIcosahedron()

# Subdivision: apply 3 iterations of Loop subdivision
subdivider = vtkLoopSubdivisionFilter()
subdivider.SetInputConnection(icosahedron.GetOutputPort())
subdivider.SetNumberOfSubdivisions(3)

# Mapper: original icosahedron
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(icosahedron.GetOutputPort())
original_mapper.ScalarVisibilityOff()

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(alice_blue_rgb)
original_actor.GetProperty().EdgeVisibilityOn()
original_actor.GetProperty().SetEdgeColor(steel_blue_rgb)

# Mapper: subdivided mesh
subdivided_mapper = vtkPolyDataMapper()
subdivided_mapper.SetInputConnection(subdivider.GetOutputPort())
subdivided_mapper.ScalarVisibilityOff()

subdivided_actor = vtkActor()
subdivided_actor.SetMapper(subdivided_mapper)
subdivided_actor.GetProperty().SetColor(alice_blue_rgb)
subdivided_actor.GetProperty().EdgeVisibilityOn()
subdivided_actor.GetProperty().SetEdgeColor(steel_blue_rgb)

# Shared camera
camera = vtkCamera()
camera.SetPosition(0, 0, 3)
camera.SetFocalPoint(0, 0, 0)

# Left renderer: original mesh
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.AddActor(original_actor)
left_renderer.SetActiveCamera(camera)
left_renderer.ResetCamera()

# Right renderer: subdivided mesh
right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.SetBackground(cornflower_blue_background_rgb)
right_renderer.AddActor(subdivided_actor)
right_renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Subdivision")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
