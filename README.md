# WIKC: Warping-Inclusive Kinematic Coupling

Component macro models are a method of reducing the computational effort of full continuum component finite element models, while maintaining their solution fidelity.
Macro models contain 1D beam-column (or beam) element domains and 2D/3D continuum elements.
Some coupling method is required to join these domains of differing kinematics - a warping-inclusive kinematic coupling (WIKC) is proposed in this repository for this purpose.
Including warping in the coupling formulation is particularly important for components subjected to primarily torsion, and components that are susceptible to elastic or inelastic lateral-torsional buckling.

This repository mainly contains two things: (1) the warping-inclusive kinematic coupling (WIKC) MPC user subroutine for Abaqus, and (2) a Python pre-processor for Abaqus models.
The WIKC user subroutine can be used in a valid Abaqus model to couple beam-column element and continuum element domains (i.e., shell or solid elements).
The pre-processor is useful to generate the necessary keywords to include in the input file for use of the user MPC subroutine.
The pre-processor also includes an imperfection module that can be used to generate local and member geometric imperfections.

Notes:
- The remainder of this README file provides instructions for how to obtain, install, and use the WIKC method in Abaqus analyses.
The WIKC method is general, and could be used in other finite element simulation platforms, however, this functionality has not yet been implemented.
- The WIKC method is currently only implemented for wide-flange (i.e., I-shaped) cross-sections.
The functionality can be extended for other functions given that the warping function can be computed at each continuum node.
- See reference [1] at the end for the theory of the coupling method, and some applications.

## Installation

Command-line instructions are provided to obtain and use the WIKC subroutine and the Python pre-processor.

1. Clone the WIKC repository

With `git` installed, open your command-line tool of choice (e.g., Command Prompt, Terminal, etc.) and enter:
```
git clone git@github.com:ahartloper/WIKC.git
```

2. Locate the WIKC subroutine

The Abaqus MPC user subroutine for the WIKC method is contained within the file `wikc/wikc_subroutine.for`.

3. Install the `pywikc` pre-processor

The `pywikc` pre-processor, including the imperfection generator, is specified as a Python package.
One way to install the package is to change the directory of your command-line tool to the `wikc` directory, and install using `pip`, e.g.:
```
cd wikc
pip install .
```

## Usage

### WIKC MPC user subroutine

The following are general instructions to use the WIKC in an Abaqus model.
Examples are provided in the `examples` directory.

0. Do not use parts in the model definition.

The pre-processor assumes that parts are not used in the input file.
This is because the pre-processor assumes that each node id is unique, whereas, this is not the case when parts are used.

1. Specify the user subroutine.

The WIKC MPC user subroutine needs to be included with the analysis.
In Abaqus/CAE:
```
Double-click on the associated Job > General tab > Locate the user subroutine file
```

2. Add the `*MPC` keyword definitions

See the Abaqus keyword manual for more information on the `*MPC` keyword.
For each continuum node, the following keyword needs to be specified:
```
*MPC, MODE=NODE, USER
<jtype>, <continuum node id>, <beam node id>
```
where `jtype` is the mode specification of the WIKC subroutine, `continuum node id` is the id number of a node in the continuum domain on the interface, and `beam node id` is the id number of the beam node on the interface.
The valid `jtype` entries are: 16 = linear, no warping; 17 = linear, warping; 26 = nonlinear, no warping; 27 = nonlinear, warping.

These keywords will need to be repeated many times, therefore, one job of the pre-processor is to generate all the `*MPC` keywords.
This will be discussed later.

3. Add the `*Amplitude` keywords

An amplitude is necessary because field variables are used later-on to supply certain information to the subroutine.
This amplitude is just immediately set to 1.0, and kept there for 1e6 units of analysis time (if the analysis exceeds this amount of time, then the upper limit can be modified).
The keyword entry is:
```
*Amplitude, name=warp_fun_amp
0.0, 1.0
1.E6, 1.0
```

Again, the generation of this is included in the pre-processor.

4. Add the `*Field` keywords for the warping function

The warping function is a cross-section dependent property.
More information is needed to compute the value of the warping function than is provided to the MPC subroutine.
For this reason, the values of the warping function are stored in a field variable at each continuum node.
By default, the warping function is stored in **field variable 1**.
Be aware of this if you are using field variables for other purposes.

The pre-processor can handle the computation of the warping function over the cross-section, and generates the `*Field` keywords.

5. Add the `*Field` keywords for the normal axis direction

Torsion warping occurs normal to the cross-section.
As with the warping function, not enough information is provided to the MPC subroutine to know the direction of the axis normal to the cross-section.
For this reason, the initial orientation of the normal axis needs to be provided for each coupling.
This is done by setting field variables for the beam nodes active in each coupling.

By default, the normals are stored in **field variables 2, 3, and 4**.
Field variable 2 contains the component in the x-axis, 3 the component in the y-axis, and 4 the component in the z-axis.
Be aware of this if you are using field variables for other purposes.

Again, the pre-processor can handle the computation of the normal directions for each coupling, and the generation of the `*Field` keywords.

6. (Optional) Add the `*Imperfection` keyword

If the imperfection pre-processor module is used, then the initial geometric imperfections can be specified by using the `*Imperfection` keyword.
The addition is:
```
*IMPERFECTION, input=<imperfection file>
```
where `imperfection file` is the path to the file that contains the nodal imperfections.
The imperfection file follows the definition
```
<node id>, <imp x>, <imp y>, <imp z>
```
where `node id` is the node, and `imp x/y/z` are the imperfections in the global coordinate system.
The use of the imperfection module requires that parts are **not** used in the model definition.

### `pywikc` pre-processor

The pre-processor requires two inputs: (1) the properly defined Abaqus input file, and (2) a component definition file.
The Abaqus input file must be "properly" defined because the pre-processor makes some assumptions regarding the part definitions.
Instructions for the component definition file are provided in the `docs/` directory.

The basic rules that need to be adhered to when making the Abaqus model are as follows:
- Beam section sketches should start at the origin (0, 0) and extend in the x-axis to (L, 0).
- Continuum section sketches should be centered at the origin (0, 0), the strong axis should be aligned with the x-axis, and the weak axis should be aligned with the y-axis.
- Beam and continuum domains are defined through node sets.
- The interface beam and continuum nodes are defined through node sets.

The component definition file is a plain text file that provides information regarding: the cross-section geometry, the beam and continuum domains, couplings, and imperfections.
Each definition file is related to an input file.
Together, these two files are used to generate an internal representation of the model in `pywikc` that can be used to output the Abaqus keywords and imperfection files.
See the `component_def.md` and `Example-CDef.md` files in the `docs/` directory for more information.

The `pywikc` package provides the following functions:
```
gen_aba_couples(input_file, definition_file, output_dir)
gen_aba_imperfections(input_file, definition_file, output_dir)
gen_aba_couples_imperfections(input_file, definition_file, output_dir)
```
where `gen_aba_couples` creates only the keyword file for using the WIKC subroutine, `gen_aba_imperfections` creates only the imperfection file, and `gen_aba_couples_imperfections` creates both files.
In all these functions, the `input_file` is the Abaqus .inp file, the `definition_file` is the component definition file, and the imperfection and keywords output will be written to files in `output_dir`.
See the `examples/` directory for how these functions can be used.

The `gen_aba_couples_imperfections` function generates two outputs: (1) an `MPC_Keywords.txt` file that contains all the keywords that need to be added to the input file, and (2) an `-Imp.txt` file that contains the nodal imperfections.
The keywords need to be copied into the input file.
One method is to directly modify the input file, and running a new job using this modified file.
Another method is to copy the additions into the Keyword editor for the model in Abaqus/CAE.
The keyword editor can be accessed by right-clicking on the model in Abaqus/CAE and selecting `Edit Keywords`.
The imperfections can likewise be integrated into the model using the `*Imperfection` keyword as noted above.

### A note on convergence

Bi-moments are the energy conjugate to warping in beam-column elements.
Therefore, including the warping degree of freedom (DOF) in the constraint formulation leads to residuals in DOF7 in Abaqus (DOF7 = warping degree of freedom).
Abaqus, oddly, treats DOF7 as a "force" quantity when testing for convergence based on the relative residual values.
The bi-moment, however, has a unit of force x length x length, therefore, a bi-moment residual that is completely inconsequential may have a "large" residual compared to force quantities because of this dimensional mismatch (i.e., force vs force x length x length).
In turn, this may affect the overall convergence of the model, especially if the time-averaged applied force is low (e.g., in first increment or first few increments).

One way of alleviating this convergence issue is to relax the tolerance on the relative force (displacement) residual using the "General Solution Controls".
**IF THIS METHOD IS USED, IT SHOULD ONLY BE DONE FOR THE FIRST INCREMENT**.
After the first increment, the tolerance should be set back to the desired level (e.g., the default of 0.5% or as dictated by the problem).
This could be done, for instance, by creating an extra step with the relaxed tolerance and applying a small fraction of the loads before proceeding to the target loading with the desired tolerance.


## Contributing

Bug fixes and contributions can be raised by opening a new issue in the WIKC repository.

## Authors

Code written and maintained by Alex Hartloper.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

- Dimitrios Lignos and Albano de Castro e Sousa for their invaluable input.

## References
[1] Hartloper A.R., de Castro e Sousa A., and Lignos D.G. (2022). "Warping-Inclusive Kinematic Coupling in Mixed-Dimension Macro Models for Wide Flange Beam-Columns", Journal of Structural Engineering. DOI: 10.1061/(ASCE)ST.1943-541X.0003211.
