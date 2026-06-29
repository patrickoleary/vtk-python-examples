#!/usr/bin/env python

# Read PentaHexa mesh, clip, contour, triangulate+shrink and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersGeneral import (
    vtkClipDataSet,
    vtkDataSetTriangleFilter,
    vtkShrinkFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOLegacy import vtkUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read unstructured grid
grid_reader = vtkUnstructuredGridReader()
grid_reader.SetFileName(os.path.join(data_dir, "PentaHexa.vtk"))
grid_reader.Update()

# Clip
plane = vtkPlane()
plane.SetNormal(1, 1, 0)

clip = vtkClipDataSet()
clip.SetInputConnection(grid_reader.GetOutputPort())
clip.SetClipFunction(plane)
clip.GenerateClipScalarsOn()

surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(clip.GetOutputPort())

clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(surface.GetOutputPort())

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)

# Contour
contour = vtkContourFilter()
contour.SetInputConnection(grid_reader.GetOutputPort())
contour.SetValue(0, 0.125)
contour.SetValue(1, 0.25)
contour.SetValue(2, 0.5)
contour.SetValue(3, 0.75)
contour.SetValue(4, 1.0)

contour_surface = vtkDataSetSurfaceFilter()
contour_surface.SetInputConnection(contour.GetOutputPort())

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_surface.GetOutputPort())
contour_mapper.ScalarVisibilityOff()

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(1, 0, 0)
contour_actor.GetProperty().SetRepresentationToWireframe()

# Triangulate and shrink
tris = vtkDataSetTriangleFilter()
tris.SetInputConnection(grid_reader.GetOutputPort())

shrink = vtkShrinkFilter()
shrink.SetInputConnection(tris.GetOutputPort())
shrink.SetShrinkFactor(0.8)

tri_mapper = vtkDataSetMapper()
tri_mapper.SetInputConnection(shrink.GetOutputPort())
tri_mapper.SetScalarRange(0, 26)

tri_actor = vtkActor()
tri_actor.SetMapper(tri_mapper)
tri_actor.AddPosition(2, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(clip_actor)
renderer.AddActor(contour_actor)
renderer.AddActor(tri_actor)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("test hexa penta")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
