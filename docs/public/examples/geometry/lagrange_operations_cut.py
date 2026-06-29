#!/usr/bin/env python

# Demonstrate vtkCutter on Lagrange higher-order elements with a
# plane cut function and translucent surface overlay.

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
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import (
    vtkCutter,
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

# Color scheme
clr = vtkColorSeries()
lkup = vtkLookupTable()
clr.SetColorScheme(vtkColorSeries.BREWER_QUALITATIVE_DARK2)
clr.BuildLookupTable(lkup, vtkColorSeries.CATEGORICAL)
lkup.SetAnnotation(vtkVariant(0), "First cell")
lkup.SetAnnotation(vtkVariant(1), "Second cell")

# Cut with a plane
pln = vtkPlane()
pln.SetOrigin(4, 2, 2)
pln.SetNormal(-0.28735, -0.67728, 0.67728)

cut = vtkCutter()
cut.SetInputConnection(reader.GetOutputPort())
cut.SetCutFunction(pln)
cut.Update()

# Cut actor
cut_mapper = vtkDataSetMapper()
cut_mapper.SetInputConnection(cut.GetOutputPort())
cut_mapper.SetScalarModeToUseCellFieldData()
cut_mapper.SelectColorArray("SrcCellNum")
cut_mapper.SetLookupTable(lkup)

cut_actor = vtkActor()
cut_actor.SetMapper(cut_mapper)

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
renderer.AddActor(cut_actor)
renderer.AddActor(surface_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("lagrange operations cut")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetPosition(16.0784261776, 11.8079343039, -6.69074553411)
cam.SetFocalPoint(4.54685488135, 1.74152986486, 2.38091647662)
cam.SetViewUp(-0.523934540522, 0.81705750638, 0.240644194852)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
