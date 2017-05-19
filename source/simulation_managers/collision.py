import math
from source.models.replication_origin import ReplicationOrigin


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
                return None, None

            if replication.direction == transcription.direction:
                self.tail_collisions += 1
                return "tail", None
            else:
                self.head_collisions += 1
                return "head", final_position

        return None, None

    def activate_origin_nearby(self, replication):
        maximum_score = max([1, max([origin.score for origin in self.chromosome.replication_origins])])

        new_origin_position = replication.fork_position + replication.direction * 20
        if new_origin_position < 0:
            new_origin_position = 0
        elif new_origin_position >= self.chromosome.length:
            new_origin_position = self.chromosome.length - 1

        new_origin = ReplicationOrigin(position=new_origin_position,
                                       score=maximum_score,
                                       chromosome=self.chromosome)
        if new_origin not in self.chromosome.replication_origins:
            self.chromosome.replication_origins.append(new_origin)

    def resolve(self, replications, transcriptions):
        """ Solves confirmed collisions. """

        for transcription in transcriptions:
            for replication in replications:
                kind, position = self.verify(replication, transcription)
                if kind == "head" and replication.speed > 0:
                    print("collision at " + str(position))
                    replication.pause(position)
                    self.activate_origin_nearby(replication)
                if kind is not None or transcription.is_leaving_region():
                    transcription.finish()
                    break

        transcriptions[:] = [x for x in transcriptions if x.is_active()]
