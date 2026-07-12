from typing import Dict, List, Optional, Sequence, TypedDict, Union


State = str
PointValue = Union[str, int]
Points = Sequence[PointValue]
NormalizedPoints = List[str]
StateValues = Dict[State, float]
QTable = Dict[State, StateValues]


class MoveCoordinatePayload(TypedDict):
    x: int
    y: int


GameConfig = TypedDict(
    'GameConfig',
    {
        'learning': bool,
        'board-size': int,
        'ai-char': str,
    },
)

LastMove = TypedDict(
    'LastMove',
    {
        'from': State,
        'to': State,
        'points': NormalizedPoints,
        'advantage': int,
    },
)


class StatePayload(TypedDict):
    last_move: Optional[LastMove]
