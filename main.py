#!/usr/bin/env python3
import plotille
import numpy as np
from collections import OrderedDict
from pprint import pformat
from copy import deepcopy
from typing import Optional

from tap import Tap

class Args(Tap):
    # Params
    n_plays: int = 666 # number of times to bet
    win_rate: float = 5 / 6 # win rate. loss rate is implicit (1 - win_rate)
    win_amt: float = 1 # amount for a win
    loss_amt: float = -4 # amount for a loss
    starting_resources: float = 1 # initial position
    n_positions: int = 200 # number of position sizes to compute in the range of [0, (1-win_rate))
    n_sims: int = 1 # number of simulations to smooth the distribution
    seed: Optional[int] = None # optionally seed
    # Plot
    height: int = 30 # terminal plot width
    width: int = 80 # terminal plot width
    log_scale: Optional[bool] = False # show chart in log scale
    # Meta
    echo: Optional[bool] = True # print configuration

    def __str__(self):
        d = {}
        for k in type(self).__annotations__.keys():
            d[k] = getattr(self, k)
        return pformat(d, sort_dicts=False)


def main():
    args = Args().parse_args()
    # Assign a random seed.
    if args.seed:
        args.seed = np.random.randint(np.iinfo(np.int64).max)

    # Print configuration if echo
    if args.echo:
        print(args)
        print()

    np.random.seed(args.seed)

    position_sizes = np.linspace(0, 1 - args.win_rate, args.n_positions)

    # wins = (np.random.rand(args.n_plays, args.n_sims) < args.win_rate).astype(np.int64)
    wins = (np.random.rand(args.n_sims, args.n_plays) < args.win_rate).astype(np.int64)
    losses = 1 - wins

    profit = (
        args.starting_resources
        + position_sizes[..., np.newaxis, np.newaxis]
        * ((wins * args.win_amt) + (losses * args.loss_amt))
    ).prod(axis=-1).mean(axis=-1)



    fig = plotille.Figure()
    fig.height = args.height
    fig.width = args.width
    fig.set_x_limits(min_=0, max_=position_sizes[-1])
    fig.scatter(position_sizes, np.log(profit) if args.log_scale else profit)
    print(fig.show())

if __name__ == "__main__":
    main()
