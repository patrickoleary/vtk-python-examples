#!/usr/bin/env python

# Extract the outer surface of a hexahedron and cut it with a plane.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkHexahedron,
    vtkPlane,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
yellow = (1.000, 1.000, 0.000)
black = (0.000, 0.000, 0.000)
red = (1.000, 0.000, 0.000)
seashell = (1.000, 0.961, 0.933)

# Source: define the eight corner points of a hexahedron
point_coords = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 1.0],
]

points = vtkPoints()
hexa = vtkHexahedron()
for i, coord in enumerate(point_coords):
    points.InsertNextPoint(coord)
    hexa.GetPointIds().SetId(i, i)

hexs = vtkCellArray()
hexs.InsertNextCell(hexa)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(hexa.GetCellType(), hexa.GetPointIds())

# Filter: extract the outer polygonal surface
surface = vtkDataSetSurfaceFilter()
surface.SetInputData(u_grid)
surface.Update()

# Mapper: map the surface to graphics primitives
beam_mapper = vtkDataSetMapper()
beam_mapper.SetInputConnection(surface.GetOutputPort())

# Actor: display the hexahedron surface with edge visibility
beam_actor = vtkActor()
beam_actor.SetMapper(beam_mapper)
beam_actor.GetProperty().SetColor(yellow)
beam_actor.GetProperty().SetOpacity(0.60)
beam_actor.GetProperty().EdgeVisibilityOn()
beam_actor.GetProperty().SetEdgeColor(black)
beam_actor.GetProperty().SetLineWidth(1.5)

# Implicit function: cutting plane in the XZ direction
plane = vtkPlane()
plane.SetOrigin(0.5, 0, 0)
plane.SetNormal(1, 0, 0)

# Filter: cut the surface with the plane
cutter = vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputData(beam_actor.GetMapper().GetInput())
cutter.Update()

# Mapper: map the cut line to graphics primitives
cutter_mapper = vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())

# Actor: display the cut line
plane_actor = vtkActor()
plane_actor.SetMapper(cutter_mapper)
plane_actor.GetProperty().SetColor(red)
plane_actor.GetProperty().SetLineWidth(2)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(beam_actor)
renderer.AddActor(plane_actor)
renderer.SetBackground(seashell)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(-25)
renderer.GetActiveCamera().Elevation(30)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("DataSetSurface")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
