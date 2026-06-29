#!/usr/bin/env python

# Demonstrate structured grid blanking with vtkDataSetSurfaceFilter,
# blanking specific cells and verifying visible surface polygons.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Grid dimensions
xlim = 10
ylim = 10
zlim = 3

# Create structured grid
sg = vtkStructuredGrid()
sg.SetExtent(0, xlim, 0, ylim, 0, zlim)

# Set point coordinates
points = vtkPoints()
for z in range(0, zlim + 1):
    for y in range(0, ylim + 1):
        for x in range(0, xlim + 1):
            points.InsertNextPoint(x, y, z)
sg.SetPoints(points)

# Set scalar array
scalars = vtkDoubleArray()
scalars.SetNumberOfComponents(1)
scalars.SetName("Xcoord")
for z in range(0, zlim + 1):
    for y in range(0, ylim + 1):
        for x in range(0, xlim + 1):
            scalars.InsertNextValue(x + y + z)
sg.GetPointData().SetScalars(scalars)

# Blank specific cells
num_cells = sg.GetNumberOfCells()
if 11 < num_cells:
    sg.BlankCell(11)
if 64 < num_cells:
    sg.BlankCell(64)
if 164 < num_cells:
    sg.BlankCell(164)
for c in range(180, 261):
    if c < sg.GetNumberOfCells():
        sg.BlankCell(c)

# Extract surface
dsf = vtkDataSetSurfaceFilter()
dsf.SetInputData(sg)
dsf.Update()

# Render
mapper = vtkDataSetMapper()
mapper.SetInputData(sg)
mapper.SetScalarRange(scalars.GetRange())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("structuredgrid blanking")

# Set camera to view blanked cells
cam = renderer.GetActiveCamera()
cam.SetClippingRange(14.0456, 45.4716)
cam.SetFocalPoint(5, 5, 1.5)
cam.SetPosition(-19.0905, -6.73006, -6.37738)
cam.SetViewUp(-0.400229, 0.225459, 0.888248)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
