# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

import numpy as np


from scipy.signal import butter, lfilter
from scipy.signal import freqs
from scipy import fft

from matplotlib import pyplot as plt


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 20 ns (50 MHz)
    
    clock_per = 20
    clock_freq = 1.0 / (clock_per * 1.e-9)

    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Feed in white noise and compare the result with python filter implementation

    y0 = 0
    y1 = 0
    y2 = 0
    x0 = 0
    x1 = 0
    x2 = 0
    
    a = np.array([  8192., -16276.,   8110.])
    b = np.array([ 5.,   0., -5.])

    rand_data = np.random.normal(0, 1, 1000) * 128.0
    rand_data = np.clip(rand_data, -128, 128)

    v_filt_out = []
    p_filt_out = []

    out = 0

    for d in rand_data:
  
        y2 = y1
        y1 = y0 
        x2 = x1
        x1 = x0
        x0 = int(d)

        out = int((-a[1]*y1 // 8192) - (a[2]*y2 // 8192) + b[0]*x0 + b[2]*x2)
     
        dut.if_out.value = x0

        v_filt_out.append(dut.if_filt_out.value.signed_integer)
        p_filt_out.append(out // 8192)

        print("model = {}, dut = {}".format(out // 8192, dut.if_filt_out.value.signed_integer))
        print("model: y0 {} y1 {} y2 {} x0 {} x1 {} x2 {}".format(y0, y1, y2, x0, x1, x2))
        print()

        await ClockCycles(dut.clk, 1)
        y0 = out

    plt.plot(p_filt_out)
    plt.plot(v_filt_out)
    plt.show()



