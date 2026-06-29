#!/usr/bin/env python

# Assign colors to cells using a predefined lookup table and a color transfer function.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
midnight_blue = (0.098, 0.098, 0.439)

resolution = 3
table_size = max(resolution * resolution + 1, 10)

# ---- Lookup table 1: predefined named colors ----
lut1 = vtkLookupTable()
lut1.SetNumberOfTableValues(table_size)
lut1.Build()
lut1.SetTableValue(0, 0.000, 0.000, 0.000, 1.0)  # Black
lut1.SetTableValue(1, 0.891, 0.812, 0.341, 1.0)  # Banana
lut1.SetTableValue(2, 1.000, 0.388, 0.278, 1.0)  # Tomato
lut1.SetTableValue(3, 0.961, 0.871, 0.702, 1.0)  # Wheat
lut1.SetTableValue(4, 0.902, 0.902, 0.980, 1.0)  # Lavender
lut1.SetTableValue(5, 1.000, 0.490, 0.314, 1.0)  # Flesh
lut1.SetTableValue(6, 0.502, 0.000, 0.502, 1.0)  # Raspberry
lut1.SetTableValue(7, 0.980, 0.502, 0.447, 1.0)  # Salmon
lut1.SetTableValue(8, 0.741, 0.988, 0.788, 1.0)  # Mint
lut1.SetTableValue(9, 0.200, 0.631, 0.788, 1.0)  # Peacock

# ---- Lookup table 2: color transfer function (green → white → tan) ----
ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
ctf.AddRGBPoint(0.0, 0.085, 0.532, 0.201)
ctf.AddRGBPoint(0.5, 0.865, 0.865, 0.865)
ctf.AddRGBPoint(1.0, 0.677, 0.492, 0.093)

lut2 = vtkLookupTable()
lut2.SetNumberOfTableValues(table_size)
lut2.Build()
for i in range(table_size):
    rgb = list(ctf.GetColor(float(i) / table_size)) + [1.0]
    lut2.SetTableValue(i, rgb)

# Source: generate two plane geometries
plane1 = vtkPlaneSource()
plane1.SetXResolution(resolution)
plane1.SetYResolution(resolution)
plane1.Update()

plane2 = vtkPlaneSource()
plane2.SetXResolution(resolution)
plane2.SetYResolution(resolution)
plane2.Update()

# Build cell color array from predefined LUT
colors_1 = vtkUnsignedCharArray()
colors_1.SetName("colors")
colors_1.SetNumberOfComponents(3)
for i in range(1, table_size):
    rgb = [0.0, 0.0, 0.0]
    lut1.GetColor(float(i) / (table_size - 1), rgb)
    colors_1.InsertNextTuple3(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
plane1.GetOutput().GetCellData().SetScalars(colors_1)

# Build cell color array from transfer function LUT
colors_2 = vtkUnsignedCharArray()
colors_2.SetName("colors")
colors_2.SetNumberOfComponents(3)
for i in range(1, table_size):
    rgb = [0.0, 0.0, 0.0]
    lut2.GetColor(float(i) / (table_size - 1), rgb)
    colors_2.InsertNextTuple3(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
plane2.GetOutput().GetCellData().SetScalars(colors_2)

# Mapper: predefined color LUT
mapper1 = vtkPolyDataMapper()
mapper1.SetInputConnection(plane1.GetOutputPort())
mapper1.SetScalarModeToUseCellData()

# Mapper: color transfer function LUT
mapper2 = vtkPolyDataMapper()
mapper2.SetInputConnection(plane2.GetOutputPort())
mapper2.SetScalarModeToUseCellData()

# Actor: predefined color plane
actor1 = vtkActor()
actor1.SetMapper(mapper1)

# Actor: transfer function color plane
actor2 = vtkActor()
actor2.SetMapper(mapper2)

# Renderer 0: predefined LUT (bottom viewport)
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 1.0, 0.5)
renderer_0.SetBackground(midnight_blue)
renderer_0.AddActor(actor1)

# Renderer 1: transfer function LUT (top viewport)
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.0, 0.5, 1.0, 1.0)
renderer_1.SetBackground(midnight_blue)
renderer_1.AddActor(actor2)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("assign cell colors from lut")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 640)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
