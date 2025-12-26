from __future__ import annotations

from collections.abc import Sequence
from dataclasses import InitVar, dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from functools import total_ordering
from typing import Final

DECIMAL_CENT: Final = Decimal("0.01")
BASE_CURRENCY: Final = "BRL"

type Scalar = int | Decimal
type ToDecimal = Decimal | float | str | tuple[int, Sequence[int], int]


@dataclass(frozen=True)
@total_ordering
class Money:
    raw_amount: InitVar[ToDecimal]
    amount: Decimal = field(init=False)
    currency: str = BASE_CURRENCY

    def __post_init__(self, raw_amount: ToDecimal) -> None:
        quantized_amount = Decimal(raw_amount).quantize(
            DECIMAL_CENT, rounding=ROUND_HALF_UP
        )
        object.__setattr__(self, "amount", quantized_amount)

    def __add__(self, other: Money) -> Money:
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, scalar: Scalar) -> Money:
        return Money(self.amount * Decimal(scalar), self.currency)

    __rmul__ = __mul__

    def __truediv__(self, scalar: Scalar) -> Money:
        return Money(self.amount / Decimal(scalar), self.currency)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount < other.amount

    @classmethod
    def zero(cls, currency: str = BASE_CURRENCY) -> Money:
        return cls("0.00", currency)