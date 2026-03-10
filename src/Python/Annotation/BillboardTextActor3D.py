#!/usr/bin/env python

# Demonstrate screen-facing 3D text using vtkBillboardTextActor3D,
# labeling three spheres at different positions in the scene.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkBillboardTextActor3D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
gold_rgb = (1.0, 0.843, 0.0)
background_rgb = (0.200, 0.302, 0.400)

# Labels and positions for three spheres
labels = [
    {"text": "Sphere A", "center": (-2.0, 0.0, 0.0), "color": tomato_rgb},
    {"text": "Sphere B", "center": (0.0, 0.0, 0.0), "color": steel_blue_rgb},
    {"text": "Sphere C", "center": (2.0, 0.0, 0.0), "color": gold_rgb},
]

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(background_rgb)

for item in labels:
    # Source: generate a sphere at the specified position
    source = vtkSphereSource()
    source.SetCenter(item["center"])
    source.SetRadius(0.5)
    source.SetThetaResolution(20)
    source.SetPhiResolution(20)

    # Mapper: map polygon data to graphics primitives
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(source.GetOutputPort())

    # Actor: assign the mapped geometry
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(item["color"])
    renderer.AddActor(actor)

    # Billboard text: screen-facing 3D text label above each sphere
    billboard = vtkBillboardTextActor3D()
    billboard.SetInput(item["text"])
    billboard.SetPosition(item["center"][0], item["center"][1] + 0.8, item["center"][2])
    billboard.GetTextProperty().SetFontSize(24)
    billboard.GetTextProperty().SetColor(item["color"])
    billboard.GetTextProperty().SetJustificationToCentered()
    billboard.GetTextProperty().BoldOn()
    renderer.AddActor(billboard)

# Camera: frame all objects
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("BillboardTextActor3D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
