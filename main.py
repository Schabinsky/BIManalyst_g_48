from pathlib import Path
import ifcopenshell
import ifcopenshell.util.element

#Filename (.ifc assumed)
modelname = "25-08-D-ARCH"

#Load ifc model
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

# Import funktion
from rules import SpaceRequirement
from A3 import A3_kladde


# A1
# Check (model, room type (string), required amount(integer))
# spaceresult = SpaceRequirement.check_space_requirement(model, 'Meeting room', 12)
# There is currently no return, only a print statement in the function.


# A3
Area_sum = A3_kladde.total_area_and_number(model)
print(Area_sum)

space_type = A3_kladde.get_area_by_space_types(model)
print(space_type)