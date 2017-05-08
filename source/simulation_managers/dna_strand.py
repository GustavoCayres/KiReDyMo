import numpy as np


class DNAStrand:
    def __init__(self, length):
        self.strand = np.ndarray(shape=(length,), dtype=bool)
        self.strand[:] = False

    def duplicate_segment(self, start, end):
        if start < end:
            self.strand[start:end + 1] = True
        else:
            self.strand[end:start + 1] = True

    def is_duplicated(self):
        return self.strand.all()
