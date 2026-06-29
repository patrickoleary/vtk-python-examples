#!/usr/bin/env python

# Compare triangle-generating and polygon-generating vtkCutter modes
# on an unstructured grid loaded from a VTU file, displayed in two
# viewports.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data file path (relative to this script)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read unstructured grid
xml_reader = vtkXMLUnstructuredGridReader()
xml_reader.SetFileName(os.path.join(data_dir, "cuttertest.vtu"))

# Cut plane
plane = vtkPlane()
plane.SetOrigin(50, 0, 405)
plane.SetNormal(0, 0, 1)

# Triangle cutter
tri_cutter = vtkCutter()
tri_cutter.SetInputConnection(xml_reader.GetOutputPort())
tri_cutter.SetCutFunction(plane)

tri_mapper = vtkPolyDataMapper()
tri_mapper.SetInputConnection(tri_cutter.GetOutputPort())
tri_mapper.ScalarVisibilityOff()

tri_actor = vtkActor()
tri_actor.SetMapper(tri_mapper)
tri_actor.GetProperty().SetColor(1, 0, 0)
tri_actor.GetProperty().EdgeVisibilityOn()
tri_actor.GetProperty().SetEdgeColor(1, 1, 1)

# Polygon cutter
poly_cutter = vtkCutter()
poly_cutter.GenerateTrianglesOff()
poly_cutter.SetInputConnection(xml_reader.GetOutputPort())
poly_cutter.SetCutFunction(plane)

poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputConnection(poly_cutter.GetOutputPort())
poly_mapper.ScalarVisibilityOff()

poly_actor = vtkActor()
poly_actor.SetMapper(poly_mapper)
poly_actor.GetProperty().SetColor(0, 0, 1)

# Two viewports
renderer_0 = vtkRenderer()
renderer_0.AddViewProp(tri_actor)
renderer_0.SetViewport(0, 0, 0.5, 1.0)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(poly_actor)
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 500)
render_window.SetWindowName("cutter")

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
