# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import spynnaker8 as p
import matplotlib.pyplot as plt
import pyNN.utility.plotting as plot

p.setup(0.1)
runtime = 50
populations = []
title = "PyNN0.8 alpha synapse testing"

pop_src1 = p.Population(1, p.SpikeSourceArray,
                        {'spike_times': [[5, 15, 20, 30]]}, label="src1")

populations.append(p.Population(1, p.IF_curr_alpha, {}, label="test"))

populations[0].set(tau_syn_E=2)
populations[0].set(tau_syn_I=4)

# define the projections
exc_proj = p.Projection(pop_src1, populations[0],
                        p.OneToOneConnector(),
                        p.StaticSynapse(weight=1, delay=1),
                        receptor_type="excitatory")
inh_proj = p.Projection(pop_src1, populations[0],
                        p.OneToOneConnector(),
                        p.StaticSynapse(weight=1, delay=10),
                        receptor_type="inhibitory")

populations[0].record("all")
p.run(runtime)

v = populations[0].get_data("v")
gsyn_exc = populations[0].get_data("gsyn_exc")
gsyn_inh = populations[0].get_data("gsyn_inh")
spikes = populations[0].get_data("spikes")

plot.Figure(
    plot.Panel(v.segments[0].filter(name='v')[0],
               ylabel="Membrane potential (mV)",
               data_labels=[populations[0].label],
               yticks=True, xlim=(0, runtime)),
    plot.Panel(gsyn_exc.segments[0].filter(name='gsyn_exc')[0],
               ylabel="gsyn excitatory (mV)",
               data_labels=[populations[0].label],
               yticks=True, xlim=(0, runtime)),
    plot.Panel(gsyn_inh.segments[0].filter(name='gsyn_inh')[0],
               ylabel="gsyn inhibitory (mV)",
               data_labels=[populations[0].label],
               yticks=True, xlim=(0, runtime)),
    title=title,
    annotations="Simulated with {}".format(p.name())
)
plt.show()
p.end()
