# NeuroNote

## Description:

This is a regular note taking app with a different approach of taking notes in the form of nodes or as I'd like to call it Neuron. Each neuron holds
a piece of information and one neuron can be connected with another neuron through links and give the whole thing a UI to make it look like an
evidence board from a detective movie.

## Stack

- Frontend (UI): Python + PyQt (for the graphical user interface)
- Backend: C++ (for performance-heavy processing)
- Interfacing: Pybind11 (to connect Python and C++)
- Storage: SQLite / Markdown files (for saving notes)
- Rendering: Markdown2, MathJax (for text and LaTeX support)
- Visualization: Graph-based connections (like an evidence board)

## Approach

First the user get's to create a directory which will be called brain. Inside each brain, there will be files inside that folder each representing a neuron.
Each neuron can be linked with multiple other neurons. Each will have attribute like neuron id, id' of other files that are linked to it and
neuron content (only text for now).
