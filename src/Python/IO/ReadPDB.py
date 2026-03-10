#!/usr/bin/env python

# Read a Protein Data Bank (.pdb) file using vtkPDBReader and display the
# molecular structure as sphere glyphs colored by atom type.  A small PDB
# file (caffeine molecule) is generated if it does not already exist.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOChemistry import vtkPDBReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
pdb_path = data_dir / "caffeine.pdb"

# Generate a minimal PDB file (caffeine) if it does not exist
if not pdb_path.exists():
    pdb_text = """\
HEADER    CAFFEINE
ATOM      1  C1  CAF A   1       3.243   1.382   0.044  1.00  0.00           C
ATOM      2  C2  CAF A   1       1.816   1.382  -0.030  1.00  0.00           C
ATOM      3  C3  CAF A   1       1.166   0.190  -0.078  1.00  0.00           C
ATOM      4  N1  CAF A   1       1.886  -0.962  -0.050  1.00  0.00           N
ATOM      5  C4  CAF A   1       3.277  -0.972   0.025  1.00  0.00           C
ATOM      6  N2  CAF A   1       3.893   0.181   0.071  1.00  0.00           N
ATOM      7  N3  CAF A   1       1.334   2.672  -0.068  1.00  0.00           N
ATOM      8  C5  CAF A   1       2.294   3.559  -0.022  1.00  0.00           C
ATOM      9  N4  CAF A   1       3.523   2.685   0.038  1.00  0.00           N
ATOM     10  O1  CAF A   1       3.915  -2.016   0.047  1.00  0.00           O
ATOM     11  O2  CAF A   1      -0.045   0.100  -0.148  1.00  0.00           O
ATOM     12  C6  CAF A   1       1.204  -2.254  -0.088  1.00  0.00           C
ATOM     13  C7  CAF A   1      -0.060   2.989  -0.144  1.00  0.00           C
ATOM     14  C8  CAF A   1       4.846   3.277   0.107  1.00  0.00           C
END
"""
    pdb_path.write_text(pdb_text)

# Reader: load the PDB file
reader = vtkPDBReader()
reader.SetFileName(str(pdb_path))
reader.Update()

# GlyphSource: small sphere for each atom
glyph_source = vtkSphereSource()
glyph_source.SetRadius(0.3)
glyph_source.SetPhiResolution(16)
glyph_source.SetThetaResolution(16)

# Mapper: place a sphere glyph at each atom position
mapper = vtkGlyph3DMapper()
mapper.SetInputConnection(reader.GetOutputPort())
mapper.SetSourceConnection(glyph_source.GetOutputPort())
mapper.SetScalarRange(reader.GetOutput().GetScalarRange())
mapper.ScalingOff()

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ReadPDB")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
