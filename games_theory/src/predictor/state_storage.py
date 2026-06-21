from games_theory.resources.resource import Resource


class StateStorage:
    def __init__(self, resources_path):
        self.resources_path = resources_path

    def persist(self, last_move):
        Resource.save('state.json', 'last_move', last_move, self.resources_path)

    def clear_last_move(self):
        Resource.save('state.json', 'last_move', None, self.resources_path)
