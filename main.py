from pathlib import Path
import ifcopenshell

modelname = "25-08-D-STR"

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
def element_count(model, entityName, ifcClass):
    print("{} = {}".format(entityName,len(model.by_type(ifcClass))))

# Test if everything works:
spaces = model.by_type("IfcSpace")
for space in spaces:
    print(space.LongName)

# Get eleveations from each model
element_count(model, 'Floors', 'ifcBuildingStorey')
element_count(model, 'Beams', 'ifcBeam')
element_count(model, 'Special Walls', 'ifcWall')
element_count(model, 'Curtain Walls', 'ifcCurtainWall')
element_count(model, 'Stairs', 'ifcStair')
element_count(model, 'Doors', 'ifcDoor')
element_count(model, 'Slabs', 'ifcSlab')
