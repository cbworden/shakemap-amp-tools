# stdlib imports
import os

# third party imports
import numpy as np

# local imports
from amptools.constants import GAL_TO_PCTG
from amptools.io.read import read_data
from pgm.oscillators import get_acceleration, get_spectral, get_velocity


def test_acceleration():
    homedir = os.path.dirname(os.path.abspath(
        __file__))  # where is this script?
    acc_file = os.path.join(homedir, '..', 'data', 'geonet',
                               '20161113_110259_WTMC_20.V2A')
    acc = read_data(acc_file)
    target_g = acc[0].data * GAL_TO_PCTG
    target_m = acc[0].data / 100
    target_cm = acc[0].data

    acc_g = get_acceleration(acc, units='%%g')
    assert acc_g[0].stats['units'] == '%%g'
    np.testing.assert_allclose(acc_g[0], target_g)

    acc_m = get_acceleration(acc, units='m/s/s')
    assert acc_m[0].stats['units'] == 'm/s/s'
    np.testing.assert_allclose(acc_m[0], target_m)

    acc_cm = get_acceleration(acc, units='cm/s/s')
    assert acc_cm[0].stats['units'] == 'cm/s/s'
    np.testing.assert_allclose(acc_cm[0], target_cm)

def test_spectral():
    homedir = os.path.dirname(os.path.abspath(
        __file__))  # where is this script?
    acc_file = os.path.join(homedir, '..', 'data', 'geonet',
                               '20161113_110259_WTMC_20.V2A')
    acc = read_data(acc_file)
    get_spectral(1.0, acc, 0.05, rotation='gm')

def test_velocity():
    homedir = os.path.dirname(os.path.abspath(
        __file__))  # where is this script?
    acc_file = os.path.join(homedir, '..', 'data', 'geonet',
                               '20161113_110259_WTMC_20.V2A')
    acc = read_data(acc_file)
    target_v = acc.copy().integrate()[0]
    v = get_velocity(acc)
    np.testing.assert_allclose(v[0], target_v)


if __name__ == '__main__':
    test_acceleration()
    test_spectral()
    test_velocity()
