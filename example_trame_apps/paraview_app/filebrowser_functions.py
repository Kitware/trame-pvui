from pathlib import Path
from pwd import getpwuid


def get_dir_tree_as_list(root_dir):
    root_path = Path(root_dir)
    # this is the list used in the drop down populate with parents of root in increasing depth order
    ret = [str(root_path.absolute())]
    ret += [str(p) for p in root_path.parents]
    return ret


def get_dir_contents(dir_name):
    ret = []
    for p in Path(dir_name).glob("*"):
        stats = p.stat()
        filename = p.name
        filetype = "folder" if p.is_dir() else f'{filename.split(".")[-1].upper()} file'
        size = stats.st_size
        modification_time = stats.st_mtime
        owner = getpwuid(stats.st_uid).pw_name

        ret.append(
            {
                "name": filename,
                "type": filetype,
                "size": size,
                "modification_time": modification_time,
                "owner": owner,
                "full_path": str(p.absolute()),
            }
        )
    return ret


def get_initial_state(local_root, remote_root):
    local_root = Path(local_root).absolute()
    remote_root = Path(remote_root).absolute()
    return {
        "local_hierarchy": get_dir_tree_as_list(local_root),
        "remote_hierarchy": get_dir_tree_as_list(remote_root),
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
