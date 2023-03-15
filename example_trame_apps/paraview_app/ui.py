from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify
from trame.widgets import paraview
from trame.app import get_server

from trame_pvui.widgets.infopanel import InfoPanel
from trame_pvui.widgets.filebrowser import FileBrowser
from trame_pvui.widgets.serverbrowser import ServerBrowser

server = get_server()
state, ctrl = server.state, server.controller


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
                    vuetify.VTab(children=["Info Panel"])
                    vuetify.VTab(children=["File browser"])
                    vuetify.VTab(children=["Server browser"])
                with vuetify.VTabsItems(v_model=("tab", 0)):
                    with vuetify.VTabItem():
                        InfoPanel(
                            selected_node=("selected_node",),
                            file_properties=("file_properties",),
                            data_grouping=("data_grouping",),
                            data_statistics=("data_statistics",),
                            data_arrays=("data_arrays",),
                            timesteps=("timesteps",),
                            set_selected_node="selected_node = $event",
                        )
                    with vuetify.VTabItem():
                        FileBrowser(
                            current_local_dir=("current_local_dir",),
                            current_remote_dir=("current_remote_dir",),
                            current_local_dir_contents=("current_local_dir_contents",),
                            current_remote_dir_contents=(
                                "current_remote_dir_contents",
                            ),
                            local_hierarchy=("local_hierarchy",),
                            remote_hierarchy=("remote_hierarchy",),
                            file_types=("file_types",),
                            set_local_dir="current_local_dir = $event",
                            set_remote_dir="current_remote_dir = $event",
                            mode="Save",
                            submit=ctrl.save_file,
                            byte_formatter=("utils.fmt.bytes",),
                            date_formatter=(
                                "(m)=> new Date(m *1000).toLocaleString()",
                            ),
                        )
                        FileBrowser(
                            current_local_dir=("current_local_dir",),
                            current_remote_dir=("current_remote_dir",),
                            current_local_dir_contents=("current_local_dir_contents",),
                            current_remote_dir_contents=(
                                "current_remote_dir_contents",
                            ),
                            local_hierarchy=("local_hierarchy",),
                            remote_hierarchy=("remote_hierarchy",),
                            set_local_dir="current_local_dir = $event",
                            set_remote_dir="current_remote_dir = $event",
                            mode="Open",
                            submit=ctrl.open_file,
                            byte_formatter=("utils.fmt.bytes",),
                            date_formatter=("(m)=> new Date(m*1000).toLocaleString()",),
                        )
                    with vuetify.VTabItem():
                        ServerBrowser(
                            servers=("servers",),
                            add=ctrl.add_server,
                            update=ctrl.update_server,
                        )

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                html_view = paraview.VtkRemoteView(ctrl.get_render_window())
                ctrl.on_server_ready.add(html_view.update)
                ctrl.view_update = html_view.update

        # Footer
        layout.footer.hide()
