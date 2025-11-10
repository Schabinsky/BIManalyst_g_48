import ifcopenshell
import ifcopenshell.util.element
import numpy as np
import json

def total_area_and_number(model):
    spaces = model.by_type("IfcSpace")
    Area_sum = []

    for space in spaces:
        qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
        sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
        Area_sum.append(sqrm)
    return round(sum(Area_sum), 1), len(Area_sum)

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
    wall_lengths = []
    wall_widths = []

    for wall in walls:
        wall_type = wall.ObjectType
        wall_name = wall.Name
        if wall_type and "Interior".lower() in wall_type.lower() or wall_name and "Interior".lower() in wall_name.lower():
            qtos = ifcopenshell.util.element.get_psets(wall, qtos_only=True)
            psets = ifcopenshell.util.element.get_psets(wall, qtos_only=False)
            if 'Qto_WallBaseQuantities' in qtos and 'Construction' in psets:
                length = qtos['Qto_WallBaseQuantities'].get('Length',0)
                width = psets['Construction'].get('Width',0)
                wall_lengths.append(float(length))
                wall_widths.append(float(width))

    interior_walls_summed_area = round(sum(length * width for length, width in zip(wall_lengths, wall_widths))*10**-6, 1)

    return interior_walls_summed_area

def exterior_walls_area(model):
    walls = model.by_type("IfcWall")
    wall_lengths = []
    wall_widths = []

    for wall in walls:
        wall_type = wall.ObjectType
        wall_name = wall.Name
        if wall_type and "Exterior".lower() in wall_type.lower() or wall_name and "Exterior".lower() in wall_name.lower():
            qtos = ifcopenshell.util.element.get_psets(wall, qtos_only=True)
            psets = ifcopenshell.util.element.get_psets(wall, qtos_only=False)
            if 'Qto_WallBaseQuantities' in qtos and 'Construction' in psets:
                length = qtos['Qto_WallBaseQuantities'].get('Length',0)
                width = psets['Construction'].get('Width',0)
                wall_lengths.append(float(length))
                wall_widths.append(float(width))

    exterior_walls_summed_area = round(sum(length * width for length, width in zip(wall_lengths, wall_widths))*10**-6, 1)

    return exterior_walls_summed_area

def output_to_json(model):
    spaces_area = get_area_by_space_types(model)
    total_area_number_of_spaces = total_area_and_number(model)
    walls_area_int = interior_walls_area(model)
    walls_area_ext = exterior_walls_area(model)

    output_data = {
        "Area of spaces": spaces_area,
        "Total area and number of spaces": total_area_number_of_spaces,
        "Area of interior walls": walls_area_int,
        "Area of exterior walls": walls_area_ext
    }

    with open("output.json", "w") as json_file:
        json.dump(output_data, json_file, indent=4)


    




