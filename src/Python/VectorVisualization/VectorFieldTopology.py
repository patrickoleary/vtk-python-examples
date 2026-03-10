#!/usr/bin/env python

# Compute the topology of a 3D vector field using vtkVectorFieldTopology.
# Critical points, separating lines, separating surfaces, and boundary
# switch features are extracted from a vector field derived from the
# wavelet source via vtkArrayCalculator: v = (x+z, y, x-z).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkArrayCalculator
from vtkmodules.vtkFiltersFlowPaths import vtkVectorFieldTopology
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_gray_rgb = (0.1, 0.1, 0.1)
light_gray_rgb = (0.4, 0.4, 0.4)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: generate a wavelet image data as the computational domain
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)

# Calculator: define a vector field v = (x+z, y, x-z)
calc = vtkArrayCalculator()
calc.AddCoordinateScalarVariable("coordsX", 0)
calc.AddCoordinateScalarVariable("coordsY", 1)
calc.AddCoordinateScalarVariable("coordsZ", 2)
calc.SetFunction(
    "(coordsX+coordsZ)*iHat + coordsY*jHat + (coordsX-coordsZ)*kHat"
)
calc.SetInputConnection(wavelet.GetOutputPort())

# Filter: compute vector field topology
topo = vtkVectorFieldTopology()
topo.SetInputConnection(calc.GetOutputPort())
topo.SetIntegrationStepUnit(1)
topo.SetSeparatrixDistance(1)
topo.SetIntegrationStepSize(1)
topo.SetMaxNumSteps(1000)
topo.SetComputeSurfaces(True)
topo.SetUseBoundarySwitchPoints(True)
topo.SetUseIterativeSeeding(True)
topo.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "resultArray"
)

# Bounding box: semi-transparent wavelet surface for context
bbox_mapper = vtkDataSetMapper()
bbox_mapper.SetInputConnection(wavelet.GetOutputPort())

bbox_actor = vtkActor()
bbox_actor.SetMapper(bbox_mapper)
bbox_actor.GetProperty().SetColor(light_gray_rgb)
bbox_actor.GetProperty().SetOpacity(0.1)
bbox_actor.GetProperty().SetRepresentationToSurface()

# Critical points (output port 0)
cp_mapper = vtkDataSetMapper()
cp_mapper.SetInputConnection(topo.GetOutputPort(0))

cp_actor = vtkActor()
cp_actor.SetMapper(cp_mapper)
cp_actor.GetProperty().SetColor(dark_gray_rgb)
cp_actor.GetProperty().SetPointSize(20)
cp_actor.GetProperty().SetRenderPointsAsSpheres(True)

# Separating lines (output port 1)
sep_mapper = vtkDataSetMapper()
sep_mapper.SetInputConnection(topo.GetOutputPort(1))

sep_actor = vtkActor()
sep_actor.SetMapper(sep_mapper)
sep_actor.GetProperty().SetColor(dark_gray_rgb)
sep_actor.GetProperty().SetLineWidth(10)
sep_actor.GetProperty().SetRenderLinesAsTubes(True)

# Separating surfaces (output port 2)
surf_mapper = vtkDataSetMapper()
surf_mapper.SetInputConnection(topo.GetOutputPort(2))

surf_actor = vtkActor()
surf_actor.SetMapper(surf_mapper)
surf_actor.GetProperty().SetColor(dark_gray_rgb)
surf_actor.GetProperty().SetRepresentationToWireframe()

# Boundary switch lines (output port 3)
bnd_mapper = vtkDataSetMapper()
bnd_mapper.SetInputConnection(topo.GetOutputPort(3))

bnd_actor = vtkActor()
bnd_actor.SetMapper(bnd_mapper)
bnd_actor.GetProperty().SetColor(dark_gray_rgb)
bnd_actor.GetProperty().SetLineWidth(10)
bnd_actor.GetProperty().SetRenderLinesAsTubes(True)

# Boundary switch surfaces (output port 4)
bnd_surf_mapper = vtkDataSetMapper()
bnd_surf_mapper.SetInputConnection(topo.GetOutputPort(4))

bnd_surf_actor = vtkActor()
bnd_surf_actor.SetMapper(bnd_surf_mapper)
bnd_surf_actor.GetProperty().SetColor(dark_gray_rgb)
bnd_surf_actor.GetProperty().SetRepresentationToWireframe()

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(bbox_actor)
renderer.AddActor(cp_actor)
renderer.AddActor(sep_actor)
renderer.AddActor(surf_actor)
renderer.AddActor(bnd_actor)
renderer.AddActor(bnd_surf_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("VectorFieldTopology")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
