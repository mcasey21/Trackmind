import cv2
import numpy as np
from skimage.morphology import skeletonize

# Expirement one
# Convert image to grayscale, applies Gaussian Blur then 
# applies canny (where pixel brightness changes sharply)
# def process_image(image):

#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
#     edges = cv2.Canny(blurred_image, 50, 150)

#     # Identifies connected outlines
#     contours, hierarchy = cv2.findContours(
#         edges,
#         cv2.RETR_LIST,
#         cv2.CHAIN_APPROX_SIMPLE
#     )

#     # Creates a copy and draws detected contours
#     contour_image = image.copy()

#     # Calculates perimiter of each contour in pixels (try to filter out background items)
#     large_contours = [
#         contour for contour in contours
#         if cv2.arcLength(contour, True) > 150
#     ]

#     cv2.drawContours(contour_image, large_contours, -1, (0, 255, 0), 2)

#     return contour_image

# Expirement two
# Uses HSV segmentation to identify track then 
# Morphological closing to try fix imperfections in asphalt segmentation
# def process_image(image):
#     hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     lower_asphalt = np.array([0, 0, 60])
#     upper_asphalt = np.array([180, 65, 230])

#     mask = cv2.inRange(hsv_image, lower_asphalt, upper_asphalt)

#     # Run morpho close
#     kernel = np.ones((5, 5), np.uint8)
#     cleaned_mask = cv2.morphologyEx(
#         mask,
#         cv2.MORPH_CLOSE,
#         kernel
#     )

#     # Run morpho open
#     opening_kernel = np.ones((3, 3), np.uint8)

#     cleaned_mask = cv2.morphologyEx(
#         cleaned_mask,
#         cv2.MORPH_OPEN,
#         opening_kernel
#     )

#     # Try to get largest white area on image and only display this
#     num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
#     cleaned_mask,
#     connectivity=8
#     )
#     print("Connected components:", num_labels - 1)

#     # Safety check - if opencv detects no white regions
#     if num_labels <= 1:
#         return np.zeros_like(cleaned_mask)

#     largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

#     track_mask = np.zeros_like(cleaned_mask)
#     track_mask[labels == largest_label] = 255

#     # Distance transform experiment
#     # distance_map = cv2.distanceTransform(
#     #     track_mask,
#     #     cv2.DIST_L2,
#     #     5
#     # )
#     # print("Maximum distance:", distance_map.max())
#     # normalised_map = cv2.normalize(
#     #     distance_map, None, 0, 255, cv2.NORM_MINMAX
#     # )
#     # distance_visual = normalised_map.astype(np.uint8)

#     # Skeletonisation experiment
#     # binary_mask = track_mask > 0
#     # skeleton = skeletonize(binary_mask)
#     # skeleton_image = skeleton.astype(np.uint8) * 255

#     return track_mask

def process_image(image):
    # HSV segmentation to threshold the image
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_asphalt = np.array([0, 0, 60])
    upper_asphalt = np.array([180, 65, 230])
    mask = cv2.inRange(hsv_image, lower_asphalt, upper_asphalt)

    # Opening and closing to remove specks and fill in the holes
    # Closing
    closing_kernel = np.ones((5, 5), np.uint8)
    cleaned_mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        closing_kernel
    )

    # Opening
    opening_kernel = np.ones((3, 3), np.uint8)
    cleaned_mask = cv2.morphologyEx(
        cleaned_mask,
        cv2.MORPH_OPEN,
        opening_kernel
    )

    # Contour image
    contours, hierarchy = cv2.findContours(
        cleaned_mask,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Sort contours to get 2 largest (outer and inner boundary)
    sorted_contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True
    )
    largest_contours = sorted_contours[:2]

    # Create contour image and draw in green
    contour_image = image.copy()
    cv2.drawContours(
        contour_image,
        largest_contours,
        -1,
        (0, 255, 0),
        2
    )

    return contour_image
