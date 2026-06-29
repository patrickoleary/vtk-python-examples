#!/usr/bin/env python

# Demonstrate vtkAdaptiveSubdivisionFilter by creating a low-resolution
# sphere, generating cell IDs, adaptively subdividing based on maximum
# edge length, and rendering with edge visibility and cell ID coloring.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkGenerateIds
from vtkmodules.vtkFiltersModeling import vtkAdaptiveSubdivisionFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a low-resolution sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(6)
sphere.SetPhiResolution(24)

# Generate cell and point IDs
generate_ids = vtkGenerateIds()
generate_ids.SetInputConnection(sphere.GetOutputPort())

# Adaptive subdivision by maximum edge length
adapt = vtkAdaptiveSubdivisionFilter()
adapt.SetInputConnection(generate_ids.GetOutputPort())
adapt.SetMaximumEdgeLength(0.1)
adapt.Update()

# Mapper colored by cell IDs
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(adapt.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("vtkCellIds")
mapper.SetScalarRange(adapt.GetOutput().GetCellData().GetScalars().GetRange())

# Edge property
edge_prop = vtkProperty()
edge_prop.EdgeVisibilityOn()
edge_prop.SetEdgeColor(0, 0, 0)

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetProperty(edge_prop)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("adaptive subdivision filter")

# Scene
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
