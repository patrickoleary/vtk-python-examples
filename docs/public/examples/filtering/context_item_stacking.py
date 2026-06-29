#!/usr/bin/env python
# Demonstrate context item stacking operations: Lower, Raise, StackAbove, StackUnder.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkRenderingContext2D import vtkBlockItem, vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create block items.
s = 120
step = s // 3
i = 0

root_item = vtkBlockItem()
root_item.SetDimensions(0, 350, 50, 50)

test1 = vtkBlockItem()
test1.SetDimensions(i, i, s, s)
test1.SetLabel("1")
i += step

test2 = vtkBlockItem()
test2.SetDimensions(i, i, s, s)
test2.SetLabel("2")
i += step

test3 = vtkBlockItem()
test3.SetDimensions(i, i, s, s)
test3.SetLabel("3")
i += step

test4 = vtkBlockItem()
test4.SetDimensions(i, i, s, s)
test4.SetLabel("4")
i += step

test41 = vtkBlockItem()
test41.SetDimensions(i, i, s, s)
test41.SetLabel("4.1")
i += step

test411 = vtkBlockItem()
test411.SetDimensions(i, i, s, s)
test411.SetLabel("4.1.1")
i += step

test42 = vtkBlockItem()
test42.SetDimensions(i, i, s, s)
test42.SetLabel("4.2")
i += step

test5 = vtkBlockItem()
test5.SetDimensions(i, i, s, s)
test5.SetLabel("5")

# Build multi-level scene.
root_item.AddItem(test1)
root_item.AddItem(test2)
root_item.AddItem(test3)
root_item.AddItem(test4)
test4.AddItem(test41)
test41.AddItem(test411)
test4.AddItem(test42)
root_item.AddItem(test5)

# Restack item 3 under all items.
index3 = root_item.GetItemIndex(test3)
root_item.Lower(index3)

# Restack item 1 above 4.
index1 = root_item.GetItemIndex(test1)
index4 = root_item.GetItemIndex(test4)
root_item.StackAbove(index1, index4)

# Raise item 41 above 42.
index41 = test4.GetItemIndex(test41)
test4.Raise(index41)

# StackUnder item 2 under item 3.
index2 = root_item.GetItemIndex(test2)
index3 = root_item.GetItemIndex(test3)
root_item.StackUnder(index2, index3)

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(root_item)
context_actor.GetScene().SetUseBufferId(False)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.32, 0.40, 0.47)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("context item stacking")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
