#!/usr/bin/env python

# Test vtkBoxClipDataSet on tetrahedra with all 12 valid winding orders,
# clipped by 8 different box configurations. Displays axis-aligned and
# oriented box clips with and without clipped output in a large grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_TETRA,
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

# Tetrahedra points
tet_points = [
    1.0, 0.0, 0.0,
    -1.0, 0.0, 0.0,
    0.0, 0.0, 1.0,
    0.0, 1.0, 0.5,
]

# All 12 valid cell connectivities
tet_windings = [
    [0, 1, 2, 3], [2, 0, 1, 3], [1, 2, 0, 3],
    [0, 3, 1, 2], [1, 0, 3, 2], [3, 1, 0, 2],
    [0, 2, 3, 1], [3, 0, 2, 1], [2, 3, 0, 1],
    [1, 3, 2, 0], [2, 1, 3, 0], [3, 2, 1, 0],
]

minusx = [-1.0, 0.0, 0.0]
minusy = [0.0, -1.0, 0.0]
minusz = [0.0, 0.0, -1.0]
plusx = [1.0, 0.0, 0.0]
plusy = [0.0, 1.0, 0.0]
plusz = [0.0, 0.0, 1.0]

num_clip_boxes = 8

# Box configurations
boxes = [
    (0.15, 2.0, -2.0, 2.0, -2.0, 2.0),
    (-2.0, 0.15, -2.0, 2.0, -2.0, 2.0),
    (-2.0, 2.0, -2.0, 2.0, -2.0, 0.4),
    (-2.0, 2.0, -2.0, 2.0, 0.4, 2.0),
    (-2.0, 2.0, -2.0, 2.0, -2.0, 0.5),
    (-2.0, 2.0, -2.0, 2.0, 0.5, 2.0),
    (-2.0, 0.0, -2.0, 2.0, -2.0, 2.0),
    (0.0, 2.0, -2.0, 2.0, -2.0, 2.0),
]


def _build_tetrahedron_grid(winding):
    """Build a single-tetrahedron unstructured grid."""
    pts_arr = vtkDoubleArray()
    pts_arr.SetNumberOfComponents(3)
    pts_arr.SetNumberOfTuples(4)
    for p in range(4):
        pts_arr.SetTuple3(p, tet_points[p * 3], tet_points[p * 3 + 1], tet_points[p * 3 + 2])
    pts = vtkPoints()
    pts.SetData(pts_arr)
    ugrid = vtkUnstructuredGrid()
    ugrid.SetPoints(pts)
    ugrid.InsertNextCell(VTK_TETRA, 4, winding)
    return ugrid


def _build_axis_aligned_viewport(ugrid, minx, maxx, miny, maxy, minz, maxz, viewport):
    """Build axis-aligned clip pipeline and renderer for one viewport."""
    clip = vtkBoxClipDataSet()
    clip.SetInputData(ugrid)
    clip.GenerateClippedOutputOff()
    clip.SetBoxClip(minx, maxx, miny, maxy, minz, maxz)
    surface = vtkDataSetSurfaceFilter()
    surface.SetInputConnection(clip.GetOutputPort(0))
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(surface.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.0, 0.5, 0.5)
    renderer.SetViewport(*viewport)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Azimuth(25.0)
    renderer.GetActiveCamera().Elevation(-25.0)
    return renderer


def _build_oriented_viewport(ugrid, min_pt, max_pt, viewport):
    """Build oriented clip pipeline and renderer for one viewport."""
    clip = vtkBoxClipDataSet()
    clip.SetInputData(ugrid)
    clip.GenerateClippedOutputOff()
    clip.SetBoxClip(minusx, min_pt, minusy, min_pt, minusz, min_pt,
                    plusx, max_pt, plusy, max_pt, plusz, max_pt)
    surface = vtkDataSetSurfaceFilter()
    surface.SetInputConnection(clip.GetOutputPort(0))
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(surface.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.0, 0.5, 0.5)
    renderer.SetViewport(*viewport)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Azimuth(25.0)
    renderer.GetActiveCamera().Elevation(-25.0)
    return renderer


# Build all 192 renderers (8 boxes × 12 windings × 2 clip modes)
all_renderers = []
for box_num, (minx, maxx, miny, maxy, minz, maxz) in enumerate(boxes):
    min_pt = [minx, miny, minz]
    max_pt = [maxx, maxy, maxz]

    for tet_num in range(12):
        ugrid = _build_tetrahedron_grid(tet_windings[tet_num])

        x0 = tet_num / 24.0
        y0 = 1.0 - (box_num / num_clip_boxes + 1.0 / (2 * num_clip_boxes))
        x1 = (tet_num + 1) / 24.0
        y1 = 1.0 - (box_num / num_clip_boxes)

        all_renderers.append(_build_axis_aligned_viewport(
            ugrid, minx, maxx, miny, maxy, minz, maxz, (x0, y0, x1, y1)))

        all_renderers.append(_build_oriented_viewport(
            ugrid, min_pt, max_pt, (x0 + 0.5, y0, x1 + 0.5, y1)))

# Window
render_window = vtkRenderWindow()
for renderer in all_renderers:
    render_window.AddRenderer(renderer)
render_window.SetSize(960, 640)
render_window.SetWindowName("box clip tetrahedra")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
