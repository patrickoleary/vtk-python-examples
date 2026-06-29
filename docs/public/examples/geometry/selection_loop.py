#!/usr/bin/env python
# Demonstrate implicit selection loop with closest point connectivity on a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkImplicitSelectionLoop
from vtkmodules.vtkFiltersCore import vtkConnectivityFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractGeometry
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

colors = vtkNamedColors()

# Create a sphere.
sphere = vtkSphereSource()
sphere.SetRadius(1)
sphere.SetPhiResolution(100)
sphere.SetThetaResolution(100)

# Define selection points.
selection_points = vtkPoints()
selection_points.InsertPoint(0, 0.07325, 0.8417, 0.5612)
selection_points.InsertPoint(1, 0.07244, 0.6568, 0.7450)
selection_points.InsertPoint(2, 0.1727, 0.4597, 0.8850)
selection_points.InsertPoint(3, 0.3265, 0.6054, 0.7309)
selection_points.InsertPoint(4, 0.5722, 0.5848, 0.5927)
selection_points.InsertPoint(5, 0.4305, 0.8138, 0.4189)

# Create the implicit selection loop.
loop = vtkImplicitSelectionLoop()
loop.SetLoop(selection_points)

# Extract geometry inside the loop.
extract = vtkExtractGeometry()
extract.SetInputConnection(sphere.GetOutputPort())
extract.SetImplicitFunction(loop)

# Use connectivity to find the closest region.
connect = vtkConnectivityFilter()
connect.SetInputConnection(extract.GetOutputPort())
connect.SetExtractionModeToClosestPointRegion()
connect.SetClosestPoint(selection_points.GetPoint(0))

# Mapper and actor.
clip_mapper = vtkDataSetMapper()
clip_mapper.SetInputConnection(connect.GetOutputPort())

back_prop = vtkProperty()
peacock_rgb = [0.0, 0.0, 0.0]
tomato_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("peacock", peacock_rgb)
colors.GetColorRGB("tomato", tomato_rgb)
back_prop.SetDiffuseColor(tomato_rgb)

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetColor(peacock_rgb)
clip_actor.SetBackfaceProperty(back_prop)

renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("selection loop")

renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
