#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE - created by John Yu
# Implements the algorithm in reference [1]
#
# [1] I. Reda and A. Andreas, Solar position algorithm for solar radiation
#     applications. Solar Energy, vol. 76, no. 5, pp. 577-589, 2004.



class Observer:
    def __init__(self, latitude, longitude, elevation):
    pass


def solar(datetime):




    # geocentric latitude (degrees)
    Theta = (L + 180) % 360

    # geocentric longitude (degrees)
    beta = -B

    # nutation in longitude (degrees)
    delta_psi = sum(
        (a + b * JCE) * sin(sum(
            x * y
            for x, y in zip(
                (X0, X1, X2, X3, X4),
                (Y0, Y1, Y2, Y3, Y4))
        ))

        for Y0, Y1, Y2, Y3, Y4, a, b, _, _ in _nutation_table
    ) / 36000000

    # nutation in obliquity (degrees)
    delta_epsilon = sum(
        (c + d * JCE) * cos(sum(
            x * y
            for x, y in zip(
                (X0, X1, X2, X3, X4),
                (Y0, Y1, Y2, Y3, Y4))
        ))

        for Y0, Y1, Y2, Y3, Y4, _, _, c, d in _nutation_table
    ) / 36000000


    U = JME / 10

    # mean obliquity of the ecliptic (arc seconds)
    epsilon0 = (
        84381.448        -
        U      * 4860.93 -
        U**2   * 1.55    +
        U**3   * 1999.25 -
        U**4   * 51.38   -
        U**5   * 249.67  -
        U**6   * 39.05   +
        U**7   * 7.12    +
        U**8   * 27.87   +
        U**9   * 5.79    +
        U**10  * 2.45
    )

    # true obliquity of the ecliptic (degrees)
    epsilon = epsilon0 / 3600 + delta_epsilon


    # apparent sun longitude
    lambda_ = Theta + delta_psi + delta_tau



    sigma = longitude
    phi = latitude
    E = elevation

    # observer local hour angle
    H = (v + sigma - alpha) % 360

    # topocentric sun right ascension
    xi = 8.794 / 3600 / R

    u = atan(0.99664719 * tan(phi))
    x = cos(u) + E / 6378140 * cos(phi)
    y = 0.99664719 * sin(u) + E / 6378140 * sin(phi)

    # parallax in sun right ascension (degrees)
    delta_alpha = (
        atan(-x * sin(xi) * sin(H))
        /
        atan(cos(delta) - x * sin(xi) * cos(H))
    ) / pi * 180

    # topocentric sun right ascention (degrees)
    alpha_prime = alpha + delta_alpha

    # topocentric sun declination (degrees)
    delta_prime = (
        atan((sin(delta) - y * sin(xi)) * cos(delta_alpha))
        /
        atan(cos(delta) - x * sin(xi) * cos(H))
    )

    # topocentric local hour angle (degrees)
    H_prime = H - delta_alpha

    # topocentric zenith angle (degrees)
    e0 = asin(
        sin(phi) * sin(delta_prime) +
        cos(phi) * cos(delta_prime) * cos(H_prime))

    # atmospheric refraction correction (degrees)
    P = annual_average_local_millibars
    T = annual_average_local_celsius
    delta_e = (
        P / 1010        *
        283 / (273 + T) *
        1.02 / 60 / tan(e0 + 10.3 / (e0 + 5.11))
    )

    # topocentric elevation angle (degrees)
    e = e0 + delta_e

    # topocentric zenith angle (degrees)
    theta = 90 - e

    # topocentric astronomers azimuth angle (degrees)
    Gamma = (
        atan(sin(H_prime))
        /
        atan(cos(H_prime) * sin(phi) - tan(delta_prime) * cos(phi))
    ) / pi * 180 % 360

    # topocentric azimuth angle (degrees)
    Phi = (Gamma + 180) % 360

    # incidence angle (degrees)
    omega = horizontal_slope
    gamma = surface_azimuth_rotation_angle
    I = acos(
        cos(theta) * cos(omega) +
        sin(omega) * sin(theta) * cos(Gamma - gamma)
    )
