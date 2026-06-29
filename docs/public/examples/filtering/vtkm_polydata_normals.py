#!/usr/bin/env python
# Demonstrate vtkmPolyDataNormals with point and cell normal glyphs on a cylinder.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmPolyDataNormals
from vtkmodules.vtkFiltersCore import vtkCellCenters, vtkCleanPolyData, vtkGlyph3D, vtkTriangleFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource, vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build input: triangulated, cleaned cylinder.
cylinder = vtkCylinderSource()
cylinder.SetRadius(1.0)
cylinder.SetResolution(8)
cylinder.CappingOn()

triangle = vtkTriangleFilter()
triangle.SetInputConnection(cylinder.GetOutputPort())

clean = vtkCleanPolyData()
clean.SetInputConnection(triangle.GetOutputPort())
clean.Update()

input_pd = clean.GetOutput()
input_pd.GetPointData().Initialize()
input_pd.GetCellData().Initialize()

# Compute normals via VTK-m.
normals = vtkmPolyDataNormals()
normals.SetInputData(input_pd)
normals.ComputePointNormalsOn()
normals.ComputeCellNormalsOn()
normals.AutoOrientNormalsOn()
normals.FlipNormalsOn()
normals.ConsistencyOn()

# Wireframe cylinder actor.
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputData(input_pd)

cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_property = cylinder_actor.MakeProperty()
cylinder_property.SetRepresentationToWireframe()
cylinder_property.SetColor(0.3, 0.3, 0.3)
cylinder_actor.SetProperty(cylinder_property)

arrow = vtkArrowSource()

# --- Point normals viewport ---
pn_glyphs = vtkGlyph3D()
pn_glyphs.SetInputConnection(normals.GetOutputPort())
pn_glyphs.SetSourceConnection(arrow.GetOutputPort())
pn_glyphs.SetScaleFactor(0.5)
pn_glyphs.OrientOn()
pn_glyphs.SetVectorModeToUseNormal()

pn_mapper = vtkPolyDataMapper()
pn_mapper.SetInputConnection(pn_glyphs.GetOutputPort())

pn_actor = vtkActor()
pn_actor.SetMapper(pn_mapper)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.AddActor(cylinder_actor)
renderer_0.AddActor(pn_actor)

# --- Cell normals viewport ---
cells = vtkCellCenters()
cells.SetInputConnection(normals.GetOutputPort())

cn_glyphs = vtkGlyph3D()
cn_glyphs.SetInputConnection(cells.GetOutputPort())
cn_glyphs.SetSourceConnection(arrow.GetOutputPort())
cn_glyphs.SetScaleFactor(0.5)
cn_glyphs.OrientOn()
cn_glyphs.SetVectorModeToUseNormal()

cn_mapper = vtkPolyDataMapper()
cn_mapper.SetInputConnection(cn_glyphs.GetOutputPort())

cn_actor = vtkActor()
cn_actor.SetMapper(cn_mapper)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.AddActor(cylinder_actor)
renderer_1.AddActor(cn_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetWindowName("vtkm polydata normals")
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)

# Scene
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().SetPosition(0.0, 4.5, 7.5)
renderer_0.ResetCameraClippingRange()
renderer_1.ResetCamera()
renderer_1.GetActiveCamera().SetPosition(0.0, 8.0, 0.1)
renderer_1.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
