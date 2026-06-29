#!/usr/bin/env python

# Demonstrate vtkHyperTreeGridPreConfiguredSource by cycling through
# several pre-configured modes and a custom configuration, rendering
# the final geometry with depth-based coloring and edge visibility.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersHyperTree import vtkHyperTreeGridGeometry
from vtkmodules.vtkFiltersSources import vtkHyperTreeGridPreConfiguredSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
generator = vtkHyperTreeGridPreConfiguredSource()

# Geometry filter
geometry_filter = vtkHyperTreeGridGeometry()
geometry_filter.SetInputConnection(generator.GetOutputPort())

# Cycle through pre-configured modes
generator.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.UNBALANCED_3DEPTH_2BRANCH_2X3)
geometry_filter.Update()

generator.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.BALANCED_3DEPTH_2BRANCH_2X3)
geometry_filter.Update()

generator.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.UNBALANCED_2DEPTH_3BRANCH_3X3)
geometry_filter.Update()

generator.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.BALANCED_4DEPTH_3BRANCH_2X2)
geometry_filter.Update()

generator.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.UNBALANCED_3DEPTH_2BRANCH_3X2X3)
geometry_filter.Update()

generator.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.BALANCED_2DEPTH_3BRANCH_3X3X2)
geometry_filter.Update()

# Custom mode
generator.SetHTGMode(vtkHyperTreeGridPreConfiguredSource.CUSTOM)
geometry_filter.Update()

generator.SetCustomArchitecture(vtkHyperTreeGridPreConfiguredSource.UNBALANCED)
generator.SetCustomDim(2)
generator.SetCustomFactor(3)
generator.SetCustomDepth(4)
geometry_filter.Update()

# Mapper with depth coloring
lookup_table = vtkLookupTable()
lookup_table.SetNumberOfTableValues(5)
lookup_table.SetTableRange(0, 4)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry_filter.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetLookupTable(lookup_table)
mapper.UseLookupTableScalarRangeOn()
mapper.SetScalarModeToUseCellFieldData()
mapper.ColorByArrayComponent("Depth", 0)
mapper.InterpolateScalarsBeforeMappingOn()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToSurface()
actor.GetProperty().EdgeVisibilityOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("hypertreegrid pre configured source")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
