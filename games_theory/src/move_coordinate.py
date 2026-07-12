from games_theory.src.domain_types import MoveCoordinate, State


def derive_move_coordinate(
    current_state: State,
    selected_state: State,
    board_size: int,
) -> MoveCoordinate:
    if board_size <= 0:
        raise ValueError("Board size must be greater than zero")

    current_cells = current_state.split(',')
    selected_cells = selected_state.split(',')
    expected_cells = board_size * board_size
    if len(current_cells) != expected_cells or len(selected_cells) != expected_cells:
        raise ValueError("States must contain board-size * board-size cells")

    changed_indices = [
        index
        for index, (current, selected) in enumerate(zip(current_cells, selected_cells))
        if current != selected
    ]
    if len(changed_indices) != 1:
        raise ValueError("Selected state must differ from current state by exactly one cell")

    index = changed_indices[0]
    if current_cells[index] != '0' or selected_cells[index] != '-1':
        raise ValueError("Selected move must place the bot marker in an empty cell")

    return {'x': index % board_size, 'y': index // board_size}
