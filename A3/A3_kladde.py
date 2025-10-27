import ifcopenshell
import ifcopenshell.util.element
import numpy as np

def total_area_and_number(model):
    spaces = model.by_type("IfcSpace")
    Area_sum = []

    for space in spaces:
        qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
        sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
        Area_sum.append(sqrm)
    return len(Area_sum), round(sum(Area_sum),2)

def get_area_by_space_types(model):
    spaces = model.by_type("IfcSpace")
    space_list = []
    area_by_type = {}

    for space in spaces:
        space_list.append(space.LongName)

    space_types = list(dict.fromkeys(space_list))

    for type in space_types:
        area_by_type[type] = []
        for space in spaces:
            if space.LongName == type:
                qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
                sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
                area_by_type[type].append(sqrm)
            else:
                continue
        area_by_type[type] = round(sum(area_by_type[type]),2)
    return area_by_type



