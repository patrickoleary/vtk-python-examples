#!/usr/bin/env python
# Demonstrate vtkCategoryLegend with colored categories.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkCategoryLegend
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import vtkLookupTable, vtkVariant, vtkVariantArray
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextTransform
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create values.
values = vtkVariantArray()
values.InsertNextValue(vtkVariant("a"))
values.InsertNextValue(vtkVariant("b"))
values.InsertNextValue(vtkVariant("c"))

# Create lookup table with annotations.
lut = vtkLookupTable()
for i in range(values.GetNumberOfTuples()):
    lut.SetAnnotation(values.GetValue(i), values.GetValue(i).ToString())

color_series = vtkColorSeries()
color_series.SetColorScheme(vtkColorSeries.BREWER_QUALITATIVE_SET3)
color_series.BuildLookupTable(lut)

# Create the legend.
legend = vtkCategoryLegend()
legend.SetScalarsToColors(lut)
legend.SetValues(values)
legend.SetTitle("legend")

# Transform to position the legend.
trans = vtkContextTransform()
trans.SetInteractive(True)
trans.AddItem(legend)
trans.Translate(180, 70)

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(trans)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(300, 200)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("category legend")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
