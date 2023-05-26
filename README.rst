Trame Paraview UI widgets
===========================================================

Trame widgets which may be used in the Paraview user interface (Pvui)

License
-----------------------------------------------------------

Apache Software License


Features
-----------------------------------------------------------

This package includes the following widgets:

 - Colormapper
 - FileBrowser
 - ServerBrowser
 - InfoPanel


Installing
-----------------------------------------------------------
Build and install the Vue components:

.. code-block:: console

    cd vue-components
    npm i
    npm run build
    cd -


Getting Started
-----------------------------------------------------------

Paraview >= 5.11 is a prerequisite to running this application.
Go to https://www.paraview.org/download/ for more information.
Once Paraview is installed, take note of its file path.

You will also need a python virtual environment
with this application and its requirements installed

.. code-block:: console

    python3.9 -m venv ~/venvs/trame
    source ~/venvs/trame/bin/activate
    pip install -e .
    deactivate


Running the example apps
-----------------------------------------------------------

To run the example paraview app, use the following

.. code-block:: console

    [path_to_paraview]/bin/pvpython example_trame_apps/paraview_app/main.py --venv ~/venvs/trame


To run the example vtk app (which hosts the colormapper widget), use the following

.. code-block:: console

    python3 example_trame_apps/vtk_app/main.py


Contributing
-----------------------------------------------------------

see `CONTRIBUTING.rst`
