import numpy as np


class DNAStrand:
    def __init__(self, length):
        self.strand = np.ndarray(shape=(length,), dtype=bool)
        self.strand[:] = False
        self.amount_of_duplicated_bases = 0

    def __getitem__(self, item):
        return self.strand[item]

    def __str__(self):
        return str(self.strand)

    @property
    def duplicated_percentage(self):
        return float(self.amount_of_duplicated_bases/len(self.strand))

    @property
    def duplicated_segments(self):
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
        return strand_state

    def duplicate_segment(self, start, end):
        if end < start:
            start, end = end, start
        for i in range(start, end + 1):
            if not self.strand[i]:
                self.strand[i] = True
                self.amount_of_duplicated_bases += 1

    def is_duplicated(self, threshold=1):
        return float(self.amount_of_duplicated_bases / len(self.strand)) >= threshold

    def is_position_duplicated(self, position):
        return self.strand[position]
