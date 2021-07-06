

class Generator:
    @staticmethod
    def generate_empty_state(q_table, state_hash, origin):
        q_table[state_hash] = []
        for i in range(len(origin)):
            q_table[state_hash].append([])
            for j in range(len(origin)):
                q_table[state_hash][i].append(0)
