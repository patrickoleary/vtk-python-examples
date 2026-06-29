#!/usr/bin/env python

# Demonstrate vtkContourFilter with vtkSpanSpace scalar tree on an
# Exodus II dataset, contouring the CH4 point result array.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonExecutionModel import vtkSpanSpace
from vtkmodules.vtkFiltersCore import (
    vtkAssignAttribute,
    vtkContourFilter,
)
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Exodus II data
reader = vtkExodusIIReader()
reader.SetFileName(os.path.join(data_dir, "disk_out_ref.ex2"))
reader.UpdateInformation()
reader.SetPointResultArrayStatus("CH4", 1)
reader.Update()

# Span space scalar tree
tree = vtkSpanSpace()

# Contour the CH4 field
contour = vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.SetInputArrayToProcess(0, 0, 0, vtkAssignAttribute.POINT_DATA, "CH4")
contour.SetValue(0, 0.000718448)
contour.UseScalarTreeOn()
contour.SetScalarTree(tree)
contour.Update()

mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(contour.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("smp contour grid with span space")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
