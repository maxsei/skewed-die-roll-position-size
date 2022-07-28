#!/usr/bin/env python3
from collections import OrderedDict
from copy import deepcopy

import numpy as np
import plotille
import toml

from scipy.stats.mstats import gmean

from args import Args


def main():
    args = Args(underscores_to_dashes=True).parse_args()

    # Load args if necessary.
    if args.load_from is not None:
        args.load(args.load_from)

    # Assign a random seed.
    if args.seed is None and args.load_from is not None:
        args.seed = np.random.randint(np.iinfo(np.int32).max - 1)

    # Save args if necessary.
    if args.save_to is not None:
        args.save(args.save_to)

    # Print out args.
    print(" params ".center(args.width, "-"))
    print(args, end="\n\n")

    # Seed and generate (sims, plays).
    np.random.seed(args.seed)
    rand = np.random.rand(args.sims, args.trials)
    wins = (rand < args.win_rate).astype(np.int64)
    losses = ((1 - rand) < args.loss_rate).astype(np.int64)

    # Create position size strategies.
    position_sizes = np.linspace(0, 1 - args.win_rate, args.positions)

    # [Position sizes, simulation, plays]
    outcomes = (
        args.size
        + position_sizes[..., np.newaxis, np.newaxis]
        * ((wins * args.win_amt) + (losses * args.loss_amt))
    )
    profit = gmean(np.prod(outcomes, axis=-1), axis=-1)
    # profit = np.mean(np.prod(outcomes, axis=-1), axis=-1)

    fig = plotille.Figure()
    fig.height = args.height
    fig.width = args.width
    # fig.set_x_limits(min_=0, max_=position_sizes[-1])
    fig.set_x_limits(min_=0, max_=1)
    fig.scatter(position_sizes, np.log(profit) if args.log else profit)
    fig_str = fig.show()
    print(fig_str)

if __name__ == "__main__":
    main()
