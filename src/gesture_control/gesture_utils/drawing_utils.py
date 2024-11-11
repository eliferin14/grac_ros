import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

def denormalize_landmarks(matrix, width, height):
    """Converts landmarks coordinates from normalized image coordinates to pixel coordinates

    Args:
        matrix (_type_): _description_
        width (_type_): _description_
        height (_type_): _description_

    Returns:
        _type_: _description_
    """    ''''''
    landmarks_pixel = np.empty((0,2), dtype=np.int16)
    
    for lm in matrix:
        pixel = np.zeros((1,2), dtype=np.int16)
        pixel[0,0] = int( lm[0] * width)
        pixel[0,1] = int( lm[1] * height)
        landmarks_pixel = np.vstack([landmarks_pixel, pixel])
    
    return landmarks_pixel

def draw_landmarks(frame, landmarks, point_color, line_color):
    """Draw the lanmdarks on the image

    Args:
        frame (opencv image): _description_
        landmarks (np matrix): pixel coordinates of the landmarks
        point_color (_type_): _description_
        line_color (_type_): _description_
    """    ''''''
    # Draw all the landmarks
    for lm in landmarks:
        #print((lm[0], lm[1]))
        cv2.circle(frame, (lm[0], lm[1]), radius=3, color=point_color, thickness=-1)
        cv2.circle(frame, (lm[0], lm[1]), radius=4, color=line_color, thickness=1)
        

hand_connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
    (0, 5),  # Thumb to wrist
    (5, 6), (6, 7), (7, 8),  # Index finger
    (5, 9),  # Index finger to wrist
    (9, 10), (10, 11), (11, 12),  # Middle finger
    (9, 13),  # Middle finger to wrist
    (13, 14), (14, 15), (15, 16),  # Ring finger
    (13, 17),  # Ring finger to wrist
    (17, 18), (18, 19), (19, 20),  # Pinky
    (0, 17)
]
hand_connections = list(mp_hands.HAND_CONNECTIONS)
def draw_hand(frame, landmarks, point_color, line_color):
    """Draw the hand landmarks and connections

    Args:
        frame (_type_): _description_
        landmarks (_type_): _description_
        point_color (_type_): _description_
        line_color (_type_): _description_
    """    ''''''
    
    if landmarks.shape[0] == 0: return 
    
    # Draw connections
    for (p1, p2) in hand_connections:
        cv2.line(frame, landmarks[p1], landmarks[p2], line_color, 2)
    
    # Draw all the landmarks
    draw_landmarks(frame, landmarks, point_color, line_color)

pose_connections = pose_connections = list(mp_pose.POSE_CONNECTIONS)
def draw_pose(frame, landmarks, point_color, line_color):
    """Draw the pose landmarks and connections

    Args:
        frame (_type_): _description_
        landmarks (_type_): _description_
        point_color (_type_): _description_
        line_color (_type_): _description_
    """    
    # Draw connections
    for (p1, p2) in pose_connections:
        cv2.line(frame, landmarks[p1], landmarks[p2], line_color, 2)
    
    # Draw all the landmarks
    draw_landmarks(frame, landmarks, point_color, line_color)