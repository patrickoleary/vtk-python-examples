#!/usr/bin/env python

# Demonstrate vtkGlyph3DMapper with hardware cell picking and masking.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkBitArray
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkRenderedAreaPicker,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleRubberBandPick
from vtkmodules.vtkRenderingCore import vtkHardwareSelector

# Plane with elevation coloring
res = 1
plane = vtkPlaneSource()
plane.SetResolution(res, res)

colors = vtkElevationFilter()
colors.SetInputConnection(plane.GetOutputPort())
colors.SetLowPoint(-1, -1, -1)
colors.SetHighPoint(0.5, 0.5, 0.5)

# Glyph source
squad = vtkSphereSource()
squad.SetPhiResolution(4)
squad.SetThetaResolution(6)

# Glyph mapper for selection target
glypher = vtkGlyph3DMapper()
glypher.SetInputConnection(colors.GetOutputPort())
glypher.SetScaleFactor(1.5)
glypher.SetSourceConnection(squad.GetOutputPort())

glyph_actor_1 = vtkActor()
glyph_actor_1.SetMapper(glypher)
glyph_actor_1.PickableOn()

# Result glyph mapper with masking
colors.Update()
selection = colors.GetOutput().NewInstance()
selection.ShallowCopy(colors.GetOutput())

selection_mask = vtkBitArray()
selection_mask.SetName("mask")
selection_mask.SetNumberOfComponents(1)
selection_mask.SetNumberOfTuples(selection.GetNumberOfPoints())
for i in range(selection_mask.GetNumberOfTuples()):
    selection_mask.SetValue(i, True)
selection.GetPointData().AddArray(selection_mask)

glypher_2 = vtkGlyph3DMapper()
glypher_2.SetMasking(True)
glypher_2.SetMaskArray("mask")
glypher_2.SetInputData(selection)
glypher_2.SetScaleFactor(1.5)
glypher_2.SetSourceConnection(squad.GetOutputPort())

glyph_actor_2 = vtkActor()
glyph_actor_2.PickableOff()
glyph_actor_2.SetMapper(glypher_2)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.2, 0.2)

render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("glyph3d mapper cell picking")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Rubber band pick style
rbp = vtkInteractorStyleRubberBandPick()
interactor.SetInteractorStyle(rbp)

area_picker = vtkRenderedAreaPicker()
interactor.SetPicker(area_picker)

renderer.AddActor(glyph_actor_1)
renderer.AddActor(glyph_actor_2)
glyph_actor_2.SetPosition(2, 0, 0)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.0)

# Pipeline exception: hardware selection requires a rendered scene
render_window.Render()

# Perform an area pick
area_picker.AreaPick(233, 120, 241, 160, renderer)

# Hardware selection
sel = vtkHardwareSelector()
sel.SetFieldAssociation(0)  # FIELD_ASSOCIATION_CELLS
sel.SetRenderer(renderer)
x0 = renderer.GetPickX1()
y0 = renderer.GetPickY1()
x1 = renderer.GetPickX2()
y1 = renderer.GetPickY2()
sel.SetArea(int(x0), int(y0), int(x1), int(y1))
result = sel.Select()

# Reset mask
num_points = selection_mask.GetNumberOfTuples()
for i in range(num_points):
    selection_mask.SetValue(i, False)

# Apply selection
if result.GetNumberOfNodes() > 0:
    node = result.GetNode(0)
    if node is not None:
        ids = node.GetSelectionList()
        if ids is not None:
            for i in range(ids.GetNumberOfTuples()):
                value = ids.GetValue(i)
                if 0 <= value < num_points:
                    selection_mask.SetValue(value, True)
selection.Modified()

# Pipeline exception: re-render after selection applied
render_window.Render()

interactor.Initialize()
interactor.Start()
