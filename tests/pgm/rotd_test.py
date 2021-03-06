#!/usr/bin/env python

# stdlib imports
import os.path

# third party imports
import numpy as np
from obspy.core.stream import Stream
from obspy.core.trace import Trace

# local imports
from amptools.io.geonet.core import read_geonet
from pgm.exception import PGMException
from pgm.station_summary import StationSummary


def test_rotd():
    homedir = os.path.dirname(os.path.abspath(__file__))
    datadir = os.path.join(homedir, '..', 'data', 'process')
    # Create a stream and station summary, convert from m/s^2 to cm/s^2 (GAL)
    osc1_data = np.genfromtxt(datadir + '/ALCTENE.UW..sac.acc.final.txt')
    osc2_data = np.genfromtxt(datadir + '/ALCTENN.UW..sac.acc.final.txt')
    osc1_data = osc1_data.T[1] * 100
    osc2_data = osc2_data.T[1] * 100
    tr1 = Trace(data=osc1_data, header={'channel': 'H1', 'delta': 0.01,
                                        'npts': 10400})
    tr2 = Trace(data=osc2_data, header={'channel': 'H2', 'delta': 0.01,
                                        'npts': 10400})
    st = Stream([tr1, tr2])

    target_pga50 = 4.12528265306
    target_sa1050 = 10.7362857143
    target_pgv50 = 6.239364
    target_sa0350 = 10.1434159021
    target_sa3050 = 1.12614169215
    station = StationSummary.from_stream(st, ['rotd50'],
            ['pga', 'pgv', 'sa0.3', 'sa1.0', 'sa3.0'])
    pgms = station.pgms
    np.testing.assert_allclose(pgms['PGA']['ROTD50.0'], target_pga50, atol=0.1)
    np.testing.assert_allclose(pgms['SA1.0']['ROTD50.0'], target_sa1050, atol=0.1)
    np.testing.assert_allclose(pgms['PGV']['ROTD50.0'], target_pgv50, atol=0.1)
    np.testing.assert_allclose(pgms['SA0.3']['ROTD50.0'], target_sa0350, atol=0.1)
    np.testing.assert_allclose(pgms['SA3.0']['ROTD50.0'], target_sa3050, atol=0.1)

def test_exceptions():
    homedir = os.path.dirname(os.path.abspath(
        __file__))  # where is this script?
    datafile_v2 = os.path.join(homedir, '..', 'data', 'geonet',
                               '20161113_110259_WTMC_20.V2A')
    stream_v2 = read_geonet(datafile_v2)
    stream1 = stream_v2.select(channel="HN1")
    try:
        StationSummary.from_stream(stream1, ['rotd50'], ['pga'])
        sucess = True
    except PGMException:
        sucess = False
    assert sucess == False

    stream2 = Stream(
            [stream_v2.select(channel="HN1")[0],
            Trace(data=np.asarray([]), header={"channel":"HN2"})])
    try:
        StationSummary.from_stream(stream2,
                ['rotd50'], ['pga'])
        sucess = True
    except PGMException:
        sucess = False
    assert sucess == False

    for trace in stream_v2:
        stream1.append(trace)
    try:
        StationSummary.from_stream(stream1, ['rotd50'], ['pga'])
        sucess = True
    except PGMException:
        sucess = False
    assert sucess == False


if __name__ == '__main__':
    test_rotd()
    test_exceptions()
