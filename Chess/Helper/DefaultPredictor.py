

class DefaultPredictor:
    def __init__(self, current_state, next_states, learning_rate=0.1, discount_rate=0.5):
        self.__current_state = current_state
        self.__next_states = next_states
        self.__learning_rate = learning_rate
        self.__discount_rate = discount_rate

    def evaluate(self):
        pass

    def predict(self):
        pass
