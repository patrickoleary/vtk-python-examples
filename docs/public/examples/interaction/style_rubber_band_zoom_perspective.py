#!/usr/bin/env python
# Demonstrate vtkInteractorStyleRubberBandZoom with perspective projection options.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkGenerateIds
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere with cell ids for coloring
sphere = vtkSphereSource()

id_filter = vtkGenerateIds()
id_filter.PointIdsOff()
id_filter.CellIdsOn()
id_filter.SetInputConnection(sphere.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(id_filter.GetOutputPort())
mapper.SetColorModeToMapScalars()
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("vtkCellIds")
mapper.UseLookupTableScalarRangeOff()
mapper.SetScalarRange(0, 95)

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("style rubber band zoom perspective")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
