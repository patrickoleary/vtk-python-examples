#!/usr/bin/env python
# Demonstrate Lagrange geometric operations: contour, boundary, clip, cut on higher-order elements.

import os

import numpy as np

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    mutable,
    vtkDoubleArray,
    vtkLookupTable,
    vtkMinimalStandardRandomSequence,
    vtkPoints,
    vtkVariant,
)
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkDataSet,
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkCutter,
    vtkGlyph3D,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import (
    vtkDataSetSurfaceFilter,
    vtkUnstructuredGridGeometryFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read higher-order Lagrange elements
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "Elements.vtu"))
reader.Update()

# --- Contour ---
contour = vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.SetInputArrayToProcess(
    0, 0, 0, vtkDataSet.FIELD_ASSOCIATION_POINTS_THEN_CELLS, "Ellipsoid")
contour.SetComputeNormals(1)
contour.SetComputeScalars(1)
contour.SetComputeGradients(1)
contour.SetNumberOfContours(4)
contour.SetValue(0, 2.5)
contour.SetValue(1, 1.5)
contour.SetValue(2, 0.5)
contour.SetValue(3, 1.05)
contour.Update()

contour_mapper = vtkDataSetMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())

clr = vtkColorSeries()
lkup = vtkLookupTable()
clr.SetColorScheme(vtkColorSeries.BREWER_QUALITATIVE_DARK2)
clr.BuildLookupTable(lkup, vtkColorSeries.CATEGORICAL)
lkup.SetAnnotation(vtkVariant(0.5), "Really Low")
lkup.SetAnnotation(vtkVariant(1.05), "Somewhat Low")
lkup.SetAnnotation(vtkVariant(1.5), "Medium")
lkup.SetAnnotation(vtkVariant(2.5), "High")
contour_mapper.SelectColorArray("Ellipsoid")
contour_mapper.SetLookupTable(lkup)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# --- Surface (translucent) ---
dss = vtkDataSetSurfaceFilter()
dss.SetInputConnection(reader.GetOutputPort())
dss.SetNonlinearSubdivisionLevel(3)

nrm = vtkPolyDataNormals()
nrm.SetInputConnection(dss.GetOutputPort())

surface_mapper = vtkDataSetMapper()
surface_mapper.SetInputConnection(nrm.GetOutputPort())

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().SetOpacity(0.2)

# --- Clip ---
clip_plane = vtkPlane()
clip_plane.SetOrigin(4, 2, 2)
clip_plane.SetNormal(-0.28735, -0.67728, 0.67728)

clip = vtkClipDataSet()
clip.SetInputConnection(reader.GetOutputPort())
clip.SetClipFunction(clip_plane)
clip.Update()

clip_mapper = vtkDataSetMapper()
clip_mapper.SetInputConnection(clip.GetOutputPort())

clip_lkup = vtkLookupTable()
clip_clr = vtkColorSeries()
clip_clr.SetColorScheme(vtkColorSeries.BREWER_QUALITATIVE_DARK2)
clip_clr.BuildLookupTable(clip_lkup, vtkColorSeries.CATEGORICAL)
clip_lkup.SetAnnotation(vtkVariant(0), "First cell")
clip_lkup.SetAnnotation(vtkVariant(1), "Second cell")
clip_mapper.SetScalarModeToUseCellFieldData()
clip_mapper.SelectColorArray("SrcCellNum")
clip_mapper.SetLookupTable(clip_lkup)

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)

# --- Cut ---
cut = vtkCutter()
cut.SetInputConnection(reader.GetOutputPort())
cut.SetCutFunction(clip_plane)
cut.Update()

cut_mapper = vtkDataSetMapper()
cut_mapper.SetInputConnection(cut.GetOutputPort())
cut_mapper.SetScalarModeToUseCellFieldData()
cut_mapper.SelectColorArray("SrcCellNum")
cut_mapper.SetLookupTable(clip_lkup)

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

# --- Boundary extraction ---
ugg = vtkUnstructuredGridGeometryFilter()
ugg.SetInputConnection(reader.GetOutputPort())
ugg.Update()

boundary_mapper = vtkDataSetMapper()
boundary_mapper.SetInputConnection(ugg.GetOutputPort())

boundary_lkup = vtkLookupTable()
boundary_clr = vtkColorSeries()
boundary_clr.SetColorScheme(vtkColorSeries.BREWER_QUALITATIVE_DARK2)
boundary_clr.BuildLookupTable(boundary_lkup, vtkColorSeries.CATEGORICAL)
boundary_lkup.SetAnnotation(vtkVariant(0), "Cell Low")
boundary_lkup.SetAnnotation(vtkVariant(1), "Somewhat Low")
boundary_lkup.SetAnnotation(vtkVariant(2), "Medium")
boundary_lkup.SetAnnotation(vtkVariant(3), "High")
boundary_mapper.SetScalarModeToUseCellFieldData()
boundary_mapper.SelectColorArray("SrcCellNum")
boundary_mapper.SetLookupTable(boundary_lkup)

boundary_actor = vtkActor()
boundary_actor.SetMapper(boundary_mapper)

# --- Intersection with random lines ---
rn = vtkMinimalStandardRandomSequence()

def rnums(n, vmin, vmax):
    result = []
    delta = vmax - vmin
    for _ in range(n):
        result.append(rn.GetValue() * delta + vmin)
        rn.Next()
    return result

p1 = [
    (-4, 2, 2), (2, -4, 2), (2, 2, -4),
    (0.125, 0.125, 4.125), (8.125, 0.125, 4.125),
    (0.125, 0.125, 0.125), (7.875, 3.875, 3.875),
] + list(zip(rnums(100, -4, 8), rnums(100, -4, 4), rnums(100, -4, 4)))

p2 = [
    (12, 2, 2), (2, 8, 2), (2, 2, 8),
    (3.45, 0.125, 4.125), (3.65, 0.125, 4.125),
    (4.8, 4.3, 4.3), (3.3, -0.5, -0.5),
] + list(zip(rnums(100, 0, 12), rnums(100, 0, 8), rnums(100, 0, 8)))

ug = reader.GetOutputDataObject(0)
tt = mutable(0)
sub_id = mutable(-1)
xx = [0, 0, 0]
rr = [0, 0, 0]
ipt = vtkPoints()
ica = vtkCellArray()
rst = [vtkDoubleArray(), vtkDoubleArray(), vtkDoubleArray()]
pname = ["R", "S", "T"]
for i in range(3):
    rst[i].SetName(pname[i])

for cidx in range(ug.GetNumberOfCells()):
    cell = ug.GetCell(cidx)
    if not hasattr(cell, "GetOrder"):
        continue
    order = [cell.GetOrder(i) for i in range(cell.GetCellDimension())]
    npts = 1
    for o in order:
        npts = npts * (o + 1)
    weights = np.zeros((npts, 1))
    for pp in range(len(p1)):
        done = False
        xp1 = np.array(p1[pp], dtype=np.float64)
        xp2 = np.array(p2[pp], dtype=np.float64)
        while not done:
            done = not cell.IntersectWithLine(xp1, xp2, 1e-8, tt, xx, rr, sub_id)
            if not done:
                pid = [ipt.InsertNextPoint(xx)]
                ica.InsertNextCell(1, pid)
                for i in range(3):
                    rst[i].InsertNextTuple([rr[i]])
                delta = xp2 - xp1
                mag = np.sqrt(np.sum(delta * delta))
                xp1 = np.array(xx) + (delta / mag) * np.finfo(np.float32).eps

ipd = vtkPolyData()
ipd.SetPoints(ipt)
ipd.SetVerts(ica)
for i in range(3):
    ipd.GetPointData().AddArray(rst[i])

gly = vtkGlyph3D()
ssc = vtkSphereSource()
gly.SetSourceConnection(ssc.GetOutputPort())
gly.SetInputDataObject(0, ipd)
gly.SetScaleFactor(0.15)
gly.FillCellDataOn()

gly_mapper = vtkDataSetMapper()
gly_mapper.SetInputConnection(gly.GetOutputPort())

stab_lkup = vtkLookupTable()
stab_clr = vtkColorSeries()
stab_clr.SetColorScheme(vtkColorSeries.BREWER_SEQUENTIAL_BLUE_PURPLE_9)
stab_clr.BuildLookupTable(stab_lkup, vtkColorSeries.ORDINAL)
stab_lkup.SetRange(0, 1)
gly_mapper.SetScalarModeToUseCellFieldData()
gly_mapper.SelectColorArray("R")
gly_mapper.SetLookupTable(stab_lkup)

gly_actor = vtkActor()
gly_actor.SetMapper(gly_mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(contour_actor)
renderer.AddActor(surface_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("lagrange operations")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(12.9377265875, 6.5914481094, 7.54647854482)
camera.SetFocalPoint(4.38052401617, 0.925973308028, 1.91021697659)
camera.SetViewUp(-0.491867406412, -0.115590747077, 0.862963054655)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
