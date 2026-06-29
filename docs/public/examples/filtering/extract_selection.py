#!/usr/bin/env python

# Demonstrate vtkExtractSelection extracting specific cells by index
# from a sphere source.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkSelectionNode
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkFiltersSources import (
    vtkSelectionSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Selection: cell indices 2, 4, 5, 8
selection = vtkSelectionSource()
selection.SetContentType(vtkSelectionNode.INDICES)
selection.SetFieldType(vtkSelectionNode.CELL)
selection.AddID(-1, 2)
selection.AddID(-1, 4)
selection.AddID(-1, 5)
selection.AddID(-1, 8)

# Sphere source
sphere = vtkSphereSource()

# Extract selected cells
sel_filter = vtkExtractSelection()
sel_filter.SetInputConnection(0, sphere.GetOutputPort())
sel_filter.SetInputConnection(1, selection.GetOutputPort())

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(sel_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("extract selection")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
