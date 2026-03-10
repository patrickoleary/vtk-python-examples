#!/usr/bin/env python
"""
Generate and fix all .md files to match the Arrow.md standard.

For each .py file, reads:
  - The header comments (lines after shebang) for the description
  - The VTK imports to identify all classes used
  - The inline comments (# Stage: description) to build bullet descriptions
  - Whether it uses interactor.Start() or view.Start()

Generates a .md file with:
  - ### Description
  - Description paragraph (prefixed with "This example" if not already)
  - **Pipeline arrow notation** from existing .md or built from .py comments
  - Bulleted list of ALL VTK classes with links and descriptions
  - Initialize()/Start() bullet if applicable

Usage:
    python scripts/fix_md_files.py audit          # report issues only
    python scripts/fix_md_files.py generate       # regenerate all .md files
    python scripts/fix_md_files.py generate --dry  # show what would be written
"""

import re
import sys
from pathlib import Path

# VTK docs base URL
VTK_DOC_BASE = "https://www.vtk.org/doc/nightly/html/class"

# Standard bullets for well-known pipeline classes.
# These are the canonical descriptions used across all examples.
KNOWN_CLASS_BULLETS = {
    # --- Rendering tail (order matters) ---
    "vtkRenderer":
        "assembles the scene and configures the camera.",
    "vtkRenderWindow":
        "displays the rendered scene in a window on screen.",
    "vtkRenderWindowInteractor":
        "captures mouse and keyboard events.",
    # --- Common mappers ---
    "vtkPolyDataMapper":
        "maps polygon data to graphics primitives.",
    "vtkDataSetMapper":
        "maps unstructured data to graphics primitives.",
    "vtkGlyph3DMapper":
        "places a glyph at each input point.",
    "vtkImageMapper":
        "maps a 2-D image to a plane in the scene.",
    # --- Common actors ---
    "vtkActor":
        "assigns the mapped geometry to the scene.",
    "vtkImageActor":
        "displays a 2D image slice on a quadrilateral plane.",
    "vtkActor2D":
        "renders 2D overlay geometry.",
    "vtkTextActor":
        "overlays text in the viewport.",
    "vtkAxesActor":
        "renders labeled X/Y/Z axes.",
    "vtkContextActor":
        "hosts a chart scene inside a standard vtkRenderer.",
    # --- Common sources ---
    "vtkArrowSource": "generates an arrow.",
    "vtkConeSource": "generates a cone.",
    "vtkCubeSource": "generates a cube.",
    "vtkCylinderSource": "generates a cylinder.",
    "vtkDiskSource": "generates a disk.",
    "vtkLineSource": "generates a line segment.",
    "vtkPlaneSource": "generates a plane.",
    "vtkPointSource": "generates random points in a sphere.",
    "vtkSphereSource": "generates a sphere.",
    "vtkTextSource": "generates polygonal text.",
    "vtkRegularPolygonSource": "generates a regular polygon.",
    "vtkParametricFunctionSource": "tessellates a parametric function.",
    "vtkSuperquadricSource": "generates a superquadric.",
    "vtkPlatonicSolidSource": "generates a Platonic solid.",
    "vtkTessellatedBoxSource": "generates a tessellated box.",
    # --- Image sources ---
    "vtkImageCanvasSource2D":
        "creates a 2D image with drawing primitives.",
    "vtkImageSinusoidSource":
        "generates a procedural sinusoidal image.",
    "vtkImageMandelbrotSource":
        "generates a Mandelbrot fractal image.",
    "vtkImageEllipsoidSource":
        "generates a binary ellipsoidal mask image.",
    # --- Readers ---
    "vtkMetaImageReader":
        "reads a MetaImage (.mhd/.raw) volume.",
    "vtkPNGReader": "reads a PNG image.",
    "vtkJPEGReader": "reads a JPEG image.",
    "vtkBMPReader": "reads a BMP image.",
    "vtkTIFFReader": "reads a TIFF image.",
    "vtkSTLReader": "reads an STL file.",
    "vtkPLYReader": "reads a PLY file.",
    "vtkOBJReader": "reads a Wavefront OBJ file.",
    "vtkXMLPolyDataReader": "reads a VTP file.",
    "vtkXMLUnstructuredGridReader": "reads a VTU file.",
    "vtkXMLStructuredGridReader": "reads a VTS file.",
    "vtkXMLRectilinearGridReader": "reads a VTR file.",
    "vtkXMLImageDataReader": "reads a VTI file.",
    "vtkGenericDataObjectReader": "reads legacy VTK files.",
    "vtkUnstructuredGridReader": "reads a legacy unstructured grid file.",
    "vtkStructuredPointsReader": "reads a legacy structured points file.",
    "vtkPolyDataReader": "reads a legacy polydata file.",
    "vtkStructuredGridReader": "reads a legacy structured grid file.",
    "vtkRectilinearGridReader": "reads a legacy rectilinear grid file.",
    # --- Writers ---
    "vtkXMLPolyDataWriter": "writes a VTP file.",
    "vtkXMLUnstructuredGridWriter": "writes a VTU file.",
    "vtkSTLWriter": "writes an STL file.",
    "vtkPLYWriter": "writes a PLY file.",
    # --- Common filters ---
    "vtkFlyingEdges3D":
        "extracts an iso-surface using a parallelized marching-cubes algorithm.",
    "vtkMarchingCubes":
        "extracts an iso-surface using the marching-cubes algorithm.",
    "vtkContourFilter":
        "generates contour lines or surfaces at specified scalar values.",
    "vtkOutlineFilter":
        "generates a bounding box wireframe.",
    "vtkExtractVOI":
        "extracts a Volume Of Interest (sub-region) from image data.",
    "vtkImageThreshold":
        "segments image data by scalar range.",
    "vtkImageDataGeometryFilter":
        "converts image data into polydata for rendering.",
    "vtkImageChangeInformation":
        "modifies image metadata (spacing, origin, extent) without altering pixel data.",
    "vtkImageFlip":
        "mirrors image data along a specified axis.",
    "vtkImageCast":
        "converts image scalar type for display.",
    "vtkImageGradientMagnitude":
        "computes the gradient magnitude at each voxel.",
    "vtkImagePermute":
        "reorders volume axes.",
    "vtkImageResize":
        "resamples an image to a different resolution.",
    "vtkImageReslice":
        "extracts an arbitrary 2D slice from a 3D volume.",
    "vtkImageShrink3D":
        "downsamples an image by integer factors.",
    "vtkImageNormalize":
        "normalizes pixel vectors to unit magnitude.",
    "vtkImageMathematics":
        "performs pixel-wise arithmetic on images.",
    "vtkImageWeightedSum":
        "computes a weighted sum of multiple images.",
    "vtkImageAccumulate":
        "computes a histogram of scalar values.",
    "vtkImageStencil":
        "applies a stencil mask to image data.",
    "vtkImageToImageStencil":
        "converts a binary mask image into an image stencil.",
    "vtkImageMapToColors":
        "maps scalar values to colors through a lookup table.",
    "vtkImageLuminance":
        "converts an RGB image to grayscale luminance.",
    "vtkClipDataSet":
        "clips data with an implicit function.",
    "vtkProbeFilter":
        "samples data values at probe point locations.",
    "vtkGlyph3D":
        "copies a glyph to each input point.",
    "vtkHedgeHog":
        "creates oriented lines from vector data at each point.",
    "vtkStreamTracer":
        "generates streamlines from vector field data.",
    "vtkTubeFilter":
        "generates tubes around lines.",
    "vtkStripper":
        "creates triangle strips and/or polylines.",
    "vtkCleanPolyData":
        "merges duplicate points and removes degenerate cells.",
    "vtkTriangleFilter":
        "converts input polygons to triangles.",
    "vtkDecimatePro":
        "reduces the number of triangles in a mesh.",
    "vtkSmoothPolyDataFilter":
        "smooths a polygonal mesh using Laplacian smoothing.",
    "vtkPolyDataNormals":
        "computes point and/or cell normals.",
    "vtkWarpScalar":
        "warps geometry along normals by scalar values.",
    "vtkWarpVector":
        "warps geometry by vector data.",
    "vtkElevationFilter":
        "generates scalar values based on elevation.",
    "vtkCutter":
        "cuts data with an implicit function to produce contour lines.",
    "vtkClipPolyData":
        "clips polygonal data with an implicit function.",
    "vtkThreshold":
        "extracts cells whose scalars satisfy a threshold criterion.",
    "vtkShrinkFilter":
        "shrinks cells toward their centroids.",
    "vtkShrinkPolyData":
        "shrinks polygonal cells toward their centroids.",
    "vtkAppendPolyData":
        "appends multiple polydata datasets into one.",
    "vtkTransformPolyDataFilter":
        "applies a geometric transformation to polydata.",
    "vtkDepthSortPolyData":
        "sorts polygons by depth for correct transparency.",
    "vtkCellCenters":
        "generates points at cell centers.",
    "vtkConnectivityFilter":
        "extracts connected regions.",
    "vtkBandedPolyDataContourFilter":
        "generates filled contour bands between scalar values.",
    "vtkFeatureEdges":
        "extracts boundary, non-manifold, and feature edges.",
    "vtkIdFilter":
        "generates point and cell id arrays.",
    "vtkGenerateIds":
        "generates point and cell id arrays.",
    "vtkVertexGlyphFilter":
        "creates a vertex glyph at each input point.",
    "vtkAssignAttribute":
        "assigns a named array as the active attribute.",
    # --- Implicit functions ---
    "vtkSphere": "defines an implicit spherical function.",
    "vtkPlane": "defines an implicit plane function.",
    "vtkCylinder": "defines an implicit cylinder function.",
    "vtkBox": "defines an implicit box function.",
    "vtkQuadric": "defines an implicit quadric function.",
    "vtkImplicitBoolean": "combines implicit functions with boolean operations.",
    "vtkSampleFunction": "samples an implicit function over a grid.",
    # --- Lookup tables & color ---
    "vtkLookupTable":
        "maps scalar values to colors.",
    "vtkColorTransferFunction":
        "maps scalar values to colors via piecewise interpolation.",
    "vtkScalarBarActor":
        "displays a color bar legend.",
    "vtkColorSeries":
        "provides predefined color palettes.",
    # --- Transforms ---
    "vtkTransform": "defines a 4×4 geometric transformation.",
    # --- Data structures ---
    "vtkPoints": "stores 3D point coordinates.",
    "vtkCellArray": "stores cell connectivity.",
    "vtkPolyData": "represents polygonal geometry.",
    "vtkUnstructuredGrid": "represents unstructured geometry.",
    "vtkStructuredGrid": "represents a structured grid with explicit point positions.",
    "vtkRectilinearGrid": "represents a rectilinear grid.",
    "vtkImageData": "represents a regular image or volume.",
    "vtkTable": "holds columns of data for charting.",
    "vtkFloatArray": "stores float data arrays.",
    "vtkDoubleArray": "stores double data arrays.",
    "vtkIntArray": "stores integer data arrays.",
    "vtkUnsignedCharArray": "stores unsigned char data arrays.",
    "vtkStringArray": "stores string data arrays.",
    "vtkIdList": "stores lists of VTK ids.",
    "vtkMath": "provides mathematical utility functions.",
    # --- Properties ---
    "vtkProperty": "defines surface appearance (color, lighting, representation).",
    "vtkVolumeProperty": "defines volume rendering appearance.",
    "vtkTextProperty": "defines text appearance (font, color, size).",
    # --- Camera ---
    "vtkCamera": "defines the viewpoint and projection.",
    # --- Interaction styles ---
    "vtkInteractorStyleTrackballCamera":
        "maps mouse motion to camera transformations.",
    "vtkInteractorStyleTrackballActor":
        "maps mouse motion to per-actor transformations.",
    "vtkInteractorStyleImage":
        "provides 2D image-appropriate interaction (pan and zoom).",
    "vtkInteractorStyleRubberBandZoom":
        "maps a rubber-band rectangle to a camera zoom.",
    "vtkInteractorStyleSwitch":
        "switches between joystick and trackball styles.",
    # --- Pickers ---
    "vtkCellPicker": "performs cell-level picking.",
    "vtkPointPicker": "picks the closest point.",
    "vtkPropPicker": "picks the frontmost prop.",
    "vtkWorldPointPicker": "picks the world point under the cursor.",
    "vtkAreaPicker": "picks all actors in a rectangular region.",
    "vtkHardwareSelector": "selects cells or points using GPU hardware.",
    # --- Widgets ---
    "vtkOrientationMarkerWidget":
        "displays an interactive orientation marker in a viewport corner.",
    "vtkBoxWidget": "provides an interactive box widget.",
    "vtkBoxWidget2": "provides an interactive box widget (version 2).",
    "vtkSphereWidget": "provides an interactive sphere widget.",
    "vtkPlaneWidget": "provides an interactive plane widget.",
    "vtkImplicitPlaneWidget2": "provides an interactive implicit plane widget.",
    "vtkSliderWidget": "provides an interactive slider widget.",
    "vtkSliderRepresentation2D": "2D slider representation.",
    "vtkBalloonWidget": "displays popup text near actors.",
    "vtkBalloonRepresentation": "defines balloon popup appearance.",
    "vtkTextWidget": "provides an interactive movable text widget.",
    "vtkTextRepresentation": "defines text widget appearance.",
    "vtkSplineWidget": "provides an interactive spline widget.",
    "vtkContourWidget": "provides an interactive contour/polyline widget.",
    "vtkOrientedGlyphContourRepresentation":
        "displays oriented glyphs along a contour.",
    "vtkScalarBarWidget": "provides an interactive scalar bar.",
    "vtkCameraOrientationWidget":
        "displays an interactive camera orientation indicator.",
    "vtkCompassWidget": "displays an interactive compass widget.",
    "vtkCompassRepresentation": "defines compass widget appearance.",
    "vtkLineWidget2": "provides an interactive line widget.",
    "vtkLineRepresentation": "defines line widget geometry.",
    # --- Charts ---
    "vtkChartXY": "creates a 2D X-Y chart.",
    "vtkPlotBar": "adds a bar plot to a chart.",
    "vtkPlotLine": "adds a line plot to a chart.",
    "vtkPlotPoints": "adds a scatter plot to a chart.",
    "vtkContextView": "displays 2D chart/context scenes.",
    "vtkContextScene": "manages 2D drawing items.",
    # --- Graph/info-vis ---
    "vtkMutableDirectedGraph": "builds a mutable directed graph.",
    "vtkMutableUndirectedGraph": "builds a mutable undirected graph.",
    "vtkTree": "represents a tree data structure.",
    "vtkGraphLayoutView": "displays a graph with layout and labels.",
    "vtkViewTheme": "applies a color theme to a view.",
    "vtkRandomGraphSource": "generates a random graph.",
    "vtkGraphToPolyData": "converts a graph to polydata.",
    "vtkTreeRingView": "displays a tree as nested rings.",
    "vtkTreeMapView": "displays a tree as a treemap.",
    "vtkRenderedGraphRepresentation": "graph rendering representation.",
    # --- Volume rendering ---
    "vtkVolume": "represents a volume in the scene.",
    "vtkSmartVolumeMapper": "selects the best volume mapper automatically.",
    "vtkGPUVolumeRayCastMapper": "GPU-based volume ray casting.",
    "vtkFixedPointVolumeRayCastMapper": "fixed-point volume ray casting.",
    "vtkPiecewiseFunction": "defines a piecewise-linear transfer function.",
    "vtkMultiBlockVolumeMapper": "renders multi-block volume data.",
    "vtkProjectedTetrahedraMapper": "renders unstructured grid volumes.",
    "vtkUnstructuredGridVolumeRayCastMapper":
        "ray-casts unstructured grid volumes.",
    # --- HyperTreeGrid ---
    "vtkHyperTreeGridSource": "generates a hyper tree grid.",
    "vtkHyperTreeGridGeometry": "extracts the outer surface of a hyper tree grid.",
    "vtkHyperTreeGridContour": "generates contours on a hyper tree grid.",
    "vtkHyperTreeGridThreshold": "thresholds cells of a hyper tree grid.",
    "vtkHyperTreeGridPlaneCutter": "cuts a hyper tree grid with a plane.",
    "vtkHyperTreeGridDepthLimiter": "limits the depth of a hyper tree grid.",
    "vtkHyperTreeGridAxisReflection": "reflects a hyper tree grid across an axis.",
    "vtkHyperTreeGridCellCenters": "generates points at hyper tree grid cell centers.",
    "vtkHyperTreeGridOutlineFilter": "generates the outline of a hyper tree grid.",
    "vtkHyperTreeGridGradient": "computes the gradient of a hyper tree grid.",
    # --- Misc ---
    "vtkAnnotatedCubeActor": "displays an annotated orientation cube.",
    "vtkCubeAxesActor": "draws labeled axes around a bounding box.",
    "vtkCornerAnnotation": "places text annotations in viewport corners.",
    "vtkArrayCalculator": "evaluates expressions on data arrays.",
    "vtkWindowToImageFilter": "captures a render window to an image.",
    "vtkLight": "defines a scene light source.",
    "vtkNamedColors": "provides named color lookup.",
}

LAUNCH_BULLET = (
    "- `Initialize()` and `Start()` launch the interactive visualization"
    " — `Initialize()` prepares the interactor and `Start()` begins the"
    " event loop."
)


def _conjugate(verb):
    """Conjugate an imperative verb to third-person singular.

    e.g. "Demonstrate" -> "demonstrates", "display" -> "displays",
         "Extract" -> "extracts", "Render" -> "renders"
    """
    low = verb.lower()
    if low.endswith('y') and len(low) > 2 and low[-2] not in 'aeiou':
        return low[:-1] + 'ies'
    elif low.endswith(('s', 'sh', 'ch', 'x', 'z')):
        return low + 'es'
    elif low.endswith('e'):
        return low + 's'
    else:
        return low + 's'


def _link(cls_name):
    """Return a markdown link for a VTK class."""
    return f"[{cls_name}]({VTK_DOC_BASE}{cls_name}.html)"


def extract_description_from_py(py_path):
    """Extract the description from the .py file header comments."""
    lines = py_path.read_text().splitlines()
    desc_lines = []
    started = False
    for line in lines[1:]:  # skip shebang
        stripped = line.strip()
        if stripped.startswith('#') and not stripped.startswith('#!'):
            text = stripped.lstrip('# ').strip()
            if text.startswith('Factory overrides') or text.startswith('VTK pipeline classes'):
                break
            if text:
                desc_lines.append(text)
                started = True
        elif started and stripped == '':
            break
        elif started:
            break
        elif stripped == '':
            continue
    return ' '.join(desc_lines) if desc_lines else ''


def extract_vtk_imports(py_path):
    """Extract all VTK class names imported in the .py file."""
    text = py_path.read_text()
    classes = set()
    for match in re.finditer(r'from\s+vtkmodules\.\S+\s+import\s+\(([^)]+)\)', text, re.DOTALL):
        for name in re.findall(r'\b(vtk[A-Z]\w+)', match.group(1)):
            classes.add(name)
    for match in re.finditer(r'from\s+vtkmodules\.\S+\s+import\s+([^(\n]+)', text):
        for name in re.findall(r'\b(vtk[A-Z]\w+)', match.group(1)):
            classes.add(name)
    return sorted(classes)


def extract_stage_comments(py_path):
    """Extract '# Stage: description' comments from the .py file.

    Returns a dict mapping VTK class names to their inline descriptions,
    derived from the comment that immediately precedes their first use.
    """
    text = py_path.read_text()
    lines = text.splitlines()
    stage_descs = {}  # class_name -> description from comment
    current_comment = None

    for line in lines:
        stripped = line.strip()
        # Capture "# StageName: description" comments
        m = re.match(r'^#\s*[\w\s]+:\s+(.+)$', stripped)
        if m:
            current_comment = m.group(1).strip()
            continue
        # If the next code line instantiates a VTK class, associate the comment
        m2 = re.match(r'^\w+\s*=\s*(vtk[A-Z]\w+)\(\)', stripped)
        if m2 and current_comment:
            cls = m2.group(1)
            if cls not in stage_descs:
                stage_descs[cls] = current_comment
            current_comment = None
        elif stripped and not stripped.startswith('#'):
            current_comment = None

    return stage_descs


def read_existing_md(md_path):
    """Read existing .md and extract description, pipeline, and per-class bullets."""
    if not md_path.exists():
        return None, None, {}
    text = md_path.read_text()
    lines = text.splitlines()

    desc = ''
    pipeline = ''
    bullets = {}  # class_name -> full bullet text

    # Description
    in_desc = False
    for line in lines:
        if line.strip() == '### Description':
            in_desc = True
            continue
        if in_desc:
            if line.strip() == '':
                if desc:
                    break
                continue
            desc += line.strip() + ' '

    # Pipeline arrow
    for line in lines:
        if line.strip().startswith('**') and '→' in line:
            pipeline = line.strip()
            break

    # Per-class bullets
    for line in lines:
        stripped = line.strip()
        m = re.match(r'^- \[(vtk[A-Z]\w+)\]', stripped)
        if m:
            bullets[m.group(1)] = stripped

    return desc.strip(), pipeline, bullets


def has_interactor_start(py_path):
    """Check if the .py uses interactor.Initialize()/Start()."""
    text = py_path.read_text()
    return bool(re.search(r'\.Initialize\(\)', text) and re.search(r'\.Start\(\)', text))


def generate_md(py_path, md_path):
    """Generate a complete .md file from the .py file and existing .md (if any)."""
    # Extract info from .py
    py_desc = extract_description_from_py(py_path)
    vtk_classes = extract_vtk_imports(py_path)
    stage_descs = extract_stage_comments(py_path)
    uses_start = has_interactor_start(py_path)

    # Read existing .md for reuse
    existing_desc, existing_pipeline, existing_bullets = read_existing_md(md_path)

    # --- Description ---
    desc = existing_desc or py_desc
    if not desc:
        desc = f"This example demonstrates {py_path.stem}."
    # Ensure starts with "This example"
    if not desc.startswith("This example"):
        # Conjugate the first word (imperative verb) and prepend "This example"
        # e.g. "Demonstrate VTK..." -> "This example demonstrates VTK..."
        # e.g. "Extract and display..." -> "This example extracts and displays..."
        words = desc.split()
        if words:
            # Conjugate all leading verbs connected by 'and'/'or'
            new_words = []
            i = 0
            while i < len(words):
                w = words[i]
                # Only conjugate words that look like imperative verbs
                # (start with uppercase letter, are pure alpha, and aren't
                # acronyms like VTK or class names like vtkFoo)
                is_verb = (w[0].isupper() and w.isalpha()
                           and not w.isupper() and not w.startswith('vtk'))
                if i == 0 and is_verb:
                    new_words.append(_conjugate(w))
                    i += 1
                elif i > 0 and w.lower() in ('and', 'or'):
                    new_words.append(w)
                    i += 1
                    # Conjugate the word after 'and'/'or' if it's a verb
                    if i < len(words):
                        nw = words[i]
                        nw_is_verb = (nw[0].islower() and nw.isalpha()
                                      and not nw.startswith('vtk'))
                        if nw_is_verb:
                            new_words.append(_conjugate(nw))
                        else:
                            new_words.append(nw)
                        i += 1
                else:
                    new_words.extend(words[i:])
                    break
            desc = "This example " + ' '.join(new_words)
        else:
            desc = "This example " + desc

    # --- Pipeline arrow ---
    pipeline = existing_pipeline or ''

    # --- Bullets ---
    # Standard rendering tail classes (in order)
    TAIL_CLASSES = ['vtkRenderer', 'vtkRenderWindow', 'vtkRenderWindowInteractor']

    # Build bullet for each class
    bullet_lines = []
    # Non-tail classes first (in import order)
    for cls in vtk_classes:
        if cls in TAIL_CLASSES:
            continue
        bullet = _build_bullet(cls, existing_bullets, stage_descs)
        bullet_lines.append(bullet)

    # Tail classes in standard order
    for cls in TAIL_CLASSES:
        if cls in vtk_classes:
            bullet = _build_bullet(cls, existing_bullets, stage_descs)
            bullet_lines.append(bullet)

    # Launch bullet — only for standard rendering pipeline (not graph views)
    py_text = py_path.read_text()
    is_graph_view = 'GraphLayoutView' in py_text or 'vtkViewTheme' in py_text
    if uses_start and not is_graph_view:
        bullet_lines.append(LAUNCH_BULLET)

    # --- Assemble ---
    parts = ['### Description', '', desc, '']
    if pipeline:
        parts.append(pipeline)
        parts.append('')
    for b in bullet_lines:
        parts.append(b)
    parts.append('')  # trailing newline

    return '\n'.join(parts)


def _build_bullet(cls, existing_bullets, stage_descs):
    """Build a single bullet line for a VTK class.

    Priority:
      1. Existing bullet from the current .md (preserves hand-written prose)
      2. Known class description from KNOWN_CLASS_BULLETS
      3. Description from the .py stage comment
      4. Simple fallback
    """
    # 1. Reuse existing bullet if it has good phrasing
    if cls in existing_bullets:
        bullet = existing_bullets[cls]
        # Fix known phrasing issues
        if cls == 'vtkRenderWindow' and 'in a window on screen' not in bullet:
            bullet = f"- {_link(cls)} displays the rendered scene in a window on screen."
        if cls == 'vtkRenderWindowInteractor' and 'captures mouse and keyboard' not in bullet:
            bullet = f"- {_link(cls)} captures mouse and keyboard events."
        if cls == 'vtkActor' and 'to the scene' not in bullet:
            bullet = bullet.rstrip('.')
            if bullet.endswith('assigns the mapped geometry'):
                bullet += ' to the scene.'
            else:
                bullet += '.'
        return bullet

    # 2. Known class description
    if cls in KNOWN_CLASS_BULLETS:
        return f"- {_link(cls)} {KNOWN_CLASS_BULLETS[cls]}"

    # 3. Stage comment from .py
    if cls in stage_descs:
        desc = stage_descs[cls]
        # lowercase first char if needed
        if desc[0].isupper() and not desc.startswith('VTK'):
            desc = desc[0].lower() + desc[1:]
        if not desc.endswith('.'):
            desc += '.'
        return f"- {_link(cls)} {desc}"

    # 4. Fallback
    # Try to make a human-readable name from the class
    name = cls.replace('vtk', '', 1)
    # Insert spaces before capitals
    readable = re.sub(r'([a-z])([A-Z])', r'\1 \2', name).lower()
    return f"- {_link(cls)} provides {readable} functionality."


def check_md_standard(md_path, py_path):
    """Check if an .md file meets the Arrow.md standard. Returns list of issues."""
    issues = []

    if not md_path.exists():
        issues.append("MISSING: .md file does not exist")
        return issues

    text = md_path.read_text()
    lines = text.splitlines()

    if not any(l.strip() == '### Description' for l in lines):
        issues.append("Missing '### Description' heading")
    if not any(l.strip().startswith('**') and '→' in l for l in lines):
        issues.append("Missing pipeline arrow notation")
    if any(l.strip() == '### VTK Classes' for l in lines):
        issues.append("Has old '### VTK Classes' heading")
    if any('Pipeline classes:' in l for l in lines):
        issues.append("Has old 'Pipeline classes:' header")

    if py_path.exists():
        vtk_classes = extract_vtk_imports(py_path)
        for cls in vtk_classes:
            if cls not in text:
                issues.append(f"Missing class: {cls}")

    uses_start = has_interactor_start(py_path) if py_path.exists() else False
    has_launch = any('launch' in l.lower() for l in lines)
    is_graph_view = False
    if py_path.exists():
        py_text = py_path.read_text()
        is_graph_view = 'GraphLayoutView' in py_text or 'vtkViewTheme' in py_text
    if uses_start and not has_launch and not is_graph_view:
        issues.append("Missing Initialize()/Start() bullet")

    has_window_ok = any('vtkRenderWindow' in l and 'in a window on screen' in l for l in lines)
    has_interactor_ok = any('vtkRenderWindowInteractor' in l and 'captures mouse and keyboard' in l for l in lines)
    if any('vtkRenderWindow]' in l for l in lines) and not has_window_ok:
        issues.append("vtkRenderWindow bullet missing standard phrasing")
    if any('vtkRenderWindowInteractor]' in l for l in lines) and not has_interactor_ok:
        issues.append("vtkRenderWindowInteractor bullet missing standard phrasing")

    return issues


def main():
    src = Path('src/Python')
    if not src.exists():
        print("Run from the project root", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1] if len(sys.argv) > 1 else 'audit'
    dry_run = '--dry' in sys.argv

    if mode == 'audit':
        total = 0
        with_issues = 0
        by_category = {}
        for cat_dir in sorted(src.iterdir()):
            if not cat_dir.is_dir():
                continue
            for md in sorted(cat_dir.glob('*.md')):
                py = md.with_suffix('.py')
                total += 1
                issues = check_md_standard(md, py)
                if issues:
                    with_issues += 1
                    by_category.setdefault(cat_dir.name, []).append((md.name, issues))

        print(f"\nAudit: {total} .md files, {with_issues} with issues\n")
        for cat, entries in sorted(by_category.items()):
            print(f"=== {cat} ({len(entries)} files) ===")
            for name, issues in entries:
                for iss in issues:
                    print(f"  {Path(name).stem}: {iss}")
            print()

    elif mode == 'generate':
        generated = 0
        skipped = 0
        for cat_dir in sorted(src.iterdir()):
            if not cat_dir.is_dir():
                continue
            for md in sorted(cat_dir.glob('*.md')):
                py = md.with_suffix('.py')
                if not py.exists():
                    skipped += 1
                    continue

                new_content = generate_md(py, md)
                old_content = md.read_text() if md.exists() else ''

                if new_content.rstrip() != old_content.rstrip():
                    generated += 1
                    if dry_run:
                        print(f"\n{'='*60}")
                        print(f"WOULD WRITE: {md}")
                        print(f"{'='*60}")
                        print(new_content)
                    else:
                        md.write_text(new_content)
                        print(f"  Updated: {md}")
                else:
                    if dry_run:
                        print(f"  Unchanged: {md}")

        action = "Would update" if dry_run else "Updated"
        print(f"\n{action} {generated} files, skipped {skipped} (no .py)")

    else:
        print(f"Unknown mode: {mode}. Use 'audit' or 'generate'.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
