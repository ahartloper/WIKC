import numpy as np


class ICoupling:
    """ Warping-Inclusive Kinematic Coupling for I-shaped cross-sections. """

    def __init__(self, beam_node, continuum_nodes, use_nonlinear, include_warping):
        """ Constructor.
        :param dict beam_node: {int: [float, float]} Beam node in the coupling in local coords.
        :param dict continuum_nodes: {int: [float, float]} Continuum nodes in the coupling in local coords.
        :param bool use_nonlinear: If True, then nonlinear version of coupling used.
        :param bool include_warping: If True, then use warping-inclusive coupling.
        """
        self.beam_node = beam_node
        self.continuum_nodes = continuum_nodes
        self.use_nonlinear = use_nonlinear
        self.include_warping = include_warping

        self.warping_fun = self._compute_warping_fun()

    def _compute_warping_fun(self):
        """ Returns the warping function evaluated at each continuum node. """
        wfun = dict()
        for node_id, coords in self.continuum_nodes.items():
            wfun[node_id] = coords[0] * coords[1]
        return wfun


class CoordSys:
    """ Defines the local, right-handed coordinate system in R^3 for a component. """

    def __init__(self, point, basis):
        """ Constructor.
        :param np.ndarray point: (3, ) Origin of the coord sys wrt the global coord sys.
        :param np.ndarray n1: (3, 3) Matrix defining the local-to-global rotation.
        """
        self.pt = point
        self.basis = basis


class ISection:
    """ Defines an I-shaped cross-section. """

    def __init__(self, name, d, bf, tf, tw):
        """ Constructor.
        :param str name: Identifier for cross-section.
        :param float d: Total depth.
        :param float bf: Total flange width.
        :param float tf: Flange thickness.
        :param float tw: Web thickness.
        """
        self.name = name
        self.d = d
        self.tf = tf
        self.tw = tw


class IComponent:
    """ Defines the origin, nodes, and couplings for a component with an I-shaped cross-section. """

    def __init__(self, component_id, section):
        """ Constructor.
        :param str component_id: Unique identifier for the component.
        :param ISection section: Defines the geometry of the cross-section.
        :param CoordSys coord_sys: Origin and orientation of the component.
        :param dict beam_nodes: {int: [float, float]} Defines all the beam nodes in local coords.
        :param dict continuum_nodes: {int: [float, float]} Defines all the continuum nodes in local coords.
        :param list couplings: [Coupling] Defines the couplings in the component.
        """
        self.id = component_id
        self.section = section

        self.beam_node_sets = list()
        self.continuum_node_sets = list()
        self.couplings_info = list()

        self.coord_sys = None
        self.beam_nodes = dict()
        self.continuum_nodes = dict()
        self.couplings = list()
