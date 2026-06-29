#!/usr/bin/env python

# Demonstrate vtkSelectPolyData with Dijkstra edge search on a cow mesh,
# generating selection scalars around the ear, clipping the mesh, and
# verifying that point and cell data pass through correctly.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIntArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersModeling import vtkSelectPolyData
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read cow mesh
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "cow.vtp"))
reader.Update()

# Loop around the ear of the cow
loop_point_positions = [
    [4.5208645, 2.0485868, -0.5763462],
    [4.5447617, 1.9674546, -0.57545805],
    [4.538317, 1.8611917, -0.5673257],
    [4.5059876, 1.7356979, -0.55352426],
    [4.4522295, 1.5968721, -0.53562874],
    [4.381498, 1.4506135, -0.51521415],
    [4.2982492, 1.3028216, -0.49385568],
    [4.206939, 1.1593955, -0.47312826],
    [4.112025, 1.0262344, -0.454607],
    [4.0179615, 0.9092375, -0.43986693],
    [3.9292052, 0.8143042, -0.43048313],
    [3.8492908, 0.74591345, -0.42754683],
    [3.7780685, 0.7028636, -0.430214],
    [3.7144666, 0.68253285, -0.43715683],
    [3.657414, 0.6822994, -0.44704747],
    [3.605839, 0.6995413, -0.4585581],
    [3.5586705, 0.7316368, -0.47036093],
    [3.514837, 0.7759641, -0.4811281],
    [3.4732673, 0.8299013, -0.4895318],
    [3.43289, 0.8908266, -0.49424416],
    [3.3926337, 0.9561181, -0.4939374],
    [3.3520544, 1.023584, -0.48774803],
    [3.3132184, 1.0927521, -0.47666985],
    [3.2788188, 1.1635803, -0.4621611],
    [3.2515495, 1.2360263, -0.4456799],
    [3.2341034, 1.3100479, -0.42868453],
    [3.2291746, 1.385603, -0.4126331],
    [3.2394562, 1.4626493, -0.39898378],
    [3.267642, 1.5411446, -0.38919482],
    [3.316425, 1.6210469, -0.38472438],
    [3.388499, 1.7023138, -0.38703063],
    [3.4850955, 1.784371, -0.3970445],
    [3.6015983, 1.8645154, -0.41358784],
    [3.731929, 1.9395119, -0.43495524],
    [3.8700097, 2.0061252, -0.4594413],
    [4.0097623, 2.0611203, -0.48534057],
    [4.145108, 2.1012616, -0.5109477],
    [4.2699695, 2.1233141, -0.5345572],
    [4.3782682, 2.1240425, -0.55446374],
    [4.463926, 2.1002119, -0.5689619],
    [4.5208645, 2.0485868, -0.5763462],
]

loop_points = vtkPoints()
for xyz in loop_point_positions:
    loop_points.InsertNextPoint(xyz)

# Add attribute arrays to the cow polydata
cow_poly_data = vtkPolyData()
cow_poly_data.ShallowCopy(reader.GetOutput())

pt_scalar_array = vtkIntArray()
pt_scalar_array.SetName("ScalarArray")
pt_scalar_array.SetNumberOfComponents(1)
pt_scalar_array.SetNumberOfTuples(cow_poly_data.GetNumberOfPoints())
pt_scalar_array.Fill(1)
cow_poly_data.GetPointData().AddArray(pt_scalar_array)

cell_scalar_array = vtkIntArray()
cell_scalar_array.SetName("ScalarArray")
cell_scalar_array.SetNumberOfComponents(1)
cell_scalar_array.SetNumberOfTuples(cow_poly_data.GetNumberOfCells())
cell_scalar_array.Fill(1)
cow_poly_data.GetCellData().AddArray(cell_scalar_array)

# Selection filter using Dijkstra edge search
selection_filter = vtkSelectPolyData()
selection_filter.SetInputData(cow_poly_data)
selection_filter.SetLoop(loop_points)
selection_filter.GenerateSelectionScalarsOn()
selection_filter.SetSelectionScalarsArrayName("SelectionArray")
selection_filter.SetSelectionModeToSmallestRegion()
selection_filter.SetEdgeSearchModeToDijkstra()
selection_filter.Update()

# Clip the mesh with the selection
clip_filter = vtkClipPolyData()
clip_filter.SetInputConnection(selection_filter.GetOutputPort())

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clip_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("select polydata filter")

# Scene
renderer.GetActiveCamera().Azimuth(140)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
