#!/usr/bin/env python

# Demonstrate vtkMergeVectorComponents by creating three scalar arrays
# on a sphere (one per component), merging them into a vector, and
# rendering the sphere colored by the merged vector magnitude.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersGeneral import vtkMergeVectorComponents
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere
sphere = vtkSphereSource()
sphere.SetRadius(5.0)
sphere.SetPhiResolution(30)
sphere.SetThetaResolution(30)
sphere.Update()

dataset = sphere.GetOutput()

# Create three scalar arrays for point data
x_arr = vtkDoubleArray()
x_arr.SetNumberOfValues(dataset.GetNumberOfPoints())
x_arr.SetName("xPD")

y_arr = vtkDoubleArray()
y_arr.SetNumberOfValues(dataset.GetNumberOfPoints())
y_arr.SetName("yPD")

z_arr = vtkDoubleArray()
z_arr.SetNumberOfValues(dataset.GetNumberOfPoints())
z_arr.SetName("zPD")

for i in range(dataset.GetNumberOfPoints()):
    pt = dataset.GetPoint(i)
    x_arr.SetValue(i, pt[0])
    y_arr.SetValue(i, pt[1])
    z_arr.SetValue(i, pt[2])

dataset.GetPointData().AddArray(x_arr)
dataset.GetPointData().AddArray(y_arr)
dataset.GetPointData().AddArray(z_arr)

# Merge the three scalar arrays into a vector
merge = vtkMergeVectorComponents()
merge.SetInputData(dataset)
merge.SetXArrayName("xPD")
merge.SetYArrayName("yPD")
merge.SetZArrayName("zPD")
merge.SetAttributeType(vtkDataObject.POINT)
merge.SetOutputVectorName("MergedVector")
merge.Update()

# Render colored by merged vector magnitude
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(merge.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("MergedVector")
mapper.SetScalarRange(0, 5)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("merge vector components")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
