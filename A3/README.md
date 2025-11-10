# A3: Tool

Group 48, BUILD Analyst

## About the tool

Group 48 has developed a simple tool that, for a given ifc architectural model, returns a list of area types, areas and total areas, including floor area occupied by walls.

The aim of the tool is to serve as a convenient way to check whether certain area targets are met, such as '3000 sqm of office area', or a '500 sqm lobby' etc, or simply to check on how the area is distributed on rooms, hallways and so on.

All the tool needs to run is a loaded ifc model. When run, the output data will be saved as a local .json file.

## Advanced Building Design

This tool can be used as soon as areas have been defined in a BIM model, which roughly translates into stage B, but can also be used for documentation in stages C and D.

The tool should be useful to:
- ARCH as a form of self-monitoring,  
- MEP for ventilation calculations and
- PM as a way to document area compliance.

### Necessary information:

In order for the program to run optimally, the .ifc model must meet the following criteria:
- All floor areas are defined and named. (IfcSpace)
- All interior and exterior walls include 'Interior' or 'Exterior' in the name. (IfcWall)
- Dimensions are documented in specific quantity sets ({'Length'(mm), 'NetSideArea'(m2), 'NetVolume'(m3)} in 'Qto_WallBaseQuantities' & {'NetFloorArea'} in 'Qto_SpaceBaseQuantities'). This should be the case by default.

### Known issues:

- some special characters (e.g. é) will be output as a typecode (e.g. \u00e9)

## Tutorial

### Prerequisites
For the tool to function correctly, the IFC model must include the following information:

- **Spaces**
  - Must be of type *IfcSpace*.
  - Must contain *NetFloorArea* in the quantity set *Qto_SpaceBaseQuantities*.

- **Walls**
  - Must be of type *IfcWall*.
  - The *Name* or *ObjectType* must include either *interior* or *exterior*.
  - Must contain *Length*, *NetSideArea*, and *NetVolume* in the quantity set *Qto_WallBaseQuantities*.

### How to Use the Tool
1. Load your IFC model.  
2. Import the tool from the project folder.  
3. Run the tool.  
4. Open the generated JSON file to view the results.

### The Tool

**Importing the tool**

```python
from A3_Tool import output_to_json
```

**Using the tool**

```python
output = output_to_json(model)
```

Only the IFC model is required as input.

**Reading the output**

- The tool generates a JSON file containing the results in a dictionary format.  
- Open the JSON file to inspect the results.  