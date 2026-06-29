#!/usr/bin/env python

# Demonstrate vtkFastLabeledDataMapper with multiple text properties and styles.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIntArray,
    vtkStringArray,
)
from vtkmodules.vtkFiltersCore import vtkGenerateIds
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)
from vtkmodules.vtkRenderingOpenGL2 import vtkFastLabeledDataMapper

LABEL_TYPES = "types"
LABEL_TEXT_NAMES = "names"

# Create plane data to label
plane = vtkPlaneSource()
plane.SetResolution(10, 10)
plane.Update()

dataset = plane.GetOutput()
point_data = dataset.GetPointData()

# Add type and name arrays
types = vtkIntArray()
types.SetNumberOfComponents(1)
types.SetName(LABEL_TYPES)

names = vtkStringArray()
names.SetName(LABEL_TEXT_NAMES)

for i in range(dataset.GetNumberOfPoints()):
    types.InsertNextValue(i % 10)
    names.InsertNextValue("Z_{}_a".format(i))

point_data.AddArray(types)
point_data.AddArray(names)

# Generate IDs for labeling
ids = vtkGenerateIds()
ids.SetInputConnection(plane.GetOutputPort())
ids.PointIdsOn()

# Configure label mapper
label_mapper = vtkFastLabeledDataMapper()
label_mapper.SetLabelModeToLabelFieldData()
label_mapper.SetFieldDataName(LABEL_TEXT_NAMES)
label_mapper.SetInputArrayToProcess(0, 0, 0, 0, LABEL_TYPES)  # FIELD_ASSOCIATION_POINTS
label_mapper.SetInputConnection(ids.GetOutputPort())

# Text property 0: family=2, size=24, frame=2
tprop_0 = vtkTextProperty()
tprop_0.SetFontFamily(2)
tprop_0.SetColor(1, 0, 0)
tprop_0.SetOpacity(1)
tprop_0.SetBackgroundColor(0, 1, 0)
tprop_0.SetBackgroundOpacity(1)
tprop_0.SetFontSize(24)
tprop_0.SetFrame(True)
tprop_0.SetFrameWidth(2)
tprop_0.SetFrameColor(0, 0, 0.1)
label_mapper.SetLabelTextProperty(tprop_0, 0)

# Text property 1: family=0, size=24, frame=4
tprop_1 = vtkTextProperty()
tprop_1.SetFontFamily(0)
tprop_1.SetColor(1, 1, 1)
tprop_1.SetOpacity(1)
tprop_1.SetBackgroundColor(0.2, 1, 0.2)
tprop_1.SetBackgroundOpacity(1)
tprop_1.SetFontSize(24)
tprop_1.SetFrame(True)
tprop_1.SetFrameWidth(4)
tprop_1.SetFrameColor(0.1, 0.6, 0.6)
label_mapper.SetLabelTextProperty(tprop_1, 1)

# Text property 2: family=1, size=24, frame=8
tprop_2 = vtkTextProperty()
tprop_2.SetFontFamily(1)
tprop_2.SetColor(0, 0, 0)
tprop_2.SetOpacity(1)
tprop_2.SetBackgroundColor(0.8, 1, 0.8)
tprop_2.SetBackgroundOpacity(1)
tprop_2.SetFontSize(24)
tprop_2.SetFrame(True)
tprop_2.SetFrameWidth(8)
tprop_2.SetFrameColor(0.8, 0.2, 0.2)
label_mapper.SetLabelTextProperty(tprop_2, 2)

# Text property 3: family=0, size=12, frame=1
tprop_3 = vtkTextProperty()
tprop_3.SetFontFamily(0)
tprop_3.SetColor(0.8, 1, 0.2)
tprop_3.SetOpacity(1)
tprop_3.SetBackgroundColor(0.1, 0.4, 0.2)
tprop_3.SetBackgroundOpacity(1)
tprop_3.SetFontSize(12)
tprop_3.SetFrame(True)
tprop_3.SetFrameWidth(1)
tprop_3.SetFrameColor(0, 0, 0)
label_mapper.SetLabelTextProperty(tprop_3, 3)

# Text property 4: family=0, size=32, frame=4
tprop_4 = vtkTextProperty()
tprop_4.SetFontFamily(0)
tprop_4.SetColor(0.5, 0.5, 0.2)
tprop_4.SetOpacity(1)
tprop_4.SetBackgroundColor(0, 0, 1)
tprop_4.SetBackgroundOpacity(1)
tprop_4.SetFontSize(32)
tprop_4.SetFrame(True)
tprop_4.SetFrameWidth(4)
tprop_4.SetFrameColor(0.8, 0.5, 0.3)
label_mapper.SetLabelTextProperty(tprop_4, 4)

# Text property 5: family=2, size=16, frame=3
tprop_5 = vtkTextProperty()
tprop_5.SetFontFamily(2)
tprop_5.SetColor(1, 0.2, 1)
tprop_5.SetOpacity(1)
tprop_5.SetBackgroundColor(0.2, 1, 0.6)
tprop_5.SetBackgroundOpacity(1)
tprop_5.SetFontSize(16)
tprop_5.SetFrame(True)
tprop_5.SetFrameWidth(3)
tprop_5.SetFrameColor(0.1, 0, 0.3)
label_mapper.SetLabelTextProperty(tprop_5, 5)

# Text property 6: family=1, size=18, frame=0
tprop_6 = vtkTextProperty()
tprop_6.SetFontFamily(1)
tprop_6.SetColor(1, 1, 1)
tprop_6.SetOpacity(1)
tprop_6.SetBackgroundColor(0, 0, 0)
tprop_6.SetBackgroundOpacity(0)
tprop_6.SetFontSize(18)
tprop_6.SetFrame(False)
tprop_6.SetFrameWidth(0)
tprop_6.SetFrameColor(0, 0, 0)
label_mapper.SetLabelTextProperty(tprop_6, 6)

# Text property 7: family=1, size=22, frame=1
tprop_7 = vtkTextProperty()
tprop_7.SetFontFamily(1)
tprop_7.SetColor(0, 0, 0)
tprop_7.SetOpacity(1)
tprop_7.SetBackgroundColor(0.2, 1, 0.2)
tprop_7.SetBackgroundOpacity(1)
tprop_7.SetFontSize(22)
tprop_7.SetFrame(True)
tprop_7.SetFrameWidth(1)
tprop_7.SetFrameColor(0, 0, 0)
label_mapper.SetLabelTextProperty(tprop_7, 7)

# Text property 8: family=2, size=18, frame=1
tprop_8 = vtkTextProperty()
tprop_8.SetFontFamily(2)
tprop_8.SetColor(0, 1, 1)
tprop_8.SetOpacity(1)
tprop_8.SetBackgroundColor(0, 0, 0)
tprop_8.SetBackgroundOpacity(1)
tprop_8.SetFontSize(18)
tprop_8.SetFrame(True)
tprop_8.SetFrameWidth(1)
tprop_8.SetFrameColor(1, 1, 1)
label_mapper.SetLabelTextProperty(tprop_8, 8)

# Text property 9: family=0, size=24, frame=4
tprop_9 = vtkTextProperty()
tprop_9.SetFontFamily(0)
tprop_9.SetColor(1, 0.5, 0.5)
tprop_9.SetOpacity(1)
tprop_9.SetBackgroundColor(0.5, 0.5, 1)
tprop_9.SetBackgroundOpacity(1)
tprop_9.SetFontSize(24)
tprop_9.SetFrame(True)
tprop_9.SetFrameWidth(4)
tprop_9.SetFrameColor(0.5, 1, 0.5)
label_mapper.SetLabelTextProperty(tprop_9, 9)

label_actor = vtkActor()
label_actor.SetMapper(label_mapper)

# Origin points visualization
origin_mapper = vtkPolyDataMapper()
origin_mapper.SetInputConnection(ids.GetOutputPort())

origin_actor = vtkActor()
origin_actor.SetMapper(origin_mapper)
origin_actor.GetProperty().SetRepresentationToPoints()
origin_actor.GetProperty().RenderPointsAsSpheresOn()
origin_actor.GetProperty().SetPointSize(5)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(origin_actor)
renderer.AddActor(label_actor)
renderer.SetBackground(0.5, 0.5, 0.6)

render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("labeled data mappers")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Pipeline exception: render before releasing graphics resources
render_window.Render()

# Release and re-render to test resource management
label_mapper.ReleaseGraphicsResources(render_window)

# Pipeline exception: re-render after releasing resources
render_window.Render()

interactor.Initialize()
interactor.Start()
