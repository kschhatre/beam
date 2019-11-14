package beam.utils.beam_to_matsim.visualization

import beam.utils.beam_to_matsim.events.BeamPathTraversal

import scala.collection.mutable

object visualization_35_person1_alternatives {
  val personUid: String = "026303-2015000142533-0-3364370"

  val alternative0_ride_hail: Seq[BeamPathTraversal] = Seq(
    BeamPathTraversal(
      29182,
      "rideHailVehicle-026301-2016000858086-1-3746736",
      "rideHailAgent-026301-2016000858086-1-3746736",
      "Car",
      "CAR",
      Seq[Int](88932, 3126, 3128, 815, 813, 811, 809, 807, 805, 105, 50500, 50502, 50504, 50506, 50508, 55750, 10863,
        10861, 10859, 10857, 27578, 43138, 43140, 51884, 86776, 71225, 46077, 46075, 46073, 46071, 46069, 52103, 89823,
        83221, 26967, 83225, 26965, 46052, 89141, 10803, 51676, 83246, 83242, 51678, 83250, 85931, 51859, 3939, 7648,
        7650, 7652, 7654, 7656, 7658, 7660, 7662, 7664, 7666, 7668, 7670, 7672, 7674, 7676, 7678, 7680, 7682, 49416,
        49418, 49420, 94340, 49422, 49424, 91218, 81297, 20661, 51684, 51828, 8401, 12545, 13545, 13543, 13541, 13539,
        11777, 8392, 26187, 20579, 20577, 20575, 20573, 20571, 20569, 52359, 92999, 5995, 5546, 54679, 54677, 54675,
        54673, 54671, 54668, 54648, 64358, 64376, 30245, 10027, 10025, 10023, 52170, 90950, 90930, 90926, 52420, 54696,
        64360, 89664, 36426, 36428, 36430, 54542, 89720, 47249, 88561, 47247, 47238, 88556, 47240, 47242, 47244, 47232,
        52785, 52783, 52781, 52779, 52777, 52775, 52773, 52771, 52769, 52767, 88605, 88601, 52765, 52763, 88597, 88593,
        52761, 52759, 57075),
      Seq[Double](6, 3, 5, 9, 11, 19, 6, 5, 5, 11, 5, 4, 5, 5, 5, 2, 3, 5, 5, 10, 3, 6, 45, 1, 2, 1, 14, 9, 19, 19, 19,
        4, 2, 17, 1, 18, 1, 8, 1, 18, 9, 2, 1, 7, 1, 1, 8, 13, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 5,
        2, 1, 5, 1, 4, 2, 2, 4, 3, 25, 6, 15, 5, 6, 7, 8, 12, 1, 10, 2, 6, 33, 7, 2, 5, 2, 1, 4, 8, 19, 2, 1, 1, 1, 4,
        2, 2, 4, 5, 8, 8, 8, 2, 9, 2, 1, 4, 2, 2, 1, 9, 18, 6, 16, 2, 8, 2, 7, 1, 11, 1, 1, 1, 6, 8, 8, 8, 8, 8, 8, 8,
        8, 8, 2, 1, 2, 2, 13, 2, 1, 14, 1, 26)
    )
  )

  val alternative1_ride_hail_pooled: Seq[BeamPathTraversal] = Seq(
    BeamPathTraversal(
      29565,
      "rideHailVehicle-026301-2014000082333-0-2601704",
      "rideHailAgent-026301-2014000082333-0-2601704",
      "Car",
      "CAR",
      Seq[Int](3125, 88929, 55759, 50576, 6845, 11018, 11020, 67107, 67105, 67103, 67101, 78014, 78018, 78020, 11372,
        11374, 11376, 11378, 11701, 11699, 11697, 11695, 86539, 11693, 48884, 67034, 86530, 67036, 67038, 67040, 67042,
        67044, 67046, 67048, 67050, 67052, 67054, 13300, 2427, 22212, 22214, 22216, 22218, 11675, 54284, 54286, 54288,
        41244, 8796, 8798, 54319, 54317, 8802, 9320, 55906, 19427, 24244, 10816, 2288, 53109, 53107, 53105, 53103,
        53101, 40841, 7880, 7882, 7884, 5163, 5161, 3582, 3584, 3586, 3588, 40552, 40554, 40556, 20198, 20200, 4280,
        4282, 4284, 4286, 36597, 36595, 36649, 36647, 36645, 80116, 36641, 36639, 90017, 78443, 78441, 78444, 78446,
        78448, 78450, 78452, 55812, 55814, 55816, 55817, 55815, 55813, 89435, 49399, 49397, 42741, 20192, 20194, 28286,
        28288, 28290, 48968, 48970, 86744, 75472, 51892, 53728, 23294, 41206, 41208, 86520, 41484, 55803, 55801, 11698,
        11700, 11702, 11704, 78011, 78009, 78007, 78005, 78018, 78020, 11371, 11369, 11367, 11365, 8670, 10091, 15802,
        50506, 50508, 55750, 10863, 10861, 10859, 10857, 27578, 43138, 43140, 51884, 86776, 71225, 46077, 46075, 46073,
        46071, 46069, 52103, 89823, 83221, 26967, 83225, 26965, 46052, 89141, 10803, 51676, 83246, 83242, 51678, 83250,
        85931, 51859, 3939, 7648, 7650, 7652, 7654, 7656, 7658, 7660, 7662, 7664, 7666, 7668, 7670, 7672, 7674, 7676,
        7678, 7680, 7682, 49416, 49418, 49420, 94340, 49422, 49424, 91218, 81297, 20661, 51684, 51828, 8401, 12545,
        13545, 13543, 13541, 13539, 11777, 8392, 26187, 20579, 20577, 20575, 20573, 20571, 20569, 52359, 92999, 5995,
        5546, 54679, 54677, 54675, 54673, 54671, 54668, 54648, 64358, 64376, 30245, 10027, 10025, 10023, 52170, 90950,
        90930, 90926, 52420, 54696, 64360, 89664, 36426, 36428, 36430, 54542, 89720, 47249, 64634, 89943, 34237, 34235,
        89939, 34233, 89935, 34231, 34229, 89931, 34227, 4921, 4919, 4917, 4915, 4913, 23212, 85834, 1109, 1107, 1105,
        1103, 1101, 1099, 3361, 3359, 29810, 4728, 4730, 4732, 57066, 85210, 57068, 57070),
      Seq[Double](29, 1, 3, 6, 15, 7, 8, 8, 7, 7, 7, 2, 2, 4, 1, 7, 8, 9, 7, 7, 5, 4, 6, 1, 7, 2, 6, 6, 9, 5, 9, 7, 7,
        8, 7, 4, 3, 7, 5, 4, 4, 5, 5, 10, 5, 5, 1, 2, 1, 9, 6, 1, 5, 16, 2, 9, 3, 2, 9, 18, 18, 18, 11, 13, 4, 7, 7, 7,
        12, 18, 4, 5, 7, 1, 4, 4, 1, 1, 7, 8, 8, 9, 8, 7, 12, 8, 9, 8, 9, 9, 9, 1, 8, 8, 10, 3, 1, 3, 1, 1, 5, 1, 1, 5,
        1, 1, 1, 3, 40, 10, 29, 2, 3, 2, 8, 1, 3, 2, 2, 1, 2, 1, 2, 45, 15, 2, 14, 7, 7, 6, 8, 5, 7, 6, 1, 2, 4, 8, 2,
        7, 7, 11, 9, 14, 5, 5, 2, 3, 5, 5, 10, 3, 6, 45, 1, 2, 1, 14, 9, 19, 19, 19, 4, 2, 17, 1, 18, 1, 8, 1, 18, 9, 2,
        1, 7, 1, 1, 8, 13, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 5, 2, 1, 5, 1, 4, 2, 2, 4, 3, 25, 6,
        15, 5, 6, 7, 8, 12, 1, 10, 2, 6, 33, 7, 2, 5, 2, 1, 4, 8, 19, 2, 1, 1, 1, 4, 2, 2, 4, 5, 8, 8, 8, 2, 9, 2, 1, 4,
        2, 2, 1, 9, 18, 6, 16, 2, 8, 8, 1, 7, 4, 4, 1, 1, 8, 8, 8, 12, 8, 8, 8, 8, 8, 1, 7, 7, 3, 5, 4, 8, 3, 1, 3, 3,
        1, 1, 1, 4, 3, 1, 3)
    )
  )

  val alternative2_bike: Seq[BeamPathTraversal] = Seq(
    BeamPathTraversal(
      29160,
      "bike-10001-1",
      "026303-2015000142533-0-3364370",
      "BIKE-DEFAULT",
      "BIKE",
      Seq[Int](55761, 27548, 34050, 50490, 50492, 50494, 50496, 50498, 50500, 50502, 50504, 50506, 50508, 55750, 10863,
        10861, 10859, 10857, 27578, 43138, 43140, 52074, 88515, 52087, 88495, 88523, 52085, 52083, 88535, 52081, 52079,
        52077, 88505, 52073, 8909, 8907, 8905, 34160, 34162, 34164, 91368, 34166, 91364, 34168, 34170, 34172, 91336,
        91340, 34174, 34176, 91408, 34178, 91404, 34180, 34182, 34184, 34186, 91360, 34188, 91356, 34190, 34192, 34194,
        91328, 34196, 91372, 34198, 91384, 34200, 91380, 34202, 34204, 34206, 34208, 91420, 20664, 25238, 20662, 36504,
        91332, 36506, 36508, 36510, 36512, 36514, 91324, 36516, 93448, 36518, 91426, 36520, 36522, 36524, 91416, 91412,
        64350, 64352, 64354, 89736, 36467, 36465, 1119, 1117, 1115, 87617, 87621, 87613, 48169, 4921, 4919, 4917, 4915,
        4913, 4911, 68882, 6172, 6174, 6176, 23358, 54504, 57066, 85210, 57068, 57070, 57074),
      Seq[Double](19, 18, 25, 40, 15, 3, 12, 8, 11, 9, 10, 10, 10, 4, 7, 10, 10, 21, 6, 13, 5, 3, 6, 23, 5, 16, 2, 41,
        39, 2, 41, 41, 2, 39, 41, 41, 42, 20, 9, 17, 2, 3, 17, 19, 19, 3, 4, 14, 22, 17, 2, 2, 17, 12, 7, 7, 7, 6, 6, 7,
        6, 19, 12, 6, 6, 14, 10, 2, 2, 6, 19, 15, 4, 18, 2, 3, 16, 3, 7, 2, 19, 15, 5, 11, 2, 8, 5, 2, 12, 2, 13, 3, 29,
        4, 3, 2, 17, 19, 4, 9, 9, 17, 30, 39, 3, 3, 33, 3, 18, 17, 18, 18, 18, 17, 3, 2, 1, 2, 34, 25, 10, 6, 1, 6, 64)
    )
  )

  val alternative3_walk_transit_bike_bus: Seq[BeamPathTraversal] = Seq(
    BeamPathTraversal(
      29682,
      "bike-10001-1",
      "026303-2015000142533-0-3364370",
      "BIKE-DEFAULT",
      "BIKE",
      Seq[Int](55761, 88929, 55759, 88859, 55757, 88855, 55755, 88833, 55753, 45453, 88809, 45451, 45449, 45447, 45445,
        45443, 88769, 45441, 88867, 45439, 45437, 45435, 45433, 64869, 45429, 88825, 50857, 55065, 55063, 55061, 55059,
        88849, 55057, 88845, 55055, 55053, 55051, 55049, 55047, 55045, 88881, 55043, 55041, 88901, 50855, 50853, 88885,
        49845, 52031, 88875, 88789, 52029, 52037, 52035, 52033, 88813, 88803, 22631, 22629, 22627, 22625, 22623, 22621,
        34214, 91399),
      Seq[Double](19, 2, 14, 26, 2, 2, 5, 32, 2, 3, 2, 3, 6, 9, 7, 10, 18, 2, 3, 22, 4, 5, 8, 10, 2, 7, 2, 13, 1, 10,
        21, 7, 7, 4, 6, 4, 15, 2, 3, 26, 2, 10, 24, 8, 8, 3, 9, 11, 4, 7, 9, 2, 15, 16, 13, 2, 3, 6, 16, 15, 13, 5, 15,
        2, 2)
    ),
    BeamPathTraversal(
      30240,
      "SF:7686588",
      "TransitDriverAgent-SF:7686588",
      "DEFAULT",
      "BUS",
      Seq[Int](34214, 91396, 91392, 34148, 10030, 91376, 91377, 10031, 34150, 93716, 34152, 34154, 34156, 91352, 34158,
        91348, 34160, 34162, 34164, 91368, 34166, 91364, 34168, 34170, 34172, 91336, 91340, 34174, 34176, 91408, 34178,
        91404, 34180, 34182, 34184, 34186, 91360, 34188, 91356, 34190, 34192, 34194, 91328, 34196, 91372, 34198, 91384,
        34200, 91380, 34202, 34204, 34206, 34208, 91420, 20664, 25238, 20662, 36504, 91332, 36506, 36508, 36510, 36512,
        36514, 91324, 36516, 93448, 36518, 91426, 36520, 36522, 36524, 91416),
      Seq[Double](8, 8, 8, 8, 8, 4, 6, 6, 6, 6, 6, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 13, 13, 13, 14, 7, 7, 7, 7,
        7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 7, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 8, 8, 8, 8, 8, 8, 8, 8, 10, 10,
        10, 10, 10, 10, 10, 0)
    ),
    BeamPathTraversal(
      30836,
      "body-026303-2015000142533-0-3364370",
      "026303-2015000142533-0-3364370",
      "BODY-TYPE-DEFAULT",
      "WALK",
      Seq[Int](91414, 91412, 64350, 64352, 64354, 89736, 36467, 36465, 1119, 1117, 1115, 87617, 87621, 87613, 48169,
        4921, 4919, 4917, 4915, 4913, 4911, 15713, 54695, 54693, 54511, 54509, 54507, 54504, 57066, 85210, 57068,
        57070),
      Seq[Double](2, 3, 2, 17, 19, 4, 9, 9, 17, 30, 39, 3, 3, 33, 3, 18, 17, 18, 18, 18, 17, 12, 7, 16, 1, 1, 2, 25, 10,
        6, 1, 6)
    )
  )

  val alternative4_walk: Seq[BeamPathTraversal] = Seq(
    BeamPathTraversal(
      29160,
      "body-026303-2015000142533-0-3364370",
      "026303-2015000142533-0-3364370",
      "BODY-TYPE-DEFAULT",
      "WALK",
      Seq[Int](88933, 3125, 27548, 34050, 50490, 50492, 50494, 50496, 50498, 50500, 50502, 50504, 50506, 50508, 55750,
        10863, 10861, 10859, 10857, 27578, 43138, 43140, 52074, 88515, 52087, 88495, 88523, 52085, 52083, 88535, 52081,
        52079, 52077, 88505, 52073, 8909, 8907, 8905, 34160, 34162, 34164, 91368, 34166, 91364, 34168, 34170, 34172,
        91336, 91340, 34174, 34176, 91408, 34178, 91404, 34180, 34182, 34184, 34186, 91360, 34188, 91356, 34190, 34192,
        34194, 91328, 34196, 91372, 34198, 91384, 34200, 91380, 34202, 34204, 34206, 34208, 91420, 20664, 25238, 20662,
        36504, 91332, 36506, 36508, 36510, 36512, 36514, 91324, 36516, 93448, 36518, 91426, 36520, 36522, 36524, 91416,
        91412, 64350, 64352, 64354, 89736, 36467, 36465, 1119, 1117, 1115, 87617, 87621, 87613, 48169, 4921, 4919, 4917,
        4915, 4913, 4911, 15713, 54695, 54693, 54511, 54509, 54507, 54504, 57066, 85210, 57068, 57070, 57074),
      Seq[Double](51, 11, 67, 96, 151, 57, 10, 45, 31, 40, 35, 36, 37, 38, 13, 24, 38, 37, 78, 21, 50, 18, 11, 23, 88,
        17, 60, 6, 155, 149, 7, 156, 155, 7, 149, 155, 155, 158, 77, 33, 66, 8, 8, 65, 73, 71, 9, 16, 52, 83, 65, 8, 7,
        65, 47, 24, 24, 26, 23, 23, 27, 22, 72, 45, 22, 23, 52, 36, 6, 7, 23, 71, 56, 15, 67, 5, 10, 59, 10, 24, 4, 72,
        57, 17, 40, 7, 28, 17, 6, 45, 8, 49, 9, 110, 15, 9, 7, 66, 71, 15, 33, 34, 66, 116, 148, 10, 10, 125, 11, 66,
        66, 66, 66, 67, 65, 46, 24, 60, 4, 4, 5, 95, 38, 23, 2, 21, 245)
    )
  )

  val alternative5_walk_transit_bus: Seq[BeamPathTraversal] = Seq(
    BeamPathTraversal(
      29347,
      "body-026303-2015000142533-0-3364370",
      "026303-2015000142533-0-3364370",
      "BODY-TYPE-DEFAULT",
      "WALK",
      Seq[Int](88933, 3125, 88929, 55759, 88859, 55757, 88855, 88857),
      Seq[Double](51, 11, 8, 53, 98, 8, 8, 2)
    ),
    BeamPathTraversal(
      29535,
      "SF:7597760",
      "TransitDriverAgent-SF:7597760",
      "DEFAULT",
      "BUS",
      Seq[Int](88855, 55755, 88833, 55753, 45453, 88809, 45451, 45449, 45447, 45445, 45443, 88769, 45441, 88867, 45439,
        45437, 45435, 45433, 64869, 45429, 88825, 50857, 55065, 55063, 55061, 55059, 88849, 55057, 88845, 55055, 55053,
        55051, 55049, 55047, 55045, 88881, 55043, 55041, 88901, 50855, 50853, 88885, 49845, 52031, 88875, 88789, 52029,
        52037, 52035, 52033, 88813, 88803, 22631, 22629, 22627, 22625, 22623, 22621),
      Seq[Double](7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 18, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
        8, 8, 8, 8, 8, 8, 8, 8, 30, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11)
    ),
    BeamPathTraversal(
      30060,
      "body-026303-2015000142533-0-3364370",
      "026303-2015000142533-0-3364370",
      "BODY-TYPE-DEFAULT",
      "WALK",
      Seq[Int](88908, 34214, 91399),
      Seq[Double](2, 8, 5)
    ),
    BeamPathTraversal(
      30240,
      "SF:7686588",
      "TransitDriverAgent-SF:7686588",
      "DEFAULT",
      "BUS",
      Seq[Int](34214, 91396, 91392, 34148, 10030, 91376, 91377, 10031, 34150, 93716, 34152, 34154, 34156, 91352, 34158,
        91348, 34160, 34162, 34164, 91368, 34166, 91364, 34168, 34170, 34172, 91336, 91340, 34174, 34176, 91408, 34178,
        91404, 34180, 34182, 34184, 34186, 91360, 34188, 91356, 34190, 34192, 34194, 91328, 34196, 91372, 34198, 91384,
        34200, 91380, 34202, 34204, 34206, 34208, 91420, 20664, 25238, 20662, 36504, 91332, 36506, 36508, 36510, 36512,
        36514, 91324, 36516, 93448, 36518, 91426, 36520, 36522, 36524, 91416, 91412, 64350, 64352, 64354, 89736, 34238,
        34239, 89733, 19111, 89729, 19109, 89725, 89717, 47279, 47250, 47252, 38644, 54703, 54701, 54699, 54696, 64360,
        89664, 89713, 19115, 89709, 89701, 89705, 19113, 87793, 8941, 87789, 88547, 8939, 15750, 15736, 15737, 15752,
        52350, 52352, 93026, 93030, 7725, 6860, 6861, 87199, 7723, 87177, 87181, 7721, 87383, 1077, 87379, 1075, 88573,
        93297, 3041, 88585, 88581, 3039, 3037, 3035, 88577, 3033, 39976, 85798, 39978, 85826, 74810, 74812),
      Seq[Double](8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 12, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 13, 13, 13, 14, 7, 7, 7,
        7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 7, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5, 8, 8, 8, 8, 8, 8, 8,
        8, 6, 10, 10, 10, 10, 10, 10, 10, 6, 6, 6, 6, 6, 6, 9, 8, 8, 8, 8, 13, 12, 12, 12, 10, 6, 6, 6, 6, 6, 6, 6, 6,
        6, 10, 10, 10, 10, 9, 9, 9, 9, 8, 9, 9, 8, 8, 7, 8, 8, 8, 8, 9, 7, 7, 7, 4, 10, 10, 10, 10, 14, 12, 12, 12, 10,
        20, 20, 20, 17, 17, 18, 10, 10, 10, 8)
    ),
    BeamPathTraversal(
      31516,
      "body-026303-2015000142533-0-3364370",
      "026303-2015000142533-0-3364370",
      "BODY-TYPE-DEFAULT",
      "WALK",
      Seq[Int](93204, 93202, 88605, 88601, 52765, 52763, 88597, 88593, 52761, 52759),
      Seq[Double](1, 10, 5, 16, 11, 106, 10, 8, 115, 4)
    )
  )

  lazy val vehicleIds: mutable.HashSet[String] = {
    def getVehicleId(pte: BeamPathTraversal) = pte.vehicleId
    val alts = {
      alternative0_ride_hail.map(getVehicleId) ++
      alternative1_ride_hail_pooled.map(getVehicleId) ++
      alternative2_bike.map(getVehicleId) ++
      alternative3_walk_transit_bike_bus.map(getVehicleId) ++
      alternative4_walk.map(getVehicleId) ++
      alternative5_walk_transit_bus.map(getVehicleId)
    }

    mutable.HashSet[String](alts: _*)
  }
}
