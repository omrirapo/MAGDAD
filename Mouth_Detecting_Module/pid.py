


def PID(Kp, Ki, Kd, MV_bar=0):
    """
    uses a pid controller to minigate vibrations in arm movement
    :param Kp: the constant regarding proportional
    :param Ki: the constant regarding integral
    :param Kd: the constant regarding derivative
    :param MV_bar:  start position
    :return: commands to the arm
    """
    # initialize stored data
    e_prev = 0
    t_prev = -1
    I = 0

    # initial control
    MV = MV_bar

    while True:
        # yield MV, wait for new t, PV, SP
        t, PV, SP = yield MV

        # PID calculations
        e = SP - PV

        P = Kp * e
        I = I + Ki * e * (t - t_prev)
        D = Kd * (e - e_prev) / (t - t_prev)

        MV = MV_bar + P + I + D

        # update stored data for next iteration
        e_prev = e
        t_prev = t




