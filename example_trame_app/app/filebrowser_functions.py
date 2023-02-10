from pathlib import Path
from datetime import datetime
from pwd import getpwuid


local_root_dir = Path(".").absolute()


def get_file_size_string(num_bytes):
    size_units = ["GB", "MB", "kB", "bytes"]
    for i, suffix in enumerate(size_units):
        exponent = len(size_units) - 1 - i
        divisor = 1024**exponent
        if num_bytes > divisor:
            return f"{num_bytes / divisor} {suffix}"


def get_dir_tree_as_list(root_dir):
    return [str(p) for p in Path(root_dir).rglob("*") if p.is_dir()]


def get_dir_contents(dir_name):
    ret = []
    for p in Path(dir_name).glob("*"):
        stats = p.stat()
        filename = str(p).split("/")[-1]
        filetype = "folder" if p.is_dir() else f'{filename.split(".")[-1].upper()} file'
        size = get_file_size_string(stats.st_size)
        modified = datetime.fromtimestamp(stats.st_mtime).strftime("%m/%d/%Y, %H:%M:%S")
        owner = getpwuid(stats.st_uid).pw_name

        ret += [
            {
                "name": filename,
                "type": filetype,
                "size": size,
                "modified": modified,
                "owner": owner,
            }
        ]
    return ret


def get_initial_state():
    return {
        "local_directories": get_dir_tree_as_list(local_root_dir),
        "remote_directories": ["remote_host:/root"],
        "current_local_dir_contents": get_dir_contents(local_root_dir),
        "current_remote_dir_contents": [],
        "current_local_dir": str(local_root_dir),
        "current_remote_dir": "remote_host:/root",
    }


def get_applicable_file_types():
    return [
        {
            "value": ".vtpd",
            "text": "VTK PartitionedDataSetCollection File (*.vtpd)",
        },
    ]


def save_file(file_info):
    print("save", file_info)


def open_file(file_info):
    print("open", file_info)
