#!/usr/bin/env python

# Demonstrate vtkTessellatorFilter by reading a quadratic tetrahedral mesh,
# adding random cell data, tessellating the higher-order elements, and
# rendering the tessellated output with a shrink filter applied.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import (
    vtkRandomAttributeGenerator,
    vtkShrinkFilter,
    vtkTessellatorFilter,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read quadratic tetrahedral mesh
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "quadraticTetra01.vtu"))

# Add random cell scalars and vectors
random_gen = vtkRandomAttributeGenerator()
random_gen.SetInputConnection(reader.GetOutputPort())
random_gen.SetGenerateCellScalars(True)
random_gen.SetGenerateCellVectors(True)

# Tessellate higher-order elements
tessellator = vtkTessellatorFilter()
tessellator.SetInputConnection(random_gen.GetOutputPort())
tessellator.MergePointsOn()
tessellator.SetOutputDimension(3)

# Shrink cells for visibility
shrink = vtkShrinkFilter()
shrink.SetInputConnection(tessellator.GetOutputPort())
shrink.SetShrinkFactor(0.8)

# Extract surface
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(shrink.GetOutputPort())

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetScalarModeToUseCellData()

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
render_window.SetWindowName("tessellator")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
