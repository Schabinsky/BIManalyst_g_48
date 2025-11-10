from pathlib import Path
import ifcopenshell
import ifcopenshell.util.element

modelname = "25-08-D-ARCH"

try:
    dir_path = Path(__file__).parent
    model_url = Path.joinpath(dir_path, 'model', modelname).with_suffix('.ifc')
    model = ifcopenshell.open(model_url)
except OSError:
    try:
        import bpy
        model_url = Path.joinpath(Path(bpy.context.space_data.text.filepath).parent, 'model', modelname).with_suffix('.ifc')
        model = ifcopenshell.open(model_url)
    except OSError:
        print(f"ERROR: please check your model folder : {model_url} does not exist")

# Your script goes here
def check_meeting_room_requirement(model):
    spaces = model.by_type("IfcSpace")
    for space in spaces:
        # print('{} - {}'.format(space.Name, space.LongName))
        if space.LongName == 'Meeting room':
            qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
            sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
            print(f'The area for Meeting room {space.Name} is {sqrm:.1f} m2')
        else:
            continue

check_meeting_room_requirement(model)

# Hvor mange spaces er der?
# Hvilke af disse spaces er har label 'Meeting Room'?
# Hvor store er disse spaces?

spaces = model.by_type("IfcSpace")
meeting_room = []
meeting_room_no = []
room_no = -1

for space in spaces:
    # print('{} - {}'.format(space.Name, space.LongName))
    if space.LongName == 'Meeting room':
        meeting_room_no.append(room_no)
        meeting_room.append(int(space.Name))
        room_no = room_no + 1
    else:
        room_no = room_no + 1
        continue
print(meeting_room)

# PROBLEM: index bliver forkert i koden herunder fordi spaces i spaces listen starter ved 65 og ikke 0. 
# Find anden måde at hente de rigtige rooms fra den lange liste spaces.
# Found a way ;-)
meeting_areas = []

for room in meeting_room_no:
    # print(spaces[room+1])
    qtos = ifcopenshell.util.element.get_psets(spaces[room+1], qtos_only=True)
    print('The area for Meeting room: ' + str(spaces[room+1].Name) + ' is ' + str(qtos['Qto_SpaceBaseQuantities']['NetFloorArea']))
    meeting_areas.append(str(qtos['Qto_SpaceBaseQuantities']['NetFloorArea']))

# Hvor mange spaces er der?

# Hvilke af disse spaces er har label 'Meeting Room'?
print('A total of ' + str(len(meeting_room)) + ' meeting rooms are present in the model')


def check_meeting_room_requirement_ver2(model, requirement_nam, requirement_num):
    spaces = model.by_type("IfcSpace")
    meeting_room = []

    for space in spaces:
        # print('{} - {}'.format(space.Name, space.LongName))
        if space.LongName == requirement_nam:
            meeting_room.append(int(space.Name))
            qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
            sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
            # print(f'The area for Meeting room {space.Name} is {sqrm:.1f} m2')
        else:
            continue
    if len(meeting_room) == requirement_num:
        print(f'The requirement of {requirement_nam} = {requirement_num} is fulfilled')
    elif len(meeting_room) > requirement_num:
        print(f'There are more {requirement_nam} then the required {requirement_num}')
    elif len(meeting_room) < requirement_num:
        print(f'There are less {requirement_nam} then the required {requirement_num}')

check_meeting_room_requirement_ver2(model, 'Meeting room', 15)

def check_meeting_room_requirement(model):
    spaces = model.by_type("IfcSpace")
    meeting_room = []

    for space in spaces:
        if space.LongName == 'Meeting room':
            meeting_room.append(int(space.Name))
            qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
            sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
            print(f'The area for Meeting room {space.Name} is {sqrm:.1f} m2')
        else:
            continue
    print('A total of ' + str(len(meeting_room)) + ' meeting rooms are present in the model')

def check_space_requirement(model, requirement_nam, requirement_num):
    spaces = model.by_type("IfcSpace")
    meeting_room = []

    for space in spaces:
        if space.LongName == requirement_nam:
            meeting_room.append(int(space.Name))
            qtos = ifcopenshell.util.element.get_psets(space, qtos_only=True)
            sqrm = qtos['Qto_SpaceBaseQuantities']['NetFloorArea']
        else:
            continue
    if len(meeting_room) == requirement_num:
        print(f'The requirement of {requirement_nam} = {requirement_num} is fulfilled')
    elif len(meeting_room) > requirement_num:
        print(f'There are {len(meeting_room)} {requirement_nam} in the model which is more than the required {requirement_num}')
    elif len(meeting_room) < requirement_num:
        print(f'There are {len(meeting_room)} {requirement_nam} in the model which is less than the required {requirement_num}')

check_space_requirement(model, 'Meeting room', 15)


def get_all_space_types(model):
    spaces = model.by_type("IfcSpace")
    space_list = []

    for space in spaces:
        space_list.append(space.LongName)
    return list(dict.fromkeys(space_list))

def walls_area(model):
    walls = model.by_type("IfcWall")
    int_wall_lengths = []
    int_wall_widths = []
    ext_wall_lengths = []
    ext_wall_widths = []

    for wall in walls:
        wall_type = wall.ObjectType
        if wall_type and "Interior".lower() in wall_type.lower():
            qtos = ifcopenshell.util.element.get_psets(wall, qtos_only=True)
            psets = ifcopenshell.util.element.get_psets(wall, qtos_only=False)
            if 'Qto_WallBaseQuantities' in qtos and 'Construction' in psets:
                int_length = qtos['Qto_WallBaseQuantities'].get('Length',0)
                int_width = psets['Construction'].get('Width',0)
                int_wall_lengths.append(float(int_length))
                int_wall_widths.append(float(int_width))
        if wall_type and "Exterior".lower() in wall_type.lower():    
            qtos = ifcopenshell.util.element.get_psets(wall, qtos_only=True)
            psets = ifcopenshell.util.element.get_psets(wall, qtos_only=False)
            if 'Qto_WallBaseQuantities' in qtos and 'Construction' in psets:
                ext_length = qtos['Qto_WallBaseQuantities'].get('Length',0)
                ext_width = psets['Construction'].get('Width',0)
                ext_wall_lengths.append(float(ext_length))
                ext_wall_widths.append(float(ext_width))

    interior_walls_summed_area = round(sum(int_length * int_width for int_length, int_width in zip(int_wall_lengths, int_wall_widths))*10**-6, 1)
    exterior_walls_summed_area = round(sum(ext_length * ext_width for ext_length, ext_width in zip(ext_wall_lengths, ext_wall_widths))*10**-6, 1)

    return interior_walls_summed_area, exterior_walls_summed_area

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

def read_csv(model):
    # Define all informations from other functions
    spaces_area = get_area_by_space_types(model)
    total_area_number_of_spaces = total_area_and_number(model)
    walls_area_int = interior_walls_area(model)
    walls_area_ext = exterior_walls_area(model)
    curtainwalls_area = curtain_walls_area(model)
    gross_floor_area = round(total_area_number_of_spaces[0] + walls_area_int + walls_area_ext + curtainwalls_area, 2)

    # Create a dictionary with the informations
    output_data = {
        "Area of spaces": spaces_area,
        "Total area and number of spaces": total_area_number_of_spaces,
        "Area of interior walls": walls_area_int,
        "Area of exterior walls": walls_area_ext,
        "Area of curtain walls": curtainwalls_area,
        "Gross Floor Area": gross_floor_area
    }

    # File path setup
    folder_1 = "ADV_BIM"
    folder_2 = "A3"
    filename = "Prisdata.csv"
    file_path = os.path.join(folder_1, folder_2, filename)

    pris_values = []
    with open(file_path, mode='r', encoding='utf-8', newline='') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            pris_str = row['Pris'].strip().replace('.', '').replace(',', '.')
            if pris_str:  # Only convert if string is not empty
                try:
                    pris_values.append(float(pris_str))
                except ValueError:
                    # Handle rows where conversion fails
                    pris_values.append(0.0)  # or skip, or log error
            else:
                # Handle empty string case
                pris_values.append(0.0)  # or skip, or log error
    pris_values = round(sum(pris_values),2)

    return pris_values