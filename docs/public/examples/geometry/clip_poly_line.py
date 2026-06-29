#!/usr/bin/env python
# Demonstrate clipping polyline cells from an unstructured grid with a plane.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read input dataset with polyline cells.
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "poly_lines.vtu"))
reader.Update()
dataset = reader.GetOutput()

# Clip the dataset.
clipper = vtkClipDataSet()
clipper.SetInputData(dataset)
plane = vtkPlane()
plane.SetNormal(1, 0, 0)
plane.SetOrigin(0, 1.6149157704255361, -0.98122887884924)
clipper.SetClipFunction(plane)
clipper.Update()

# Get surface representation to render.
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputData(clipper.GetOutput())
surface_filter.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputData(surface_filter.GetOutput())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToSurface()
actor.GetProperty().EdgeVisibilityOn()

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 200)
render_window.AddRenderer(renderer)
render_window.SetWindowName("clip poly line")

renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
