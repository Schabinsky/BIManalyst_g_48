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
    return len(Area_sum), round(sum(Area_sum), 1)

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


def interior_walls_area(model):
    walls = model.by_type("IfcWall")
    walls_object_type_list = []
    wall_lengths = []
    wall_widths = []

    for wall in walls:
        wall_type = wall.ObjectType
        if wall_type and "Interior".lower() in wall_type.lower():
            qtos = ifcopenshell.util.element.get_psets(wall, qtos_only=True)
            psets = ifcopenshell.util.element.get_psets(wall, qtos_only=False)
            if 'Qto_WallBaseQuantities' in qtos and 'Construction' in psets:
                length = qtos['Qto_WallBaseQuantities'].get('Length',0)
                width = psets['Construction'].get('Width',0)
                wall_lengths.append(float(length))
                wall_widths.append(float(width))

    interior_walls_summed_area = round(sum(length * width for length, width in zip(wall_lengths, wall_widths))*10**-6, 1)

    return interior_walls_summed_area