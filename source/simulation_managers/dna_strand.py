import numpy as np


class DNAStrand:
    def __init__(self, length):
        self.duplicated = np.ndarray(shape=(length,), dtype=bool)
        self.duplicated[:] = False
        self.machinery = np.ndarray(shape=(length,))
        self.machinery[:] = None

    def __len__(self):
        return len(self.machinery)

    def insert_transcription(self, transcription, position):
        if self.machinery[position] is None:
            self.machinery[position] = transcription

    def insert_replication(self, replication, position):
        if not self.duplicated[position] and not str(self.machinery[position]).startswith('Replication'):
            self.machinery[position] = replication

    def update(self):
        for position in range(len(self)):
            if str(self.machinery[position]).startswith('Replication'):
                replication = self.machinery[position]
                j = position + replication.direction
                while abs(j - position) <= replication.speed:
                    if str(self.machinery[position]).startswith('Replication') and\
                       self.machinery[position].direction != replication.direction:
                        pass
                    if self.duplicated[j]:
                        next_position = j

                        pass
                    elif j == len(self) - 1 or j == 0:
                        self.duplicate_segment(start=position, end=j)
                        break
                    j += replication.direction

    def is_fully_duplicated(self):
        return self.duplicated.all()

    def duplicate_segment(self, start, end):
        if start < end:
            self.duplicated[start:end + 1] = True
        else:
            self.duplicated[end:start + 1] = True
