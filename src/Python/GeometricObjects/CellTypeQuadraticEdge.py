#!/usr/bin/env python

# Demonstrate vtkCellTypeSource for the Quadratic Edge cell type. The source
# generates an unstructured grid of quadratic edge cells, which are perturbed,
# shrunk, tessellated, and color-mapped by cell ID.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType text rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkIntArray,
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import VTK_QUADRATIC_EDGE
from vtkmodules.vtkFiltersGeneral import (
    vtkShrinkFilter,
    vtkTessellatorFilter,
)
from vtkmodules.vtkFiltersSources import vtkCellTypeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_blue_background_rgb = (0.2, 0.302, 0.4)

# Source: generate quadratic edge cells
source = vtkCellTypeSource()
source.SetCellType(VTK_QUADRATIC_EDGE)
source.Update()

# Perturb points so cell edges are visible after tessellation
original_points = source.GetOutput().GetPoints()
points = vtkPoints()
points.SetNumberOfPoints(source.GetOutput().GetNumberOfPoints())
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(5070)
for i in range(points.GetNumberOfPoints()):
    perturbation = [0.0, 0.0, 0.0]
    for j in range(3):
        rng.Next()
        perturbation[j] = rng.GetRangeValue(-0.1, 0.1)
    current = [0.0, 0.0, 0.0]
    original_points.GetPoint(i, current)
    points.SetPoint(i,
                    current[0] + perturbation[0],
                    current[1] + perturbation[1],
                    current[2] + perturbation[2])
source.GetOutput().SetPoints(points)

# Cell ID array for scalar coloring
num_cells = source.GetOutput().GetNumberOfCells()
id_array = vtkIntArray()
id_array.SetNumberOfTuples(num_cells)
for i in range(num_cells):
    id_array.InsertTuple1(i, i + 1)
id_array.SetName("Ids")
source.GetOutput().GetCellData().AddArray(id_array)
source.GetOutput().GetCellData().SetActiveScalars("Ids")

# Shrink: separate cells visually
shrink = vtkShrinkFilter()
shrink.SetInputConnection(source.GetOutputPort())
shrink.SetShrinkFactor(0.8)

# Tessellate: subdivide higher-order cells into linear primitives
tessellate = vtkTessellatorFilter()
tessellate.SetInputConnection(shrink.GetOutputPort())
tessellate.SetMaximumNumberOfSubdivisions(3)

# Mapper: color by cell ID
mapper = vtkDataSetMapper()
mapper.SetInputConnection(tessellate.GetOutputPort())
mapper.SetScalarRange(0, num_cells + 1)
mapper.SetScalarModeToUseCellData()
mapper.SetResolveCoincidentTopologyToPolygonOffset()

# Actor
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_blue_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("CellTypeQuadraticEdge")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
