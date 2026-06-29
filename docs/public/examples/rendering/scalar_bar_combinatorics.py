#!/usr/bin/env python

# Demonstrate vtkScalarBarActor with various combinatoric settings and MathText.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingMatplotlib  # noqa: F401

from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Lookup tables
lut_indexed = vtkLookupTable()
lut_continuous = vtkLookupTable()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

# T1: Horizontal, Precede, indexed, annotations+nan
sba_1 = vtkScalarBarActor()
sba_1.SetTitle("$T_1$")
sba_1.SetLookupTable(lut_indexed)
sba_1.SetOrientation(0)
sba_1.SetTextPosition(vtkScalarBarActor.PrecedeScalarBar)
sba_1.SetDrawAnnotations(1)
sba_1.SetDrawNanAnnotation(1)
sba_1.SetFixedAnnotationLeaderLineColor(0)
sba_1.SetPosition(0.000, 0.015)
sba_1.SetPosition2(0.400, 0.135)
sba_1.SetVerticalTitleSeparation(0)
renderer.AddActor(sba_1)

# T2: Horizontal, Precede, indexed, annotations only
sba_2 = vtkScalarBarActor()
sba_2.SetTitle("$T_2$")
sba_2.SetLookupTable(lut_indexed)
sba_2.SetOrientation(0)
sba_2.SetTextPosition(vtkScalarBarActor.PrecedeScalarBar)
sba_2.SetDrawAnnotations(1)
sba_2.SetDrawNanAnnotation(0)
sba_2.SetFixedAnnotationLeaderLineColor(1)
sba_2.SetPosition(0.000, 0.230)
sba_2.SetPosition2(0.400, 0.146)
sba_2.SetVerticalTitleSeparation(0)
renderer.AddActor(sba_2)

# T3: Horizontal, Succeed, indexed, annotations+nan, vtitle_sep=5
sba_3 = vtkScalarBarActor()
sba_3.SetTitle("$T_3$")
sba_3.SetLookupTable(lut_indexed)
sba_3.SetOrientation(0)
sba_3.SetTextPosition(vtkScalarBarActor.SucceedScalarBar)
sba_3.SetDrawAnnotations(1)
sba_3.SetDrawNanAnnotation(1)
sba_3.SetFixedAnnotationLeaderLineColor(1)
sba_3.SetPosition(0.000, 0.850)
sba_3.SetPosition2(0.630, 0.154)
sba_3.SetVerticalTitleSeparation(5)
renderer.AddActor(sba_3)

# T4: Vertical, Precede, indexed, annotations+nan, vtitle_sep=5
sba_4 = vtkScalarBarActor()
sba_4.SetTitle("$T_4$")
sba_4.SetLookupTable(lut_indexed)
sba_4.SetOrientation(1)
sba_4.SetTextPosition(vtkScalarBarActor.PrecedeScalarBar)
sba_4.SetDrawAnnotations(1)
sba_4.SetDrawNanAnnotation(1)
sba_4.SetFixedAnnotationLeaderLineColor(0)
sba_4.SetPosition(0.799, 0.032)
sba_4.SetPosition2(0.061, 0.794)
sba_4.SetVerticalTitleSeparation(5)
renderer.AddActor(sba_4)

# T5: Vertical, Precede, indexed, annotations only
sba_5 = vtkScalarBarActor()
sba_5.SetTitle("$T_5$")
sba_5.SetLookupTable(lut_indexed)
sba_5.SetOrientation(1)
sba_5.SetTextPosition(vtkScalarBarActor.PrecedeScalarBar)
sba_5.SetDrawAnnotations(1)
sba_5.SetDrawNanAnnotation(0)
sba_5.SetFixedAnnotationLeaderLineColor(1)
sba_5.SetPosition(0.893, 0.036)
sba_5.SetPosition2(0.052, 0.752)
sba_5.SetVerticalTitleSeparation(0)
renderer.AddActor(sba_5)

# T6: Vertical, Succeed, indexed, annotations+nan
sba_6 = vtkScalarBarActor()
sba_6.SetTitle("$T_6$")
sba_6.SetLookupTable(lut_indexed)
sba_6.SetOrientation(1)
sba_6.SetTextPosition(vtkScalarBarActor.SucceedScalarBar)
sba_6.SetDrawAnnotations(1)
sba_6.SetDrawNanAnnotation(1)
sba_6.SetFixedAnnotationLeaderLineColor(1)
sba_6.SetPosition(0.792, 0.081)
sba_6.SetPosition2(0.061, 0.617)
sba_6.SetVerticalTitleSeparation(0)
renderer.AddActor(sba_6)

# T7: Vertical, Succeed, continuous, annotations+nan
sba_7 = vtkScalarBarActor()
sba_7.SetTitle("$T_7$")
sba_7.SetLookupTable(lut_continuous)
sba_7.SetOrientation(1)
sba_7.SetTextPosition(vtkScalarBarActor.SucceedScalarBar)
sba_7.SetDrawAnnotations(1)
sba_7.SetDrawNanAnnotation(1)
sba_7.SetFixedAnnotationLeaderLineColor(0)
sba_7.SetPosition(0.646, 0.061)
sba_7.SetPosition2(0.084, 0.714)
sba_7.SetVerticalTitleSeparation(0)
renderer.AddActor(sba_7)

# T8: Horizontal, Succeed, continuous, nan only
sba_8 = vtkScalarBarActor()
sba_8.SetTitle("$T_8$")
sba_8.SetLookupTable(lut_continuous)
sba_8.SetOrientation(0)
sba_8.SetTextPosition(vtkScalarBarActor.SucceedScalarBar)
sba_8.SetDrawAnnotations(0)
sba_8.SetDrawNanAnnotation(1)
sba_8.SetFixedAnnotationLeaderLineColor(1)
sba_8.SetPosition(0.076, 0.535)
sba_8.SetPosition2(0.313, 0.225)
sba_8.SetVerticalTitleSeparation(0)
renderer.AddActor(sba_8)

# Configure continuous lookup table with color series
pal = vtkColorSeries()
pal.SetColorSchemeByName("Brewer Sequential Blue-Green (5)")
pal.BuildLookupTable(lut_continuous)
lut_continuous.IndexedLookupOff()
lut_continuous.Build()
lut_continuous.SetAnnotation(5.00, "Just Wow")
lut_continuous.SetAnnotation(4.00, "Super-Special")
lut_continuous.SetAnnotation(3.00, "Amazingly Special")
lut_continuous.SetAnnotation(1.00, "Special")
lut_continuous.SetAnnotation(0.00, "Special $\\cap$ This $= \\emptyset$")
lut_continuous.SetRange(0.0, 4.0)
lut_continuous.Build()

# Configure indexed lookup table with even number of entries
pal.SetColorSchemeByName("Brewer Diverging Purple-Orange (10)")
pal.BuildLookupTable(lut_indexed)
lut_indexed.SetAnnotation(5.00, "A")
lut_indexed.SetAnnotation(4.00, "B")
lut_indexed.SetAnnotation(3.00, "C")
lut_indexed.SetAnnotation(2.00, "D")
lut_indexed.SetAnnotation(1.00, "")
lut_indexed.SetAnnotation(0.00, "F")
lut_indexed.SetAnnotation(6.00, "G")
lut_indexed.SetAnnotation(7.00, "H")
lut_indexed.SetAnnotation(8.00, "I")
lut_indexed.SetAnnotation(9.00, "")

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("scalar bar combinatorics")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
