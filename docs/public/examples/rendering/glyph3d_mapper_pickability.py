#!/usr/bin/env python

# Demonstrate vtkGlyph3DMapper block pickability with vtkCompositeDataDisplayAttributes.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet, vtkPolyData
from vtkmodules.vtkFiltersSources import vtkPlaneSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositeDataDisplayAttributes,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build multi-block of 4 planes at different positions
multi_block = vtkMultiBlockDataSet()
multi_block.SetNumberOfBlocks(4)

plane = vtkPlaneSource()

plane.SetOrigin(-0.5, -0.5, 0)
plane.SetPoint1(0.5, -0.5, 0)
plane.SetPoint2(-0.5, 0.5, 0)
plane.Update()
blk_0 = vtkPolyData()
blk_0.DeepCopy(plane.GetOutputDataObject(0))
multi_block.SetBlock(0, blk_0)

plane.SetOrigin(0.5, -0.5, 1)
plane.SetPoint1(1.5, -0.5, 1)
plane.SetPoint2(0.5, 0.5, 1)
plane.Update()
blk_1 = vtkPolyData()
blk_1.DeepCopy(plane.GetOutputDataObject(0))
multi_block.SetBlock(1, blk_1)

plane.SetOrigin(-0.5, 0.5, 2)
plane.SetPoint1(0.5, 0.5, 2)
plane.SetPoint2(-0.5, 1.5, 2)
plane.Update()
blk_2 = vtkPolyData()
blk_2.DeepCopy(plane.GetOutputDataObject(0))
multi_block.SetBlock(2, blk_2)

plane.SetOrigin(0.5, 0.5, 3)
plane.SetPoint1(1.5, 0.5, 3)
plane.SetPoint2(0.5, 1.5, 3)
plane.Update()
blk_3 = vtkPolyData()
blk_3.DeepCopy(plane.GetOutputDataObject(0))
multi_block.SetBlock(3, blk_3)

sphere = vtkSphereSource()
cdda = vtkCompositeDataDisplayAttributes()

mapper = vtkGlyph3DMapper()
mapper.SetSourceConnection(sphere.GetOutputPort())
mapper.SetInputDataObject(0, multi_block)
mapper.SetBlockAttributes(cdda)

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.GetCullers().RemoveAllItems()

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("glyph3d mapper pickability")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Color each block differently
cdda.SetBlockColor(blk_0, [0.5, 0.5, 0.5])
cdda.SetBlockColor(blk_1, [0.0, 1.0, 1.0])
cdda.SetBlockColor(blk_2, [1.0, 1.0, 0.0])
cdda.SetBlockColor(blk_3, [1.0, 0.0, 1.0])

# Set all visible and pickable
cdda.SetBlockVisibility(blk_0, True)
cdda.SetBlockPickability(blk_0, True)
cdda.SetBlockVisibility(blk_1, True)
cdda.SetBlockPickability(blk_1, True)
cdda.SetBlockVisibility(blk_2, True)
cdda.SetBlockPickability(blk_2, True)
cdda.SetBlockVisibility(blk_3, True)
cdda.SetBlockPickability(blk_3, True)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
