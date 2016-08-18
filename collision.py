class Collision:
    """ Controls the collisions between replication's and transcriptions' machineries. """

    def __init__(self):
        pass

    @staticmethod
    def verify_collision(replication, transcription):
        """ Verifies whether there is an imminent collision between a transcription and a replication. """

        if transcription.current_position is None:
            return None, None

        added_speed = transcription.region.speed + replication.chromosome.replication_speed
        subtracted_speed = replication.chromosome.replication_speed - transcription.region.speed
        if transcription.direction > 0:
            if 0 < replication.left_fork - transcription.current_position <= added_speed:
                return "left", "head"
            if 0 < transcription.current_position - replication.right_fork <= subtracted_speed:
                return "right", "tail"
        else:
            if 0 < transcription.current_position - replication.right_fork <= added_speed:
                return "right", "head"
            if 0 < replication.left_fork - transcription.current_position <= subtracted_speed:
                return "left", "tail"
        return None, None

    @staticmethod
    def resolve_collisions(replication, transcriptions):
        """ Solves confirmed collisions. """

        for transcription in transcriptions:
            fork, kind = Collision.verify_collision(replication, transcription)
            if kind == "tail":
                transcription.finish()
            elif kind == "head":
                transcription.finish()
                replication.pause(fork)
