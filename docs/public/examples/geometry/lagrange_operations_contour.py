#!/usr/bin/env python

# Demonstrate Lagrange element contouring using vtkContourFilter
# on a higher-order unstructured grid with surface overlay.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkVariant,
)
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonDataModel import vtkDataSet
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Lagrange elements
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "Elements.vtu"))
reader.Update()

# Contour filter
con = vtkContourFilter()
con.SetInputConnection(reader.GetOutputPort())
con.SetInputArrayToProcess(
    0, 0, 0, vtkDataSet.FIELD_ASSOCIATION_POINTS_THEN_CELLS, "Ellipsoid"
)
con.SetComputeNormals(1)
con.SetComputeScalars(1)
con.SetComputeGradients(1)
con.SetNumberOfContours(4)
con.SetValue(0, 2.5)
con.SetValue(1, 1.5)
con.SetValue(2, 0.5)
con.SetValue(3, 1.05)
con.Update()

# Contour actor with qualitative color scheme
clr = vtkColorSeries()
lkup = vtkLookupTable()
clr.SetColorScheme(vtkColorSeries.BREWER_QUALITATIVE_DARK2)
clr.BuildLookupTable(lkup, vtkColorSeries.CATEGORICAL)
lkup.SetAnnotation(vtkVariant(0.5), "Really Low")
lkup.SetAnnotation(vtkVariant(1.05), "Somewhat Low")
lkup.SetAnnotation(vtkVariant(1.5), "Medium")
lkup.SetAnnotation(vtkVariant(2.5), "High")

contour_mapper = vtkDataSetMapper()
contour_mapper.SetInputConnection(con.GetOutputPort())
contour_mapper.SelectColorArray("Ellipsoid")
contour_mapper.SetLookupTable(lkup)

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Surface actor (translucent)
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

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(contour_actor)
renderer.AddActor(surface_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("lagrange operations contour")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetPosition(12.9377265875, 6.5914481094, 7.54647854482)
cam.SetFocalPoint(4.38052401617, 0.925973308028, 1.91021697659)
cam.SetViewUp(-0.491867406412, -0.115590747077, 0.862963054655)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
