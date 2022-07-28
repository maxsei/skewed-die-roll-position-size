from pprint import pformat
from tap import Tap
from typing import Optional


class TapBase(Tap):
    def __str__(self):
        return pformat(self.as_dict(), sort_dicts=False)

    def as_dict(self):
        mro_all = type(self).__mro__
        mro_tap = mro_all[:mro_all.index(Tap) - 1]
        annots = [annot for cls in mro_tap for annot in cls.__annotations__.keys()]
        return {k: self.__dict__[k] for k in annots}

class ArgsPlot(TapBase):
    height: int = 30 # terminal plot width
    width: int = 80 # terminal plot width
    log: bool = False # show chart in log scale

class ArgsMeta(TapBase):
    save_to: Optional[str] = None # optional json path to save to
    load_from: Optional[str] = None # optional json path to load from
    hide_plot: Optional[str] = None # optional json path to load from

    def process_args(self):
        if self.save_to != None and self.load_from != None:
            raise ValueError("do not save and load simultaneosly")

class ArgsParams(TapBase):
    trials: int = 666 # number of trials to bet in a single simluation
    win_amt: float = 1 # amount for a win
    win_rate: float = 5 / 6 # win rate
    loss_amt: float = -4 # amount for a loss
    loss_rate: float = 1 - win_rate # loss rate. implicit (1 - win_rate)
    size: float = 1 # initial position size
    positions: int = 200 # number of position sizes to compute in the range of [0, (1-win_rate))
    sims: int = 1 # number of simulations to smooth the distribution
    seed: Optional[int] = None # optionally seed


class Args(ArgsParams, ArgsPlot, ArgsMeta):
    def process_args(self):
        # If we are loading args we don't want to set any params.
        if self.load_from == None:
            return
        if any([ArgsParams.__dict__[k] != self.__dict__[k] for k in ArgsParams.__annotations__.keys()]):
            raise ValueError("do not set any params when loading a configuration")

    def as_dict(self):
        # Only save args params.
        d = super().as_dict()
        ret = {k: d[k] for k in ArgsParams.__annotations__} 
        return ret
