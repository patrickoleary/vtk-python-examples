#!/usr/bin/env python
# Demonstrate vtkLogoWidget with alpha blending and translucent geometry.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCylinderSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import (
    vtkLogoRepresentation,
    vtkLogoWidget,
)
from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: logo image
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

image_reader = vtkTIFFReader()
image_reader.SetFileName(os.path.join(data_dir, "beach.tif"))
image_reader.SetOrientationType(4)
image_reader.Update()

# Sources
sphere_source = vtkSphereSource()

cylinder_source = vtkCylinderSource()

cone_source = vtkConeSource()

# Mapper + Actor
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_property = vtkProperty()
sphere_property.SetOpacity(0.2)
sphere_property.SetColor(0.0, 1.0, 0.0)
sphere_actor.SetProperty(sphere_property)

cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder_source.GetOutputPort())

cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.AddPosition(5, 0, 0)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_source.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.AddPosition(0, 5, 0)

# Renderer (alpha blending)
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cylinder_actor)
renderer.AddActor(cone_actor)
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.SetUseDepthPeeling(0)
renderer.SetMaximumNumberOfPeels(200)
renderer.SetOcclusionRatio(0.1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("logo widget alpha blending")
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.SetSize(300, 300)

# Interactor
style = vtkInteractorStyleTrackballCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

# Widget
logo_rep = vtkLogoRepresentation()
logo_rep.SetImage(image_reader.GetOutput())

logo_widget = vtkLogoWidget()
logo_widget.SetInteractor(interactor)
logo_widget.SetRepresentation(logo_rep)
logo_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
