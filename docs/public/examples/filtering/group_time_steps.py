#!/usr/bin/env python

# Demonstrate vtkGroupTimeStepsFilter by generating spheres at multiple
# positions (simulating grouped time steps) and displaying them together.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import (
    vtkPartitionedDataSetCollectionSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Generate spheres at 10 positions (simulating grouped time steps)
append_spheres = vtkAppendPolyData()

sphere_0 = vtkSphereSource()
sphere_0.SetCenter(0, 0, 0)
sphere_0.Update()
append_spheres.AddInputData(sphere_0.GetOutput())

sphere_1 = vtkSphereSource()
sphere_1.SetCenter(0, 2, 0)
sphere_1.Update()
append_spheres.AddInputData(sphere_1.GetOutput())

sphere_2 = vtkSphereSource()
sphere_2.SetCenter(0, 4, 0)
sphere_2.Update()
append_spheres.AddInputData(sphere_2.GetOutput())

sphere_3 = vtkSphereSource()
sphere_3.SetCenter(0, 6, 0)
sphere_3.Update()
append_spheres.AddInputData(sphere_3.GetOutput())

sphere_4 = vtkSphereSource()
sphere_4.SetCenter(0, 8, 0)
sphere_4.Update()
append_spheres.AddInputData(sphere_4.GetOutput())

sphere_5 = vtkSphereSource()
sphere_5.SetCenter(0, 10, 0)
sphere_5.Update()
append_spheres.AddInputData(sphere_5.GetOutput())

sphere_6 = vtkSphereSource()
sphere_6.SetCenter(0, 12, 0)
sphere_6.Update()
append_spheres.AddInputData(sphere_6.GetOutput())

sphere_7 = vtkSphereSource()
sphere_7.SetCenter(0, 14, 0)
sphere_7.Update()
append_spheres.AddInputData(sphere_7.GetOutput())

sphere_8 = vtkSphereSource()
sphere_8.SetCenter(0, 16, 0)
sphere_8.Update()
append_spheres.AddInputData(sphere_8.GetOutput())

sphere_9 = vtkSphereSource()
sphere_9.SetCenter(0, 18, 0)
sphere_9.Update()
append_spheres.AddInputData(sphere_9.GetOutput())

append_spheres.Update()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(append_spheres.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Generate translated shapes at 10 positions (simulating grouped PDC time steps)
append_shapes = vtkAppendPolyData()

pdc_source_0 = vtkPartitionedDataSetCollectionSource()
pdc_source_0.SetNumberOfShapes(1)
pdc_source_0.Update()
transform_0 = vtkTransform()
transform_0.Identity()
transform_0.Translate(2, 0, 0)
xform_0 = vtkTransformPolyDataFilter()
xform_0.SetTransform(transform_0)
xform_0.SetInputConnection(pdc_source_0.GetOutputPort())
xform_0.Update()
append_shapes.AddInputData(xform_0.GetOutput())

pdc_source_1 = vtkPartitionedDataSetCollectionSource()
pdc_source_1.SetNumberOfShapes(2)
pdc_source_1.Update()
transform_1 = vtkTransform()
transform_1.Identity()
transform_1.Translate(2, 2, 0)
xform_1 = vtkTransformPolyDataFilter()
xform_1.SetTransform(transform_1)
xform_1.SetInputConnection(pdc_source_1.GetOutputPort())
xform_1.Update()
append_shapes.AddInputData(xform_1.GetOutput())

pdc_source_2 = vtkPartitionedDataSetCollectionSource()
pdc_source_2.SetNumberOfShapes(3)
pdc_source_2.Update()
transform_2 = vtkTransform()
transform_2.Identity()
transform_2.Translate(2, 4, 0)
xform_2 = vtkTransformPolyDataFilter()
xform_2.SetTransform(transform_2)
xform_2.SetInputConnection(pdc_source_2.GetOutputPort())
xform_2.Update()
append_shapes.AddInputData(xform_2.GetOutput())

pdc_source_3 = vtkPartitionedDataSetCollectionSource()
pdc_source_3.SetNumberOfShapes(1)
pdc_source_3.Update()
transform_3 = vtkTransform()
transform_3.Identity()
transform_3.Translate(2, 6, 0)
xform_3 = vtkTransformPolyDataFilter()
xform_3.SetTransform(transform_3)
xform_3.SetInputConnection(pdc_source_3.GetOutputPort())
xform_3.Update()
append_shapes.AddInputData(xform_3.GetOutput())

pdc_source_4 = vtkPartitionedDataSetCollectionSource()
pdc_source_4.SetNumberOfShapes(2)
pdc_source_4.Update()
transform_4 = vtkTransform()
transform_4.Identity()
transform_4.Translate(2, 8, 0)
xform_4 = vtkTransformPolyDataFilter()
xform_4.SetTransform(transform_4)
xform_4.SetInputConnection(pdc_source_4.GetOutputPort())
xform_4.Update()
append_shapes.AddInputData(xform_4.GetOutput())

pdc_source_5 = vtkPartitionedDataSetCollectionSource()
pdc_source_5.SetNumberOfShapes(3)
pdc_source_5.Update()
transform_5 = vtkTransform()
transform_5.Identity()
transform_5.Translate(2, 10, 0)
xform_5 = vtkTransformPolyDataFilter()
xform_5.SetTransform(transform_5)
xform_5.SetInputConnection(pdc_source_5.GetOutputPort())
xform_5.Update()
append_shapes.AddInputData(xform_5.GetOutput())

pdc_source_6 = vtkPartitionedDataSetCollectionSource()
pdc_source_6.SetNumberOfShapes(1)
pdc_source_6.Update()
transform_6 = vtkTransform()
transform_6.Identity()
transform_6.Translate(2, 12, 0)
xform_6 = vtkTransformPolyDataFilter()
xform_6.SetTransform(transform_6)
xform_6.SetInputConnection(pdc_source_6.GetOutputPort())
xform_6.Update()
append_shapes.AddInputData(xform_6.GetOutput())

pdc_source_7 = vtkPartitionedDataSetCollectionSource()
pdc_source_7.SetNumberOfShapes(2)
pdc_source_7.Update()
transform_7 = vtkTransform()
transform_7.Identity()
transform_7.Translate(2, 14, 0)
xform_7 = vtkTransformPolyDataFilter()
xform_7.SetTransform(transform_7)
xform_7.SetInputConnection(pdc_source_7.GetOutputPort())
xform_7.Update()
append_shapes.AddInputData(xform_7.GetOutput())

pdc_source_8 = vtkPartitionedDataSetCollectionSource()
pdc_source_8.SetNumberOfShapes(3)
pdc_source_8.Update()
transform_8 = vtkTransform()
transform_8.Identity()
transform_8.Translate(2, 16, 0)
xform_8 = vtkTransformPolyDataFilter()
xform_8.SetTransform(transform_8)
xform_8.SetInputConnection(pdc_source_8.GetOutputPort())
xform_8.Update()
append_shapes.AddInputData(xform_8.GetOutput())

pdc_source_9 = vtkPartitionedDataSetCollectionSource()
pdc_source_9.SetNumberOfShapes(1)
pdc_source_9.Update()
transform_9 = vtkTransform()
transform_9.Identity()
transform_9.Translate(2, 18, 0)
xform_9 = vtkTransformPolyDataFilter()
xform_9.SetTransform(transform_9)
xform_9.SetInputConnection(pdc_source_9.GetOutputPort())
xform_9.Update()
append_shapes.AddInputData(xform_9.GetOutput())

append_shapes.Update()

shape_mapper = vtkPolyDataMapper()
shape_mapper.SetInputConnection(append_shapes.GetOutputPort())

shape_actor = vtkActor()
shape_actor.SetMapper(shape_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(shape_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("group time steps")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
