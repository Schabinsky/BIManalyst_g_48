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

# Check (model, room type (string), required amount(integer))
spaceresult = SpaceRequirement.check_space_requirement(model, 'Meeting room', 12)