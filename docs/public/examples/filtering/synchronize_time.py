#!/usr/bin/env python

# Visualize the Exodus can.ex2 dataset used by vtkSynchronizeTimeFilter,
# showing the mesh at the first time step with element block coloring.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the Exodus dataset
reader = vtkExodusIIReader()
reader.SetFileName(os.path.join(data_dir, "can.ex2"))
reader.UpdateInformation()
reader.SetAllArrayStatus(vtkExodusIIReader.NODAL, 1)
reader.UpdateTimeStep(0.00199999)

# Extract surface geometry from composite dataset
geom = vtkCompositeDataGeometryFilter()
geom.SetInputConnection(reader.GetOutputPort())

# Compute velocity magnitude
calc = vtkArrayCalculator()
calc.SetInputConnection(geom.GetOutputPort())
calc.AddVectorArrayName("VEL")
calc.SetFunction("mag(VEL)")
calc.SetResultArrayName("VEL_MAG")
calc.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(calc.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("VEL_MAG")
sr = calc.GetOutput().GetPointData().GetArray("VEL_MAG").GetRange()
mapper.SetScalarRange(sr)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.2, 0.3, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("synchronize time")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(0, -40, -5)
renderer.GetActiveCamera().SetFocalPoint(0, 4, -5)
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
