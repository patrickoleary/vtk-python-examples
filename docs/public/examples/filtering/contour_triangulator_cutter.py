#!/usr/bin/env python

# Demonstrate vtkContourTriangulator by cutting an outline box with a
# plane and triangulating the resulting contour.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkFiltersGeneral import vtkContourTriangulator
from vtkmodules.vtkFiltersSources import vtkOutlineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create outline box with faces
outline = vtkOutlineSource()
outline.SetBounds(-210.0, 210.0, -210.0, 210.0, -100.0, 150.0)
outline.GenerateFacesOn()

# Cut with a plane
plane = vtkPlane()
plane.SetNormal(0.0, 0.0, -1.0)
plane.SetOrigin(0.0, 0.0, 0.0)

cutter = vtkCutter()
cutter.SetInputConnection(outline.GetOutputPort())
cutter.SetCutFunction(plane)

# Cut contour lines actor
cut_mapper = vtkDataSetMapper()
cut_mapper.SetInputConnection(cutter.GetOutputPort())
cut_mapper.ScalarVisibilityOff()

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)
cut_actor.GetProperty().SetColor(0, 0, 0)

# Triangulate the cut contour
triangulator = vtkContourTriangulator()
triangulator.TriangulationErrorDisplayOn()
triangulator.SetInputConnection(cutter.GetOutputPort())

# Triangulated polygons actor
poly_mapper = vtkDataSetMapper()
poly_mapper.SetInputConnection(triangulator.GetOutputPort())
poly_mapper.ScalarVisibilityOff()

poly_actor = vtkActor()
poly_actor.SetMapper(poly_mapper)
poly_actor.GetProperty().SetColor(0.7, 0.9, 0.3)
poly_actor.GetProperty().EdgeVisibilityOn()
poly_actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(poly_actor)
renderer.AddActor(cut_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("contour triangulator cutter")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(-60)
renderer.GetActiveCamera().Elevation(25)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
