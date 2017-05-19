import numpy as np


class DNAStrand:
    def __init__(self, length):
        self.strand = np.ndarray(shape=(length,), dtype=bool)
        self.strand[:] = False
        self.amount_of_duplicated_bases = 0

    def __getitem__(self, item):
        return self.strand[item]

    def __str__(self):
        strand_state = []
        current_value = self.strand[0]
        start = 0
        for index, value in enumerate(self.strand):
            if current_value != value:
                end = index - 1
                strand_state.append((start, end, current_value))
                start = index
                current_value = value

        end = len(self.strand) - 1
        strand_state.append((start, end, current_value))
        return str(strand_state)

    def duplicate_segment(self, start, end):
        if end < start:
            start, end = end, start
        for i in range(start, end + 1):
            if not self.strand[i]:
                self.strand[i] = True
                self.amount_of_duplicated_bases += 1

    def is_completely_duplicated(self):
        return self.amount_of_duplicated_bases == len(self.strand)
