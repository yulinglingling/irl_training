import numpy as np
from scipy.spatial.transform import Rotation as R

def euler_to_quaternion(roll, pitch, yaw):
    # Convert Euler angles (in degrees) to quaternion
    r = R.from_euler('xyz', [roll, pitch, yaw], degrees=True)
    return r.as_quat()

def quaternion_to_euler(quat):
    # Convert quaternion to Euler angles (in degrees)
    r = R.from_quat(quat)
    return r.as_euler('xyz', degrees=True)

def quaternion_apply_to_vector(quat, vector=np.array([0, 0, 1])):
    # Apply the quaternion rotation to a vector
    r = R.from_quat(quat)
    return r.apply(vector)

def vector_to_quaternion(v):
    # Normalize the input vector
    v = v / np.linalg.norm(v)
    # The initial orientation vector (aligned with Z-axis)
    z_axis = np.array([0, 0, 1])
    
    # Find the rotation quaternion to align z_axis to vector v
    r = R.align_vectors([v], [z_axis])[0]
    return r.as_quat()

def quaternion_to_euler_angles(quat):
    # Convert quaternion to Euler angles (in degrees)
    return quaternion_to_euler(quat)

if __name__ == "__main__":
    """
    euler angle和vector之間的轉換要拿Quaternion當中繼站
    """
    # Test vector
    vector = np.array([0, 1, -1])  # Example vector
    
    # Convert vector to quaternion that aligns Z-axis with the vector
    quat = vector_to_quaternion(vector)
    print(f"Input vector: {vector}")
    
    # Convert quaternion to roll, pitch, yaw
    roll, pitch, yaw = quaternion_to_euler_angles(quat)
    
    print(f"Quaternion: {quat}")
    print(f"Roll: {roll} degrees, Pitch: {pitch} degrees, Yaw: {yaw} degrees")
    
    # Convert Euler angles to quaternion
    quat = euler_to_quaternion(roll, pitch, yaw)
    
    # Apply quaternion rotation to initial vector [0, 0, 1]
    target_vector = quaternion_apply_to_vector(quat)
    
    print(f"Quaternion: {quat}")
    print(f"Target vector: {target_vector}")