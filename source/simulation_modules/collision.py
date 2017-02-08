import math


class Collision:
    """ Controls the collisions between replication's and transcriptions' machineries. """

    def __init__(self):
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
            return None

        if 0 < replication.direction * (transcription.current_position - replication.fork_position) <=\
                replication.speed - (replication.direction * transcription.direction) * transcription.speed:
            final_position = Collision.position(replication.fork_position,
                                                replication.direction * replication.speed,
                                                transcription.current_position,
                                                transcription.direction * transcription.speed)
            if transcription.direction * final_position > transcription.direction * transcription.region.end:
                return None

            replication.fork_position = final_position
            if replication.direction == transcription.direction:
                self.tail_collisions += 1
                return "tail"
            else:
                self.head_collisions += 1
                return "head"

        return None

    def resolve(self, replications, transcriptions):
        """ Solves confirmed collisions. """

        for transcription in transcriptions:
            for replication in replications:
                kind = self.verify(replication, transcription)
                if kind == "head" and replication.speed > 0:
                    replication.pause()
                if kind is not None or transcription.is_leaving_region():
                    transcription.finish()
                    break

        transcriptions[:] = [x for x in transcriptions if x.is_active()]
