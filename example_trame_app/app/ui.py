from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify
from trame.widgets import vtk
from trame.app import get_server

from colormapper.widget import ColormapEditor
from filebrowser.widget import FileBrowser

server = get_server()
state, ctrl = server.state, server.controller


# @zach add a tab here


def initialize(server):
    ctrl = server.controller

    with SinglePageWithDrawerLayout(server) as layout:
        layout.title.set_text("Trame Widget Tester")

        with layout.toolbar:
            vuetify.VSpacer()
            vuetify.VSwitch(
                v_model="$vuetify.theme.dark",
                hide_details=True,
                label="Dark Mode",
                dense=True,
            )

        with layout.drawer as drawer:
            drawer.width = 450
            with vuetify.VContainer(classes="pa-5"):
                with vuetify.VTabs(grow=True, v_model=("tab", 0)):
                    vuetify.VTab(children=["Color mapper"])
                    vuetify.VTab(children=["File browser"])
                with vuetify.VTabsItems(v_model=("tab", 0)):
                    with vuetify.VTabItem():
                        ColormapEditor(
                            histogram_data=("histogram_data",),
                            colors=("colormap_points",),
                            opacities=("opacity_points",),
                            update_colors="colormap_points = $event",
                            update_opacities="opacity_points = $event",
                        )
                    with vuetify.VTabItem():
                        FileBrowser(
                            current_local_dir=("current_local_dir",),
                            current_remote_dir=("current_remote_dir",),
                            current_local_dir_contents=("current_local_dir_contents",),
                            current_remote_dir_contents=(
                                "current_remote_dir_contents",
                            ),
                            local_directories=("local_directories",),
                            remote_directories=("remote_directories",),
                            file_types=("file_types",),
                            set_local_dir="current_local_dir = $event",
                            set_remote_dir="current_remote_dir = $event",
                            mode="Save",
                            submit=ctrl.save_file,
                        )
                        FileBrowser(
                            current_local_dir=("current_local_dir",),
                            current_remote_dir=("current_remote_dir",),
                            current_local_dir_contents=("current_local_dir_contents",),
                            current_remote_dir_contents=(
                                "current_remote_dir_contents",
                            ),
                            local_directories=("local_directories",),
                            remote_directories=("remote_directories",),
                            set_local_dir="current_local_dir = $event",
                            set_remote_dir="current_remote_dir = $event",
                            mode="Open",
                            submit=ctrl.open_file,
                        )

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                html_view = vtk.VtkRemoteView(ctrl.get_render_window())
                ctrl.on_server_ready.add(html_view.update)
                ctrl.view_update = html_view.update

        # Footer
        layout.footer.hide()
