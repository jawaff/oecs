# OECS (Opinionated Entity-Component-System)

This framework provides a complete solution for making entity-component-system based games -- 2d games are the main focus. 
The chosen ECS implementation is heavily object oriented and kind of breaks some of the traditional ECS rules.
Other ECS implementations seem to have the components in a dictionary with the component type as a key.
In this implementation, the components choose a unique name and are stored within an Entity class -- it doesn't have to be subclassed. 
This allows an entity to potentially have many components of the same type. Systems are thus able to target a component type -- resulting in a list of components potentially --
or a particular component based on its unique name.
Despite it being unconventional, this framework is also integrated with a particular multi-media library and collision library -- PySFML and PyMunk.
They're both terrific object oriented libraries that synergize with this framework very well. By integrating with these libraries, this framework 
is able to offer more utilities.

## Rendering

PySFML is the chosen multi-media library because it has an object oriented architecture. This allows
us to store meshes, sounds, textures, 2d shapes and etc in a component. 

## Physics

PyMunk is the chosen physics library because it has an object oriented architecture. This allows us to store
collision shapes, constraints, spaces and etc in a component.