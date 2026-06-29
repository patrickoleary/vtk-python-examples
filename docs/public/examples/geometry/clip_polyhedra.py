#!/usr/bin/env python
# Demonstrate clipping n-faced polyhedra from an Exodus dataset with a plane.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkIOExodus import vtkExodusIIReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read input dataset that has n-faced polyhedra.
reader = vtkExodusIIReader()
reader.SetFileName(os.path.join(data_dir, "cube-1.exo"))
reader.Update()
dataset = reader.GetOutput()

# Clip the dataset.
clipper = vtkClipDataSet()
clipper.SetInputData(dataset.GetBlock(0).GetBlock(0))
plane = vtkPlane()
plane.SetNormal(0.5, 0.5, 0.5)
plane.SetOrigin(0.5, 0.5, 0.5)
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
render_window.SetWindowName("clip polyhedra")

renderer.GetActiveCamera().SetPosition(-0.5, 0.5, 0)
renderer.GetActiveCamera().SetFocalPoint(0.5, 0.5, 0.5)
renderer.GetActiveCamera().SetViewUp(0.0820, 0.934, -0.348)
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
