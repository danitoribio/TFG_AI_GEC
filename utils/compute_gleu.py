#!/usr/bin/env python

import argparse
import sys
import os
from gleu import GLEU
import scipy.stats
import numpy as np
import random

def get_gleu_stats(scores):
    mean = np.mean(scores)
    std = np.std(scores)
    # Imprimir mean y std para depuración
    print(f"Mean: {mean}, Std: {std}")
    
    # Si std es cero, devuelve un valor predeterminado para evitar el error
    if std == 0:
        return ['%f' % mean, '%f' % std, '(nan, nan)']
    
    ci = scipy.stats.norm.interval(0.95, loc=mean, scale=std)
    return ['%f' % mean, '%f' % std, '(%.3f, %.3f)' % (ci[0], ci[1])]

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--reference",
                        help="Target language reference sentences. Multiple files for multiple references.",
                        nargs="*",
                        dest="reference",
                        required=True)
    parser.add_argument("-s", "--source",
                        help="Source language source sentences",
                        dest="source",
                        required=True)
    parser.add_argument("-o", "--hypothesis",
                        help="Target language hypothesis sentences to evaluate (can be more than one file--the GLEU score of each file will be output separately). Use '-o -' to read hypotheses from stdin.",
                        nargs="*",
                        dest="hypothesis",
                        required=True)
    parser.add_argument("-n",
                        help="Maximum order of ngrams",
                        type=int,
                        default=4)
    parser.add_argument("-d", "--debug",
                        help="Debug; print sentence-level scores",
                        default=False,
                        action="store_true")
    parser.add_argument('--iter',
                        type=int,
                        default=500,
                        help='the number of iterations to run')
    parser.add_argument('-f',"--file_out",
                        )

    args = parser.parse_args()
    
    num_iterations = args.iter

    # if there is only one reference, just do one iteration
    if len(args.reference) == 1:
        num_iterations = 1

    gleu_calculator = GLEU(args.n)
    
    gleu_calculator.load_sources(args.source)
    gleu_calculator.load_references(args.reference)
    file_out = args.file_out
    for hpath in args.hypothesis:
        instream = sys.stdin if hpath == '-' else open(hpath)
        hyp = [line.split() for line in instream]
        
        if not args.debug:
            print(os.path.basename(hpath), end=' ')
        
        # first generate a random list of indices, using a different seed for each iteration
        indices = []
        for j in range(num_iterations):
            random.seed(j * 101)
            indices.append([random.randint(0, len(args.reference) - 1) for i in range(len(hyp))])
        
        if args.debug:
            print()
            print('===== Sentence-level scores =====')
            print('SID Mean Stdev 95%CI GLEU')
        
        iter_stats = [[0 for _ in range(2 * args.n + 2)] for _ in range(num_iterations)]
        
        for i, h in enumerate(hyp):
            gleu_calculator.load_hypothesis_sentence(h)
            # store the score of this sentence for each ref to avoid recalculating them 500 times
            stats_by_ref = [None for _ in range(len(args.reference))]
            
            for j in range(num_iterations):
                ref = indices[j][i]
                this_stats = stats_by_ref[ref]

                if this_stats is None:
                    this_stats = [s for s in gleu_calculator.gleu_stats(i, r_ind=ref)]
                    stats_by_ref[ref] = this_stats
                
                iter_stats[j] = [sum(scores) for scores in zip(iter_stats[j], this_stats)]
            
            if args.debug:
                for r in range(len(args.reference)):
                    if stats_by_ref[r] is None:
                        stats_by_ref[r] = [s for s in gleu_calculator.gleu_stats(i, r_ind=r)]
                
                print(i, end=' ')
                print(' '.join(get_gleu_stats([gleu_calculator.gleu(stats, smooth=True) for stats in stats_by_ref])))
        
        if args.debug:
            print('\n==== Overall score =====')
            print('Mean Stdev 95%CI GLEU')
            print(' '.join(get_gleu_stats([gleu_calculator.gleu(stats) for stats in iter_stats])))
        else:
            s = get_gleu_stats([gleu_calculator.gleu(stats) for stats in iter_stats])[0]
            print(s)
            with open(file_out, 'a') as file:
                file.write(str(s) + '\n')