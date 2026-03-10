#!/usr/bin/env python

# Visualize multidimensional financial data using vtkGaussianSplatter
# and vtkContourFilter. The gray surface represents the total population
# and the red surface represents delinquent loan payments.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkAxes
from vtkmodules.vtkImagingHybrid import vtkGaussianSplatter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
wheat_background_rgb = (0.961, 0.871, 0.702)
pop_rgb = (0.902, 0.902, 0.902)
red_rgb = (1.000, 0.000, 0.000)


# Reader: load and parse the financial data file
script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = os.path.join(script_dir, "financial.txt")

res = dict()
with open(file_name) as f:
    k = ""
    v = []
    has_key = False
    for line in f:
        cl = " ".join(line.split()).split()
        if cl:
            if len(cl) == 2 and cl[0] == "NUMBER_POINTS":
                k = cl[0]
                v = [int(cl[1])]
                has_key = True
                continue
            if len(cl) == 1 and not has_key:
                has_key = True
                k = cl[0]
                v = []
            else:
                v += list(map(float, cl))
        else:
            if has_key:
                minimum = min(v)
                maximum = max(v)
                for i in v:
                    if i > minimum:
                        maximum = i
                if maximum != minimum:
                    res[k] = [minimum + x / (maximum - minimum) for x in v]
                else:
                    res[k] = v
                has_key = False

# Source: build an unstructured grid from the parsed data
new_pts = vtkPoints()
new_scalars = vtkFloatArray()
xyz = list(zip(res["MONTHLY_PAYMENT"], res["INTEREST_RATE"], res["LOAN_AMOUNT"]))
for i in range(int(res["NUMBER_POINTS"][0])):
    new_pts.InsertPoint(i, xyz[i])
    new_scalars.InsertValue(i, res["TIME_LATE"][i])

data_set = vtkUnstructuredGrid()
data_set.SetPoints(new_pts)
data_set.GetPointData().SetScalars(new_scalars)

# Pipeline: total population (gray translucent surface)
pop_splatter = vtkGaussianSplatter()
pop_splatter.SetInputData(data_set)
pop_splatter.SetSampleDimensions(100, 100, 100)
pop_splatter.SetRadius(0.05)
pop_splatter.ScalarWarpingOff()

pop_surface = vtkContourFilter()
pop_surface.SetInputConnection(pop_splatter.GetOutputPort())
pop_surface.SetValue(0, 0.01)

pop_mapper = vtkPolyDataMapper()
pop_mapper.SetInputConnection(pop_surface.GetOutputPort())
pop_mapper.ScalarVisibilityOff()

pop_actor = vtkActor()
pop_actor.SetMapper(pop_mapper)
pop_actor.GetProperty().SetOpacity(0.3)
pop_actor.GetProperty().SetColor(pop_rgb)

# Pipeline: delinquent population (red surface)
late_splatter = vtkGaussianSplatter()
late_splatter.SetInputData(data_set)
late_splatter.SetSampleDimensions(50, 50, 50)
late_splatter.SetRadius(0.05)
late_splatter.SetScaleFactor(0.005)

late_surface = vtkContourFilter()
late_surface.SetInputConnection(late_splatter.GetOutputPort())
late_surface.SetValue(0, 0.01)

late_mapper = vtkPolyDataMapper()
late_mapper.SetInputConnection(late_surface.GetOutputPort())
late_mapper.ScalarVisibilityOff()

late_actor = vtkActor()
late_actor.SetMapper(late_mapper)
late_actor.GetProperty().SetColor(red_rgb)

# Axes: tube axes at the data origin
pop_splatter.Update()
bounds = pop_splatter.GetOutput().GetBounds()

axes = vtkAxes()
axes.SetOrigin(bounds[0], bounds[2], bounds[4])
axes.SetScaleFactor(pop_splatter.GetOutput().GetLength() / 5)

axes_tubes = vtkTubeFilter()
axes_tubes.SetInputConnection(axes.GetOutputPort())
axes_tubes.SetRadius(axes.GetScaleFactor() / 25.0)
axes_tubes.SetNumberOfSides(6)

axes_mapper = vtkPolyDataMapper()
axes_mapper.SetInputConnection(axes_tubes.GetOutputPort())

axes_actor = vtkActor()
axes_actor.SetMapper(axes_mapper)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(late_actor)
renderer.AddActor(axes_actor)
renderer.AddActor(pop_actor)
renderer.SetBackground(wheat_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.3)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Finance")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
