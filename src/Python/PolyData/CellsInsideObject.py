#!/usr/bin/env python

# Classify cells of a cow mesh as inside, outside, or on the border of a
# rotated copy using vtkSelectEnclosedPoints and vtkMultiThreshold.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import (
    vtkMultiThreshold,
    vtkTransformPolyDataFilter,
)
from vtkmodules.vtkFiltersModeling import vtkSelectEnclosedPoints
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
crimson_rgb = (0.863, 0.078, 0.235)
banana_rgb = (0.890, 0.810, 0.340)
mint_rgb = (0.741, 0.988, 0.788)
peacock_rgb = (0.200, 0.631, 0.788)
silver_rgb = (0.753, 0.753, 0.753)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
cow_file = str(data_dir / "cow.vtp")

# Reader: load the cow mesh
reader = vtkXMLPolyDataReader()
reader.SetFileName(cow_file)
reader.Update()
polydata1 = reader.GetOutput()

# Generate a closed surface by rotating the cow 90 degrees about its Y axis
center = polydata1.GetCenter()
rotate_transform = vtkTransform()
rotate_transform.Translate(center[0], center[1], center[2])
rotate_transform.RotateY(90.0)
rotate_transform.Translate(-center[0], -center[1], -center[2])

transform_pd = vtkTransformPolyDataFilter()
transform_pd.SetTransform(rotate_transform)
transform_pd.SetInputData(polydata1)
transform_pd.Update()
polydata2 = transform_pd.GetOutput()

# Filter: mark points as inside (1) or outside (0) the closed surface
select = vtkSelectEnclosedPoints()
select.SetInputData(polydata1)
select.SetSurfaceData(polydata2)

# Filter: threshold into outside, inside, and border cell sets
threshold = vtkMultiThreshold()
outside_id = threshold.AddBandpassIntervalSet(
    0, 0,
    vtkDataObject.FIELD_ASSOCIATION_POINTS, "SelectedPoints",
    0, 1)
inside_id = threshold.AddBandpassIntervalSet(
    1, 1,
    vtkDataObject.FIELD_ASSOCIATION_POINTS, "SelectedPoints",
    0, 1)
border_id = threshold.AddIntervalSet(
    0, 1,
    vtkMultiThreshold.OPEN, vtkMultiThreshold.OPEN,
    vtkDataObject.FIELD_ASSOCIATION_POINTS, "SelectedPoints",
    0, 0)

threshold.SetInputConnection(select.GetOutputPort())
threshold.OutputSet(outside_id)
threshold.OutputSet(inside_id)
threshold.OutputSet(border_id)
threshold.Update()

# Mapper & Actor: outside cells (crimson)
outside_mapper = vtkDataSetMapper()
outside_mapper.SetInputData(threshold.GetOutput().GetBlock(outside_id).GetBlock(0))
outside_mapper.ScalarVisibilityOff()

outside_actor = vtkActor()
outside_actor.SetMapper(outside_mapper)
outside_actor.GetProperty().SetDiffuseColor(crimson_rgb)
outside_actor.GetProperty().SetSpecular(0.6)
outside_actor.GetProperty().SetSpecularPower(30)

# Mapper & Actor: inside cells (banana)
inside_mapper = vtkDataSetMapper()
inside_mapper.SetInputData(threshold.GetOutput().GetBlock(inside_id).GetBlock(0))
inside_mapper.ScalarVisibilityOff()

inside_actor = vtkActor()
inside_actor.SetMapper(inside_mapper)
inside_actor.GetProperty().SetDiffuseColor(banana_rgb)
inside_actor.GetProperty().SetSpecular(0.6)
inside_actor.GetProperty().SetSpecularPower(30)
inside_actor.GetProperty().EdgeVisibilityOn()

# Mapper & Actor: border cells (mint)
border_mapper = vtkDataSetMapper()
border_mapper.SetInputData(threshold.GetOutput().GetBlock(border_id).GetBlock(0))
border_mapper.ScalarVisibilityOff()

border_actor = vtkActor()
border_actor.SetMapper(border_mapper)
border_actor.GetProperty().SetDiffuseColor(mint_rgb)
border_actor.GetProperty().SetSpecular(0.6)
border_actor.GetProperty().SetSpecularPower(30)
border_actor.GetProperty().EdgeVisibilityOn()

# Mapper & Actor: translucent enclosing surface (peacock)
surface_mapper = vtkDataSetMapper()
surface_mapper.SetInputData(polydata2)
surface_mapper.ScalarVisibilityOff()

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().SetDiffuseColor(peacock_rgb)
surface_actor.GetProperty().SetOpacity(0.1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.AddActor(outside_actor)
renderer.AddActor(inside_actor)
renderer.AddActor(border_actor)
renderer.SetBackground(silver_rgb)
renderer.UseHiddenLineRemovalOn()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.25)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CellsInsideObject")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
