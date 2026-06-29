#!/usr/bin/env python

# Generate random cell scalars (constant per block) on a multi-block
# dataset containing a plane and a sphere using vtkRandomAttributeGenerator.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import (
    vtkMultiBlockDataGroupFilter,
    vtkRandomAttributeGenerator,
)
from vtkmodules.vtkFiltersSources import (
    vtkPlaneSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Force a starting random value
ra_math = vtkMath()
ra_math.RandomSeed(6)

# Create a plane and sphere, group into multi-block
ps = vtkPlaneSource()
ps.SetXResolution(10)
ps.SetYResolution(10)

ss = vtkSphereSource()
ss.SetRadius(0.3)

group = vtkMultiBlockDataGroupFilter()
group.AddInputConnection(ps.GetOutputPort())
group.AddInputConnection(ss.GetOutputPort())

# Generate random cell scalars constant per block
ag = vtkRandomAttributeGenerator()
ag.SetInputConnection(group.GetOutputPort())
ag.GenerateCellScalarsOn()
ag.AttributesConstantPerBlockOn()

normals = vtkPolyDataNormals()
normals.SetInputConnection(ag.GetOutputPort())
normals.Update()

# Iterate over blocks and create actors
output_mb = normals.GetOutputDataObject(0)

block_mapper_0 = vtkPolyDataMapper()
block_mapper_0.SetInputData(output_mb.GetBlock(0))

block_actor_0 = vtkActor()
block_actor_0.SetMapper(block_mapper_0)

block_mapper_1 = vtkPolyDataMapper()
block_mapper_1.SetInputData(output_mb.GetBlock(1))

block_actor_1 = vtkActor()
block_actor_1.SetMapper(block_mapper_1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(block_actor_0)
renderer.AddActor(block_actor_1)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("random attribute generator scalar")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = renderer.GetActiveCamera()
camera.Azimuth(20)
camera.Elevation(20)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
