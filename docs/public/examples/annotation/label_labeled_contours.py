#!/usr/bin/env python

# Demonstrate labeling of contour lines with scalar values.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkMaskPoints,
)
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkSelectVisiblePoints,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read a slice of volume data
reader = vtkVolume16Reader()
reader.SetDataDimensions(64, 64)
reader.GetOutput().SetOrigin(0.0, 0.0, 0.0)
reader.SetDataByteOrderToLittleEndian()
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetImageRange(45, 45)
reader.SetDataSpacing(3.2, 3.2, 1.5)

# Generate contours
contour_filter = vtkContourFilter()
contour_filter.SetInputConnection(reader.GetOutputPort())
contour_filter.GenerateValues(6, 500, 1150)
contour_filter.Update()

num_contour_points = contour_filter.GetOutput().GetNumberOfPoints()

# Contour mapper and actor
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_filter.GetOutputPort())
contour_mapper.ScalarVisibilityOn()
contour_mapper.SetScalarRange(contour_filter.GetOutput().GetScalarRange())

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)

# Subsample points for labeling
mask = vtkMaskPoints()
mask.SetInputConnection(contour_filter.GetOutputPort())
mask.SetOnRatio(num_contour_points // 50)
mask.SetMaximumNumberOfPoints(50)
mask.RandomModeOn()

# Renderer (functional exception: needed by vtkSelectVisiblePoints)
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)

# Show only visible points
visible_points = vtkSelectVisiblePoints()
visible_points.SetInputConnection(mask.GetOutputPort())
visible_points.SetRenderer(renderer)

# Label mapper
label_mapper = vtkLabeledDataMapper()
label_mapper.SetInputConnection(mask.GetOutputPort())
label_mapper.SetLabelModeToLabelScalars()

text_property = label_mapper.GetLabelTextProperty()
text_property.SetFontFamilyToArial()
text_property.SetFontSize(10)
text_property.SetColor(1, 0, 0)

contour_labels = vtkActor2D()
contour_labels.SetMapper(label_mapper)

# Add actors to renderer
renderer.AddViewProp(contour_actor)
renderer.AddViewProp(contour_labels)

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer)
render_window.SetWindowName("label labeled contours")

# Functional render: establish geometry before camera Zoom
render_window.Render()

# Scene
camera = renderer.GetActiveCamera()
camera.Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
