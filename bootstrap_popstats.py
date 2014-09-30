#!/usr/local/env python

import numpy as np
import numpy.random as npr
import pylab
import optparse

usage_line = """
A script to bootstrap over private allele data for each population from Stacks \
and calculate a confidence interval. User must specify the <batch>.sumstats.tsv file, \
the number of bootstrap reps, the value of alpha (0.05 by default), and the population \
ID for the population of interest in the <batch>.sumstats.tsv file (1, 2, ..., N). \
Output to terminal is the observed number of private alleles in the population and \
a confidence interval based on the boostrapping.
"""

usage = usage_line

parser = optparse.OptionParser(usage=usage)
parser.add_option("--input", action= "store", type= "string", dest="input", help="""The input <batch>.sumstats.tsv file""")
parser.add_option("--permutations", action="store", type= "string", dest="perms", help="""The number of bootstrap reps/permutations""")
parser.add_option("--alpha", action="store", type= "string", dest= "alpha", help="""The value of alpha for the confidence interval width [0.05]""", default = "0.05")
parser.add_option("--population", action = "store", type = "string", dest = "population", help = "Name/number of the population you want to estimate CI for")
options, args = parser.parse_args()

def bootstrap(data, num_samples, statistic, alpha):
    ## Returns bootstrap estimate of 100.0*(1-alpha) CI for statistic.
    n = len(data)
    idx = npr.randint(0, n, (num_samples,n))
    samples = data[idx]
    stat = np.sort(statistic(samples, 1))
    return (stat[int((alpha/2.0)*num_samples)],
            stat[int((1-alpha/2.0)*num_samples)])

if __name__ == '__main__':
    pop = []
    for line in open(options.input, "r"):
	    if not line.strip().startswith("#"):
        	record = line.rstrip().split("\t")
        	if record[5] == options.population:
        		pop.append(float(record[14]))
        	else:
        		nothing = 1
    observed = float(sum(pop))/len(pop)
    x = np.array(pop)

    low, high = bootstrap(x, int(options.perms), np.mean, float(options.alpha))
    
    obsline = "The observation from the input dataset is "+str(observed)+"."
    ciline = "The CI after "+options.perms+" bootstraps with alpha = "+options.alpha+" is "+str(low)+"-"+str(high)+"."
    print "\n\nPopulation = "+options.population
    print obsline
    print ciline+"\n\n"