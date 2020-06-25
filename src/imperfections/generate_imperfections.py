""" Functions to generate the imperfection geometries.

"""
import numpy as np
from .i_sec_imperfections import flange_imperfection, web_imperfection, straightness_imperfection, \
    twisting_imperfection, plumbness_imperfection


# -------------------------------------------------------------------------------------------------------------------- #


def set_imperfection_properties(component):
    """ Sets all the imperfection properties for the component.

    Properties dictionary contains:
    n1
    n2
    length
    num_waves
    total_wave_length
    flange_width
    web_depth
    delta_flange
    delta_web
    epsilon
    delta_global
    delta_plumbness
    theta_twist
    oos_axis
    oop_axis
    """

    # Constants
    WEB_FACTOR = 300.
    FLANGE_FACTOR = 250.
    STRAIGHT_FACTOR = 1500.
    TWIST_FACTOR = 0.6 / 100.

    def local_amplitudes(geom, dw_max, df_max):
        """ Calculate the flange and web imperfection amplitudes.

        :param float dw_max: max allowable web amplitude.
        :param float df_max: max allowable flange amplitude.
        :return list: [float] web and flange imperfection amplitudes.
        """
        # First try dw = dw_max
        dw = dw_max
        df = dw * geom.bf / 2. / ((geom.d - geom.tf) / 2.)

        # Then try df = df_max if not satisfied
        if df > df_max:
            df = df_max
            dw = df * ((geom.d - geom.tf) / 2.) / (geom.bf / 2.)
            print('Flange controlled imperfection amplitude. Web amp = {0:0.3f}, flange amp = {1:0.3f}'.format(dw, df))
        else:
            print('Web controlled imperfection amplitude. Web amp = {0:0.3f}, flange amp = {1:0.3f}'.format(dw, df))

        return [dw, df]

    # Start setting properties
    props = dict()
    props['n1'] = component.coord_sys.basis[:, 0]
    props['n2'] = component.coord_sys.basis[:, 1]
    # todo: need to compute the component length
    props['length'] = None
    # todo: num waves wavelength needs to be input
    props['num_waves'] = None
    props['total_wave_length'] = None
    props['flange_width'] = component.section.bf
    props['web_depth'] = component.section.d - 2. * component.section.tf
    # todo: other than constant, also for flange and web?
    props['epsilon'] = 0.2

    # Compute maximum amplitudes
    max_flange_amp = component.section.bf / FLANGE_FACTOR
    max_web_amp = component.section.d / WEB_FACTOR
    local_amps = local_amplitudes(geom, max_web_amp, max_flange_amp)
    props['delta_web'] = local_amps[0]
    props['delta_flange'] = local_amps[1]
    oos_amp = props['length'] / STRAIGHT_FACTOR
    props['delta_global'] = oos_amp
    oop_amp = props['length'] * 0.
    props['delta_plumbness'] = oop_amp
    props['theta_twist'] = TWIST_FACTOR
    props['oos_axis'] = component.coord_sys.basis[:, 0]
    props['oop_axis'] = component.coord_sys.basis[:, 0]

    component.imperfection_props = props
    pass


def generate_component_imp(component):
    """ Generates the imperfections for a component. """
    props = component.imperfection_props
    # Process the beam nodes
    for node_id, coords in component.beam_nodes.items():
        imp = np.array([0., 0., 0.])
        imp += i_straight_imp(coords, props)
        imp += i_plumb_imp(coords, props)
        component.node_imperfections[node_id] = imp
    # Process the continuum nodes
    for node_id, coords in component.continuum_nodes.items():
        imp = np.array([0., 0., 0.])
        imp += i_straight_imp(coords, props)
        imp += i_plumb_imp(coords, props)
        imp += i_local_imp(coords, props, is_top)
        imp += i_twist_imp(coords, props)
        component.node_imperfections[node_id] = imp
    pass


def i_local_imp(coord, props, is_top_seg):
    """ Returns the local flange/web imperfection.
    :param list coord: Node position in component coordinate system.
    :param dict props: Defines the properties of the imperfection.
    :param bool is_top_seg: If yes, the treat as top segment.
    """
    x = coord[0]
    y = coord[1]
    z = coord[2]
    # Check if top segment or bottom segment
    if is_top_seg:
        # Top segment z_mod starts at the top of the column and is positive in -z direction
        z_mod = props.length - z
        should_reverse = True
    else:
        z_mod = z
        should_reverse = False
    # Separate flange and web
    # todo: is seperating on x==0 the best condition? - is it necessary?
    x_tol = 1.e-8
    is_web_node = (abs(x) <= x_tol)
    if is_web_node:
        # Web node
        local_imp = web_imperfection(y, z_mod, should_reverse, **props)
    else:  # Flange node
        local_imp = flange_imperfection(x, y, z_mod, should_reverse, **props)
    return np.array(local_imp)


def i_straight_imp(coord, props):
    """ Returns the out-of-straightness imperfection.
    :param list coord: Node position in component coordinate system.
    :param dict props: Defines the properties of the imperfection.
    """
    z = coord[2]

    return np.array(straightness_imperfection(z, **props))


def i_twist_imp(coord, props):
    """ Returns the out-of-straightness imperfection.
    :param list coord: Node position in component coordinate system.
    :param dict props: Defines the properties of the imperfection.
    """
    x = coord[0]
    y = coord[1]
    z = coord[2]
    return np.array(twisting_imperfection(x, y, z, **props))


def i_plumb_imp(coord, props):
    """ Returns the out-of-straightness imperfection.
    :param list coord: Node position in component coordinate system.
    :param dict props: Defines the properties of the imperfection.
    """
    z = coord[2]
    return np.array(plumbness_imperfection(z, **props))

# -------------------------------------------------------------------------------------------------------------------- #
