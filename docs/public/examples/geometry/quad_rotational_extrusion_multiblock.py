#!/usr/bin/env python

# Demonstrate vtkQuadRotationalExtrusionFilter with multi-block input
# by reading two semi-disk polydata blocks, assembling a nested
# multi-block dataset, extruding with per-block angles, and rendering
# the smooth surface with wireframe overlays per block.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkCompositeDataSet, vtkMultiBlockDataSet
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeometry import vtkCompositeDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkQuadRotationalExtrusionFilter
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read block 0
reader_0 = vtkXMLPolyDataReader()
reader_0.SetFileName(os.path.join(data_dir, "SemiDisk", "SemiDisk-0.vtp"))
reader_0.Update()

# Read block 1
reader_1 = vtkXMLPolyDataReader()
reader_1.SetFileName(os.path.join(data_dir, "SemiDisk", "SemiDisk-1.vtp"))
reader_1.Update()

# Assemble nested multi-block dataset
in_mesh = vtkMultiBlockDataSet()
in_mesh.SetNumberOfBlocks(2)
in_mesh.GetMetaData(0).Set(vtkCompositeDataSet.NAME(), "Block 0")
in_mesh.SetBlock(0, reader_0.GetOutput())

in_mesh_2 = vtkMultiBlockDataSet()
in_mesh.SetBlock(1, in_mesh_2)
in_mesh_2.SetNumberOfBlocks(1)
in_mesh_2.GetMetaData(0).Set(vtkCompositeDataSet.NAME(), "Block 1")
in_mesh_2.SetBlock(0, reader_1.GetOutput())

# Quad-based rotational extrusion with per-block angles
sweeper = vtkQuadRotationalExtrusionFilter()
sweeper.SetResolution(18)
sweeper.SetInputData(in_mesh)
sweeper.SetAxisToX()
sweeper.SetDefaultAngle(270)
sweeper.AddPerBlockAngle(1, 90.0)
sweeper.AddPerBlockAngle(3, 45.0)

# Composite geometry for smooth surface
out_mesh = vtkCompositeDataGeometryFilter()
out_mesh.SetInputConnection(sweeper.GetOutputPort())

# Normals for smooth rendering
normals = vtkPolyDataNormals()
normals.SetInputConnection(out_mesh.GetOutputPort())

# Smooth surface mapper and actor
out_mesh_mapper = vtkPolyDataMapper()
out_mesh_mapper.SetInputConnection(normals.GetOutputPort())
out_mesh_mapper.SetResolveCoincidentTopologyToPolygonOffset()

out_mesh_actor = vtkActor()
out_mesh_actor.SetMapper(out_mesh_mapper)
out_mesh_actor.GetProperty().SetRepresentationToSurface()
out_mesh_actor.GetProperty().SetInterpolationToGouraud()
out_mesh_actor.GetProperty().SetColor(0.9, 0.9, 0.9)

# Retrieve per-block polydata for wireframe overlays
sweeper.Update()
out_mesh_mb = sweeper.GetOutput()
out_mesh_0 = out_mesh_mb.GetBlock(0)
out_mesh_mb_2 = out_mesh_mb.GetBlock(1)
out_mesh_1 = out_mesh_mb_2.GetBlock(0)

# Wireframe for block 0
out_block_mapper_0 = vtkPolyDataMapper()
out_block_mapper_0.SetInputData(out_mesh_0)
out_block_mapper_0.SetResolveCoincidentTopologyToPolygonOffset()

out_block_actor_0 = vtkActor()
out_block_actor_0.SetMapper(out_block_mapper_0)
out_block_actor_0.GetProperty().SetRepresentationToWireframe()
out_block_actor_0.GetProperty().SetColor(0.9, 0.0, 0.0)
out_block_actor_0.GetProperty().SetAmbient(1.0)
out_block_actor_0.GetProperty().SetDiffuse(0.0)
out_block_actor_0.GetProperty().SetSpecular(0.0)

# Wireframe for block 1
out_block_mapper_1 = vtkPolyDataMapper()
out_block_mapper_1.SetInputData(out_mesh_1)
out_block_mapper_1.SetResolveCoincidentTopologyToPolygonOffset()

out_block_actor_1 = vtkActor()
out_block_actor_1.SetMapper(out_block_mapper_1)
out_block_actor_1.GetProperty().SetRepresentationToWireframe()
out_block_actor_1.GetProperty().SetColor(0.0, 0.9, 0.0)
out_block_actor_1.GetProperty().SetAmbient(1.0)
out_block_actor_1.GetProperty().SetDiffuse(0.0)
out_block_actor_1.GetProperty().SetSpecular(0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(out_mesh_actor)
renderer.AddActor(out_block_actor_0)
renderer.AddActor(out_block_actor_1)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.SetWindowName("quad rotational extrusion multiblock")

# Scene
camera = vtkCamera()
camera.SetFocalPoint(36.640094041788934, 0.3387609170199118, 1.2087523663629445)
camera.SetPosition(37.77735939083618, 0.42739828159854326, 2.988046512725565)
camera.SetViewUp(-0.40432906992858864, 0.8891923825021084, 0.21413759621072337)
camera.SetViewAngle(30.0)
renderer.SetActiveCamera(camera)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
