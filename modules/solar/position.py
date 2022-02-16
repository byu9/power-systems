#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
#
# Calculates the solar position for a given observer location and date time.
# Implements the algorithm in reference [1]
#
# [1] I. Reda and A. Andreas, Solar position algorithm for solar radiation
#     applications. Solar Energy, vol. 76, no. 5, pp. 577-589, 2004.
#
from math import (
    cos, sin, tan, asin, acos, atan, atan2,
    degrees, radians
)

try:
    from functools import cached_property
except ImportError:
    from backports.cached_property import cached_property

_L0_table = (
    # (A, B, C),
    (175347046,  0,          0          ),
    (3341656,    4.6692568,  6283.07585 ),
    (34894,      4.6261,     12566.1517 ),
    (3497,       2.7441,     5753.3849  ),
    (3418,       2.8289,     3.5231     ),
    (3136,       3.6277,     77713.7715 ),
    (2676,       4.4181,     7860.4194  ),
    (2343,       6.1352,     3930.2097  ),
    (1324,       0.7425,     11506.7698 ),
    (1273,       2.0371,     529.691    ),
    (1199,       1.1096,     1577.3435  ),
    (990,        5.233,      5884.927   ),
    (902,        2.045,      26.298     ),
    (857,        3.508,      398.149    ),
    (780,        1.179,      5223.694   ),
    (753,        2.533,      5507.553   ),
    (505,        4.583,      18849.228  ),
    (492,        4.205,      775.523    ),
    (357,        2.92,       0.067      ),
    (317,        5.849,      11790.629  ),
    (284,        1.899,      796.298    ),
    (271,        0.315,      10977.079  ),
    (243,        0.345,      5486.778   ),
    (206,        4.806,      2544.314   ),
    (205,        1.869,      5573.143   ),
    (202,        2.458,      6069.777   ),
    (156,        0.833,      213.299    ),
    (132,        3.411,      2942.463   ),
    (126,        1.083,      20.775     ),
    (115,        0.645,      0.98       ),
    (103,        0.636,      4694.003   ),
    (102,        0.976,      15720.839  ),
    (102,        4.267,      7.114      ),
    (99,         6.21,       2146.17    ),
    (98,         0.68,       155.42     ),
    (86,         5.98,       161000.69  ),
    (85,         1.3,        6275.96    ),
    (85,         3.67,       71430.7    ),
    (80,         1.81,       17260.15   ),
    (79,         3.04,       12036.46   ),
    (75,         1.76,       5088.63    ),
    (74,         3.5,        3154.69    ),
    (74,         4.68,       801.82     ),
    (70,         0.83,       9437.76    ),
    (62,         3.98,       8827.39    ),
    (61,         1.82,       7084.9     ),
    (57,         2.78,       6286.6     ),
    (56,         4.39,       14143.5    ),
    (56,         3.47,       6279.55    ),
    (52,         0.19,       12139.55   ),
    (52,         1.33,       1748.02    ),
    (51,         0.28,       5856.48    ),
    (49,         0.49,       1194.45    ),
    (41,         5.37,       8429.24    ),
    (41,         2.4,        19651.05   ),
    (39,         6.17,       10447.39   ),
    (37,         6.04,       10213.29   ),
    (37,         2.57,       1059.38    ),
    (36,         1.71,       2352.87    ),
    (36,         1.78,       6812.77    ),
    (33,         0.59,       17789.85   ),
    (30,         0.44,       83996.85   ),
    (30,         2.74,       1349.87    ),
    (25,         3.16,       4690.48    ),
)

_L1_table = (
    # (A, B, C),
    (628331966747,  0,         0          ),
    (206059,        2.678235,  6283.07585 ),
    (4303,          2.6351,    12566.1517 ),
    (425,           1.59,      3.523      ),
    (119,           5.796,     26.298     ),
    (109,           2.966,     1577.344   ),
    (93,            2.59,      18849.23   ),
    (72,            1.14,      529.69     ),
    (68,            1.87,      398.15     ),
    (67,            4.41,      5507.55    ),
    (59,            2.89,      5223.69    ),
    (56,            2.17,      155.42     ),
    (45,            0.4,       796.3      ),
    (36,            0.47,      775.52     ),
    (29,            2.65,      7.11       ),
    (21,            5.34,      0.98       ),
    (19,            1.85,      5486.78    ),
    (19,            4.97,      213.3      ),
    (17,            2.99,      6275.96    ),
    (16,            0.03,      2544.31    ),
    (16,            1.43,      2146.17    ),
    (15,            1.21,      10977.08   ),
    (12,            2.83,      1748.02    ),
    (12,            3.26,      5088.63    ),
    (12,            5.27,      1194.45    ),
    (12,            2.08,      4694       ),
    (11,            0.77,      553.57     ),
    (10,            1.3,       6286.6     ),
    (10,            4.24,      1349.87    ),
    (9,             2.7,       242.73     ),
    (9,             5.64,      951.72     ),
    (8,             5.3,       2352.87    ),
    (6,             2.65,      9437.76    ),
    (6,             4.67,      4690.48    ),
)

_L2_table = (
    # (A, B, C),
    (52919,  0,       0         ),
    (8720,   1.0721,  6283.0758 ),
    (309,    0.867,   12566.152 ),
    (27,     0.05,    3.52      ),
    (16,     5.19,    26.3      ),
    (16,     3.68,    155.42    ),
    (10,     0.76,    18849.23  ),
    (9,      2.06,    77713.77  ),
    (7,      0.83,    775.52    ),
    (5,      4.66,    1577.34   ),
    (4,      1.03,    7.11      ),
    (4,      3.44,    5573.14   ),
    (3,      5.14,    796.3     ),
    (3,      6.05,    5507.55   ),
    (3,      1.19,    242.73    ),
    (3,      6.12,    529.69    ),
    (3,      0.31,    398.15    ),
    (3,      2.28,    553.57    ),
    (2,      4.38,    5223.69   ),
    (2,      3.75,    0.98      ),
)

_L3_table = (
    # (A, B, C),
    (289,  5.844,  6283.076 ),
    (35,   0,      0        ),
    (17,   5.49,   12566.15 ),
    (3,    5.2,    155.42   ),
    (1,    4.72,   3.52     ),
    (1,    5.3,    18849.23 ),
    (1,    5.97,   242.73   ),
)

_L4_table = (
    # (A, B, C),
    (114,  3.142,  0        ),
    (8,    4.13,   6283.08  ),
    (1,    3.84,   12566.15 ),
)

_L5_table = (
    # (A, B, C),
    (1, 3.14, 0),
)

_B0_table = (
    # (A, B, C),
    (280,  3.199,  84334.662 ),
    (102,  5.422,  5507.553  ),
    (80,   3.88,   5223.69   ),
    (44,   3.7,    2352.87   ),
    (32,   4,      1577.34   ),
)

_B1_table = (
    # (A, B, C),
    (9,  3.9,   5507.55),
    (6,  1.73,  5223.69),
)

_R0_table = (
    # (A, B, C),
    (100013989,  0,          0          ),
    (1670700,    3.0984635,  6283.07585 ),
    (13956,      3.05525,    12566.1517 ),
    (3084,       5.1985,     77713.7715 ),
    (1628,       1.1739,     5753.3849  ),
    (1576,       2.8469,     7860.4194  ),
    (925,        5.453,      11506.77   ),
    (542,        4.564,      3930.21    ),
    (472,        3.661,      5884.927   ),
    (346,        0.964,      5507.553   ),
    (329,        5.9,        5223.694   ),
    (307,        0.299,      5573.143   ),
    (243,        4.273,      11790.629  ),
    (212,        5.847,      1577.344   ),
    (186,        5.022,      10977.079  ),
    (175,        3.012,      18849.228  ),
    (110,        5.055,      5486.778   ),
    (98,         0.89,       6069.78    ),
    (86,         5.69,       15720.84   ),
    (86,         1.27,       161000.69  ),
    (65,         0.27,       17260.15   ),
    (63,         0.92,       529.69     ),
    (57,         2.01,       83996.85   ),
    (56,         5.24,       71430.7    ),
    (49,         3.25,       2544.31    ),
    (47,         2.58,       775.52     ),
    (45,         5.54,       9437.76    ),
    (43,         6.01,       6275.96    ),
    (39,         5.36,       4694       ),
    (38,         2.39,       8827.39    ),
    (37,         0.83,       19651.05   ),
    (37,         4.9,        12139.55   ),
    (36,         1.67,       12036.46   ),
    (35,         1.84,       2942.46    ),
    (33,         0.24,       7084.9     ),
    (32,         0.18,       5088.63    ),
    (32,         1.78,       398.15     ),
    (28,         1.21,       6286.6     ),
    (28,         1.9,        6279.55    ),
    (26,         4.59,       10447.39   ),
)

_R1_table = (
    # (A, B, C),
    (103019,  1.10749,  6283.07585 ),
    (1721,    1.0644,   12566.1517 ),
    (702,     3.142,    0          ),
    (32,      1.02,     18849.23   ),
    (31,      2.84,     5507.55    ),
    (25,      1.32,     5223.69    ),
    (18,      1.42,     1577.34    ),
    (10,      5.91,     10977.08   ),
    (9,       1.42,     6275.96    ),
    (9,       0.27,     5486.78    ),
)

_R2_table = (
    # (A, B, C),
    (4359,  5.7846,  6283.0758 ),
    (124,   5.579,   12566.152 ),
    (12,    3.14,    0         ),
    (9,     3.63,    77713.77  ),
    (6,     1.87,    5573.14   ),
    (3,     5.47,    18849.23  ),
)

_R3_table = (
    # (A, B, C),
    (145,  4.273,  6283.076),
    (7,    3.92,   12566.15),
)

_R4_table = (
    # (A, B, C),
    (4, 2.56, 6283.08),
)

_L_tables = (
    _L0_table,
    _L1_table,
    _L2_table,
    _L3_table,
    _L4_table,
    _L5_table,
)

_B_tables = (
    _B0_table,
    _B1_table,
)

_R_tables = (
    _R0_table,
    _R1_table,
    _R2_table,
    _R3_table,
    _R4_table,
)
_nutation_table = {
    # ((Y0, Y1, Y2, Y3, Y4), a, b, c, d),
    ((0,   0,   0,   0,   1),  -171996,  -174.2,  92025,  8.9),
    ((-2,  0,   0,   2,   2),  -13187,   -1.6,    5736,   -3.1),
    ((0,   0,   0,   2,   2),  -2274,    -0.2,    977,    -0.5),
    ((0,   0,   0,   0,   2),  2062,     0.2,     -895,   0.5),
    ((0,   1,   0,   0,   0),  1426,     -3.4,    54,     -0.1),
    ((0,   0,   1,   0,   0),  712,      0.1,     -7,     0),
    ((-2,  1,   0,   2,   2),  -517,     1.2,     224,    -0.6),
    ((0,   0,   0,   2,   1),  -386,     -0.4,    200,    0),
    ((0,   0,   1,   2,   2),  -301,     0,       129,    -0.1),
    ((-2,  -1,  0,   2,   2),  217,      -0.5,    -95,    0.3),
    ((-2,  0,   1,   0,   0),  -158,     0,       0,      0),
    ((-2,  0,   0,   2,   1),  129,      0.1,     -70,    0),
    ((0,   0,   -1,  2,   2),  123,      0,       -53,    0),
    ((2,   0,   0,   0,   0),  63,       0,       0,      0),
    ((0,   0,   1,   0,   1),  63,       0.1,     -33,    0),
    ((2,   0,   -1,  2,   2),  -59,      0,       26,     0),
    ((0,   0,   -1,  0,   1),  -58,      -0.1,    32,     0),
    ((0,   0,   1,   2,   1),  -51,      0,       27,     0),
    ((-2,  0,   2,   0,   0),  48,       0,       0,      0),
    ((0,   0,   -2,  2,   1),  46,       0,       -24,    0),
    ((2,   0,   0,   2,   2),  -38,      0,       16,     0),
    ((0,   0,   2,   2,   2),  -31,      0,       13,     0),
    ((0,   0,   2,   0,   0),  29,       0,       0,      0),
    ((-2,  0,   1,   2,   2),  29,       0,       -12,    0),
    ((0,   0,   0,   2,   0),  26,       0,       0,      0),
    ((-2,  0,   0,   2,   0),  -22,      0,       0,      0),
    ((0,   0,   -1,  2,   1),  21,       0,       -10,    0),
    ((0,   2,   0,   0,   0),  17,       -0.1,    0,      0),
    ((2,   0,   -1,  0,   1),  16,       0,       -8,     0),
    ((-2,  2,   0,   2,   2),  -16,      0.1,     7,      0),
    ((0,   1,   0,   0,   1),  -15,      0,       9,      0),
    ((-2,  0,   1,   0,   1),  -13,      0,       7,      0),
    ((0,   -1,  0,   0,   1),  -12,      0,       6,      0),
    ((0,   0,   2,   -2,  0),  11,       0,       0,      0),
    ((2,   0,   -1,  2,   1),  -10,      0,       5,      0),
    ((2,   0,   1,   2,   2),  -8,       0,       3,      0),
    ((0,   1,   0,   2,   2),  7,        0,       -3,     0),
    ((-2,  1,   1,   0,   0),  -7,       0,       0,      0),
    ((0,   -1,  0,   2,   2),  -7,       0,       3,      0),
    ((2,   0,   0,   2,   1),  -7,       0,       3,      0),
    ((2,   0,   1,   0,   0),  6,        0,       0,      0),
    ((-2,  0,   2,   2,   2),  6,        0,       -3,     0),
    ((-2,  0,   1,   2,   1),  6,        0,       -3,     0),
    ((2,   0,   -2,  0,   1),  -6,       0,       3,      0),
    ((2,   0,   0,   0,   1),  -6,       0,       3,      0),
    ((0,   -1,  1,   0,   0),  5,        0,       0,      0),
    ((-2,  -1,  0,   2,   1),  -5,       0,       3,      0),
    ((-2,  0,   0,   0,   1),  -5,       0,       3,      0),
    ((0,   0,   2,   2,   1),  -5,       0,       3,      0),
    ((-2,  0,   2,   0,   1),  4,        0,       0,      0),
    ((-2,  1,   0,   2,   1),  4,        0,       0,      0),
    ((0,   0,   1,   -2,  0),  4,        0,       0,      0),
    ((-1,  0,   1,   0,   0),  -4,       0,       0,      0),
    ((-2,  1,   0,   0,   0),  -4,       0,       0,      0),
    ((1,   0,   0,   0,   0),  -4,       0,       0,      0),
    ((0,   0,   1,   2,   0),  3,        0,       0,      0),
    ((0,   0,   -2,  2,   2),  -3,       0,       0,      0),
    ((-1,  -1,  1,   0,   0),  -3,       0,       0,      0),
    ((0,   1,   1,   0,   0),  -3,       0,       0,      0),
    ((0,   -1,  1,   2,   2),  -3,       0,       0,      0),
    ((2,   -1,  -1,  2,   2),  -3,       0,       0,      0),
    ((0,   0,   3,   2,   2),  -3,       0,       0,      0),
    ((2,   -1,  0,   2,   2),  -3,       0,       0,      0),
}

_nutation_series = (
    (297.85036,  445267.111480, -0.0019142,  189474),
    (357.52772,  35999.0503040, -0.0001603, -300000),
    (134.96298,  477198.867398,  0.0086972,  56250 ),
    ( 93.27191,  483202.017538, -0.0036825,  327270),
    (125.04452, -1934.136261,    0.0020708,  450000),
)

_epsilon0_series = (
    84381.448,
    -4680.93,
    -1.55,
    1999.25,
    -51.38,
    -249.67,
    -39.05,
    7.12,
    27.87,
    5.79,
    2.45
)

def _from_helio_tables(tables, JME):
    coeffs = [
        sum(
            A * cos(B + C * JME)
            for (A, B, C) in table
        )
        for table in tables
    ]

    power_series_sum = sum(
        coeff * JME**power
        for power, coeff in enumerate(coeffs)
    ) / 1E8

    return power_series_sum



class Solar_Position:
    def __init__(self, julian):
        self._julian = julian

    @property
    def mean_heliocentric_longitude(self):
        return self._L

    @property
    def mean_heliocentric_latitude(self):
        return self._B

    @property
    def mean_radius(self):
        return self._R

    @property
    def mean_geocentric_longitude(self):
        return self._Theta

    @property
    def mean_geocentric_latitude(self):
        return self._beta

    @property
    def apparent_geocentric_longitude(self):
        return self._lambda

    @property
    def greenwich_sidereal_time(self):
        return self._nu

    @property
    def geocentric_right_ascension(self):
        return self._alpha

    @property
    def geocentric_declination(self):
        return self._delta

    @cached_property
    def _L(self):
        return degrees(
            _from_helio_tables(_L_tables, self._julian._JME)
        ) % 360

    @cached_property
    def _B(self):
        return degrees(
            _from_helio_tables(_B_tables, self._julian._JME)
        )

    @cached_property
    def _R(self):
        return _from_helio_tables(_R_tables, self._julian._JME)

    @cached_property
    def _Theta(self):
        return (self._L + 180) % 360

    @cached_property
    def _beta(self):
        return -self._B

    @cached_property
    def _lambda(self):
        return self._Theta + self._Delta_Psi + self._Delta_tau

    @cached_property
    def _X(self):
        return [
            c0 +
            c1 * self._julian._JCE +
            c2 * self._julian._JCE**2 +
            self._julian._JCE**3 / c3
            for c0, c1, c2, c3 in _nutation_series
        ]

    @cached_property
    def _Delta_Psi(self):
        # nutation in longitude (degrees)
        return sum(
            (a + b * self._julian._JCE) * sin(radians(sum(
                x * y
                for x, y in zip(self._X, Y)
            )))

            for Y, a, b, _, _ in _nutation_table
        ) / 36000000

    @cached_property
    def _Delta_epsilon(self):
        # nutation in obliquity
        return sum(
            (c + d * self._julian._JCE) * cos(radians(sum(
                x * y
                for x, y in zip(self._X, Y)
            )))

            for Y, _, _, c, d in _nutation_table
        ) / 36000000

    @cached_property
    def _Delta_tau(self):
        # aberration correction (degrees)
        return -20.4898 / 3600 / self._R

    @cached_property
    def _epsilon0(self):
        U = self._julian._JME / 10
        return sum(
            coeff * U**power
            for power, coeff in enumerate(_epsilon0_series)
        )

    @cached_property
    def _epsilon(self):
        return self._epsilon0 / 3600 + self._Delta_epsilon

    @cached_property
    def _nu0(self):
        # mean Greenwich sidereal time (degrees)
        return (
            280.46061837                                   +
            360.98564736629 * (self._julian._JD - 2451545) +
            0.000387933 * self._julian._JC**2              -
            self._julian._JC**3 / 38710000
        ) % 360

    @cached_property
    def _nu(self):
        # apparent Greenwich sidereal time (degrees)
        return self._nu0 + self._Delta_Psi * cos(radians(self._epsilon))

    @cached_property
    def _alpha(self):
        epsilon_rad = radians(self._epsilon)
        lambda_rad = radians(self._lambda)

        # sun right ascension (degrees)
        return degrees(atan2(
            (sin(lambda_rad) * cos(epsilon_rad) -
             tan(radians(self._beta)) * sin(epsilon_rad)),
            cos(lambda_rad)
        )) % 360

    @cached_property
    def _delta(self):
        beta_rad = radians(self._beta)
        epsilon_rad = radians(self._epsilon)

        # geocentric sun delination (degrees)
        return degrees(asin(
            sin(beta_rad) * cos(epsilon_rad) +
            cos(beta_rad) * sin(epsilon_rad) *
            sin(radians(self._lambda))
        ))

    @cached_property
    def _H(self):
        return (self._nu + self._sigma - self._alpha) % 360

    @cached_property
    def _H_prime(self):
        return self._H - self._Delta_alpha

    @cached_property
    def _xi(self):
        return 8.794 / 3600 / self._R

    @cached_property
    def _u(self):
        return atan(0.99664719 * tan(radians(self._phi)))

    @cached_property
    def _x(self):
        return (
            cos(self._u) +
            self._E / 6378140 * cos(radians(self._phi))
        )

    @cached_property
    def _y(self):
        return (
            0.99664719 * sin(self._u) +
            self._E / 6378140 * sin(self._phi)
        )

    @cached_property
    def _Delta_alpha(self):
        xi_radians = radians(self._xi)
        H_radians = radians(self._H)

        return degrees(atan2(
            -self._x * sin(xi_radians) * sin(H_radians),

            cos(radians(self._delta)) -
            self._x * sin(xi_radians) * cos(H_radians)
        ))

    @cached_property
    def _alpha_prime(self):
        return self._alpha + self._Delta_alpha

    @cached_property
    def _delta_prime(self):
        H_rad = radians(self._H)
        delta_rad = radians(self._delta)
        xi_rad = radians(self._xi)
        Delta_alpha_rad = radians(self._Delta_alpha)

        return degrees(atan2(
            (sin(delta_rad) - self._y * sin(xi_rad)) * cos(Delta_alpha_rad),
            cos(delta_rad) - self._x * sin(xi_rad) * cos(H_rad)
        ))

    @cached_property
    def _e0(self):
        phi_rad = radians(self._phi)
        delta_prime_rad = radians(self._delta_prime)
        H_prime_rad = radians(self._H_prime)
        return degrees(asin(
            sin(phi_rad) * sin(delta_prime_rad) +
            cos(phi_rad) * cos(delta_prime_rad) * cos(H_prime_rad)
        ))

    @cached_property
    def _Delta_e(self):
        # atmospheric refraction correction
        return self._P /1010 * 283 / (273 + self._T) * 1.02 / 60 / tan(
            radians(self._e0 + 10.3 / (self._e0 + 5.11)))

    @cached_property
    def _e(self):
        return self._e0 + self._Delta_e

    @cached_property
    def _theta(self):
        return 90 - self._e

    @cached_property
    def _Gamma(self):
        H_prime_rad = radians(self._H_prime)
        phi_rad = radians(self._phi)
        delta_prime_rad = radians(self._delta_prime)
        return degrees(atan2(
            sin(H_prime_rad),
            cos(H_prime_rad) * sin(phi_rad) -
            tan(delta_prime_rad) * cos(phi_rad)
        )) % 360

    @cached_property
    def _Phi(self):
        return (self._Gamma + 180) % 360

    @cached_property
    def _I(self):
        theta_rad = radians(self._theta)
        gamma_term = radians(self._Gamma - self._gamma)
        omega_rad = radians(self._omega)
        return degrees(acos(
            cos(theta_rad) * cos(omega_rad) +
            sin(omega_rad) * sin(theta_rad) * cos(gamma_term)
        ))

    @property
    def topocentric_zenith_angle(self):
        return self._theta

    @property
    def topocentric_elevation_angle(self):
        return self._e

    @property
    def topocentric_azimuth_angle(self):
        return self._Gamma

    @cached_property
    def equation_of_time(self):
        M = (
            280.4664567 +
            360007.6982779 * self._julian._JME +
            0.03032028 * self._julian._JME**2 +
            self._julian._JME**3 / 49931 +
            self._julian._JME**4 / -15300 +
            self._julian._JME**5 / -2000000
        )

        return (M - 0.0057183 - self._alpha +
                self._Delta_Psi * cos(radians(self._epsilon))) * 4 % 1440


class Observer_Solar_Position:
    def __init__(self, latitude, longitude, elevation,
                 annual_millibar, avg_celsius,
                 hori_slope, azimuth_angle):

        self._latitude = latitude
        self._longitude = longitude
        self._elevation = elevation
        self._annual_millibar = annual_millibar
        self._avg_celsius = avg_celsius
        self._hori_slope = hori_slope
        self._azimuth_angle = azimuth_angle


    def get_solar_position(self, julian):
        position = Solar_Position(julian)
        position._sigma = self._longitude
        position._phi = self._latitude
        position._E = self._elevation
        position._P = self._annual_millibar
        position._T = self._avg_celsius
        position._omega = self._hori_slope
        position._gamma = self._azimuth_angle

        return position
