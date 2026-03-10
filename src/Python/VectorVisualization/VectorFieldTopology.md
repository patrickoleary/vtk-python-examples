### Description

This example computes the topology of a 3D vector field using vtkVectorFieldTopology. Critical points, separating lines, separating surfaces, and boundary switch features are extracted from a vector field **v = (x+z, y, x-z)** defined on a wavelet image data via vtkArrayCalculator. It follows the VTK pipeline structure:

**RTAnalyticSource → ArrayCalculator → VectorFieldTopology → DataSetMapper → Actor → Renderer → Window → Interactor**

- [vtkActor](https://www.vtk.org/doc/nightly/html/classvtkActor.html) assigns the mapped geometry to the scene. Six actors show the bounding box, critical points, separating lines, separating surfaces, boundary switch lines, and boundary switch surfaces.
- [vtkArrayCalculator](https://www.vtk.org/doc/nightly/html/classvtkArrayCalculator.html) defines the vector field from coordinate variables using `iHat`, `jHat`, `kHat` notation.
- [vtkDataSetMapper](https://www.vtk.org/doc/nightly/html/classvtkDataSetMapper.html) maps the dataset to graphics primitives.
- [vtkRTAnalyticSource](https://www.vtk.org/doc/nightly/html/classvtkRTAnalyticSource.html) generates a wavelet image data as the computational domain.
- [vtkRenderer](https://www.vtk.org/doc/nightly/html/classvtkRenderer.html) assembles the scene and configures the camera.
- [vtkRenderWindow](https://www.vtk.org/doc/nightly/html/classvtkRenderWindow.html) displays the rendered scene in a window on screen.
- [vtkRenderWindowInteractor](https://www.vtk.org/doc/nightly/html/classvtkRenderWindowInteractor.html) captures mouse and keyboard events.
- [vtkVectorFieldTopology](https://www.vtk.org/doc/nightly/html/classvtkVectorFieldTopology.html) computes topological features of a vector field. Output port 0 produces critical points, port 1 separating lines, port 2 separating surfaces, port 3 boundary switch lines, and port 4 boundary switch surfaces. `SetComputeSurfaces(True)` enables surface computation and `SetUseIterativeSeeding(True)` improves critical point detection.
- `Initialize()` and `Start()` launch the interactive visualization — `Initialize()` prepares the interactor and `Start()` begins the event loop.
