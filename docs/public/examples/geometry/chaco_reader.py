#!/usr/bin/env python

# Read a Chaco graph file and render with vertex weights as scalars.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkIOGeometry import vtkChacoReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read Chaco file
chaco_reader = vtkChacoReader()
chaco_reader.SetBaseName(os.path.join(data_dir, "vwgt"))
chaco_reader.SetGenerateGlobalElementIdArray(1)
chaco_reader.SetGenerateGlobalNodeIdArray(1)
chaco_reader.SetGenerateEdgeWeightArrays(1)
chaco_reader.SetGenerateVertexWeightArrays(1)

# Extract geometry
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputConnection(chaco_reader.GetOutputPort())

# Mapper
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(geometry_filter.GetOutputPort())
poly_mapper.SetColorModeToMapScalars()
poly_mapper.SetScalarModeToUsePointFieldData()
poly_mapper.SelectColorArray("VertexWeight1")
poly_mapper.SetScalarRange(1, 5)

# Actor
chaco_actor = vtkActor()
chaco_actor.SetMapper(poly_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(chaco_actor)
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("chaco reader")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
