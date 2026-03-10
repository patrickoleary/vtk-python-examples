#!/usr/bin/env python

# Select vertices and edges interactively on a random graph. Click on
# vertices or edges in the view; the selection callback prints the selected
# IDs and their field type to the console.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkInfovisCore import vtkRandomGraphSource
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

# Source: generate a random graph
source = vtkRandomGraphSource()
source.Update()

# View: display the graph
view = vtkGraphLayoutView()
view.AddRepresentationFromInputConnection(source.GetOutputPort())


def selection_callback(caller, event):
    """Print the IDs of selected vertices and edges."""
    sel = caller.GetCurrentSelection()

    for node_idx in range(sel.GetNumberOfNodes()):
        node = sel.GetNode(node_idx)
        field_type = node.GetFieldType()
        sel_list = node.GetSelectionList()

        if sel_list.GetNumberOfTuples() > 0:
            if field_type == 3:
                print("Vertices Selected:")
            elif field_type == 4:
                print("Edges Selected:")
            else:
                print("Unknown type:")
            for i in range(sel_list.GetNumberOfTuples()):
                print(f"\t{sel_list.GetValue(i)}")

    print("- - -")


# Representation: attach selection callback via annotation link
rep = view.GetRepresentation(0)
link = rep.GetAnnotationLink()
link.AddObserver("AnnotationChangedEvent", selection_callback)

render_window = view.GetRenderWindow()
render_window.SetSize(600, 600)
render_window.SetWindowName("SelectedVerticesAndEdges")
view.ResetCamera()

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
