# Example component definition file

This file contains an example component definition file, and explains each of the lines used in the file.
The structure in this example is an interior beam-to-column subassembly that consists of two beam components and a column component.
The finite element model represents the DBBW subassembly tested by Engelhardt et al. (1998).
A component macro model approach is used with the WIKC method to couple the beam-column and shell element domains.
Imperfections are applied to the RBS regions of the beams.

## Line-by-line explanation

A detailed, line-by-line explanation is provided first, afterwards, the entire file contents are given.

First the cross-sections of the beams (W36X150) and column (W14X398) are defined:
```
*ISection, name=w14x398
465., 442., 72.4, 45.0

*ISection, name=w36x150
912., 305., 23.9, 15.9
```
The lines starting with `*ISection` indicate that a new section is to be defined, and the following line is the `<d>`, `<bf>`, `<tf>`, and `<tw>` where d is the total depth, bf is the flange width, tf is the flange thickness, and tw is the web thickness.
The `name` parameter is used to link the sections and the components.

Next, components are defined using the `*Component` keyword.
The line
```
*Component, name=column-1, section=w14x398
```
specifies a new component with the `W14x398` cross-section defined above.
The lines
```
*BeamNodes
column-beam_dom-1_all_nodes, column-beam_dom-3_all_nodes
```
specify that the nodes in the node sets `column-beam_dom-1_all_nodes, column-beam_dom-3_all_nodes` belonging to elements in the beam-column element domain.
These node sets must be defined in the input file.
Similarly, the lines
```
*ContinuumNodes
column-1_all_nodes
```
defines nodes for the continuum element domain.

A coupling instance between the domains is specified through
```
*Coupling, jtype=27
column-beam_dom-3_bot_node, column-1_top_interf
```
where `jtype=<type>` indicates the coupling option, `column-beam_dom-3_bot_node` is the node set containing the beam node in the coupling, and `column-1_top_interf` is the node set containing the continuum nodes.
`type` options are: 16 = linear, no warping; 17 = linear, with warping; 26 = nonlinear, no warping; 27 = nonlinear, with warping.

The column component has two beam-column element domains, therefore, the second coupling is
```
*Coupling, jtype=27
column-beam_dom-1_top_node, column-1_bot_interf
```

Finally, the imperfections in the component are specified using the line
```
*Imperfection, wave_length_factor=1., num_of_waves=1, local_scale=0., straight_scale=0., twist_scale=0.
```
where:
- the total length of the local imperfection (L_bw) is `wave_length_factor` multiplied by the total section depth
- the number within this total length is `num_of_waves`
- the amplitude of the local imperfections is the base scaled by `local_scale`
- the amplitude of the out-of-straightness imperfection is the base scaled by `straight_scale`
- the amplitude of the twisting imperfection is is the base scaled by `twist_scale`

Other parameters include:
- is_RBS: if True, then only include a single instance of local imperfection in the component
- RBS_offset: the distance offset of the single local imperfection instance from the origin of the component

The base scale factors can be found in `src/imperfections/generate_imperfections.py`.
Note that the scale factors are set to zero in the example above for the column.
This means that no imperfections will be applied to the column component.

The definition of the beam components in the DBBW structure is similar to the column component.
The next section can be consulted for more information.
Finally, the file must end with the line
```
*EndDef
```
for proper processing.

## Complete definition

The complete contents are contained in this section.
The contents should be placed in a file named something like `dbbw-cdef.txt`, although no assumptions are made specifically with respect to the naming convention of the file itself.
This file just needs to be provided to the Abaqus component reader along with the input file.

```
*ISection, name=w14x398
465., 442., 72.4, 45.0

*ISection, name=w36x150
912., 305., 23.9, 15.9


*Component, name=column-1, section=w14x398
*BeamNodes
column-beam_dom-1_all_nodes, column-beam_dom-3_all_nodes
*ContinuumNodes
column-1_all_nodes
*Coupling, jtype=27
column-beam_dom-3_bot_node, column-1_top_interf
*Coupling, jtype=27
column-beam_dom-1_top_node, column-1_bot_interf
*Imperfection, wave_length_factor=1., num_of_waves=1, local_scale=0., straight_scale=0., twist_scale=0.

*Component, name=beam-1, section=w36x150
*BeamNodes
beam-beam_dom-2_all_nodes
*ContinuumNodes
beam-1_all_nodes
*Coupling, jtype=27
beam-beam_dom-2_interf_node, beam-1_beam_couple_interf
*Imperfection, wave_length_factor=0.752, num_of_waves=1, is_RBS=True, RBS_offset=228.6, local_scale=1., straight_scale=0., twist_scale=0.


*Component, name=beam-2, section=w36x150
*BeamNodes
beam-beam_dom-1_all_nodes
*ContinuumNodes
beam-2_all_nodes
*Coupling, jtype=26
beam-beam_dom-1_interf_node, beam-2_beam_couple_interf
*Imperfection, wave_length_factor=0.752, num_of_waves=1, is_RBS=True, RBS_offset=228.6, local_scale=-1., straight_scale=0., twist_scale=0.

*EndDef
```
