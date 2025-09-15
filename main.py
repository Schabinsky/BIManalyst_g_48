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
spaces = model.by_type("IfcSpace")
meeting_rooms = []

for space in spaces:
    # print('{} - {}'.format(space.Name, space.LongName))
    if space.LongName == 'Meeting room':
        meeting_rooms.append(int(space.Name))
    else:
        continue
print(meeting_rooms)

# PROBLEM: index bliver forkert i koden herunder fordi spaces i spaces listen starter ved 65 og ikke 0. 
# Find anden måde at hente de rigtige rooms fra den lange liste spaces.

for room in meeting_rooms:
    # print(spaces[room+1])
    qtos = ifcopenshell.util.element.get_psets(spaces[room+1], qtos_only=True)
    print('The area for Meeting room: ' + str(spaces[room+1].Name) + ' is ' + str(qtos['Qto_SpaceBaseQuantities']['NetFloorArea']))

# Hvor mange spaces er der?
# Hvilke af disse spaces er har label 'Meeting Room'?
# Hvor store er disse spaces?
