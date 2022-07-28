from pprint import pformat
from tap import Tap
from typing import Optional


class TapBase(Tap):
    def __str__(self):
        return pformat(self.as_dict(), sort_dicts=False)

    def as_dict(self):
        mro_all = type(self).__mro__
        mro_tap = mro_all[: mro_all.index(Tap) - 1]
        annots = [annot for cls in mro_tap for annot in cls.__annotations__.keys()]
        return {k: self.__dict__[k] for k in annots}


class ArgsPlot(TapBase):
    height: int = 30  # terminal plot width
    width: int = 80  # terminal plot width
    xmin: Optional[float] = None  # min on x axis (default is position_min)
    xmax: Optional[float] = None  # min on x axis (default is position_max)
    log: bool = False  # show chart in log scale


class ArgsMeta(TapBase):
    save_to: Optional[str] = None  # optional json path to save to
    load_from: Optional[str] = None  # optional json path to load from
    hide_params: bool = False  # hide params

    def process_args(self):
        if self.save_to != None and self.load_from != None:
            raise ValueError("do not save and load simultaneosly")


class ArgsParams(TapBase):
    trials: int = 666  # number of trials to bet in a single simluation
    win_amt: float = 1  # amount for a win
    win_rate: float = 5 / 6  # win rate
    loss_amt: float = -4  # amount for a loss
    loss_rate: float = 1 - win_rate  # loss rate. implicit (1 - win_rate)
    size: float = 1  # initial position size
    position_min: int = 0  # start of position size range
    position_max: int = loss_rate  # end of position size range (default=loss_rate)
    positions: int = 32  # number of position sizes to compute
    sims: int = 1  # number of simulations to smooth the distribution
    seed: Optional[int] = None  # optionally seed


class Args(ArgsParams, ArgsPlot, ArgsMeta):
    def process_args(self):
        # win/loss rate ranges.
        if self.win_rate <= 0:
            raise ValueError("win-rate must be positive number")
        if self.loss_rate <= 0:
            raise ValueError("loss-rate must be positive number")
        total_prob = self.win_rate + self.loss_rate
        if total_prob > 1:
            raise ValueError("win-rate and loss-rate sum must be <= 1")

        # All positive numbers:
        if self.trials <= 0:
            raise ValueError("trials must be positive number")
        if self.size <= 0:
            raise ValueError("size must be positive number")
        if self.positions <= 1:
            raise ValueError("must have at least 2 positions")
        if self.sims <= 0:
            raise ValueError("sims must be positive number")

        # Acceptable range for position_min and position_max
        if self.position_max < 0 or 1 < self.position_max:
            raise ValueError("position-max must be in the range [0, 1]")
        if self.position_min < 0 or 1 < self.position_min:
            raise ValueError("position-min must be in the range [0, 1]")
        if self.position_min >= self.position_max:
            raise ValueError("position-min must be greater than position-max")

        # If we are loading args we don't want to set any params.
        if self.load_from != None and any(
            [
                ArgsParams.__dict__[k] != self.__dict__[k]
                for k in ArgsParams.__annotations__.keys()
            ]
        ):
            raise ValueError("do not set any params when loading a configuration")

    def as_dict(self):
        # Only save args params.
        d = super().as_dict()
        ret = {k: d[k] for k in ArgsParams.__annotations__}
        return ret
