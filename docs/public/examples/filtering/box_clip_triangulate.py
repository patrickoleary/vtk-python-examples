#!/usr/bin/env python

# Verify vtkBoxClipDataSet correctly triangulates multiple cell types
# (triangle strips, quads, pixels, polygons, hexahedra, voxels, wedges,
# pyramids) by clipping and displaying the resulting surfaces.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    VTK_PIXEL,
    VTK_POLYGON,
    VTK_PYRAMID,
    VTK_QUAD,
    VTK_TRIANGLE_STRIP,
    VTK_VOXEL,
    VTK_WEDGE,
    vtkCellArray,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkBoxClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# --- Col 0: Triangle strip ---
tstrip_pts = vtkPoints()
tstrip_pts.SetNumberOfPoints(13)
tstrip_pts.SetPoint(0, 0.0, 0.0, 0.0)
tstrip_pts.SetPoint(1, 0.0, 1.0, 0.0)
tstrip_pts.SetPoint(2, 1.0, 0.0, 0.0)
tstrip_pts.SetPoint(3, 1.0, 1.0, 0.0)
tstrip_pts.SetPoint(4, 2.0, 0.0, 0.0)
tstrip_pts.SetPoint(5, 2.0, 1.0, 0.0)
tstrip_pts.SetPoint(6, 0.0, 0.0, 1.0)
tstrip_pts.SetPoint(7, 0.0, 1.0, 1.0)
tstrip_pts.SetPoint(8, 1.0, 0.0, 1.0)
tstrip_pts.SetPoint(9, 1.0, 1.0, 1.0)
tstrip_pts.SetPoint(10, 2.0, 0.0, 1.0)
tstrip_pts.SetPoint(11, 2.0, 1.0, 1.0)
tstrip_pts.SetPoint(12, 2.0, 0.5, 1.0)
tstrip_grid = vtkUnstructuredGrid()
tstrip_grid.SetPoints(tstrip_pts)
tstrip_grid.InsertNextCell(VTK_TRIANGLE_STRIP, 6, [1, 0, 3, 2, 5, 4])

tstrip_clip = vtkBoxClipDataSet()
tstrip_clip.SetInputData(tstrip_grid)
tstrip_clip.SetBoxClip(0.0, 2.0, 0.0, 1.0, 0.0, 1.0)

tstrip_surface = vtkDataSetSurfaceFilter()
tstrip_surface.SetInputConnection(tstrip_clip.GetOutputPort())

tstrip_mapper = vtkPolyDataMapper()
tstrip_mapper.SetInputConnection(tstrip_surface.GetOutputPort())

tstrip_actor = vtkActor()
tstrip_actor.SetMapper(tstrip_mapper)

tstrip_renderer = vtkRenderer()
tstrip_renderer.AddActor(tstrip_actor)
tstrip_renderer.SetBackground(0.0, 0.5, 0.5)
tstrip_renderer.SetViewport(0.0 / 8, 0, 1.0 / 8, 1)
tstrip_renderer.ResetCamera()
tstrip_renderer.GetActiveCamera().Azimuth(25.0)
tstrip_renderer.GetActiveCamera().Elevation(-25.0)

# --- Col 1: Quads ---
quad_pts = vtkPoints()
quad_pts.SetNumberOfPoints(13)
quad_pts.SetPoint(0, 0.0, 0.0, 0.0)
quad_pts.SetPoint(1, 0.0, 1.0, 0.0)
quad_pts.SetPoint(2, 1.0, 0.0, 0.0)
quad_pts.SetPoint(3, 1.0, 1.0, 0.0)
quad_pts.SetPoint(4, 2.0, 0.0, 0.0)
quad_pts.SetPoint(5, 2.0, 1.0, 0.0)
quad_pts.SetPoint(6, 0.0, 0.0, 1.0)
quad_pts.SetPoint(7, 0.0, 1.0, 1.0)
quad_pts.SetPoint(8, 1.0, 0.0, 1.0)
quad_pts.SetPoint(9, 1.0, 1.0, 1.0)
quad_pts.SetPoint(10, 2.0, 0.0, 1.0)
quad_pts.SetPoint(11, 2.0, 1.0, 1.0)
quad_pts.SetPoint(12, 2.0, 0.5, 1.0)
quad_grid = vtkUnstructuredGrid()
quad_grid.SetPoints(quad_pts)
quad_grid.InsertNextCell(VTK_QUAD, 4, [0, 2, 3, 1])
quad_grid.InsertNextCell(VTK_QUAD, 4, [2, 4, 5, 3])

quad_clip = vtkBoxClipDataSet()
quad_clip.SetInputData(quad_grid)
quad_clip.SetBoxClip(0.0, 2.0, 0.0, 1.0, 0.0, 1.0)

quad_surface = vtkDataSetSurfaceFilter()
quad_surface.SetInputConnection(quad_clip.GetOutputPort())

quad_mapper = vtkPolyDataMapper()
quad_mapper.SetInputConnection(quad_surface.GetOutputPort())

quad_actor = vtkActor()
quad_actor.SetMapper(quad_mapper)

quad_renderer = vtkRenderer()
quad_renderer.AddActor(quad_actor)
quad_renderer.SetBackground(0.0, 0.5, 0.5)
quad_renderer.SetViewport(1.0 / 8, 0, 2.0 / 8, 1)
quad_renderer.ResetCamera()
quad_renderer.GetActiveCamera().Azimuth(25.0)
quad_renderer.GetActiveCamera().Elevation(-25.0)

# --- Col 2: Pixels ---
pixel_pts = vtkPoints()
pixel_pts.SetNumberOfPoints(13)
pixel_pts.SetPoint(0, 0.0, 0.0, 0.0)
pixel_pts.SetPoint(1, 0.0, 1.0, 0.0)
pixel_pts.SetPoint(2, 1.0, 0.0, 0.0)
pixel_pts.SetPoint(3, 1.0, 1.0, 0.0)
pixel_pts.SetPoint(4, 2.0, 0.0, 0.0)
pixel_pts.SetPoint(5, 2.0, 1.0, 0.0)
pixel_pts.SetPoint(6, 0.0, 0.0, 1.0)
pixel_pts.SetPoint(7, 0.0, 1.0, 1.0)
pixel_pts.SetPoint(8, 1.0, 0.0, 1.0)
pixel_pts.SetPoint(9, 1.0, 1.0, 1.0)
pixel_pts.SetPoint(10, 2.0, 0.0, 1.0)
pixel_pts.SetPoint(11, 2.0, 1.0, 1.0)
pixel_pts.SetPoint(12, 2.0, 0.5, 1.0)
pixel_grid = vtkUnstructuredGrid()
pixel_grid.SetPoints(pixel_pts)
pixel_grid.InsertNextCell(VTK_PIXEL, 4, [0, 2, 1, 3])
pixel_grid.InsertNextCell(VTK_PIXEL, 4, [2, 4, 3, 5])

pixel_clip = vtkBoxClipDataSet()
pixel_clip.SetInputData(pixel_grid)
pixel_clip.SetBoxClip(0.0, 2.0, 0.0, 1.0, 0.0, 1.0)

pixel_surface = vtkDataSetSurfaceFilter()
pixel_surface.SetInputConnection(pixel_clip.GetOutputPort())

pixel_mapper = vtkPolyDataMapper()
pixel_mapper.SetInputConnection(pixel_surface.GetOutputPort())

pixel_actor = vtkActor()
pixel_actor.SetMapper(pixel_mapper)

pixel_renderer = vtkRenderer()
pixel_renderer.AddActor(pixel_actor)
pixel_renderer.SetBackground(0.0, 0.5, 0.5)
pixel_renderer.SetViewport(2.0 / 8, 0, 3.0 / 8, 1)
pixel_renderer.ResetCamera()
pixel_renderer.GetActiveCamera().Azimuth(25.0)
pixel_renderer.GetActiveCamera().Elevation(-25.0)

# --- Col 3: Polygons ---
polygon_pts = vtkPoints()
polygon_pts.SetNumberOfPoints(13)
polygon_pts.SetPoint(0, 0.0, 0.0, 0.0)
polygon_pts.SetPoint(1, 0.0, 1.0, 0.0)
polygon_pts.SetPoint(2, 1.0, 0.0, 0.0)
polygon_pts.SetPoint(3, 1.0, 1.0, 0.0)
polygon_pts.SetPoint(4, 2.0, 0.0, 0.0)
polygon_pts.SetPoint(5, 2.0, 1.0, 0.0)
polygon_pts.SetPoint(6, 0.0, 0.0, 1.0)
polygon_pts.SetPoint(7, 0.0, 1.0, 1.0)
polygon_pts.SetPoint(8, 1.0, 0.0, 1.0)
polygon_pts.SetPoint(9, 1.0, 1.0, 1.0)
polygon_pts.SetPoint(10, 2.0, 0.0, 1.0)
polygon_pts.SetPoint(11, 2.0, 1.0, 1.0)
polygon_pts.SetPoint(12, 2.0, 0.5, 1.0)
polygon_grid = vtkUnstructuredGrid()
polygon_grid.SetPoints(polygon_pts)
polygon_grid.InsertNextCell(VTK_POLYGON, 4, [0, 2, 3, 1])
polygon_grid.InsertNextCell(VTK_POLYGON, 3, [2, 4, 5])
polygon_grid.InsertNextCell(VTK_POLYGON, 5, [6, 8, 12, 9, 7])

polygon_clip = vtkBoxClipDataSet()
polygon_clip.SetInputData(polygon_grid)
polygon_clip.SetBoxClip(0.0, 2.0, 0.0, 1.0, 0.0, 1.0)

polygon_surface = vtkDataSetSurfaceFilter()
polygon_surface.SetInputConnection(polygon_clip.GetOutputPort())

polygon_mapper = vtkPolyDataMapper()
polygon_mapper.SetInputConnection(polygon_surface.GetOutputPort())

polygon_actor = vtkActor()
polygon_actor.SetMapper(polygon_mapper)

polygon_renderer = vtkRenderer()
polygon_renderer.AddActor(polygon_actor)
polygon_renderer.SetBackground(0.0, 0.5, 0.5)
polygon_renderer.SetViewport(3.0 / 8, 0, 4.0 / 8, 1)
polygon_renderer.ResetCamera()
polygon_renderer.GetActiveCamera().Azimuth(25.0)
polygon_renderer.GetActiveCamera().Elevation(-25.0)

# --- Col 4: Hexahedra ---
hex_pts = vtkPoints()
hex_pts.SetNumberOfPoints(13)
hex_pts.SetPoint(0, 0.0, 0.0, 0.0)
hex_pts.SetPoint(1, 0.0, 1.0, 0.0)
hex_pts.SetPoint(2, 1.0, 0.0, 0.0)
hex_pts.SetPoint(3, 1.0, 1.0, 0.0)
hex_pts.SetPoint(4, 2.0, 0.0, 0.0)
hex_pts.SetPoint(5, 2.0, 1.0, 0.0)
hex_pts.SetPoint(6, 0.0, 0.0, 1.0)
hex_pts.SetPoint(7, 0.0, 1.0, 1.0)
hex_pts.SetPoint(8, 1.0, 0.0, 1.0)
hex_pts.SetPoint(9, 1.0, 1.0, 1.0)
hex_pts.SetPoint(10, 2.0, 0.0, 1.0)
hex_pts.SetPoint(11, 2.0, 1.0, 1.0)
hex_pts.SetPoint(12, 2.0, 0.5, 1.0)
hex_grid = vtkUnstructuredGrid()
hex_grid.SetPoints(hex_pts)
hex_grid.InsertNextCell(VTK_HEXAHEDRON, 8, [6, 8, 2, 0, 7, 9, 3, 1])
hex_grid.InsertNextCell(VTK_HEXAHEDRON, 8, [4, 2, 8, 10, 5, 3, 9, 11])

hex_clip = vtkBoxClipDataSet()
hex_clip.SetInputData(hex_grid)
hex_clip.SetBoxClip(0.0, 2.0, 0.0, 1.0, 0.0, 1.0)

hex_surface = vtkDataSetSurfaceFilter()
hex_surface.SetInputConnection(hex_clip.GetOutputPort())

hex_mapper = vtkPolyDataMapper()
hex_mapper.SetInputConnection(hex_surface.GetOutputPort())

hex_actor = vtkActor()
hex_actor.SetMapper(hex_mapper)

hex_renderer = vtkRenderer()
hex_renderer.AddActor(hex_actor)
hex_renderer.SetBackground(0.0, 0.5, 0.5)
hex_renderer.SetViewport(4.0 / 8, 0, 5.0 / 8, 1)
hex_renderer.ResetCamera()
hex_renderer.GetActiveCamera().Azimuth(25.0)
hex_renderer.GetActiveCamera().Elevation(-25.0)

# --- Col 5: Voxels ---
voxel_pts = vtkPoints()
voxel_pts.SetNumberOfPoints(13)
voxel_pts.SetPoint(0, 0.0, 0.0, 0.0)
voxel_pts.SetPoint(1, 0.0, 1.0, 0.0)
voxel_pts.SetPoint(2, 1.0, 0.0, 0.0)
voxel_pts.SetPoint(3, 1.0, 1.0, 0.0)
voxel_pts.SetPoint(4, 2.0, 0.0, 0.0)
voxel_pts.SetPoint(5, 2.0, 1.0, 0.0)
voxel_pts.SetPoint(6, 0.0, 0.0, 1.0)
voxel_pts.SetPoint(7, 0.0, 1.0, 1.0)
voxel_pts.SetPoint(8, 1.0, 0.0, 1.0)
voxel_pts.SetPoint(9, 1.0, 1.0, 1.0)
voxel_pts.SetPoint(10, 2.0, 0.0, 1.0)
voxel_pts.SetPoint(11, 2.0, 1.0, 1.0)
voxel_pts.SetPoint(12, 2.0, 0.5, 1.0)
voxel_grid = vtkUnstructuredGrid()
voxel_grid.SetPoints(voxel_pts)
voxel_grid.InsertNextCell(VTK_VOXEL, 8, [0, 2, 1, 3, 6, 8, 7, 9])
voxel_grid.InsertNextCell(VTK_VOXEL, 8, [10, 8, 11, 9, 4, 2, 5, 3])

voxel_clip = vtkBoxClipDataSet()
voxel_clip.SetInputData(voxel_grid)
voxel_clip.SetBoxClip(0.0, 2.0, 0.0, 1.0, 0.0, 1.0)

voxel_surface = vtkDataSetSurfaceFilter()
voxel_surface.SetInputConnection(voxel_clip.GetOutputPort())

voxel_mapper = vtkPolyDataMapper()
voxel_mapper.SetInputConnection(voxel_surface.GetOutputPort())

voxel_actor = vtkActor()
voxel_actor.SetMapper(voxel_mapper)

voxel_renderer = vtkRenderer()
voxel_renderer.AddActor(voxel_actor)
voxel_renderer.SetBackground(0.0, 0.5, 0.5)
voxel_renderer.SetViewport(5.0 / 8, 0, 6.0 / 8, 1)
voxel_renderer.ResetCamera()
voxel_renderer.GetActiveCamera().Azimuth(25.0)
voxel_renderer.GetActiveCamera().Elevation(-25.0)

# --- Col 6: Wedges ---
wedge_pts = vtkPoints()
wedge_pts.SetNumberOfPoints(13)
wedge_pts.SetPoint(0, 0.0, 0.0, 0.0)
wedge_pts.SetPoint(1, 0.0, 1.0, 0.0)
wedge_pts.SetPoint(2, 1.0, 0.0, 0.0)
wedge_pts.SetPoint(3, 1.0, 1.0, 0.0)
wedge_pts.SetPoint(4, 2.0, 0.0, 0.0)
wedge_pts.SetPoint(5, 2.0, 1.0, 0.0)
wedge_pts.SetPoint(6, 0.0, 0.0, 1.0)
wedge_pts.SetPoint(7, 0.0, 1.0, 1.0)
wedge_pts.SetPoint(8, 1.0, 0.0, 1.0)
wedge_pts.SetPoint(9, 1.0, 1.0, 1.0)
wedge_pts.SetPoint(10, 2.0, 0.0, 1.0)
wedge_pts.SetPoint(11, 2.0, 1.0, 1.0)
wedge_pts.SetPoint(12, 2.0, 0.5, 1.0)
wedge_grid = vtkUnstructuredGrid()
wedge_grid.SetPoints(wedge_pts)
wedge_grid.InsertNextCell(VTK_WEDGE, 6, [0, 1, 2, 6, 7, 8])
wedge_grid.InsertNextCell(VTK_WEDGE, 6, [7, 8, 9, 1, 2, 3])
wedge_grid.InsertNextCell(VTK_WEDGE, 6, [8, 11, 9, 2, 5, 3])
wedge_grid.InsertNextCell(VTK_WEDGE, 6, [2, 5, 4, 8, 11, 10])

wedge_clip = vtkBoxClipDataSet()
wedge_clip.SetInputData(wedge_grid)
wedge_clip.SetBoxClip(0.0, 2.0, 0.0, 1.0, 0.0, 1.0)

wedge_surface = vtkDataSetSurfaceFilter()
wedge_surface.SetInputConnection(wedge_clip.GetOutputPort())

wedge_mapper = vtkPolyDataMapper()
wedge_mapper.SetInputConnection(wedge_surface.GetOutputPort())

wedge_actor = vtkActor()
wedge_actor.SetMapper(wedge_mapper)

wedge_renderer = vtkRenderer()
wedge_renderer.AddActor(wedge_actor)
wedge_renderer.SetBackground(0.0, 0.5, 0.5)
wedge_renderer.SetViewport(6.0 / 8, 0, 7.0 / 8, 1)
wedge_renderer.ResetCamera()
wedge_renderer.GetActiveCamera().Azimuth(25.0)
wedge_renderer.GetActiveCamera().Elevation(-25.0)

# --- Col 7: Pyramids ---
pyramid_pts = vtkPoints()
pyramid_pts.SetNumberOfPoints(13)
pyramid_pts.SetPoint(0, 0.0, 0.0, 0.0)
pyramid_pts.SetPoint(1, 0.0, 1.0, 0.0)
pyramid_pts.SetPoint(2, 1.0, 0.0, 0.0)
pyramid_pts.SetPoint(3, 1.0, 1.0, 0.0)
pyramid_pts.SetPoint(4, 2.0, 0.0, 0.0)
pyramid_pts.SetPoint(5, 2.0, 1.0, 0.0)
pyramid_pts.SetPoint(6, 0.0, 0.0, 1.0)
pyramid_pts.SetPoint(7, 0.0, 1.0, 1.0)
pyramid_pts.SetPoint(8, 1.0, 0.0, 1.0)
pyramid_pts.SetPoint(9, 1.0, 1.0, 1.0)
pyramid_pts.SetPoint(10, 2.0, 0.0, 1.0)
pyramid_pts.SetPoint(11, 2.0, 1.0, 1.0)
pyramid_pts.SetPoint(12, 2.0, 0.5, 1.0)
pyramid_grid = vtkUnstructuredGrid()
pyramid_grid.SetPoints(pyramid_pts)
pyramid_grid.InsertNextCell(VTK_PYRAMID, 5, [8, 9, 3, 2, 0])
pyramid_grid.InsertNextCell(VTK_PYRAMID, 5, [2, 3, 9, 8, 12])

pyramid_clip = vtkBoxClipDataSet()
pyramid_clip.SetInputData(pyramid_grid)
pyramid_clip.SetBoxClip(0.0, 2.0, 0.0, 1.0, 0.0, 1.0)

pyramid_surface = vtkDataSetSurfaceFilter()
pyramid_surface.SetInputConnection(pyramid_clip.GetOutputPort())

pyramid_mapper = vtkPolyDataMapper()
pyramid_mapper.SetInputConnection(pyramid_surface.GetOutputPort())

pyramid_actor = vtkActor()
pyramid_actor.SetMapper(pyramid_mapper)

pyramid_renderer = vtkRenderer()
pyramid_renderer.AddActor(pyramid_actor)
pyramid_renderer.SetBackground(0.0, 0.5, 0.5)
pyramid_renderer.SetViewport(7.0 / 8, 0, 8.0 / 8, 1)
pyramid_renderer.ResetCamera()
pyramid_renderer.GetActiveCamera().Azimuth(25.0)
pyramid_renderer.GetActiveCamera().Elevation(-25.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(tstrip_renderer)
render_window.AddRenderer(quad_renderer)
render_window.AddRenderer(pixel_renderer)
render_window.AddRenderer(polygon_renderer)
render_window.AddRenderer(hex_renderer)
render_window.AddRenderer(voxel_renderer)
render_window.AddRenderer(wedge_renderer)
render_window.AddRenderer(pyramid_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("box clip triangulate")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
