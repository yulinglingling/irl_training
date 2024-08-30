from scipy.optimize import least_squares
import numpy as np
import random
def rotation_matrix(roll, pitch, yaw):
    cos_roll = np.cos(roll)
    sin_roll = np.sin(roll)
    cos_pitch = np.cos(pitch)
    sin_pitch = np.sin(pitch)
    cos_yaw = np.cos(yaw)
    sin_yaw = np.sin(yaw)
    
    R_x = np.array([
        [1, 0, 0],
        [0, cos_roll, -sin_roll],
        [0, sin_roll, cos_roll]
    ])
    
    R_y = np.array([
        [cos_pitch, 0, sin_pitch],
        [0, 1, 0],
        [-sin_pitch, 0, cos_pitch]
    ])
    
    R_z = np.array([
        [cos_yaw, -sin_yaw, 0],
        [sin_yaw, cos_yaw, 0],
        [0, 0, 1]
    ])
    
    R = R_x @ R_y @ R_z
    return R


def residuals(vars):
    roll, pitch, yaw = vars
    cos_roll = np.cos(roll)
    sin_roll = np.sin(roll)
    cos_pitch = np.cos(pitch)
    sin_pitch = np.sin(pitch)
    cos_yaw = np.cos(yaw)
    sin_yaw = np.sin(yaw)
    
    x0, y0, z0 = (0, 0, np.sqrt(14))
    x, y, z = (1, 2, -3)
    
    eq1 = x0 * (cos_yaw * cos_roll) + y0 * (-cos_roll * sin_yaw) + z0 * (sin_pitch) - x
    eq2 = x0 * (sin_roll * sin_pitch * cos_yaw + cos_roll * sin_yaw) + y0 * (-sin_yaw * sin_pitch * sin_roll + cos_yaw * cos_roll) + z0 * (-sin_roll * cos_pitch) - y
    eq3 = x0 * (-cos_roll * sin_pitch * cos_yaw + sin_roll * sin_yaw) + y0 * (cos_roll * sin_pitch * sin_yaw + sin_roll * cos_yaw) + z0 * (cos_pitch * cos_roll) - z

    xx0, yy0, zz0 = x0 / 2, y0 / 2, z0 / 2
    xx, yy, zz = x / 2, y / 2, z / 2
    eq4 = xx0 * (cos_yaw * cos_roll) + yy0 * (-cos_roll * sin_yaw) + zz0 * (sin_pitch) - xx
    eq5 = xx0 * (sin_roll * sin_pitch * cos_yaw + cos_roll * sin_yaw) + yy0 * (-sin_yaw * sin_pitch * sin_roll + cos_yaw * cos_roll) + zz0 * (-sin_roll * cos_pitch) - yy
    eq6 = xx0 * (-cos_roll * sin_pitch * cos_yaw + sin_roll * sin_yaw) + yy0 * (cos_roll * sin_pitch * sin_yaw + sin_roll * cos_yaw) + zz0 * (cos_pitch * cos_roll) - zz


    return [eq1, eq2, eq3, eq4, eq5, eq6]
    # return [eq1, eq2, eq3]

r1 = random.random() / 10
r2 = random.random() / 10
r3 = random.random() / 10
print(r1, r2, r3)
initial_guess = [r1, r2, r3]
result = least_squares(residuals, initial_guess)
roll, pitch, yaw = tuple(result.x)

roll_deg = np.degrees(roll)
pitch_deg = np.degrees(pitch)
yaw_deg = np.degrees(yaw)



print(f"roll: {roll_deg % 360} degrees")
print(f"pitch: {pitch_deg % 360} degrees")
print(f"yaw: {yaw_deg % 360} degrees")


roll = np.radians(roll_deg% 360)
pitch = np.radians(pitch_deg% 360)
yaw = np.radians(yaw_deg % 360)
cos_roll = np.cos(roll)
sin_roll = np.sin(roll)
cos_pitch = np.cos(pitch)
sin_pitch = np.sin(pitch)
cos_yaw = np.cos(yaw)
sin_yaw = np.sin(yaw)
# print(cos_roll, sin_roll, cos_pitch, sin_pitch, cos_yaw, sin_yaw)
    
x0, y0, z0 = (0, 0, np.sqrt(14))
x, y, z = (1, 2, -3)
    
eq1 = x0 * (cos_yaw * cos_roll) + y0 * (-cos_roll * sin_yaw) + z0 * (sin_pitch) - x
eq2 = x0 * (sin_roll * sin_pitch * cos_yaw + cos_roll * sin_yaw) + y0 * (-sin_yaw * sin_pitch * sin_roll + cos_yaw * cos_roll) + z0 * (-sin_roll * cos_pitch) - y
eq3 = x0 * (-cos_roll * sin_pitch * cos_yaw + sin_roll * sin_yaw) + y0 * (cos_roll * sin_pitch * sin_yaw + sin_roll * cos_yaw) + z0 * (cos_pitch * cos_roll) - z

xx0, yy0, zz0 = x0 / 2, y0 / 2, z0 / 2
xx, yy, zz = x / 2, y / 2, z / 2
eq4 = xx0 * (cos_yaw * cos_roll) + yy0 * (-cos_roll * sin_yaw) + zz0 * (sin_pitch) - xx
eq5 = xx0 * (sin_roll * sin_pitch * cos_yaw + cos_roll * sin_yaw) + yy0 * (-sin_yaw * sin_pitch * sin_roll + cos_yaw * cos_roll) + zz0 * (-sin_roll * cos_pitch) - yy
eq6 = xx0 * (-cos_roll * sin_pitch * cos_yaw + sin_roll * sin_yaw) + yy0 * (cos_roll * sin_pitch * sin_yaw + sin_roll * cos_yaw) + zz0 * (cos_pitch * cos_roll) - zz
print(eq1, eq2, eq3)
print(eq4, eq5, eq6)
