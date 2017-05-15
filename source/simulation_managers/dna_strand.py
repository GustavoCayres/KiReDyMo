import numpy as np


class DNAStrand:
    def __init__(self, length):
        self.strand = np.ndarray(shape=(length,), dtype=bool)
        self.strand[:] = False
        self.amount_of_duplicated_bases = 0

    def __getitem__(self, item):
        return self.strand[item]

    def __str__(self):
        return str(len(self.strand))

    def duplicate_segment(self, start, end):
        if end < start:
            start, end = end, start
        for i in range(start, end + 1):
            if not self.strand[i]:
                self.strand[i] = True
                self.amount_of_duplicated_bases += 1

    def is_completely_duplicated(self):
        return self.amount_of_duplicated_bases == len(self.strand)
