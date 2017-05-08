import math
from collections import defaultdict


class CollisionVerifier:
    """ Controls the collisions between replication's and transcriptions' machineries. """

    def __init__(self, chromosome, replications, transcriptions):
        self.chromosome = chromosome
        self.replications = replications
        self.transcriptions = transcriptions
        self.collided = None
        self.where_collision_occurred = None
        self.head_collisions = 0
        self.tail_collisions = 0

    def will_collide_with_replication(self, transcription):
        return self.collided[transcription]

    def will_collide_with_transcription(self, replication):
        return self.where_collision_occurred[replication] is not None

    def resulting_position_after_collision(self, replication):
        return self.where_collision_occurred[replication]

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

    def verify_collision_between(self, replication, transcription):
        """ Verifies whether there is an imminent collision between a transcription and a replication. """

        if self.collided[transcription]:
            return

        if self.where_collision_occurred[replication] is not None:    # TODO: Not very elegant
            replication_speed = 0
        else:
            replication_speed = replication.speed

        if 0 < replication.direction * (transcription.current_position - replication.fork_position) <=\
                replication_speed - (replication.direction * transcription.direction) * transcription.speed:
            final_position = CollisionVerifier.position(replication.fork_position,
                                                        replication.direction * replication_speed,
                                                        transcription.current_position,
                                                        transcription.direction * transcription.speed)
            if transcription.direction * final_position > transcription.direction * transcription.region.end:
                return

            self.collided[transcription] = True
            if replication.direction == transcription.direction:
                self.tail_collisions += 1
            else:
                self.head_collisions += 1
                self.maximize_nearest_origins_scores(final_position)
                self.where_collision_occurred[replication] = final_position

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

    def verify_collisions(self):
        self.collided = defaultdict(lambda: False)
        self.where_collision_occurred = defaultdict(lambda: None)

        for transcription in self.transcriptions:
            for replication in self.replications:
                self.verify_collision_between(replication=replication, transcription=transcription)
