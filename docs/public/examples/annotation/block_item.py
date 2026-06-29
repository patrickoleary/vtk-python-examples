#!/usr/bin/env python

# Test vtkBlockItem with various horizontal and vertical alignment options.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401

from vtkmodules.vtkRenderingContext2D import vtkBlockItem, vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Block items
left_top = vtkBlockItem()
left_top.SetLabel("Left-Top")
left_top.SetHorizontalAlignment(vtkBlockItem.LEFT)
left_top.SetVerticalAlignment(vtkBlockItem.TOP)
left_top.SetAutoComputeDimensions(True)
left_top.GetBrush().SetColorF(0.7, 0.7, 0.7)

left_center = vtkBlockItem()
left_center.SetLabel("Left-Center")
left_center.SetHorizontalAlignment(vtkBlockItem.LEFT)
left_center.SetVerticalAlignment(vtkBlockItem.CENTER)
left_center.SetAutoComputeDimensions(True)
left_center.GetBrush().SetColorF(0.7, 0.7, 0.7)

left_bottom = vtkBlockItem()
left_bottom.SetLabel("Left-Bottom")
left_bottom.SetHorizontalAlignment(vtkBlockItem.LEFT)
left_bottom.SetVerticalAlignment(vtkBlockItem.BOTTOM)
left_bottom.SetAutoComputeDimensions(True)
left_bottom.GetBrush().SetColorF(0.7, 0.7, 0.7)

right_top = vtkBlockItem()
right_top.SetLabel("Right-Top")
right_top.SetHorizontalAlignment(vtkBlockItem.RIGHT)
right_top.SetVerticalAlignment(vtkBlockItem.TOP)
right_top.SetAutoComputeDimensions(True)
right_top.GetBrush().SetColorF(0.7, 0.7, 0.7)

right_center = vtkBlockItem()
right_center.SetLabel("Right-Center")
right_center.SetHorizontalAlignment(vtkBlockItem.RIGHT)
right_center.SetVerticalAlignment(vtkBlockItem.CENTER)
right_center.SetAutoComputeDimensions(True)
right_center.GetBrush().SetColorF(0.7, 0.7, 0.7)

right_bottom = vtkBlockItem()
right_bottom.SetLabel("Right-Bottom")
right_bottom.SetHorizontalAlignment(vtkBlockItem.RIGHT)
right_bottom.SetVerticalAlignment(vtkBlockItem.BOTTOM)
right_bottom.SetAutoComputeDimensions(True)
right_bottom.GetBrush().SetColorF(0.7, 0.7, 0.7)

center_top = vtkBlockItem()
center_top.SetLabel("Center-Top")
center_top.SetHorizontalAlignment(vtkBlockItem.CENTER)
center_top.SetVerticalAlignment(vtkBlockItem.TOP)
center_top.SetAutoComputeDimensions(True)
center_top.GetBrush().SetColorF(0.7, 0.7, 0.7)

center_center = vtkBlockItem()
center_center.SetLabel("Center-Center")
center_center.SetHorizontalAlignment(vtkBlockItem.CENTER)
center_center.SetVerticalAlignment(vtkBlockItem.CENTER)
center_center.SetAutoComputeDimensions(True)
center_center.GetBrush().SetColorF(0.7, 0.7, 0.7)

center_bottom = vtkBlockItem()
center_bottom.SetLabel("Center-Bottom")
center_bottom.SetHorizontalAlignment(vtkBlockItem.CENTER)
center_bottom.SetVerticalAlignment(vtkBlockItem.BOTTOM)
center_bottom.SetAutoComputeDimensions(True)
center_bottom.GetBrush().SetColorF(0.7, 0.7, 0.7)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("block item")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
context_actor = vtkContextActor()
scene = context_actor.GetScene()
scene.SetRenderer(renderer)
scene.AddItem(left_top)
scene.AddItem(left_center)
scene.AddItem(left_bottom)
scene.AddItem(right_top)
scene.AddItem(right_center)
scene.AddItem(right_bottom)
scene.AddItem(center_top)
scene.AddItem(center_center)
scene.AddItem(center_bottom)
scene.SetUseBufferId(False)
renderer.AddActor(context_actor)

interactor.Initialize()
interactor.Start()
