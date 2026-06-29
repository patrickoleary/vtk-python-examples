#!/usr/bin/env python
# Demonstrate vtkLabelPlacementMapper with labels on a 3D polyline.

import numpy as np

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkPolyLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkLabelPlacementMapper, vtkPointSetToLabelHierarchy

# Build helix points.
theta = np.linspace(-1 * np.pi, 1 * np.pi, 100)
z = np.linspace(2, -2, 100)
r = z ** 2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
points = np.column_stack((x, y, z))

# Polyline source.
line_source = vtkPolyLineSource()
line_source.SetNumberOfPoints(len(points))
labels = vtkStringArray()
for i, point in enumerate(points):
    line_source.SetPoint(i, point[0], point[1], point[2])
    labels.InsertNextValue(f"x:{point[0]:.2f} y:{point[1]:.2f} z:{point[2]:.2f}")

line_source.Update()
line = line_source.GetOutput()
labels.SetName("labels")
line.GetPointData().AddArray(labels)

# Elevation filter for coloring.
elevation_filter = vtkElevationFilter()
elevation_filter.SetInputData(line)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(elevation_filter.GetOutputPort())

actor = vtkActor()
actor.GetProperty().SetLineWidth(10)
actor.GetProperty().SetRenderLinesAsTubes(True)
actor.SetMapper(mapper)

# Label hierarchy and placement mapper.
label_hierarchy = vtkPointSetToLabelHierarchy()
label_hierarchy.SetInputData(line)
label_hierarchy.SetLabelArrayName("labels")
label_hierarchy.Update()

label_mapper = vtkLabelPlacementMapper()
label_mapper.SetInputConnection(label_hierarchy.GetOutputPort())

label_actor = vtkActor2D()
label_actor.SetMapper(label_mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(label_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("label mapper")
render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
