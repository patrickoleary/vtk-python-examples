#!/usr/bin/env python

# Compare flat versus Gouraud shading on four different geometries:
# sphere, cylinder, isosurface, and an OBJ model (cow).

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersSources import (
    vtkCylinderSource,
    vtkSphereSource,
)
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
misty_rose = (1.0, 0.894, 0.882)
tan_color = (0.824, 0.706, 0.549)
background = (0.439, 0.502, 0.565)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# ---------- column 0: sphere ----------
sphere = vtkSphereSource()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

flat_sphere_actor = vtkActor()
flat_sphere_actor.SetMapper(sphere_mapper)
flat_sphere_actor.GetProperty().SetColor(misty_rose)
flat_sphere_actor.GetProperty().SetInterpolationToFlat()

smooth_sphere_actor = vtkActor()
smooth_sphere_actor.SetMapper(sphere_mapper)
smooth_sphere_actor.GetProperty().SetColor(misty_rose)
smooth_sphere_actor.GetProperty().SetInterpolationToGouraud()

# ---------- column 1: cylinder ----------
cylinder = vtkCylinderSource()

cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())

flat_cylinder_actor = vtkActor()
flat_cylinder_actor.SetMapper(cylinder_mapper)
flat_cylinder_actor.GetProperty().SetColor(misty_rose)
flat_cylinder_actor.GetProperty().SetInterpolationToFlat()

smooth_cylinder_actor = vtkActor()
smooth_cylinder_actor.SetMapper(cylinder_mapper)
smooth_cylinder_actor.GetProperty().SetColor(misty_rose)
smooth_cylinder_actor.GetProperty().SetInterpolationToGouraud()

# ---------- column 2: isosurface ----------
quadric = vtkQuadric()
quadric.SetCoefficients(1, 2, 3, 0, 1, 0, 0, 0, 0, 0)

sample = vtkSampleFunction()
sample.SetSampleDimensions(25, 25, 25)
sample.SetImplicitFunction(quadric)

contour = vtkContourFilter()
contour.SetInputConnection(sample.GetOutputPort())
contour.GenerateValues(5, 1.0, 6.0)

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.SetScalarRange(0, 7)

flat_iso_actor = vtkActor()
flat_iso_actor.SetMapper(contour_mapper)
flat_iso_actor.GetProperty().SetInterpolationToFlat()

smooth_iso_actor = vtkActor()
smooth_iso_actor.SetMapper(contour_mapper)
smooth_iso_actor.GetProperty().SetInterpolationToGouraud()

# ---------- column 3: OBJ model (cow) ----------
reader = vtkOBJReader()
reader.SetFileName(str(data_dir / "cow.obj"))

model_mapper = vtkPolyDataMapper()
model_mapper.SetInputConnection(reader.GetOutputPort())

flat_model_actor = vtkActor()
flat_model_actor.SetMapper(model_mapper)
flat_model_actor.GetProperty().SetColor(tan_color)
flat_model_actor.GetProperty().SetInterpolationToFlat()

smooth_model_actor = vtkActor()
smooth_model_actor.SetMapper(model_mapper)
smooth_model_actor.GetProperty().SetColor(tan_color)
smooth_model_actor.GetProperty().SetInterpolationToGouraud()

# Renderer 0: flat sphere (top-left)
renderer_0 = vtkRenderer()
renderer_0.AddActor(flat_sphere_actor)
renderer_0.SetBackground(background)
renderer_0.SetViewport(0.0, 0.5, 0.25, 1.0)

# Renderer 1: smooth sphere (bottom-left)
renderer_1 = vtkRenderer()
renderer_1.AddActor(smooth_sphere_actor)
renderer_1.SetBackground(background)
renderer_1.SetViewport(0.0, 0.0, 0.25, 0.5)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Renderer 2: flat cylinder
renderer_2 = vtkRenderer()
renderer_2.AddActor(flat_cylinder_actor)
renderer_2.SetBackground(background)
renderer_2.SetViewport(0.25, 0.5, 0.5, 1.0)

# Renderer 3: smooth cylinder
renderer_3 = vtkRenderer()
renderer_3.AddActor(smooth_cylinder_actor)
renderer_3.SetBackground(background)
renderer_3.SetViewport(0.25, 0.0, 0.5, 0.5)
renderer_3.SetActiveCamera(renderer_2.GetActiveCamera())

# Renderer 4: flat iso surface
renderer_4 = vtkRenderer()
renderer_4.AddActor(flat_iso_actor)
renderer_4.SetBackground(background)
renderer_4.SetViewport(0.5, 0.5, 0.75, 1.0)

# Renderer 5: smooth iso surface
renderer_5 = vtkRenderer()
renderer_5.AddActor(smooth_iso_actor)
renderer_5.SetBackground(background)
renderer_5.SetViewport(0.5, 0.0, 0.75, 0.5)
renderer_5.SetActiveCamera(renderer_4.GetActiveCamera())

# Renderer 6: flat model
renderer_6 = vtkRenderer()
renderer_6.AddActor(flat_model_actor)
renderer_6.SetBackground(background)
renderer_6.SetViewport(0.75, 0.5, 1.0, 1.0)

# Renderer 7: smooth model
renderer_7 = vtkRenderer()
renderer_7.AddActor(smooth_model_actor)
renderer_7.SetBackground(background)
renderer_7.SetViewport(0.75, 0.0, 1.0, 0.5)
renderer_7.SetActiveCamera(renderer_6.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.SetWindowName("flat versus gouraud")
render_window.SetMultiSamples(0)
render_window.SetSize(1024, 512)

# Scene: configure cameras
renderer_0.GetActiveCamera().Azimuth(20)
renderer_0.GetActiveCamera().Elevation(30)
renderer_0.ResetCamera()
renderer_2.GetActiveCamera().Azimuth(20)
renderer_2.GetActiveCamera().Elevation(30)
renderer_2.ResetCamera()
renderer_4.GetActiveCamera().Azimuth(20)
renderer_4.GetActiveCamera().Elevation(30)
renderer_4.ResetCamera()
renderer_6.GetActiveCamera().Azimuth(20)
renderer_6.GetActiveCamera().Elevation(30)
renderer_6.ResetCamera()

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
