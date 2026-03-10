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

# Renderers: 2 rows x 4 columns (top=flat, bottom=Gouraud)
flat_actors = [flat_sphere_actor, flat_cylinder_actor, flat_iso_actor, flat_model_actor]
smooth_actors = [smooth_sphere_actor, smooth_cylinder_actor, smooth_iso_actor, smooth_model_actor]

renderers = []
for col in range(4):
    ren_flat = vtkRenderer()
    ren_flat.AddActor(flat_actors[col])
    ren_flat.SetBackground(background)
    ren_flat.SetViewport(col / 4.0, 0.5, (col + 1) / 4.0, 1.0)
    ren_flat.GetActiveCamera().Azimuth(20)
    ren_flat.GetActiveCamera().Elevation(30)
    ren_flat.ResetCamera()
    renderers.append(ren_flat)

    ren_smooth = vtkRenderer()
    ren_smooth.AddActor(smooth_actors[col])
    ren_smooth.SetBackground(background)
    ren_smooth.SetViewport(col / 4.0, 0.0, (col + 1) / 4.0, 0.5)
    ren_smooth.SetActiveCamera(ren_flat.GetActiveCamera())
    renderers.append(ren_smooth)

# Window: display the rendered scene
render_window = vtkRenderWindow()
for ren in renderers:
    render_window.AddRenderer(ren)
render_window.SetSize(1024, 512)
render_window.SetWindowName("FlatVersusGouraud")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
