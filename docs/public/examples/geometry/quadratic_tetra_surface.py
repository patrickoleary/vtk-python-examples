#!/usr/bin/env python
# Extract and render the surface of quadratic tetrahedra data.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Load the mesh geometry and data from a file.
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "quadraticTetra01.vtu"))
reader.Update()

# Extract the surface geometry.
geom = vtkDataSetSurfaceFilter()
geom.SetInputConnection(reader.GetOutputPort())
geom.Update()

# Create a blue to red lookup table.
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)

# Mapper.
mapper = vtkPolyDataMapper()
mapper.ScalarVisibilityOff()
mapper.SetInputConnection(geom.GetOutputPort())
if geom.GetOutput().GetPointData() and geom.GetOutput().GetPointData().GetScalars():
    mapper.SetScalarRange(geom.GetOutput().GetPointData().GetScalars().GetRange())

# Actor.
actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.5, 0.5, 0.5)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("quadratic tetra surface")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
