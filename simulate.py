import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from functools import partial
from mpl_toolkits.mplot3d.art3d import Line3DCollection

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

# def draw_cone(ax, origin, direction, height, radius):
#     num_segments = 30
#     theta = np.linspace(0, 2 * np.pi, num_segments)
#     x_circle = radius * np.cos(theta)
#     y_circle = radius * np.sin(theta)
    
#     circle = np.vstack((x_circle, y_circle, np.zeros(num_segments))).T
    
#     tip = np.array(origin) + np.array(direction) * height
#     base = np.array([origin + direction * radius])
#     cone_points = np.vstack((tip, base + circle))
    
#     faces = []
#     # faces.append([tip, cone_points[0 + 1], cone_points[(0 + 1) % num_segments + 1]])
#     for i in range(num_segments):
#         faces.append([tip, cone_points[i + 1], cone_points[(i + 1) % num_segments + 1]])
    
#     cone_poly = Poly3DCollection(faces, alpha=0.5, linewidths=1, edgecolors='b')
#     ax.add_collection3d(cone_poly)


def draw_cone(ax, origin, direction, height, radius, angle):
    num_segments = 30
    theta = np.linspace(0, 2 * np.pi, num_segments)
    x_circle = radius * np.cos(theta)
    y_circle = radius * np.sin(theta)
    
    circle = np.vstack((x_circle, y_circle, np.zeros(num_segments))).T
    
    tip = np.array(origin) + np.array(direction) * height
    base = np.array([origin + direction * radius])
    cone_points = np.vstack((tip, base + circle))
    
    faces = []
    for i in range(num_segments):
        faces.append([tip, cone_points[i + 1], cone_points[(i + 1) % num_segments + 1]])
    
    cone_poly = Poly3DCollection(faces, alpha=0.5, linewidths=1, edgecolors='b')
    ax.add_collection3d(cone_poly)
    
    # 在锥体上添加一条线，增强旋转效果
    line_angle = angle  # 选择一个角度，例如45度
    x_line = radius * np.cos(line_angle)
    y_line = radius * np.sin(line_angle)
    
    line_start = tip  # 从锥体顶点开始
    line_end = origin + direction * radius + np.array([x_line, y_line, 0])  # 到达底部圆周
    
    # 创建线的顶点
    line_points = np.array([[line_start, line_end]])
    
    # 创建 Line3DCollection
    line_collection = Line3DCollection(line_points, colors='r', linewidths=0.8)
    ax.add_collection3d(line_collection)




def update(num, pen_pos, angles, pen_vec, ax):
    global vector
    global r
    global p
    global y
    global stx
    global sty
    global stz
    global change
    size = 15
    for coll in ax.collections:
        coll.remove()
    
    x, yy, z = pen_pos[0], pen_pos[1], pen_pos[2]
    pos = np.array([x, yy, z]) - np.array(pen_vec) * 15
    ax.quiver(pos[0], pos[1], pos[2], pen_vec[0] * 15, pen_vec[1] * 15, pen_vec[2] * 15, color='r', label='pen', arrow_length_ratio=0.09)
    # 应用旋转矩阵
    # roll, pitch, yaw = (angles[0] + 360) % 360, (angles[1] + 360) % 360, (angles[2] + 360) % 360
    roll, pitch, yaw = angles
    R = rotation_matrix(math.radians(0), math.radians(0), math.radians(0))
    
    end_pos = np.array([x, yy, z]) + np.array(pen_vec) * size
    # if((stx, sty, stz) != end_pos):
    end_vec = (end_pos - np.array([0, 0, 0])) / np.linalg.norm(end_pos - np.array([0, 0, 0])) * size / 50
    if(math.fabs(stx - end_pos[0]) > 0.1 and math.fabs(sty - end_pos[1]) > 0.1 and math.fabs(stz - end_pos[2]) > 0.1):
        stx += end_vec[0]
        sty += end_vec[1]
        sty += end_vec[2]
    else: 
        stx, sty, stz = end_pos[0], end_pos[1], end_pos[2]
    
    if(y < yaw):
        
        if(yaw - y > 1): 
            if(change == True):
                print("\nstart rotating around z axis")
                change = False
            y += 1
            R = rotation_matrix(math.radians(0), math.radians(0), math.radians(1))
        else: 
            R = rotation_matrix(math.radians(0), math.radians(0), math.radians(yaw - y))
            y = yaw
            if(change == False):
                print("\nfinish rotating around z axis")
                change = True
    elif(y > yaw):
        if(yaw - y < -1): 
            if(change == True):
                print("\nstart rotating around z axis")
                change = False
            y -= 1
            R = rotation_matrix(math.radians(0), math.radians(0), math.radians(-1))
        else: 
            if(change == False):
                print("\nfinish rotating around z axis")
                change = True
            R = rotation_matrix(math.radians(0), math.radians(0), math.radians(yaw - y))
            y = yaw
    elif(p < pitch):
        if(pitch - p > 1): 
            if(change == True):
                print("\nstart rotating around y axis")
                change = False
            p += 1
            R = rotation_matrix(math.radians(0), math.radians(1), math.radians(0))
        else: 
            if(change == False):
                print("\nfinish rotating around y axis")
                change = True
            R = rotation_matrix(math.radians(0), math.radians(pitch - p), math.radians(0))
            p = pitch
    elif(p > pitch):
        if(pitch - p < -1): 
            if(change == True):
                print("\nstart rotating around y axis")
                change = False
            p -= 1
            R = rotation_matrix(math.radians(0), math.radians(-1), math.radians(0))
        else: 
            if(change == False):
                print("\nfinish rotating around y axis")
                change = True
            R = rotation_matrix(math.radians(0), math.radians(pitch - p), math.radians(0))
            p = pitch
    elif(r < roll):
        if(roll - r > 1): 
            if(change == True):
                print("\nstart rotating around x axis")
                change = False
            r += 1
            R = rotation_matrix(math.radians(1), math.radians(0), math.radians(0))
        else: 
            if(change == False):
                print("\nfinish rotating around x axis")
                change = True
            R = rotation_matrix(math.radians(roll - r), math.radians(0), math.radians(0))
            r = roll
    elif(r > roll):
        if(roll - r < -1): 
            if(change == True):
                print("\nstart rotating around x axis")
                change = False
            r -= 1
            R = rotation_matrix(math.radians(-1), math.radians(0), math.radians(0))
        else: 
            if(change == False):
                print("\nfinish rotating around x axis")
                change = True
            R = rotation_matrix(math.radians(roll - r), math.radians(0), math.radians(0))
            r = roll
    else: 
        R = rotation_matrix(math.radians(0), math.radians(0), math.radians(0))
        
    
    print("\r", r, p, y, end = '')

    vector = np.dot(R, vector)
    
    # dot._offsets3d = (vector[0:1], vector[1:2], vector[2:3])

    
    # 更新箭头的方向
    
    quiver = ax.quiver(0, 0, 0, vector[0] * size, vector[1] * size, vector[2] * size, color='b', arrow_length_ratio=0)
    # quiver.set_segments([[[0, 0, 0], vector]])
    if(r == roll and p == pitch and y == yaw):
        quiver.remove()
        # end_pos = np.array([x, yy, z]) - np.array(vector) * size
        # end_vec = (end_pos - np.array([0, 0, 0])) / np.linalg.norm(end_pos - np.array([0, 0, 0]))
        # if(math.fabs(stx - end_pos[0]) > 1 and math.fabs(sty - end_pos[1]) > 1 and math.fabs(stz - end_pos[2]) > 6):
        #     stx += end_vec[0]
        #     sty += end_vec[1]
        #     sty += end_vec[2]
        # else: 
        #     stx, sty, stz = end_pos[0], end_pos[1], end_pos[2]
        quiver = ax.quiver(stx, sty, stz, vector[0] * size, vector[1] * size, vector[2] * size, color='b', label='claw', arrow_length_ratio=0.2)
    else:
        quiver.remove()
        quiver = ax.quiver(stx, sty, stz, vector[0] * size, vector[1] * size, vector[2] * size, color='b', label='claw', arrow_length_ratio=0)
        draw_cone(ax, list(np.array([stx, sty, stz]) + vector * size), vector / np.linalg.norm(vector), 0.2 * 10, 0.05 * 10, math.radians(y))
        # quiver.set_segments([[[1, 0, 0], vector]])
    ax.legend(loc='upper right')
    return quiver

stx, sty, stz = 0, 0, 0
r, p, y = 0, 0, 0
vector = np.array([0, 0, 1])
change = True
def simulate(pen_pos, angles, vec_to_top):
    # 创建一个图形
    global vector 
    global r
    global p
    global y
    global stx
    global sty
    global stz
    global change
    vector = np.array([0.05, 0, 1])
    r, p, y = 0, 0, 0
    stx, sty, stz = 0, 0, 0
    change = True
    # 设置坐标轴范围
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-25, 25])
    ax.set_ylim([0, 35])
    ax.set_zlim([0, 40])
    
    # 添加标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # 创建动画
    ani = FuncAnimation(fig, partial(update, pen_pos=pen_pos, angles=angles, pen_vec = vec_to_top, ax = ax), frames=60, interval=100, blit=False)
    # ani.save('animation.gif', writer='pillow', fps=20)  # 如果要保存为 GIF 格式
    # 显示动画
    plt.show()
    
if(__name__ == "__main__"):
    simulate((15, 15, 15), (57, -64, -180), (1, 0, 0))


