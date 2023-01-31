import random


def get_random_dir_contents():
    possible_files = [
        {
            "name": "example1",
            "type": "file",
            "size": "10KB",
            "modified": "10/30/22 12:23pm",
            "owner": "root",
        },
        {
            "name": "example2",
            "type": "file",
            "size": "20KB",
            "modified": "10/30/22 2:00pm",
            "owner": "root",
        },
        {
            "name": "example3",
            "type": "file",
            "size": "30KB",
            "modified": "10/30/22 3:00pm",
            "owner": "root",
        },
        {
            "name": "a big file",
            "type": "file",
            "size": "10MB",
            "modified": "10/31/22 10:00pm",
            "owner": "root",
        },
        {
            "name": "foo",
            "type": "file",
            "size": "1MB",
            "modified": "10/29/22 4:00pm",
            "owner": "root",
        },
        {
            "name": "bar",
            "type": "file",
            "size": "1MB",
            "modified": "10/29/22 4:00pm",
            "owner": "root",
        },
        {
            "name": "One",
            "type": "folder",
            "size": "--",
            "modified": "10/29/22 4:00pm",
            "owner": "root",
        },
        {
            "name": "Two",
            "type": "folder",
            "size": "--",
            "modified": "10/29/22 4:00pm",
            "owner": "root",
        },
    ]
    return random.sample(possible_files, k=5)


def get_dir_contents(dir_name):
    print("get items in", dir_name)
    return get_random_dir_contents()


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
