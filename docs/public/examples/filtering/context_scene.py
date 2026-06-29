#!/usr/bin/env python
# Demonstrate a context scene with block items, parent-child hierarchy, and transforms.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkRenderingContext2D import (
    vtkBlockItem,
    vtkContextActor,
    vtkContextTransform,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create block items.
test = vtkBlockItem()
test.SetDimensions(20, 20, 30, 40)
test2 = vtkBlockItem()
test2.SetDimensions(80, 20, 30, 40)

parent = vtkBlockItem()
parent.SetDimensions(20, 200, 80, 40)
parent.SetLabel("Parent")
child = vtkBlockItem()
child.SetDimensions(120, 200, 80, 46)
child.SetLabel("Child")
child2 = vtkBlockItem()
child2.SetDimensions(150, 250, 86, 46)
child2.SetLabel("Child2")

# Create a transform item.
transform = vtkContextTransform()
transform.AddItem(parent)
transform.Translate(50, -190)

# Context actor and scene wiring.
context_actor = vtkContextActor()
scene = context_actor.GetScene()

# Build up multi-level scene.
scene.AddItem(test)
scene.AddItem(test2)
scene.AddItem(parent)
parent.AddItem(child)
child.AddItem(child2)
scene.AddItem(transform)

# Turn off the color buffer.
scene.SetUseBufferId(False)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("context scene")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
