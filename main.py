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

# check_meeting_room_requirement(model)

def check_meeting_room_requirement_ver2(model, requirement_nam, requirement_num):
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

check_meeting_room_requirement_ver2(model, 'Meeting room', 15)
