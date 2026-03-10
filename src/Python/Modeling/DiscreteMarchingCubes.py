#!/usr/bin/env python

# Generate labeled blob volumes and extract discrete isosurfaces
# using vtkDiscreteFlyingEdges3D, colored by region.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkLookupTable,
    vtkMinimalStandardRandomSequence,
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkSphere,
)
from vtkmodules.vtkFiltersGeneral import vtkDiscreteFlyingEdges3D
from vtkmodules.vtkImagingCore import vtkImageThreshold
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
burlywood_background_rgb = (0.871, 0.722, 0.529)


# Source: create a labeled volume with 20 randomly placed spheres
n = 20
radius = 8
blob_image = vtkImageData()
max_r = 50 - 2.0 * radius
random_sequence = vtkMinimalStandardRandomSequence()
random_sequence.SetSeed(5071)
for i in range(n):
    sphere = vtkSphere()
    sphere.SetRadius(radius)
    x = random_sequence.GetRangeValue(-max_r, max_r)
    random_sequence.Next()
    y = random_sequence.GetRangeValue(-max_r, max_r)
    random_sequence.Next()
    z = random_sequence.GetRangeValue(-max_r, max_r)
    random_sequence.Next()
    sphere.SetCenter(int(x), int(y), int(z))

    sampler = vtkSampleFunction()
    sampler.SetImplicitFunction(sphere)
    sampler.SetOutputScalarTypeToFloat()
    sampler.SetSampleDimensions(100, 100, 100)
    sampler.SetModelBounds(-50, 50, -50, 50, -50, 50)

    thres = vtkImageThreshold()
    thres.SetInputConnection(sampler.GetOutputPort())
    thres.ThresholdByLower(radius * radius)
    thres.ReplaceInOn()
    thres.ReplaceOutOn()
    thres.SetInValue(i + 1)
    thres.SetOutValue(0)
    thres.Update()
    if i == 0:
        blob_image.DeepCopy(thres.GetOutput())

    max_value = vtkImageMathematics()
    max_value.SetInputData(0, blob_image)
    max_value.SetInputData(1, thres.GetOutput())
    max_value.SetOperationToMax()
    max_value.Modified()
    max_value.Update()
    blob_image.DeepCopy(max_value.GetOutput())

# Filter: extract discrete isosurfaces
discrete = vtkDiscreteFlyingEdges3D()
discrete.SetInputData(blob_image)
discrete.GenerateValues(n, 1, n)

# Lookup table: random color per label
lut = vtkLookupTable()
lut.SetNumberOfColors(n)
lut.SetTableRange(0, n - 1)
lut.SetScaleToLinear()
lut.Build()
lut.SetTableValue(0, 0, 0, 0, 1)
random_sequence = vtkMinimalStandardRandomSequence()
random_sequence.SetSeed(5071)
for i in range(1, n):
    r = random_sequence.GetRangeValue(0.4, 1)
    random_sequence.Next()
    g = random_sequence.GetRangeValue(0.4, 1)
    random_sequence.Next()
    b = random_sequence.GetRangeValue(0.4, 1)
    random_sequence.Next()
    lut.SetTableValue(i, r, g, b, 1.0)

# Mapper: color by label
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(discrete.GetOutputPort())
mapper.SetLookupTable(lut)
mapper.SetScalarRange(0, lut.GetNumberOfColors())

# Actor: the discrete isosurfaces
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(burlywood_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("DiscreteMarchingCubes")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
