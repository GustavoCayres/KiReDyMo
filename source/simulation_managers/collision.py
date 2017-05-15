import math


class Collision:
    """ Controls the collisions between replication's and transcriptions' machineries. """

    def __init__(self, chromosome):
        self.chromosome = chromosome

        self.head_collisions = 0
        self.tail_collisions = 0

    @staticmethod
    def position(replication_position, replication_speed, transcription_position, transcription_speed):
        """ Calculates the final position of the replication fork after a collision."""

        if replication_speed == transcription_speed:
            return math.copysign(math.inf, replication_speed)

        collision_time = (transcription_position - replication_position)/(replication_speed - transcription_speed)
        if collision_time < 0:
            print("Error during collision calculation. Verify the speed of the system's parts.")
            exit(1)

        return int(replication_position + collision_time * replication_speed)

    def verify(self, replication, transcription):
        """ Verifies whether there is an imminent collision between a transcription and a replication. """

        if not transcription.is_active() or not replication.is_active():
            return None, None

        if 0 < replication.direction * (transcription.current_position - replication.fork_position) <=\
                replication.speed - (replication.direction * transcription.direction) * transcription.speed:
            final_position = Collision.position(replication.fork_position,
                                                replication.direction * replication.speed,
                                                transcription.current_position,
                                                transcription.direction * transcription.speed)
            if transcription.direction * final_position > transcription.direction * transcription.region.end:
                return None

            if replication.direction == transcription.direction:
                self.tail_collisions += 1
                return "tail", None
            else:
                self.head_collisions += 1
                return "head", final_position

        return None, None

    def maximize_nearest_origins_scores(self, collision_position):
        maximum_score = max([origin.score for origin in self.chromosome.replication_origins])
        i = 0
        for origin in self.chromosome.replication_origins:
            if origin.position > collision_position:
                break
            i += 1
        if i < len(self.chromosome.replication_origins):
            self.chromosome.replication_origins[i].score = maximum_score
        if i > 0:
            self.chromosome.replication_origins[i - 1].score = maximum_score

    def resolve(self, replications, transcriptions):
        """ Solves confirmed collisions. """

        for transcription in transcriptions:
            for replication in replications:
                kind, position = self.verify(replication, transcription)
                if kind == "head" and replication.speed > 0:
                    self.maximize_nearest_origins_scores(replication.fork_position)
                    replication.pause(position)
                if kind is not None or transcription.is_leaving_region():
                    transcription.finish()
                    break

        transcriptions[:] = [x for x in transcriptions if x.is_active()]
