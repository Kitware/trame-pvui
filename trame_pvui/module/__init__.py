from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__trame_pvui": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__trame_pvui/vue-trame_pvui.umd.min.js"]

# List of CSS files to load (usually from the serve path above)
styles = ["__trame_pvui/vue-trame_pvui.css"]

vuetify_config = {}

# List of Vue plugins to install/load
vue_use = ["trame_pvui", ("trame_vuetify", vuetify_config)]

# Uncomment to add entries to the shared state
# state = {}


# Optional if you want to execute custom initialization at module load
def setup(app, **kwargs):
    """Method called at initialization with possibly some custom keyword arguments"""
    pass
