#!/usr/bin/env python

# Demonstrate vtkImprintFilter with sphere sources by imprinting a portion
# of one sphere onto another, rendering the imprinted result colored by
# cell field data with feature edges overlay.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkFeatureEdges
from vtkmodules.vtkFiltersModeling import vtkImprintFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

radius = 10.0
resolution = 4

# Target sphere (quarter)
target = vtkSphereSource()
target.SetRadius(radius)
target.SetCenter(0, 0, 0)
target.LatLongTessellationOn()
target.SetThetaResolution(4 * resolution)
target.SetPhiResolution(4 * resolution)
target.SetStartTheta(0)
target.SetEndTheta(90)

# Imprint sphere (smaller angular range, higher resolution)
imprint = vtkSphereSource()
imprint.SetRadius(radius)
imprint.SetCenter(0, 0, 0)
imprint.LatLongTessellationOn()
imprint.SetThetaResolution(8 * resolution)
imprint.SetPhiResolution(4 * resolution)
imprint.SetStartTheta(12)
imprint.SetEndTheta(57)
imprint.SetStartPhi(60.0)
imprint.SetEndPhi(120.0)

# Produce imprint
imprint_filter = vtkImprintFilter()
imprint_filter.SetTargetConnection(target.GetOutputPort())
imprint_filter.SetImprintConnection(imprint.GetOutputPort())
imprint_filter.SetTolerance(0.1)
imprint_filter.SetMergeTolerance(0.055)
imprint_filter.Update()

# Imprint result mapper colored by ImprintedCells field
imprint_filter_mapper = vtkPolyDataMapper()
imprint_filter_mapper.SetInputConnection(imprint_filter.GetOutputPort())
imprint_filter_mapper.SetScalarRange(0, 2)
imprint_filter_mapper.SetScalarModeToUseCellFieldData()
imprint_filter_mapper.SelectColorArray("ImprintedCells")

imprint_filter_actor = vtkActor()
imprint_filter_actor.SetMapper(imprint_filter_mapper)
imprint_filter_actor.GetProperty().SetColor(1, 0, 0)

# Feature edges (non-manifold and boundary)
feature_edges = vtkFeatureEdges()
feature_edges.SetInputConnection(imprint_filter.GetOutputPort())
feature_edges.ExtractAllEdgeTypesOff()
feature_edges.NonManifoldEdgesOn()
feature_edges.BoundaryEdgesOn()

feature_edges_mapper = vtkPolyDataMapper()
feature_edges_mapper.SetInputConnection(feature_edges.GetOutputPort())

feature_edges_actor = vtkActor()
feature_edges_actor.SetMapper(feature_edges_mapper)
feature_edges_actor.GetProperty().SetRepresentationToWireframe()
feature_edges_actor.GetProperty().SetColor(0, 1, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(imprint_filter_actor)
renderer.AddActor(feature_edges_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 200)
render_window.SetWindowName("imprint sphere sphere")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(1, 0.5, 0)
camera.SetFocalPoint(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
