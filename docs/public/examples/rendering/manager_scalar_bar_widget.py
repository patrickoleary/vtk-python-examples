#!/usr/bin/env python
# Demonstrate vtkScalarBarWidget with a lookup table on unstructured grid data.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkInteractionWidgets import vtkScalarBarWidget
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

colors = vtkNamedColors()

# Custom lookup table.
lut = vtkLookupTable()
lut.Build()

# Read unstructured grid.
reader = vtkUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "uGridEx.vtk"))
reader.Update()
output = reader.GetOutput()
scalar_range = output.GetScalarRange()

# Mapper.
mapper = vtkDataSetMapper()
mapper.SetInputData(output)
mapper.SetScalarRange(scalar_range)
mapper.SetLookupTable(lut)

# Actor.
actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(colors.GetColor3d("MidnightBlue"))

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("manager scalar bar widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scalar bar widget.
scalar_bar = vtkScalarBarActor()
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetLookupTable(lut)

scalar_bar_widget = vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(interactor)
scalar_bar_widget.SetScalarBarActor(scalar_bar)
scalar_bar_widget.On()

# Scene
renderer.GetActiveCamera().SetPosition(-6.4, 10.3, 1.4)
renderer.GetActiveCamera().SetFocalPoint(1.0, 0.5, 3.0)
renderer.GetActiveCamera().SetViewUp(0.6, 0.4, -0.7)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
