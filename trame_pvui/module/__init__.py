from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__pvui": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__pvui/pvui.umd.min.js"]

# List of CSS files to load (usually from the serve path above)
styles = ["__pvui/pvui.css"]

vuetify_config = {
    "icons": {
        "values": {
            "pqEditColor": {"component": "pq-edit-color"},
            "pqEditScalarBar": {"component": "pq-edit-scalar-bar"},
            "pqFavorites": {"component": "pq-favorites"},
            "pqResetRange": {"component": "pq-reset-range"},
            "pqResetRangeCustom": {"component": "pq-reset-range-custom"},
            "pqResetRangeTemporal": {"component": "pq-reset-range-temporal"},
            "pqScalarBar": {"component": "pq-scalar-bar"},
            "pqSeparateColorMap": {"component": "pq-separate-color-map"},
        }
    }
}

# List of Vue plugins to install/load
vue_use = ["pvui", ("trame_vuetify", vuetify_config)]

# Uncomment to add entries to the shared state
# state = {}


# Optional if you want to execute custom initialization at module load
def setup(app, **kwargs):
    """Method called at initialization with possibly some custom keyword arguments"""
    pass
