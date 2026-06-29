#!/usr/bin/env python
# Demonstrate textured button widgets placed at corners with FollowCamera using various image formats.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkEllipticalButtonSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkButtonWidget,
    vtkTexturedButtonRepresentation,
)
from vtkmodules.vtkIOImage import vtkBMPReader, vtkPNGReader, vtkTIFFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Dataset: button images
reader_1 = vtkTIFFReader()
reader_1.SetFileName(os.path.join(data_dir, "beach.tif"))
reader_1.SetOrientationType(4)
reader_1.Update()

reader_2 = vtkPNGReader()
reader_2.SetFileName(os.path.join(data_dir, "fran_cut.png"))
reader_2.Update()

reader_3 = vtkPNGReader()
reader_3.SetFileName(os.path.join(data_dir, "hearts8bit.png"))
reader_3.Update()

reader_4 = vtkBMPReader()
reader_4.SetFileName(os.path.join(data_dir, "masonry.bmp"))
reader_4.Update()

# Sources + Filters + Mapper + Actor: mace geometry
sphere = vtkSphereSource()
cone = vtkConeSource()
glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(1.0)
glyph.Update()

apd = vtkAppendPolyData()
apd.AddInputConnection(glyph.GetOutputPort())
apd.AddInputConnection(sphere.GetOutputPort())

mace_mapper = vtkPolyDataMapper()
mace_mapper.SetInputConnection(apd.GetOutputPort())

mace_actor = vtkActor()
mace_actor.SetMapper(mace_mapper)
mace_actor.VisibilityOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(mace_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("button widget placement")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget 1: button at (-1, -1, 0)
geometry_1 = vtkEllipticalButtonSource()
geometry_1.TwoSidedOn()
geometry_1.SetCircumferentialResolution(24)
geometry_1.SetShoulderResolution(24)
geometry_1.SetTextureResolution(24)
geometry_1.SetTextureStyleToFitImage()

rep_1 = vtkTexturedButtonRepresentation()
rep_1.SetNumberOfStates(1)
rep_1.SetButtonTexture(0, reader_1.GetOutput())
rep_1.SetPlaceFactor(1)
rep_1.PlaceWidget(1.0, (-1.0, -1.0, 0.0), (0.0, 0.0, 1.0))
rep_1.FollowCameraOn()
rep_1.SetButtonGeometryConnection(geometry_1.GetOutputPort())

button_widget_1 = vtkButtonWidget()
button_widget_1.SetInteractor(interactor)
button_widget_1.SetRepresentation(rep_1)
button_widget_1.EnabledOn()

# Widget 2: button at (-1, 1, 0)
geometry_2 = vtkEllipticalButtonSource()
geometry_2.TwoSidedOn()
geometry_2.SetCircumferentialResolution(24)
geometry_2.SetShoulderResolution(24)
geometry_2.SetTextureResolution(24)
geometry_2.SetTextureStyleToFitImage()

rep_2 = vtkTexturedButtonRepresentation()
rep_2.SetNumberOfStates(1)
rep_2.SetButtonTexture(0, reader_2.GetOutput())
rep_2.SetPlaceFactor(1)
rep_2.PlaceWidget(1.0, (-1.0, 1.0, 0.0), (0.0, 0.0, 1.0))
rep_2.FollowCameraOn()
rep_2.SetButtonGeometryConnection(geometry_2.GetOutputPort())

button_widget_2 = vtkButtonWidget()
button_widget_2.SetInteractor(interactor)
button_widget_2.SetRepresentation(rep_2)
button_widget_2.EnabledOn()

# Widget 3: button at (1, -1, 0)
geometry_3 = vtkEllipticalButtonSource()
geometry_3.TwoSidedOn()
geometry_3.SetCircumferentialResolution(24)
geometry_3.SetShoulderResolution(24)
geometry_3.SetTextureResolution(24)
geometry_3.SetTextureStyleToFitImage()

rep_3 = vtkTexturedButtonRepresentation()
rep_3.SetNumberOfStates(1)
rep_3.SetButtonTexture(0, reader_3.GetOutput())
rep_3.SetPlaceFactor(1)
rep_3.PlaceWidget(1.0, (1.0, -1.0, 0.0), (0.0, 0.0, 1.0))
rep_3.FollowCameraOn()
rep_3.SetButtonGeometryConnection(geometry_3.GetOutputPort())

button_widget_3 = vtkButtonWidget()
button_widget_3.SetInteractor(interactor)
button_widget_3.SetRepresentation(rep_3)
button_widget_3.EnabledOn()

# Widget 4: button at (1, 1, 0)
geometry_4 = vtkEllipticalButtonSource()
geometry_4.TwoSidedOn()
geometry_4.SetCircumferentialResolution(24)
geometry_4.SetShoulderResolution(24)
geometry_4.SetTextureResolution(24)
geometry_4.SetTextureStyleToFitImage()

rep_4 = vtkTexturedButtonRepresentation()
rep_4.SetNumberOfStates(1)
rep_4.SetButtonTexture(0, reader_4.GetOutput())
rep_4.SetPlaceFactor(1)
rep_4.PlaceWidget(1.0, (1.0, 1.0, 0.0), (0.0, 0.0, 1.0))
rep_4.FollowCameraOn()
rep_4.SetButtonGeometryConnection(geometry_4.GetOutputPort())

button_widget_4 = vtkButtonWidget()
button_widget_4.SetInteractor(interactor)
button_widget_4.SetRepresentation(rep_4)
button_widget_4.EnabledOn()

interactor.Initialize()
interactor.Start()
