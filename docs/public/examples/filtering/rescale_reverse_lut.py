#!/usr/bin/env python

# Rescale and reverse a color transfer function, shown in a 2x2 grid.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
    vtkTextProperty,
)

# Colors (normalized RGB)
light_goldenrod_yellow_rgb = (0.980, 0.980, 0.824)

# --- CTF 0: Original rainbow ---
# Newton's original seven rainbow colors as a discretized CTF.
ctf_0 = vtkDiscretizableColorTransferFunction()
ctf_0.SetColorSpaceToRGB()
ctf_0.SetScaleToLinear()
ctf_0.SetNanColor(0.5, 0.5, 0.5)
ctf_0.SetBelowRangeColor(0.0, 0.0, 0.0)
ctf_0.UseBelowRangeColorOn()
ctf_0.SetAboveRangeColor(1.0, 1.0, 1.0)
ctf_0.UseAboveRangeColorOn()
ctf_0.AddRGBPoint(-1.0, 1.0, 0.0, 0.0)
ctf_0.AddRGBPoint(-2.0 / 3.0, 1.0, 165.0 / 255.0, 0.0)
ctf_0.AddRGBPoint(-1.0 / 3.0, 1.0, 1.0, 0.0)
ctf_0.AddRGBPoint(0.0, 0.0, 125.0 / 255.0, 0.0)
ctf_0.AddRGBPoint(1.0 / 3.0, 0.0, 153.0 / 255.0, 1.0)
ctf_0.AddRGBPoint(2.0 / 3.0, 68.0 / 255.0, 0.0, 153.0 / 255.0)
ctf_0.AddRGBPoint(1.0, 153.0 / 255.0, 0.0, 1.0)
ctf_0.SetNumberOfValues(7)
ctf_0.DiscretizeOn()

# Extract node values from original CTF for rescaling
original_xv = []
original_rgbv = []
nv = [0.0] * 6
for i in range(ctf_0.GetNumberOfValues()):
    ctf_0.GetNodeValue(i, nv)
    original_xv.append(nv[0])
    original_rgbv.append(list(nv[1:4]))

original_old_min = min(original_xv)
original_old_max = max(original_xv)

# --- CTF 1: Rescaled [0, 1] ---
ctf_1 = vtkDiscretizableColorTransferFunction()
ctf_1.SetScale(ctf_0.GetScale())
ctf_1.SetColorSpace(ctf_0.GetColorSpace())
ctf_1.SetNanColor(ctf_0.GetNanColor())
ctf_1.SetBelowRangeColor(ctf_0.GetBelowRangeColor())
ctf_1.SetUseBelowRangeColor(ctf_0.GetUseBelowRangeColor())
ctf_1.SetAboveRangeColor(ctf_0.GetAboveRangeColor())
ctf_1.SetUseAboveRangeColor(ctf_0.GetUseAboveRangeColor())
ctf_1.SetNumberOfValues(len(original_xv))
ctf_1.SetDiscretize(ctf_0.GetDiscretize())
rescaled_xv_1 = [(1.0 - 0.0) / (original_old_max - original_old_min) * (x - original_old_min) + 0.0 for x in original_xv]
for i in range(len(original_xv)):
    ctf_1.AddRGBPoint(rescaled_xv_1[i], *original_rgbv[i])
ctf_1.Build()

# --- CTF 2: Reversed (same range as original) ---
ctf_2 = vtkDiscretizableColorTransferFunction()
ctf_2.SetScale(ctf_0.GetScale())
ctf_2.SetColorSpace(ctf_0.GetColorSpace())
ctf_2.SetNanColor(ctf_0.GetNanColor())
ctf_2.SetBelowRangeColor(ctf_0.GetAboveRangeColor())
ctf_2.SetUseBelowRangeColor(ctf_0.GetUseAboveRangeColor())
ctf_2.SetAboveRangeColor(ctf_0.GetBelowRangeColor())
ctf_2.SetUseAboveRangeColor(ctf_0.GetUseBelowRangeColor())
ctf_2.SetNumberOfValues(len(original_xv))
ctf_2.SetDiscretize(ctf_0.GetDiscretize())
sz = len(original_xv)
for i in range(sz):
    j = sz - 1 - i
    ctf_2.AddRGBPoint(original_xv[i], *original_rgbv[j])
ctf_2.Build()

# --- CTF 3: Rescaled [0, 1] and Reversed ---
ctf_3 = vtkDiscretizableColorTransferFunction()
ctf_3.SetScale(ctf_0.GetScale())
ctf_3.SetColorSpace(ctf_0.GetColorSpace())
ctf_3.SetNanColor(ctf_0.GetNanColor())
ctf_3.SetBelowRangeColor(ctf_0.GetAboveRangeColor())
ctf_3.SetUseBelowRangeColor(ctf_0.GetUseAboveRangeColor())
ctf_3.SetAboveRangeColor(ctf_0.GetBelowRangeColor())
ctf_3.SetUseAboveRangeColor(ctf_0.GetUseBelowRangeColor())
ctf_3.SetNumberOfValues(len(original_xv))
ctf_3.SetDiscretize(ctf_0.GetDiscretize())
rescaled_xv_3 = [(1.0 - 0.0) / (original_old_max - original_old_min) * (x - original_old_min) + 0.0 for x in original_xv]
for i in range(sz):
    j = sz - 1 - i
    ctf_3.AddRGBPoint(rescaled_xv_3[i], *original_rgbv[j])
ctf_3.Build()

text_property = vtkTextProperty()
text_property.SetFontSize(36)
text_property.SetJustificationToCentered()
text_property.SetColor(light_goldenrod_yellow_rgb)

# --- Viewport 0: Original (top-left) ---
cylinder_0 = vtkCylinderSource()
cylinder_0.SetResolution(6)
cylinder_0.Update()
bounds_0 = cylinder_0.GetOutput().GetBounds()

elevation_0 = vtkElevationFilter()
elevation_0.SetScalarRange(0, 1)
elevation_0.SetLowPoint(0, bounds_0[2], 0)
elevation_0.SetHighPoint(0, bounds_0[3], 0)
elevation_0.SetInputConnection(cylinder_0.GetOutputPort())

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(elevation_0.GetOutputPort())
mapper_0.SetLookupTable(ctf_0)
mapper_0.SetColorModeToMapScalars()
mapper_0.InterpolateScalarsBeforeMappingOn()

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

scalar_bar_0 = vtkScalarBarActor()
scalar_bar_0.SetLookupTable(ctf_0)

text_actor_0 = vtkTextActor()
text_actor_0.SetInput("Original")
text_actor_0.SetPosition(300, 16)
text_actor_0.GetTextProperty().ShallowCopy(text_property)

renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0)
renderer_0.AddActor(scalar_bar_0)
renderer_0.AddActor(text_actor_0)
renderer_0.SetBackground(0.322, 0.341, 0.431)
renderer_0.SetViewport(0.0, 0.5, 0.5, 1.0)

# --- Viewport 1: Rescaled (bottom-left) ---
cylinder_1 = vtkCylinderSource()
cylinder_1.SetResolution(6)
cylinder_1.Update()
bounds_1 = cylinder_1.GetOutput().GetBounds()

elevation_1 = vtkElevationFilter()
elevation_1.SetScalarRange(0, 1)
elevation_1.SetLowPoint(0, bounds_1[2], 0)
elevation_1.SetHighPoint(0, bounds_1[3], 0)
elevation_1.SetInputConnection(cylinder_1.GetOutputPort())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(elevation_1.GetOutputPort())
mapper_1.SetLookupTable(ctf_1)
mapper_1.SetColorModeToMapScalars()
mapper_1.InterpolateScalarsBeforeMappingOn()

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

scalar_bar_1 = vtkScalarBarActor()
scalar_bar_1.SetLookupTable(ctf_1)

text_actor_1 = vtkTextActor()
text_actor_1.SetInput("Rescaled")
text_actor_1.SetPosition(300, 16)
text_actor_1.GetTextProperty().ShallowCopy(text_property)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1)
renderer_1.AddActor(scalar_bar_1)
renderer_1.AddActor(text_actor_1)
renderer_1.SetBackground(0.322, 0.341, 0.431)
renderer_1.SetViewport(0.0, 0.0, 0.5, 0.5)

# --- Viewport 2: Reversed (top-right) ---
cylinder_2 = vtkCylinderSource()
cylinder_2.SetResolution(6)
cylinder_2.Update()
bounds_2 = cylinder_2.GetOutput().GetBounds()

elevation_2 = vtkElevationFilter()
elevation_2.SetScalarRange(0, 1)
elevation_2.SetLowPoint(0, bounds_2[2], 0)
elevation_2.SetHighPoint(0, bounds_2[3], 0)
elevation_2.SetInputConnection(cylinder_2.GetOutputPort())

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(elevation_2.GetOutputPort())
mapper_2.SetLookupTable(ctf_2)
mapper_2.SetColorModeToMapScalars()
mapper_2.InterpolateScalarsBeforeMappingOn()

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

scalar_bar_2 = vtkScalarBarActor()
scalar_bar_2.SetLookupTable(ctf_2)

text_actor_2 = vtkTextActor()
text_actor_2.SetInput("Reversed")
text_actor_2.SetPosition(300, 16)
text_actor_2.GetTextProperty().ShallowCopy(text_property)

renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_2)
renderer_2.AddActor(scalar_bar_2)
renderer_2.AddActor(text_actor_2)
renderer_2.SetBackground(0.322, 0.341, 0.431)
renderer_2.SetViewport(0.5, 0.5, 1.0, 1.0)

# --- Viewport 3: Rescaled and Reversed (bottom-right) ---
cylinder_3 = vtkCylinderSource()
cylinder_3.SetResolution(6)
cylinder_3.Update()
bounds_3 = cylinder_3.GetOutput().GetBounds()

elevation_3 = vtkElevationFilter()
elevation_3.SetScalarRange(0, 1)
elevation_3.SetLowPoint(0, bounds_3[2], 0)
elevation_3.SetHighPoint(0, bounds_3[3], 0)
elevation_3.SetInputConnection(cylinder_3.GetOutputPort())

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(elevation_3.GetOutputPort())
mapper_3.SetLookupTable(ctf_3)
mapper_3.SetColorModeToMapScalars()
mapper_3.InterpolateScalarsBeforeMappingOn()

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

scalar_bar_3 = vtkScalarBarActor()
scalar_bar_3.SetLookupTable(ctf_3)

text_actor_3 = vtkTextActor()
text_actor_3.SetInput("Rescaled and Reversed")
text_actor_3.SetPosition(300, 16)
text_actor_3.GetTextProperty().ShallowCopy(text_property)

renderer_3 = vtkRenderer()
renderer_3.AddActor(actor_3)
renderer_3.AddActor(scalar_bar_3)
renderer_3.AddActor(text_actor_3)
renderer_3.SetBackground(0.322, 0.341, 0.431)
renderer_3.SetViewport(0.5, 0.0, 1.0, 0.5)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("rescale reverse lut")
render_window.SetMultiSamples(0)
render_window.SetSize(1280, 960)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
