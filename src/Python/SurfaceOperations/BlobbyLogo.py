#!/usr/bin/env python

# Implicit modelling to create a blobby VTK logo from letter geometry.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkContourFilter,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersHybrid import vtkImplicitModeller
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato = (1.000, 0.388, 0.278)
banana = (0.890, 0.812, 0.341)
slate_gray = (0.439, 0.502, 0.565)

# Data files
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
v_file = str(data_dir / "v.vtk")
t_file = str(data_dir / "t.vtk")
k_file = str(data_dir / "k.vtk")

# Reader: load geometry for each letter
letter_v = vtkPolyDataReader()
letter_v.SetFileName(v_file)

letter_t = vtkPolyDataReader()
letter_t.SetFileName(t_file)

letter_k = vtkPolyDataReader()
letter_k.SetFileName(k_file)

# Transform: position and rotate each letter
v_transform = vtkTransform()
v_transform.Translate(-16.0, 0.0, 12.5)
v_transform.RotateY(40)

v_transform_filter = vtkTransformPolyDataFilter()
v_transform_filter.SetInputConnection(letter_v.GetOutputPort())
v_transform_filter.SetTransform(v_transform)

t_transform = vtkTransform()

t_transform_filter = vtkTransformPolyDataFilter()
t_transform_filter.SetInputConnection(letter_t.GetOutputPort())
t_transform_filter.SetTransform(t_transform)

k_transform = vtkTransform()
k_transform.Translate(14.0, 0.0, 0.0)
k_transform.RotateY(-40)

k_transform_filter = vtkTransformPolyDataFilter()
k_transform_filter.SetInputConnection(letter_k.GetOutputPort())
k_transform_filter.SetTransform(k_transform)

# Filter: append all three letters into one polydata
append_all = vtkAppendPolyData()
append_all.AddInputConnection(v_transform_filter.GetOutputPort())
append_all.AddInputConnection(t_transform_filter.GetOutputPort())
append_all.AddInputConnection(k_transform_filter.GetOutputPort())

# Filter: compute normals on the combined letter geometry
logo_normals = vtkPolyDataNormals()
logo_normals.SetInputConnection(append_all.GetOutputPort())
logo_normals.SetFeatureAngle(60)

# Mapper: map the letter polygons to graphics primitives
logo_mapper = vtkPolyDataMapper()
logo_mapper.SetInputConnection(logo_normals.GetOutputPort())

# Actor: display the polygonal letters in tomato red, shifted forward
logo_prop = vtkProperty()
logo_prop.SetDiffuseColor(tomato)
logo_prop.SetSpecular(0.3)
logo_prop.SetSpecularPower(20)

logo_actor = vtkActor()
logo_actor.SetMapper(logo_mapper)
logo_actor.SetProperty(logo_prop)
logo_actor.SetPosition(0, 0, 6)

# Filter: create an implicit distance field from the letter geometry
blobby_imp = vtkImplicitModeller()
blobby_imp.SetInputConnection(append_all.GetOutputPort())
blobby_imp.SetMaximumDistance(0.075)
blobby_imp.SetSampleDimensions(64, 64, 64)
blobby_imp.SetAdjustDistance(0.05)

# Filter: extract a blobby isosurface from the distance field
blobby_iso = vtkContourFilter()
blobby_iso.SetInputConnection(blobby_imp.GetOutputPort())
blobby_iso.SetValue(1, 1.5)

# Mapper: map the blobby surface to graphics primitives
blobby_mapper = vtkPolyDataMapper()
blobby_mapper.SetInputConnection(blobby_iso.GetOutputPort())
blobby_mapper.ScalarVisibilityOff()

# Actor: display the blobby surface in banana yellow
blobby_prop = vtkProperty()
blobby_prop.SetDiffuseColor(banana)
blobby_prop.SetDiffuse(0.7)
blobby_prop.SetSpecular(0.4)
blobby_prop.SetSpecularPower(20)

blobby_actor = vtkActor()
blobby_actor.SetMapper(blobby_mapper)
blobby_actor.SetProperty(blobby_prop)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(logo_actor)
renderer.AddActor(blobby_actor)
renderer.SetBackground(slate_gray)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("BlobbyLogo")
render_window.SetSize(300, 300)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
