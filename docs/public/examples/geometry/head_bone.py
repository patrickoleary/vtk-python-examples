#!/usr/bin/env python
# Demonstrate marching cubes isosurface of head bone from volume data with gradient normals.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkMergePoints
from vtkmodules.vtkFiltersCore import vtkMarchingCubes, vtkVectorNorm
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

colors = vtkNamedColors()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Create a point locator for marching cubes.
locator = vtkMergePoints()
locator.SetDivisions(32, 32, 46)
locator.SetNumberOfPointsPerBucket(2)
locator.AutomaticOff()

# Read the volume data.
volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.GetOutput().SetOrigin(0.0, 0.0, 0.0)
volume_reader.SetDataByteOrderToLittleEndian()
volume_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)

# Extract bone isosurface.
marching_cubes = vtkMarchingCubes()
marching_cubes.SetInputConnection(volume_reader.GetOutputPort())
marching_cubes.SetValue(0, 1150)
marching_cubes.ComputeGradientsOn()
marching_cubes.ComputeScalarsOff()
marching_cubes.SetLocator(locator)

# Compute gradient norms.
gradient = vtkVectorNorm()
gradient.SetInputConnection(marching_cubes.GetOutputPort())

# Mapper and actor for isosurface.
iso_mapper = vtkDataSetMapper()
iso_mapper.SetInputConnection(gradient.GetOutputPort())
iso_mapper.ScalarVisibilityOn()
iso_mapper.SetScalarRange(0, 1200)

antique_white_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("antique_white", antique_white_rgb)

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(antique_white_rgb)

# Outline.
outline = vtkOutlineFilter()
outline.SetInputConnection(volume_reader.GetOutputPort())
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(iso_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.SetSize(250, 250)
render_window.AddRenderer(renderer)
render_window.SetWindowName("head bone")

renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Elevation(90)
camera.SetViewUp(0, 0, -1)
camera.Zoom(1.5)
light = vtkLight()
light.SetPosition(camera.GetPosition())
light.SetFocalPoint(camera.GetFocalPoint())
renderer.AddLight(light)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
