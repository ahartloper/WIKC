# Component Abaqus def file prototype

Rules:
- Sections must be defined before Components.
- Continuum nodes in the .inp file are defined so that the strong axis is aligned with the x-axis, and the member centerline is aligned with the z-axis
- Beam nodes in the .inp file are defined so that the line-of-centroids is aligned with the x-axis.
- The cross-section is assumed to be constant along the length.
- All continuum domains within a component have the same orientation.

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
'''
