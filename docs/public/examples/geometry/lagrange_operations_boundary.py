#!/usr/bin/env python

# Demonstrate vtkUnstructuredGridGeometryFilter boundary extraction
# on Lagrange higher-order elements with cell-colored surface.

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
from vtkmodules.vtkFiltersGeometry import vtkUnstructuredGridGeometryFilter
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

# Boundary extraction
ugg = vtkUnstructuredGridGeometryFilter()
ugg.SetInputConnection(reader.GetOutputPort())
ugg.Update()

# Color by cell data with qualitative color scheme
clr = vtkColorSeries()
lkup = vtkLookupTable()
clr.SetColorScheme(vtkColorSeries.BREWER_QUALITATIVE_DARK2)
clr.BuildLookupTable(lkup, vtkColorSeries.CATEGORICAL)
lkup.SetAnnotation(vtkVariant(0), "Cell Low")
lkup.SetAnnotation(vtkVariant(1), "Somewhat Low")
lkup.SetAnnotation(vtkVariant(2), "Medium")
lkup.SetAnnotation(vtkVariant(3), "High")

mapper = vtkDataSetMapper()
mapper.SetInputConnection(ugg.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("SrcCellNum")
mapper.SetLookupTable(lkup)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("lagrange operations boundary")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetPosition(16.429826228, -5.64575247779, 12.7186363446)
cam.SetFocalPoint(4.12105459591, 1.95201869763, 1.69574200166)
cam.SetViewUp(-0.503606926552, 0.337767269532, 0.795168746344)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
