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