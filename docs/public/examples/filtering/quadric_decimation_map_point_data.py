#!/usr/bin/env python

# Decimate a sphere using vtkQuadricDecimation with volume
# preservation and point data mapping, colored by analytical scalars.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkFiltersCore import vtkQuadricDecimation
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: high-resolution sphere
sphere = vtkSphereSource()
sphere.SetRadius(1.0)
sphere.SetThetaResolution(70)
sphere.SetPhiResolution(70)
sphere.Update()

output = sphere.GetOutput()
print(f"Cells before decimation: {output.GetNumberOfCells()}")

# Create analytical scalar data based on point positions
scalars = vtkDoubleArray()
scalars.SetName("Analytical")
scalars.SetNumberOfComponents(1)
scalars.SetNumberOfTuples(output.GetNumberOfPoints())

for i in range(output.GetNumberOfPoints()):
    pt = output.GetPoint(i)
    scalars.SetTuple1(i, math.sin(3.0 * (pt[0] + pt[1] + pt[2])))

output.GetPointData().AddArray(scalars)
output.GetPointData().SetScalars(scalars)

# Filter: quadric decimation with point data mapping
decimator = vtkQuadricDecimation()
decimator.SetInputConnection(sphere.GetOutputPort())
decimator.SetTargetReduction(0.90)
decimator.SetVolumePreservation(True)
decimator.SetMapPointData(True)
decimator.Update()

print(f"Cells after decimation: {decimator.GetOutput().GetNumberOfCells()}")

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(decimator.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToSurface()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("quadric decimation map point data")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(-1.5, 1.5, 1.5)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
