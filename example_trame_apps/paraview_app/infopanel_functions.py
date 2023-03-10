# DataInformationMicroservice example
# version 0.2
#
# to run
# <ParaView 5.11 directory>/bin/pvpython ReaderExample.py
# if extra python packages are need create a virtual enviroemnt using python 3.9  and pass it throut --venv
# e.g
# $ python3.9 -m venv env39
# $ ./env39/bin/activate
# $ pip install ..
# $ deactivate
# $ <ParaView 5.11 directory>/bin/pvpython ReaderExample.py --venv env39


# Available in PV >= 5.10
import paraview.web.venv  # noqa
from paraview import simple
from paraview.modules.vtkRemotingCore import vtkPVDataInformation
from vtk import vtkIndent


class DataInformationMicroservice:
    def __init__(self):
        self.DataInformation = vtkPVDataInformation()
        self.Proxy = None

    def SetProxy(self, proxy):
        self.Proxy = proxy

    def UpdateDataInformation(self, time=0.0, selectorPath=None, assemblyName=None):
        assert self.Proxy is not None
        self.Proxy.UpdatePipeline(time)

        self.DataInformation.Initialize()
        self.DataInformation.SetPortNumber(0)
        if selectorPath is not None:
            self.DataInformation.SetSubsetSelector(selectorPath)
            if assemblyName is None:
                self.DataInformation.SetSubsetAssemblyNameToHierarchy()
            else:
                self.DataInformation.SetSubsetAssemblyName(assemblyName)

        self.Proxy.GatherInformation(self.DataInformation)

    def GetDataInformation(self):
        return self.DataInformation

    def GetTimeSteps(self):
        assert self.Proxy is not None
        timesteps = []
        prop = self.Proxy.GetProperty("TimestepValues")
        if prop:
            for i in range(prop.GetNumberOfElements()):
                timesteps.append(prop.GetElement(i))
        return timesteps


def DataAssemplyToDict(assemply):
    """simple serialization of assemply to python dictionary"""
    nodes = []
    children = [assemply.GetRootNode()]
    while len(children) > 0:
        id = children[0]
        name = assemply.GetNodeName(id)
        node_children = assemply.GetChildNodes(id)
        path = assemply.GetNodePath(id)
        d = {"id": id, "name": name, "path": path, "children": node_children}
        # use assemply.GetAttribute/GetAttributeOrDefault to get more XML attributes of a node
        nodes.append(d)
        del children[0]
        children += node_children

    return nodes


path = "data/can.ex2"
# path = "./bake.e"
if __name__ == "__main__":
    data_info_microservice = DataInformationMicroservice()
    proxy = simple.OpenDataFile(path)

    data_info_microservice.SetProxy(proxy)
    data_info_microservice.UpdateDataInformation()
    dataInfo = data_info_microservice.GetDataInformation()

    # return type is vtkPVDataInformation
    # for all available methods see
    # https://kitware.github.io/paraview-docs/latest/cxx/classvtkPVDataInformation.html

    print("---Data Grouping--")
    # return type is vtkDataAssemply for both cases, for full API see
    # https://vtk.org/doc/nightly/html/classvtkDataAssembly.html
    hierarchy = dataInfo.GetHierarchy()
    print(hierarchy.SerializeToXML(vtkIndent()))
    print(DataAssemplyToDict(hierarchy))

    print("---Data Statistics-----")
    print("Type :", dataInfo.GetPrettyDataTypeString())
    print("# of datasets :", dataInfo.GetNumberOfDataSets())
    print("# cells", dataInfo.GetNumberOfCells())
    print("# points", dataInfo.GetNumberOfPoints())
    print("Current Time", dataInfo.GetTime())
    print("# Timesteps", dataInfo.GetNumberOfTimeSteps())
    print("# time range", dataInfo.GetTimeRange())
    print("Memory ", dataInfo.GetMemorySize())
    print("Bounds", dataInfo.GetBounds())
    # if data is Image we need also extends for example open headsq.vti from example dataset in ParaView
    # print("Extends",dataInfo.GetExtends())

    print(" ---- Data Arrays -----------")
    # the return type is a vtkPVDataSetAttributesInfromation class for documentation see
    # https://kitware.github.io/paraview-docs/latest/cxx/classvtkPVDataSetAttributesInformation.html
    pointInfo = dataInfo.GetPointDataInformation()
    # print(pointInfo)
    for i in range(pointInfo.GetNumberOfArrays()):
        array = pointInfo.GetArrayInformation(i)
        print(
            array.GetName(),
            "\t",
            array.GetDataTypeAsString(),
            array.GetRangesAsString(),
            f"IsPartial -> {array.GetIsPartial()}",
        )  # if you want actual numbers use GetNumberOfComponents(), and GetComponentRange(idx) -> [double,double]

    cellInfo = dataInfo.GetCellDataInformation()
    for i in range(cellInfo.GetNumberOfArrays()):
        array = cellInfo.GetArrayInformation(i)
        print(
            array.GetName(),
            "\t",
            array.GetDataTypeAsString(),
            array.GetRangesAsString(),
            f"IsPartial -> {array.GetIsPartial()}",
        )

    fieldInfo = dataInfo.GetFieldDataInformation()
    for i in range(fieldInfo.GetNumberOfArrays()):
        array = fieldInfo.GetArrayInformation(i)
        print(
            array.GetName(),
            "\t",
            array.GetDataTypeAsString(),
            array.GetRangesAsString(),
            f"IsPartial -> {array.GetIsPartial()}",
        )

    print(" ---- Time -----------")
    print("Available Time steps", data_info_microservice.GetTimeSteps())

    # when a node is selected dataInformation reflects the selected node
    print("----------------None Selection Example------------")
    data_info_microservice.UpdateDataInformation(selectorPath="/Root/block_1")
    dataInfo = data_info_microservice.GetDataInformation()
    print(dataInfo.GetPrettyDataTypeString())
    print(dataInfo.GetNumberOfPoints())
    print(dataInfo.GetNumberOfCells())

    # update time to second timestep
    print("----------------Second timestep------------")
    data_info_microservice.UpdateDataInformation(
        time=data_info_microservice.GetTimeSteps()[1]
    )
    dataInfo = data_info_microservice.GetDataInformation()
    print("Current Time", dataInfo.GetTime())
    print(dataInfo.GetTime())
    # array values are now updated
    pointInfo = dataInfo.GetPointDataInformation()
    # print(pointInfo)
    for i in range(pointInfo.GetNumberOfArrays()):
        array = pointInfo.GetArrayInformation(i)
        print(
            array.GetName(),
            "\t",
            array.GetDataTypeAsString(),
            array.GetRangesAsString(),
            f"IsPartial -> {array.GetIsPartial()}",
        )  # if you want actual numbers use GetNumberOfComponents(), and GetComponentRange(idx) -> [double,double]
