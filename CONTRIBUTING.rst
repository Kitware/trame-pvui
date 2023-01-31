==========================
Contributing to Trame Pvui
==========================

#. Clone the repository using ``git clone``
#. Install pre-commit via ``pip install pre-commit``
#. Run ``pre-commit install`` to set up pre-commit hooks
#. Make changes to the code, and commit your changes to a separate branch
#. Create a fork of the repository on GitHub
#. Push your branch to your fork, and open a pull request


Getting started
###
Run the development server

.. code-block:: console

    cd vue-components
    npm run serve:[widget_name]

Where `widget_name` is one of [`colormapper`, `filebrowser`, `serverbrowser`].
To add a new option for `widget_name`, add a vue app file in `vue-components/src/tests`.
Make changes within `vue-components/src/components/[widget_name]`.
To make a Vue widget useable in trame, there must be a python file in `trame_pvui/widgets`.

Follow the same structure as other widget files in those locations.


Tips
####

#. When first creating a new project, it is helpful to run ``pre-commit run --all-files`` to ensure all files pass the pre-commit checks.
#. A quick way to fix ``black`` issues is by installing black (``pip install black``) and running the ``black`` command at the root of your repository.
#. Sometimes, ``black`` and ``flake8`` do not agree. Add options to your ``.flake8`` file to fix these things. See the `flake8 configuration docs <https://flake8.pycqa.org/en/latest/user/configuration.html>`_ for more details.
#. A quick way to fix ``codespell`` issues is by installing codespell (``pip install codespell``) and running the ``codespell -w`` command at the root of your directory.
#. The `.codespellrc file <https://github.com/codespell-project/codespell#using-a-config-file>`_ can be used fix any other codespell issues, such as ignoring certain files, directories, words, or regular expressions.
