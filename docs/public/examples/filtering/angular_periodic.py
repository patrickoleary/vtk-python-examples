#!/usr/bin/env python

# Demonstrate vtkAngularPeriodicFilter by reading an unstructured grid
# periodic piece, replicating it around the Z axis at 45-degree intervals,
# then stream tracing through the periodic field and rendering both the
# geometry and streamlines colored by RTData.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkMultiBlockDataSet
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersParallel import vtkAngularPeriodicFilter
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read the periodic piece
reader = vtkXMLUnstructuredGridReader()
reader.SetFileName(os.path.join(data_dir, "periodicPiece.vtu"))
reader.Update()

# Wrap in a multiblock dataset
mb = vtkMultiBlockDataSet()
mb.SetNumberOfBlocks(1)
mb.SetBlock(0, reader.GetOutput())

# Angular periodic filter — replicate around Z at 45 degrees
angular_periodic = vtkAngularPeriodicFilter()
angular_periodic.SetInputData(mb)
angular_periodic.AddIndex(1)
angular_periodic.SetIterationModeToMax()
angular_periodic.SetRotationModeToDirectAngle()
angular_periodic.SetRotationAngle(45.0)
angular_periodic.SetRotationAxisToZ()

# Geometry extraction for rendering the multiblock surface
geom = vtkGeometryFilter()
geom.SetInputData(mb)

triangle = vtkTriangleFilter()
triangle.SetInputConnection(geom.GetOutputPort())

# Seed point source for stream tracing
seed = vtkPointSource()
seed.SetCenter(5.80752824733665, -3.46144284193073, -5.83410675177451)
seed.SetNumberOfPoints(1)
seed.SetRadius(2)

# Stream tracer through the periodic field
stream_tracer = vtkStreamTracer()
stream_tracer.SetInputConnection(angular_periodic.GetOutputPort())
stream_tracer.SetInputArrayToProcess(0, 0, 0, 0, "Result")
stream_tracer.SetInterpolatorType(0)
stream_tracer.SetIntegrationDirection(2)
stream_tracer.SetIntegratorType(2)
stream_tracer.SetIntegrationStepUnit(2)
stream_tracer.SetInitialIntegrationStep(0.2)
stream_tracer.SetMinimumIntegrationStep(0.01)
stream_tracer.SetMaximumIntegrationStep(0.5)
stream_tracer.SetMaximumNumberOfSteps(2000)
stream_tracer.SetMaximumPropagation(28.0)
stream_tracer.SetTerminalSpeed(1e-12)
stream_tracer.SetMaximumError(1e-6)
stream_tracer.SetComputeVorticity(True)
stream_tracer.SetSourceConnection(seed.GetOutputPort())
stream_tracer.Update()

pd = stream_tracer.GetOutput()
pd.GetPointData().SetActiveScalars("RTData")

# Lookup table
hue_lut = vtkLookupTable()
hue_lut.SetHueRange(0.0, 1.0)
hue_lut.SetSaturationRange(1.0, 1.0)
hue_lut.Build()

# Mapper and actor pairs
multi_block_mapper = vtkCompositePolyDataMapper()
multi_block_mapper.SetInputConnection(triangle.GetOutputPort())
multi_block_mapper.SetLookupTable(hue_lut)
multi_block_mapper.SetScalarRange(131.0, 225.0)
multi_block_mapper.SetColorModeToMapScalars()
multi_block_mapper.SetScalarModeToUsePointData()
multi_block_actor = vtkActor()
multi_block_actor.SetMapper(multi_block_mapper)

stream_mapper = vtkPolyDataMapper()
stream_mapper.SetInputConnection(stream_tracer.GetOutputPort())
stream_mapper.SetLookupTable(hue_lut)
stream_mapper.SetScalarRange(131.0, 225.0)
stream_mapper.SetColorModeToMapScalars()
stream_mapper.SetScalarModeToUsePointData()
stream_actor = vtkActor()
stream_actor.SetMapper(stream_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(multi_block_actor)
renderer.AddActor(stream_actor)
renderer.SetBackground(1.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)
render_window.SetWindowName("angular periodic")

# Scene
renderer.GetActiveCamera().SetPosition(
    3.97282457351685, -0.0373859405517578, -59.3025624847687)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
