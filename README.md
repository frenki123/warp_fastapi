# Warp FastApi Documentation - DEV BRENCH

## Introduction

Warp-FastApi is a versatile Python library that serves as your navigational beacon through the intricate cosmos of FastAPI development. The library's core feature is the generation of well-structured, efficient code tailored to FastAPI, SQLAlchemy, and Pydantic. This means you can focus on crafting your application's unique logic, secure in the knowledge that the foundational code is expertly generated. Begin your FastAPI project with Warp-FastApi, where exploration and efficiency converge.

## Installation

Begin your journey by installing Warp-FastApi using pip:

```bash
pip install warp-fastapi
```

## Getting Started

Prepare for liftoff into the Warp-FastApi universe by following these simple steps:

### **Beam Up Your Crew:** 

Assemble the core components of Warp-FastApi.

```
from warp_fastapi import AppObject, Attribute, AppProject
from warp_fastapi.sqlalch_types import string_type, int_type, date_only_type
from warp_fastapi.relationships import one_to_many, one_to_one, many_to_many, many_to_one
from warp_fastapi.create_project import ProjectCreator
```

### **Warp-Define Attributes:**
```
# Engage attributes
a1 = Attribute("planet_name", string_type)
a2 = Attribute("distance", int_type)
name = Attribute("ship_name", string_type)
```
Define attributes with the precision of a star cartographer – each attribute corresponds to a specific celestial aspect. For more attribute types, refer to the SQL Types and Types documentation.

### **Launch Your App Spaceships:**
```
# Launch app spaceships
planet = AppObject("planet", a1, a2)
starship = AppObject("starship", name)
```
Initiate AppObjects, the very vessels of your application – give them designations, program their functional cores (attributes), and propel them into the coding cosmos!

You can also establish an AppObject with attributes directly:
```
alien = AppObject("alien", 
                Attribute("name", string_type), 
                Attribute("species", string_type), 
                Attribute("status", string_type, optional=True))
gadget = AppObject("gadget", 
                Attribute("name", string_type))
```
And don't forget to pack the optional "status" attribute for those unpredictable extraterrestrial encounters.

### **Navigate the Star Systems – Add Starship Relations:**
```
planet.add_relationship(starship, one_to_many, "inhabited_by", "planet")
starship.add_relationship(alien, one_to_many, "crew", "starship")
```
Much like celestial systems gravitate towards one another, your app objects require meaningful connections. Forge these connections by signaling the objects, inputting coordinates, and assigning distinctive identifiers.

The add_relationship function follows this structure:
```
main_obj.add_realtionship(related_object, <side_of_main_obj>_to_<side_of_related_object> (eg. many_to_one), name_of_rel_in_main_obj, name_of_rel_in_related_object
```
Potential relationship types encompass:

- one_to_one: A one-to-one relationship, present in both the main and related objects.
- one_to_many: A one-to-many relationship, with the main object as one and the related object as many. This configures the main object to hold a list of related objects. The foreign key is situated in the related object (typically the "many" side).
- many_to_one: The reverse of one_to_many, resulting in the main object as many and the related object as one. The related object is equipped with a list of main objects.
- many_to_many: A mutual relationship where both objects feature lists of the other. This intricate linkage is managed through an association table in SQLAlchemy.


### **Commence Warp Drive:** 
```
# Set coordinates – AppObjects ready for warp
project = AppProject("galactic_app", planet, starship, alien, gadget)

# Engage the ProjectCreator, the command bridge of coding
creator = ProjectCreator(project, project_dir=".")
creator.create_project()  # Or use creator.update_project() for warp upgrades
```

### **Explore New Discovery:**

In your shell go to the folder where your code was generated (folder "galactic_app" inside your curent working folder). You need to run startup script which will create virutal enviroment, install requirments, refactor code with black and ruff, run pytest and mypy check, create initial database migration with alembic and run your app.

Run the startup script from bash command line (use gitbash or linuxbash).

```bash
source startup.sh
```

You can go on and open your project at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). Also check input in your shell to see coverage of the tests and passing of the mypy lint test.

## Conclusion

Warp-FastApi: Embark on a voyage of FastAPI exploration, akin to the most exhilarating space odysseys. Bid farewell to repetitive code warp cores and allow Warp-FastApi to be your steadfast warp drive. Set your course now and let your code traverse new frontiers!