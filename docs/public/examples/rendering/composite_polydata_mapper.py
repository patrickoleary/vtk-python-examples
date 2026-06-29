#!/usr/bin/env python
# Demonstrate vtkCompositePolyDataMapper with per-block display attributes and serialization.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPartitionedDataSetCollectionSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkCompositeDataDisplayAttributes,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source with multiple shapes.
source = vtkPartitionedDataSetCollectionSource()
source.SetNumberOfShapes(12)
source.Update()

# Composite poly data mapper.
mapper = vtkCompositePolyDataMapper()
mapper.SetInputDataObject(source.GetOutput())

display_attributes = vtkCompositeDataDisplayAttributes()
mapper.SetCompositeDataDisplayAttributes(display_attributes)

# Override some display attributes.
mapper.SetBlockVisibility(11, False)
mapper.SetBlockOpacity(10, 0.5)

color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(0, 1, 0, 0)
color_transfer_function.AddRGBPoint(1, 1, 1, 0)
display_attributes.SetBlockLookupTable(source.GetOutput().GetPartition(2, 0), color_transfer_function)
display_attributes.SetBlockScalarVisibility(source.GetOutput().GetPartition(3, 0), False)
display_attributes.SetBlockColor(source.GetOutput().GetPartition(3, 0), (0.3, 1.0, 0.5))

# Actor.
actor = vtkActor()
actor.SetMapper(mapper)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("composite polydata mapper")
render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
