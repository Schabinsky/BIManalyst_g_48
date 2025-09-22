import ifcopenshell
import ifcopenshell.util.element

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
