import numpy as np
def point_and_vec(orbbec_left, brio_mid, orbbec_mid, brio_right):
    # dot1 on circle
    x1, y1, x2, y2 = orbbec_left[0][0], orbbec_left[0][1], brio_mid[0][0], brio_mid[0][1]
    x = 23.5733 + (-0.0001 * x1) + (0.0028 * y1) + (-0.0376 * x2) + (-0.0065 * y2)
    y = 35.2200 + (-0.0234 * x1) + (-0.0211 * y1) + (0.0040 * x2) + (0.0315 * y2)
    z = 20.3877 + (-0.0070 * x1) + (-0.0085 * y1) + (0.0004 * x2) + (-0.0253 * y2)
    real_dot1 = (x, y, z)
    # dot2 on circle and vector
    x1, y1, x2, y2 = orbbec_mid[0][0], orbbec_mid[0][1], brio_right[0][0], brio_right[0][1]
    x = 23.5733 + (-0.0001 * x1) + (0.0028 * y1) + (-0.0376 * x2) + (-0.0065 * y2)
    y = 35.2200 + (-0.0234 * x1) + (-0.0211 * y1) + (0.0040 * x2) + (0.0315 * y2)
    z = 20.3877 + (-0.0070 * x1) + (-0.0085 * y1) + (0.0004 * x2) + (-0.0253 * y2)
    real_dot2 = (x, y, z)
    # dot 3 on vector
    x1, y1, x2, y2 = orbbec_mid[1][0], orbbec_mid[1][1], brio_right[1][0], brio_right[1][1]
    x = 23.5733 + (-0.0001 * x1) + (0.0028 * y1) + (-0.0376 * x2) + (-0.0065 * y2)
    y = 35.2200 + (-0.0234 * x1) + (-0.0211 * y1) + (0.0040 * x2) + (0.0315 * y2)
    z = 20.3877 + (-0.0070 * x1) + (-0.0085 * y1) + (0.0004 * x2) + (-0.0253 * y2)
    real_dot3 = (x, y, z)

# def circle_center(p1, p2, pen_vec):
    """
    input: p1, p2, pen_vec are arrays of [x, y, z]
    p1: midpoint of the tip of the cap from orbbec 
    p2: midpoint of the tip of the cap from mx brio
    -> return array of [x, y, z] of center
    """
    print("real dot 1, real dot 2, real dot 3", real_dot1, real_dot2, real_dot3)
    p1, p2, pen_vec = np.array(real_dot2), np.array(real_dot1), np.array((real_dot2[0] - real_dot3[0], real_dot2[1] - real_dot3[1], real_dot2[2] - real_dot3[2]))
    # Calculate the vector from p2 to p1
    plane_vec = np.array(p1) - np.array(p2)

    # Calculate the cross product of pen_vec and plane_vec
    cross_product = np.cross(pen_vec, plane_vec)
    # print("Cross Product:", cross_product)

    # Calculate the midpoint of p1 and p2
    midpoint = (p1 + p2) / 2
    # print(f"midpoint: {midpoint}")

    # Calculate the distance between p1 and p2
    distance = np.linalg.norm(p1 - p2)
    # print(f"distance: {distance}")

    # Calculate the magnitude of cross_product
    magnitude = np.linalg.norm(cross_product)
    # print(f"magnitude: {cross_product}")

    # Calculate the center of the circle
    center = np.array(midpoint) + [(distance / 2) / magnitude] * np.array(cross_product)
    # print(f"center: {center}")
    return tuple(center), tuple(pen_vec)