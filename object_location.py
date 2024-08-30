import json
import math

def box_to_real_location(file_path='bounding_box_info.json', output_file_path='object_location.json'):
    # Read bounding box information from JSON file
    with open(file_path, 'r') as f:
        bounding_box_info = json.load(f)

    # Check if bounding box information is available
    if not bounding_box_info:
        print("No bounding box information found.")
        return

    real_values = {}
    real_coords = {}

    for object_name, box_info in bounding_box_info.items():
        # Calculate real distance and angle (calibration needed)
        unprocessed_x = float(box_info['center_x_ratio'])
        unprocessed_y = float(box_info['center_y_ratio'])
        real_x_val = real_x(unprocessed_x, unprocessed_y)
        real_y_val = real_y(unprocessed_x, unprocessed_y)
        
        pitch = 0


        # Print real distance and angle
        print(f"{object_name} - Real x: {real_x_val} mm")
        print(f"{object_name} - Real y: {real_y_val} mm")

        # Save real distance and angle to the dictionary
        real_values[object_name] = {
            "x": int(real_x_val),
            "y": int(real_y_val),
            "z": 45,
        }

        # Store the real coordinates for vector calculation
        real_coords[object_name] = (real_x_val, real_y_val)

    if "pen" in real_coords and "cap" in real_coords:
        pen_x, pen_y = real_coords["pen"]
        cap_x, cap_y = real_coords["cap"]
        vector_x = cap_x - pen_x
        vector_y = cap_y - pen_y
        real_values["vector"] = {
            "x": int(vector_x),
            "y": int(vector_y)
        }
        print(f"Vector from pen to cap - x: {vector_x} mm, y: {vector_y} mm")
    else:
        print("Pen or cap coordinates not found")

    # Save real values to another JSON file
    with open(output_file_path, 'w') as f:
        json.dump(real_values, f)

    print(f"Real values saved to {output_file_path}")
    return int(vector_x) * 3.375 / 5.25 / 2, int(vector_y) * 3.375 / 5.25 / 2

def real_x(x, y):
    return 10 * (31.9190 + (2.2406 * x) + (-64.4066 * y))

def real_y(x, y):
    return 10 * (45.0862 + (-40.3559 * x) + (-0.2801 * y))

if __name__ == '__main__':
    box_to_real_location()
