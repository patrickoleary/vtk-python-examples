#!/usr/bin/env python

# Rescale and reverse a color transfer function, shown in a 2x2 grid.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkDiscretizableColorTransferFunction,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextMapper,
    vtkTextProperty,
)

# Colors (normalized RGB)
light_goldenrod_yellow_rgb = (0.980, 0.980, 0.824)


def make_rainbow_ctf():
    """Newton's original seven rainbow colors as a discretized CTF."""
    ctf = vtkDiscretizableColorTransferFunction()
    ctf.SetColorSpaceToRGB()
    ctf.SetScaleToLinear()
    ctf.SetNanColor(0.5, 0.5, 0.5)
    ctf.SetBelowRangeColor(0.0, 0.0, 0.0)
    ctf.UseBelowRangeColorOn()
    ctf.SetAboveRangeColor(1.0, 1.0, 1.0)
    ctf.UseAboveRangeColorOn()
    ctf.AddRGBPoint(-1.0, 1.0, 0.0, 0.0)
    ctf.AddRGBPoint(-2.0 / 3.0, 1.0, 165.0 / 255.0, 0.0)
    ctf.AddRGBPoint(-1.0 / 3.0, 1.0, 1.0, 0.0)
    ctf.AddRGBPoint(0.0, 0.0, 125.0 / 255.0, 0.0)
    ctf.AddRGBPoint(1.0 / 3.0, 0.0, 153.0 / 255.0, 1.0)
    ctf.AddRGBPoint(2.0 / 3.0, 68.0 / 255.0, 0.0, 153.0 / 255.0)
    ctf.AddRGBPoint(1.0, 153.0 / 255.0, 0.0, 1.0)
    ctf.SetNumberOfValues(7)
    ctf.DiscretizeOn()
    return ctf


def rescale_ctf(ctf, new_min, new_max, reverse):
    """Rescale and optionally reverse a color transfer function."""
    r0, r1 = (new_max, new_min) if new_min > new_max else (new_min, new_max)
    xv, rgbv = [], []
    nv = [0.0] * 6
    for i in range(ctf.GetNumberOfValues()):
        ctf.GetNodeValue(i, nv)
        xv.append(nv[0])
        rgbv.append(nv[1:4])

    old_min, old_max = min(xv), max(xv)
    new_xv = [(r1 - r0) / (old_max - old_min) * (x - old_min) + r0 for x in xv]

    new_ctf = vtkDiscretizableColorTransferFunction()
    new_ctf.SetScale(ctf.GetScale())
    new_ctf.SetColorSpace(ctf.GetColorSpace())
    new_ctf.SetNanColor(ctf.GetNanColor())
    if not reverse:
        new_ctf.SetBelowRangeColor(ctf.GetBelowRangeColor())
        new_ctf.SetUseBelowRangeColor(ctf.GetUseBelowRangeColor())
        new_ctf.SetAboveRangeColor(ctf.GetAboveRangeColor())
        new_ctf.SetUseAboveRangeColor(ctf.GetUseAboveRangeColor())
    else:
        new_ctf.SetBelowRangeColor(ctf.GetAboveRangeColor())
        new_ctf.SetUseBelowRangeColor(ctf.GetUseAboveRangeColor())
        new_ctf.SetAboveRangeColor(ctf.GetBelowRangeColor())
        new_ctf.SetUseAboveRangeColor(ctf.GetUseBelowRangeColor())
    new_ctf.SetNumberOfValues(len(new_xv))
    new_ctf.SetDiscretize(ctf.GetDiscretize())
    sz = len(new_xv)
    for i in range(sz):
        j = (sz - 1 - i) if reverse else i
        new_ctf.AddRGBPoint(new_xv[i], *rgbv[j])
    new_ctf.Build()
    return new_ctf


# Build four variants of the rainbow CTF
original = make_rainbow_ctf()
ctfs = [
    original,
    rescale_ctf(original, 0, 1, False),
    rescale_ctf(original, *original.GetRange(), True),
    rescale_ctf(original, 0, 1, True),
]

titles = ["Original", "Rescaled", "Reversed", "Rescaled and Reversed"]
xmins = [0.0, 0.0, 0.5, 0.5]
xmaxs = [0.5, 0.5, 1.0, 1.0]
ymins = [0.5, 0.0, 0.5, 0.0]
ymaxs = [1.0, 0.5, 1.0, 0.5]

text_property = vtkTextProperty()
text_property.SetFontSize(36)
text_property.SetJustificationToCentered()
text_property.SetColor(light_goldenrod_yellow_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(1280, 960)
render_window.SetWindowName("RescaleReverseLUT")

for i in range(4):
    cylinder = vtkCylinderSource()
    cylinder.SetResolution(6)
    cylinder.Update()
    bounds = cylinder.GetOutput().GetBounds()

    elevation = vtkElevationFilter()
    elevation.SetScalarRange(0, 1)
    elevation.SetLowPoint(0, bounds[2], 0)
    elevation.SetHighPoint(0, bounds[3], 0)
    elevation.SetInputConnection(cylinder.GetOutputPort())

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(elevation.GetOutputPort())
    mapper.SetLookupTable(ctfs[i])
    mapper.SetColorModeToMapScalars()
    mapper.InterpolateScalarsBeforeMappingOn()

    actor = vtkActor()
    actor.SetMapper(mapper)

    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(ctfs[i])

    text_mapper = vtkTextMapper()
    text_mapper.SetInput(titles[i])
    text_mapper.SetTextProperty(text_property)

    text_actor = vtkActor2D()
    text_actor.SetMapper(text_mapper)
    text_actor.SetPosition(300, 16)

    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.AddActor(scalar_bar)
    renderer.AddActor(text_actor)
    renderer.SetBackground(0.322, 0.341, 0.431)
    renderer.SetViewport(xmins[i], ymins[i], xmaxs[i], ymaxs[i])
    render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
