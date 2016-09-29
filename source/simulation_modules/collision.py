class Collision:
    """ Controls the collisions between replication's and transcriptions' machineries. """

    @staticmethod
    def position(position1, speed1, position2, speed2):
        """ Calculates the final position of the replication fork after a collision."""

        if speed1 == speed2:
            return position1

        collision_time = (position2 - position1)/(speed1 - speed2)
        if collision_time < 0:
            print("Error during collision calculation. Verify the speed of the system's parts.")
            exit(1)

        return int(position1 + collision_time*speed1)

    @staticmethod
    def verify(replication, transcription):
        """ Verifies whether there is an imminent collision between a transcription and a replication. """

        if transcription.current_position is None:
            return None, None

        replication_speed = replication.chromosome.replication_speed
        transcription_speed = transcription.region.speed
        added_speed = replication_speed + transcription_speed
        subtracted_speed = replication_speed - transcription_speed

        if transcription.direction > 0:
            if replication.left_fork is not None:
                if 0 < replication.left_fork - transcription.current_position <= added_speed:
                    replication.left_fork = Collision.position(replication.left_fork, -replication_speed,
                                                               transcription.current_position, transcription_speed)
                    print("Head Collision!!")
                    return "left", "head"
            if replication.right_fork is not None:
                if 0 < transcription.current_position - replication.right_fork <= subtracted_speed:
                    print("Tail Collision!!")
                    return "right", "tail"
        else:
            if replication.right_fork is not None:
                if 0 < transcription.current_position - replication.right_fork <= added_speed:
                    replication.right_fork = Collision.position(replication.right_fork, replication_speed,
                                                                transcription.current_position, -transcription_speed)
                    print("Head Collision!!")
                    return "right", "head"
            if replication.left_fork is not None:
                if 0 < replication.left_fork - transcription.current_position <= subtracted_speed:
                    print("Tail Collision!!")
                    return "left", "tail"
        return None, None

    @staticmethod
    def resolve(replication, transcriptions):
        """ Solves confirmed collisions. """

        for transcription in transcriptions:
            fork, kind = Collision.verify(replication, transcription)
            if kind == "tail":
                transcription.collapse()
            elif kind == "head":
                transcription.collapse()
                replication.pause(fork)