

class Generator:
    @staticmethod
    def generate_empty_state(q_table, state_hash, length):
        q_table[state_hash] = []
        for i in range(length):
            q_table[state_hash].append([])
            for j in range(length):
                index = i * length + j
                q_table[state_hash][i].append(0 if state_hash[index] == 'N' else -1)
