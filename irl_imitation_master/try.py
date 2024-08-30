x_distance, y_distance, z_distance = 5, 5, 5;
def pos_3Dto1D(pos):
    """
        input:
          column-major 2d position
        returns:
          1d index
    """
    return pos[0] * (x_distance * y_distance) + pos[1] * x_distance + pos[2];

def pos_1Dto3D(idx):
    """
        input:
          1d idx
        returns:
          2d column-major position
    """
    z = idx // (x_distance * y_distance);
    y = idx % (x_distance * y_distance) // x_distance;
    x = idx % (x_distance * y_distance) % x_distance;
    return (z, y, x)

dir = [(1, 0, 0), (-1, 0, 0), (0, 0, -1), (0, 0, 1), (0, -1, 0), (0, 1, 0), (0, 0, 0)]
up = 0;
down = 1;
left = 2;
right = 3;
front = 4;
back = 5;
start_x, start_y, start_z = 1, 1, 1;
end_x, end_y, end_z = 3, 4, 3;
bfs = [{'x': start_x, 'y': start_y, 'z': start_z, 'from': -1, 'dis': 0}];
route = {};
visited = {};

# for i in range(125): visited[i] = False;
for i in range(z_distance):
    for j in range(y_distance):
        for k in range(x_distance):
            visited[(i, j, k)] = False
# visited[pos_3Dto1D(start_z, start_y, start_x)] = True;
ending = 0
while(len(bfs)):
    print("hi")
    cur_point = bfs.pop(0);
    print(cur_point)
    x0, y0, z0, dis = cur_point['x'], cur_point['y'], cur_point['z'], cur_point['dis']
    if(ending == 1): break
    if(x0 == end_x and y0 == end_y and z0 == end_z): 
        print("end!")
        break;
    # if(visited[pos_3Dto1D((z0, y0, x0))]): 
    if(visited[(z0, y0, x0)] == True):
        bfs.pop(0);
        continue;
    
    # visited[pos_3Dto1D((z0, y0, x0))] = True
    visited[(z0, y0, x0)] = True
    for i in range(len(dir) - 1):
        next_z, next_y, next_x, next_dis = z0 + dir[i][0], y0 + dir[i][1], x0 + dir[i][2], dis + 1
        if(x0 == end_x and y0 == end_y and z0 == end_z): 
            route[(next_z, next_y, next_x)] = (z0, y0, x0)
            print("end!")
            ending = 1;
            break;
        if(cur_point['z'] + dir[i][0] < 0 or cur_point['z'] + dir[i][0] >= z_distance or cur_point['y'] + dir[i][1] < 0 or cur_point['y'] + dir[i][1] >= y_distance or cur_point['x'] + dir[i][2] < 0 or cur_point['x'] + dir[i][2] >= x_distance):
            continue; 
        bfs.append({'x': next_x, 'y': next_y, 'z': next_z, 'from': -1, 'dis': -1})
        # route[pos_3Dto1D((next_z, next_y, next_x))] = (z0, x0, y0)
        route[(next_z, next_y, next_x)] = (z0, y0, x0)

print(route[(end_z, end_y, end_x)])
print(route)
# tmpz, tmpy, tmpx = end_z, end_y, end_x
# while(tmpz != start_z or tmpy != start_y or tmpx != start_x):
#     print(tmpz, tmpy, tmpx);
#     tmpz, tmpy, tmpx = route[(tmpz, tmpy, tmpx)][0], route[(tmpz, tmpy, tmpx)][1], route[(tmpz, tmpy, tmpx)][2];



        





