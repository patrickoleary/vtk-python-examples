#!/usr/bin/env python

# Demonstrate vtkBlockIdScalars by creating a recursive multi-block
# dataset of image data blocks, assigning block-id scalars, and
# visualizing each block with a different color.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkMultiBlockDataSet,
)
from vtkmodules.vtkFiltersGeneral import vtkBlockIdScalars
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create three image data blocks
image_0 = vtkImageData()
image_0.SetDimensions(3, 3, 3)

image_1 = vtkImageData()
image_1.SetDimensions(2, 2, 2)
image_1.SetOrigin(4, 0, 0)

image_2 = vtkImageData()
image_2.SetDimensions(4, 4, 4)
image_2.SetOrigin(0, 4, 0)

# Build nested multi-block
multi_block_0 = vtkMultiBlockDataSet()
multi_block_0.SetNumberOfBlocks(2)
multi_block_0.SetBlock(0, image_0)
multi_block_0.SetBlock(1, image_1)

multi_block_1 = vtkMultiBlockDataSet()
multi_block_1.SetNumberOfBlocks(2)
multi_block_1.SetBlock(0, multi_block_0)
multi_block_1.SetBlock(1, image_2)

# Apply block id scalars with leaf traversal
block_id_filter = vtkBlockIdScalars()
block_id_filter.SetInputData(multi_block_1)
block_id_filter.TraverseSubTreeOn()
block_id_filter.VisitOnlyLeavesOn()
block_id_filter.Update()

# Extract surface and render
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(block_id_filter.GetOutputPort())

mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("block id scalars")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
