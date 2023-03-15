from pathlib import Path
from datetime import datetime
from pwd import getpwuid


def get_file_size_string(num_bytes):
    size_units = ["GB", "MB", "kB", "bytes"]
    for i, suffix in enumerate(size_units):
        exponent = len(size_units) - 1 - i
        divisor = 1024**exponent
        if num_bytes > divisor:
            return f"{round(num_bytes / divisor)} {suffix}"


def get_dir_tree_as_list(root_dir):
    ret = [str(p.absolute()) for p in Path(root_dir).rglob("*") if p.is_dir()]
    ret.append(str(root_dir.absolute()))
    return ret


def get_dir_contents(dir_name):
    ret = []
    for p in Path(dir_name).glob("*"):
        stats = p.stat()
        filename = p.name
        filetype = "folder" if p.is_dir() else f'{filename.split(".")[-1].upper()} file'
        size = get_file_size_string(stats.st_size) if filetype != "folder" else "--"
        modified = datetime.fromtimestamp(stats.st_mtime).strftime("%m/%d/%Y, %H:%M:%S")
        owner = getpwuid(stats.st_uid).pw_name

        ret.append(
            {
                "name": filename,
                "type": filetype,
                "size": size,
                "modified": modified,
                "owner": owner,
                "full_path": str(p.absolute()),
            }
        )
    return ret


def get_initial_state(local_root, remote_root):
    local_root = Path(local_root).absolute()
    remote_root = Path(remote_root).absolute()
    return {
        "local_directories": get_dir_tree_as_list(local_root),
        "remote_directories": get_dir_tree_as_list(remote_root),
        "current_local_dir_contents": get_dir_contents(local_root),
        "current_remote_dir_contents": get_dir_contents(remote_root),
        "current_local_dir": str(local_root),
        "current_remote_dir": str(remote_root),
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
