# Component Abaqus def file prototype


## Abaqus model definition rules

Certain assumptions are made by the reader with respect to how the Abaqus model is defined.
These assumptions are necessary to facilitate the preprocessing, and reduce the number of inputs required by the user.
Processing of the input file may fail if the rules are not followed.

Rules:
- Continuum nodes are defined in Part coordinates so that the strong axis is aligned with the x-axis, and the member centerline is aligned with the z-axis.
- Beam nodes are defined in Part coordinates so that the line-of-centroids is aligned with the x-axis.
- The cross-section is constant along the length.
- All continuum domains within a component have the same orientation.
- It is assumed that all nodes within a node set use the same `*System` definition.


## Component definition file rules

Component definition files are used in conjunction with Abaqus input files to create the internal `Structure` representation.
`Structure`s are composed of one or more `Component`s, each `Component` is composed of:
- A `Section`
- A beam domain (may be empty)
- A continuum domain (may be empty)
- `Imperfection`s
- `Coupling`s between beam and continuum domains
Note that the internal structure allows for translation between different software formats (e.g., LS-DYNA, ANSYS, NASTRAN) as long as the necessary readers and writers exist.
At the moment, readers and writers only exist for Abaqus, thus this document is currently specific to that format.

Rules for defining the cdef (*c*omponent *def*inition) files are established, and then a prototype is given.
In terms of an Abaqus model, `Component`s are defined as node sets, and additional information such as the cross-section geometry and imperfection properties are also defined.
Several examples of cdef files can be found in the `run_files` directory.

Rules:
- `*Section`s must be defined before `*Component`s.
- All the lines that follow a `*Component` line up-to the next `*Component` or `*EndDef` line define its properties.
- The file must end with `*EndDef` (and possibly empty lines afterwards).
- If `is_RBS` is specified, the RBS is assumed to happen only on the end near the origin of the component.

The prototype for the .def file is:
'''
*ISection, name=<section_id>
<d>, <bf>, <tf>, <tw>

*Component, name=<component_id>, section=<section_id>
*BeamNodes
<beam_nset_1>, <beam_nset_2>, ...
<beam_nset_...>
*ContinuumNodes
<Continuum_nset_1>, <Continuum_nset_2>, ...
<Continuum_nset_...>
*Coupling, jtype=<jtype>
<beam_nset_id>, <continuum_nset_id>
*Imperfection, wave_length_factor=1., num_of_waves=1, twist_scale=1., local_scale=1., straight_scale=1., is_RBS=False, RBS_offset=0.

*EndDef
'''


## Tips:
Here are some tips to help:
- It is easiest if all the nodes in a part are defined in a single node set, then they can be easily used to define the beam/continuum domains for a given component

