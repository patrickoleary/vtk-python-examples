#!/usr/bin/env python

# Demonstrate vtkPlatonicSolidSource with cell normals visualized as
# arrow glyphs at cell centers, one viewport per solid type.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkCellCenters,
    vtkGlyph3D,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersSources import (
    vtkArrowSource,
    vtkPlatonicSolidSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Solid 0: Tetrahedron
source_0 = vtkPlatonicSolidSource()
source_0.SetSolidType(0)
source_0.Update()

normals_0 = vtkPolyDataNormals()
normals_0.SetInputConnection(source_0.GetOutputPort())
normals_0.ComputeCellNormalsOn()
normals_0.ComputePointNormalsOff()
normals_0.SplittingOff()
normals_0.Update()

centers_0 = vtkCellCenters()
centers_0.SetInputConnection(normals_0.GetOutputPort())
centers_0.Update()

arrow_0 = vtkArrowSource()

glyphs_0 = vtkGlyph3D()
glyphs_0.SetInputConnection(centers_0.GetOutputPort())
glyphs_0.SetSourceConnection(arrow_0.GetOutputPort())
glyphs_0.SetScaleModeToScaleByVector()
glyphs_0.SetScaleFactor(0.5)
glyphs_0.SetVectorModeToUseNormal()
glyphs_0.Update()

glyph_mapper_0 = vtkPolyDataMapper()
glyph_mapper_0.SetInputConnection(glyphs_0.GetOutputPort())
glyph_mapper_0.ScalarVisibilityOff()

glyph_actor_0 = vtkActor()
glyph_actor_0.SetMapper(glyph_mapper_0)

solid_mapper_0 = vtkPolyDataMapper()
solid_mapper_0.SetInputConnection(source_0.GetOutputPort())
solid_mapper_0.ScalarVisibilityOff()

solid_actor_0 = vtkActor()
solid_actor_0.GetProperty().SetColor(1.0, 0.3, 0.3)
solid_actor_0.SetMapper(solid_mapper_0)

renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.0, 0.0, 0.3)
renderer_0.AddActor(glyph_actor_0)
renderer_0.AddActor(solid_actor_0)

# Solid 1: Cube
source_1 = vtkPlatonicSolidSource()
source_1.SetSolidType(1)
source_1.Update()

normals_1 = vtkPolyDataNormals()
normals_1.SetInputConnection(source_1.GetOutputPort())
normals_1.ComputeCellNormalsOn()
normals_1.ComputePointNormalsOff()
normals_1.SplittingOff()
normals_1.Update()

centers_1 = vtkCellCenters()
centers_1.SetInputConnection(normals_1.GetOutputPort())
centers_1.Update()

arrow_1 = vtkArrowSource()

glyphs_1 = vtkGlyph3D()
glyphs_1.SetInputConnection(centers_1.GetOutputPort())
glyphs_1.SetSourceConnection(arrow_1.GetOutputPort())
glyphs_1.SetScaleModeToScaleByVector()
glyphs_1.SetScaleFactor(0.5)
glyphs_1.SetVectorModeToUseNormal()
glyphs_1.Update()

glyph_mapper_1 = vtkPolyDataMapper()
glyph_mapper_1.SetInputConnection(glyphs_1.GetOutputPort())
glyph_mapper_1.ScalarVisibilityOff()

glyph_actor_1 = vtkActor()
glyph_actor_1.SetMapper(glyph_mapper_1)

solid_mapper_1 = vtkPolyDataMapper()
solid_mapper_1.SetInputConnection(source_1.GetOutputPort())
solid_mapper_1.ScalarVisibilityOff()

solid_actor_1 = vtkActor()
solid_actor_1.GetProperty().SetColor(0.9, 0.9, 0.0)
solid_actor_1.SetMapper(solid_mapper_1)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.0, 0.0, 0.3)
renderer_1.AddActor(glyph_actor_1)
renderer_1.AddActor(solid_actor_1)

# Solid 2: Octahedron
source_2 = vtkPlatonicSolidSource()
source_2.SetSolidType(2)
source_2.Update()

normals_2 = vtkPolyDataNormals()
normals_2.SetInputConnection(source_2.GetOutputPort())
normals_2.ComputeCellNormalsOn()
normals_2.ComputePointNormalsOff()
normals_2.SplittingOff()
normals_2.Update()

centers_2 = vtkCellCenters()
centers_2.SetInputConnection(normals_2.GetOutputPort())
centers_2.Update()

arrow_2 = vtkArrowSource()

glyphs_2 = vtkGlyph3D()
glyphs_2.SetInputConnection(centers_2.GetOutputPort())
glyphs_2.SetSourceConnection(arrow_2.GetOutputPort())
glyphs_2.SetScaleModeToScaleByVector()
glyphs_2.SetScaleFactor(0.5)
glyphs_2.SetVectorModeToUseNormal()
glyphs_2.Update()

glyph_mapper_2 = vtkPolyDataMapper()
glyph_mapper_2.SetInputConnection(glyphs_2.GetOutputPort())
glyph_mapper_2.ScalarVisibilityOff()

glyph_actor_2 = vtkActor()
glyph_actor_2.SetMapper(glyph_mapper_2)

solid_mapper_2 = vtkPolyDataMapper()
solid_mapper_2.SetInputConnection(source_2.GetOutputPort())
solid_mapper_2.ScalarVisibilityOff()

solid_actor_2 = vtkActor()
solid_actor_2.GetProperty().SetColor(0.0, 1.0, 0.0)
solid_actor_2.SetMapper(solid_mapper_2)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(0.0, 0.0, 0.3)
renderer_2.AddActor(glyph_actor_2)
renderer_2.AddActor(solid_actor_2)

# Solid 3: Icosahedron
source_3 = vtkPlatonicSolidSource()
source_3.SetSolidType(3)
source_3.Update()

normals_3 = vtkPolyDataNormals()
normals_3.SetInputConnection(source_3.GetOutputPort())
normals_3.ComputeCellNormalsOn()
normals_3.ComputePointNormalsOff()
normals_3.SplittingOff()
normals_3.Update()

centers_3 = vtkCellCenters()
centers_3.SetInputConnection(normals_3.GetOutputPort())
centers_3.Update()

arrow_3 = vtkArrowSource()

glyphs_3 = vtkGlyph3D()
glyphs_3.SetInputConnection(centers_3.GetOutputPort())
glyphs_3.SetSourceConnection(arrow_3.GetOutputPort())
glyphs_3.SetScaleModeToScaleByVector()
glyphs_3.SetScaleFactor(0.5)
glyphs_3.SetVectorModeToUseNormal()
glyphs_3.Update()

glyph_mapper_3 = vtkPolyDataMapper()
glyph_mapper_3.SetInputConnection(glyphs_3.GetOutputPort())
glyph_mapper_3.ScalarVisibilityOff()

glyph_actor_3 = vtkActor()
glyph_actor_3.SetMapper(glyph_mapper_3)

solid_mapper_3 = vtkPolyDataMapper()
solid_mapper_3.SetInputConnection(source_3.GetOutputPort())
solid_mapper_3.ScalarVisibilityOff()

solid_actor_3 = vtkActor()
solid_actor_3.GetProperty().SetColor(0.1, 0.9, 0.9)
solid_actor_3.SetMapper(solid_mapper_3)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(0.0, 0.0, 0.3)
renderer_3.AddActor(glyph_actor_3)
renderer_3.AddActor(solid_actor_3)

# Solid 4: Dodecahedron
source_4 = vtkPlatonicSolidSource()
source_4.SetSolidType(4)
source_4.Update()

normals_4 = vtkPolyDataNormals()
normals_4.SetInputConnection(source_4.GetOutputPort())
normals_4.ComputeCellNormalsOn()
normals_4.ComputePointNormalsOff()
normals_4.SplittingOff()
normals_4.Update()

centers_4 = vtkCellCenters()
centers_4.SetInputConnection(normals_4.GetOutputPort())
centers_4.Update()

arrow_4 = vtkArrowSource()

glyphs_4 = vtkGlyph3D()
glyphs_4.SetInputConnection(centers_4.GetOutputPort())
glyphs_4.SetSourceConnection(arrow_4.GetOutputPort())
glyphs_4.SetScaleModeToScaleByVector()
glyphs_4.SetScaleFactor(0.5)
glyphs_4.SetVectorModeToUseNormal()
glyphs_4.Update()

glyph_mapper_4 = vtkPolyDataMapper()
glyph_mapper_4.SetInputConnection(glyphs_4.GetOutputPort())
glyph_mapper_4.ScalarVisibilityOff()

glyph_actor_4 = vtkActor()
glyph_actor_4.SetMapper(glyph_mapper_4)

solid_mapper_4 = vtkPolyDataMapper()
solid_mapper_4.SetInputConnection(source_4.GetOutputPort())
solid_mapper_4.ScalarVisibilityOff()

solid_actor_4 = vtkActor()
solid_actor_4.GetProperty().SetColor(0.2, 0.4, 1.0)
solid_actor_4.SetMapper(solid_mapper_4)

renderer_4 = vtkRenderer()
renderer_4.SetBackground(0.0, 0.0, 0.3)
renderer_4.AddActor(glyph_actor_4)
renderer_4.AddActor(solid_actor_4)

# Window with horizontal viewports
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(1000, 300)
render_window.SetWindowName("platonic normals")

renderer_0.SetViewport(0.0, 0.0, 0.2, 1.0)
render_window.AddRenderer(renderer_0)
renderer_1.SetViewport(0.2, 0.0, 0.4, 1.0)
render_window.AddRenderer(renderer_1)
renderer_2.SetViewport(0.4, 0.0, 0.6, 1.0)
render_window.AddRenderer(renderer_2)
renderer_3.SetViewport(0.6, 0.0, 0.8, 1.0)
render_window.AddRenderer(renderer_3)
renderer_4.SetViewport(0.8, 0.0, 1.0, 1.0)
render_window.AddRenderer(renderer_4)

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.SetFocalPoint(0.0, 0.0, 0.0)
camera_0.SetPosition(3.0, 2.0, 8.0)
camera_0.OrthogonalizeViewUp()

camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(0.0, 0.0, 0.0)
camera_1.SetPosition(3.0, 2.0, 8.0)
camera_1.OrthogonalizeViewUp()

camera_2 = renderer_2.GetActiveCamera()
camera_2.SetFocalPoint(0.0, 0.0, 0.0)
camera_2.SetPosition(3.0, 2.0, 8.0)
camera_2.OrthogonalizeViewUp()

camera_3 = renderer_3.GetActiveCamera()
camera_3.SetFocalPoint(0.0, 0.0, 0.0)
camera_3.SetPosition(3.0, 2.0, 8.0)
camera_3.OrthogonalizeViewUp()

camera_4 = renderer_4.GetActiveCamera()
camera_4.SetFocalPoint(0.0, 0.0, 0.0)
camera_4.SetPosition(3.0, 2.0, 8.0)
camera_4.OrthogonalizeViewUp()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
