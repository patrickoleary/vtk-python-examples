#!/usr/bin/env python

# Demonstrate vtkForceStaticMesh preserving mesh topology across time
# steps while allowing data attributes to change.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersTemporal import vtkForceStaticMesh
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read time-varying unstructured grid
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "cube-with-time.vtu"))

# Generate random point scalars
scalars = vtkRandomAttributeGenerator()
scalars.SetInputConnection(reader.GetOutputPort())
scalars.GenerateAllDataOff()
scalars.GeneratePointScalarsOn()
scalars.SetDataTypeToDouble()
scalars.SetComponentRange(0, 30)

# Force static mesh — geometry stays the same, attributes update
static_mesh = vtkForceStaticMesh()
static_mesh.SetInputConnection(scalars.GetOutputPort())
static_mesh.Update()

static_mesh.GetOutputDataObject(0).GetCellData().SetActiveScalars("RandomPointScalars")

# Check mesh stays the same at different time steps
init_mesh_time = static_mesh.GetOutputDataObject(0).GetMeshMTime()
static_mesh.UpdateTimeStep(3)
new_mesh_time = static_mesh.GetOutputDataObject(0).GetMeshMTime()
if init_mesh_time != new_mesh_time:
    print("Error: static mesh has different mesh times")

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(static_mesh.GetOutputPort())
mapper.UseLookupTableScalarRangeOff()
mapper.SetScalarVisibility(1)
mapper.SetScalarModeToDefault()
mapper.SetScalarRange(0, 30)

# Actor
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToSurface()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("force static mesh py")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
