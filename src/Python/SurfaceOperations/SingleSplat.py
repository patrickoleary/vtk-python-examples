#!/usr/bin/env python

# Gaussian splatting of a single oriented point with an isosurface extraction.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkImagingHybrid import vtkGaussianSplatter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
beige = (0.961, 0.961, 0.863)
brown = (0.647, 0.165, 0.165)
deep_pink = (1.000, 0.078, 0.576)

# Source: create a single point with an oriented normal
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)

verts = vtkCellArray()
verts.InsertNextCell(1)
verts.InsertCellPoint(0)

normals = vtkDoubleArray()
normals.SetNumberOfTuples(1)
normals.SetNumberOfComponents(3)
normals.InsertTuple(0, (0.707, 0.707, 0.0))

scalars = vtkDoubleArray()
scalars.SetNumberOfTuples(1)
scalars.SetNumberOfComponents(1)
scalars.InsertTuple1(0, 1.0)

point_data = vtkPolyData()
point_data.SetPoints(points)
point_data.SetVerts(verts)
point_data.GetPointData().SetNormals(normals)
point_data.GetPointData().SetScalars(scalars)

# Filter: splat the point into a volume using a Gaussian distribution
splatter = vtkGaussianSplatter()
splatter.SetInputData(point_data)
splatter.SetModelBounds(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
splatter.SetSampleDimensions(75, 75, 75)
splatter.SetRadius(0.5)
splatter.SetEccentricity(5.0)
splatter.SetExponentFactor(-3.25)

# Filter: extract an isosurface from the splatted volume
contour = vtkContourFilter()
contour.SetInputConnection(splatter.GetOutputPort())
contour.SetValue(0, 0.9)

# Mapper: map the isosurface to graphics primitives
splat_mapper = vtkPolyDataMapper()
splat_mapper.SetInputConnection(contour.GetOutputPort())

# Actor: display the splatted isosurface
splat_actor = vtkActor()
splat_actor.SetMapper(splat_mapper)

# Filter: bounding outline of the sampling volume
outline = vtkOutlineFilter()
outline.SetInputConnection(splatter.GetOutputPort())

# Mapper: map the outline to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

# Actor: display the outline
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(brown)

# Source: cone glyph indicating the normal direction
cone = vtkConeSource()
cone.SetResolution(24)

# Mapper: map the cone to graphics primitives
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

# Actor: position the cone along the normal direction
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.SetScale(0.75, 0.75, 0.75)
cone_actor.RotateZ(45.0)
cone_actor.AddPosition(0.50, 0.50, 0.0)
cone_actor.GetProperty().SetColor(deep_pink)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(splat_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(cone_actor)
renderer.SetBackground(beige)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("SingleSplat")
render_window.SetSize(640, 640)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
