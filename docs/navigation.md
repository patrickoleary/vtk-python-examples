# Navigation Guide

![Home page](/vtk-python-examples/home.png)

Welcome to the VTK Python Examples collection. This site is designed to help you discover visualization techniques, learn common VTK patterns, and reuse working code snippets in your own applications.

Each example demonstrates a specific concept or class within VTK and includes a rendered visualization, a short explanation of the pipeline used, the input data required, and the full Python source code.

You can explore the examples in three ways:

- **Spiral Graph**: A visual representation of all examples in the collection. Hover over an example to see a preview of the visualization. Click on an example to go to the example page.

- **Browse Gallery**: Visually explore examples using preview images.

- **View Examples**: Navigate examples organized by VTK topic or module.

Start with the **Gallery** if you want inspiration, or jump directly to the categorized **Examples** list if you are looking for a specific technique.

## Gallery

![Gallery page](/vtk-python-examples/gallery.png)

The Gallery provides a visual overview of all available examples. Each card shows the output produced by an example along with its name and category.

Use the gallery to quickly scan visualization styles and techniques.

You can:

- **Search** examples by name using the search field.

- **Filter** by category to focus on a particular domain (e.g., meshes, filters, IO, plotting).

- **Filter** by VTK class to find examples that use a specific component.

Click any card to open the **detailed example page**.

## Examples

![Examples page](/vtk-python-examples/examples.png)

The Examples section organizes all examples by topic to make them easier to discover.

The left sidebar groups **examples into categories** such as:

- Annotation
- Arrays
- Composite Data
- Data Manipulation
- Image Processing
- Meshes
- Rendering
- Plotting

Select a category to expand it and browse related examples. Clicking an example name opens its **detailed example page** where you can view the visualization, read about the pipeline, and inspect the source code.

In the center column, you can see all **examples organized in a table per category**. The table shows an image in the first column with a example page line and a description in the second column.

The right sidebar provides quick access to **category sections**.

## Example Page

Each example page contains several sections that explain how the visualization works and how to reproduce it.

### Header

![Example header](/vtk-python-examples/example-head.png)

**(1)** The left sidebar groups **examples into categories**. **(2)** In the center column, the **header** shows the **name of the example** and **a rendered image of the visualization** it produces. This preview lets you quickly understand the goal of the example before examining the implementation. **(3)** The right sidebar provides quick access to **example sections**.

Use this view to visually confirm that the example demonstrates the technique you are interested in.

### Description

![Example description](/vtk-python-examples/example-description.png)

The **Description** section explains what the example demonstrates and outlines the visualization pipeline used to generate the result.

This section typically includes:

- **(1)** A short explanation of the visualization task.
- **(2)** A high-level pipeline overview showing how VTK objects connect.
- **(3)** A list describing the role of each major VTK class used.

Reading this section helps you understand the conceptual workflow before examining the code.

### Data

![Example data](/vtk-python-examples/example-data.png)

Some examples require input data files. The **(1) Data** section lists these files and provides links so you can download them.

These datasets are typically small samples used to demonstrate visualization techniques. Place the files in the same directory as the example script, or update the file paths in the code if necessary.

### Python Code

![Example Python code](/vtk-python-examples/example-python-code.png)

The **(1) Python Code** section contains the complete script used to generate the visualization.

You can copy this code directly into your own environment to reproduce the result. The script demonstrates how the VTK pipeline objects are created, configured, and connected.

Use this section to:

- Learn how the VTK classes interact
- Adapt the pipeline to your own datasets
- Experiment with visualization parameters

### Footer

![Example footer](/vtk-python-examples/example-footer.png)

At the bottom of each example page you will find navigation links to the **(1) previous** and **(2) next** examples. These links allow you to easily move through related examples without returning to the main list.

This makes it convenient to explore a sequence of visualization techniques and discover new VTK capabilities as you browse.
