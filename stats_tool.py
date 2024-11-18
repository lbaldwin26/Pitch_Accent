#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time

import argparse
from functools import reduce
import operator

QUESTION_TOTAL_SIZE = 40
ITERATIONS = 10_000

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--test", type = str,
    help = "Test given values for statistical significance against a hypothetical random ditribution"
)
parser.add_argument(
    "-s", "--show", action="store_true",
    help = "Print the dotplot of the number correct answers of each trial in the simulation"
)

# random.seed(144)

def generate_distribution(size: int, iterations: int):
    dotplot = [0] * size

    for _ in range(iterations-1):
        answers = []
        for _ in dotplot:
            answers.append(not random.getrandbits(1))
        
        number_of_correct_answers: int = len(list(filter(lambda val: val is True, answers)))
        dotplot[number_of_correct_answers] += 1
    return dotplot

def test_for_stat_sig(dotplot, values):
    db = {}
    entire_total = reduce(operator.add, dotplot)
    for value in values:
        total = 1
        for position in range(value, len(dotplot)):
            total += dotplot[position]

        likelyhood = total/entire_total
        if likelyhood <= 0.05:
            db[value] = [True, likelyhood]
        else:
            db[value] = [False, likelyhood]

    return db

def find_stat_sig_threshold_index(dotplot) -> int:
    entire_total = reduce(operator.add, dotplot)
    max_sum_of_dots_exceeding_stat_sig = 0.05 * entire_total

    spot_found: bool = False
    index = len(dotplot)-1
    sum_of_dots_exceeding_stat_sig = 0

    while spot_found is False: 
        if sum_of_dots_exceeding_stat_sig >= max_sum_of_dots_exceeding_stat_sig:
            return (index+1, max_sum_of_dots_exceeding_stat_sig)

        sum_of_dots_exceeding_stat_sig += dotplot[index]
        index -= 1

if __name__ == '__main__':
    dotplot = generate_distribution(QUESTION_TOTAL_SIZE, ITERATIONS)

    args = parser.parse_args()
    
    if args.show:
        print(f'Dotplot: {dotplot}\nStat. Sig. threshold: >{find_stat_sig_threshold_index(dotplot)[0]} (<= sum of {find_stat_sig_threshold_index(dotplot)[1]})')

    if args.test:
        values = map(int, args.test.split(","))
        print(f'Stat. Sig. test: {test_for_stat_sig(dotplot, values)}')
