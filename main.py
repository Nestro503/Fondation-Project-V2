import numpy as np
import time
import cv2
import cv2.aruco as aruco

ARUCO_DICT = {
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
}

# Constantes

# Mettre à 0 pour video, 1 pour photos
TEST = 1

# Mettre à 1 pour des prints de debug, 0 pour pas debug
DEBUG = 1

DISTANCE_COIN_ARUCO_X_MM = 2940
DISTANCE_COIN_Y_MM = 1940

TAILLE_ARUCO_COIN = 100
LONGUEUR_CALIBRATION = 90

IMAGE_LONGUEUR = 1920
IMAGE_LARGEUR = 1080

CONSTANTE_RECADRAGE = 10
IMAGE_RECADRE_LONGUEUR = 1600
IMAGE_RECADRE_LARGEUR = 900

RADIUS_ROBOT = 100




def trouver_arucos_coins(corners, ids):
    # Initialize all variables at the beginning of the function to ensure they have some default value.
    x_aruco_0 = y_aruco_0 = x_aruco_1 = y_aruco_1 = 0
    x_aruco_2 = y_aruco_2 = x_aruco_3 = y_aruco_3 = 0

    # Early return if there are not enough corners to process
    if len(corners) <= 1:
        # Return None or 0 for all values indicating the function cannot proceed with calculations
        return (None, None, None, None, None, None, None, None, None, None, None, None, None, None)

    # Processing starts here because there are more than 1 corner
    index_aruco_0 = np.where(ids == 0)[0]
    index_aruco_1 = np.where(ids == 1)[0]
    index_aruco_2 = np.where(ids == 2)[0]
    index_aruco_3 = np.where(ids == 3)[0]

    if index_aruco_0.size > 0:
        x_aruco_0, y_aruco_0 = corners[index_aruco_0[0]][0][0][0], corners[index_aruco_0[0]][0][0][1]
    if index_aruco_1.size > 0:
        x_aruco_1, y_aruco_1 = corners[index_aruco_1[0]][0][1][0], corners[index_aruco_1[0]][0][1][1]
    if index_aruco_2.size > 0:
        x_aruco_2, y_aruco_2 = corners[index_aruco_2[0]][0][2][0], corners[index_aruco_2[0]][0][2][1]
    if index_aruco_3.size > 0:
        x_aruco_3, y_aruco_3 = corners[index_aruco_3[0]][0][3][0], corners[index_aruco_3[0]][0][3][1]

    return x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3


def calcul_pixel_mm(x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3):
    # Initialize all variables at the beginning of the function to ensure they have some default value.
    pixel_distance_x = pixel_distance_y = 0
    mm_nbr_pixel_x = mm_nbr_pixel_y = pixel_nbr_mm_x = pixel_nbr_mm_y = 0


    # Calculate distances and ratios
    # Ensure there's a check to prevent division by zero
    if x_aruco_2 and x_aruco_3 and y_aruco_2 and y_aruco_3:
        pixel_distance_x = abs((x_aruco_2 - x_aruco_3) + (x_aruco_1 - x_aruco_0))/2
        pixel_distance_y = abs((y_aruco_2 - y_aruco_1) + (y_aruco_3 - y_aruco_0))/2

        print("[Inference] pixel_distance_x: {:.2f}, pixel_distance_y: {:.2f}".format(pixel_distance_x, pixel_distance_y))

        if pixel_distance_x == 0 or pixel_distance_y == 0:
            # Handle the case where division by zero would occur
            return (None, None, None, None, None, None)

        mm_nbr_pixel_x = float(pixel_distance_x) / DISTANCE_COIN_ARUCO_X_MM
        pixel_nbr_mm_x = 1 / mm_nbr_pixel_x if mm_nbr_pixel_x else None
        print("[Inference] mm_nbr_pixel_x: {:.2f}, pixel_nbr_mm_x: {:.2f}".format(mm_nbr_pixel_x, pixel_nbr_mm_x))
        mm_nbr_pixel_y = float(pixel_distance_y) / DISTANCE_COIN_Y_MM
        pixel_nbr_mm_y = 1 / mm_nbr_pixel_y if mm_nbr_pixel_y else None
        print("[Inference] mm_nbr_pixel_y: {:.2f}, pixel_nbr_mm_y: {:.2f}".format(mm_nbr_pixel_y, pixel_nbr_mm_y))

    else:
        # If we can't calculate distances because markers are not detected, return Nones or zeros
        return (None, None, None, None, None, None)

    return pixel_distance_x, mm_nbr_pixel_x, pixel_nbr_mm_x, pixel_distance_y, mm_nbr_pixel_y, pixel_nbr_mm_y


def calculate_pixel_distance(corners, ids):
    # Initialize all variables at the beginning of the function to ensure they have some default value.
    pixel_distance_x = pixel_distance_y = 0
    mm_nbr_pixel_x = mm_nbr_pixel_y = pixel_nbr_mm_x = pixel_nbr_mm_y = 0
    x_aruco_0 = y_aruco_0 = x_aruco_1 = y_aruco_1 = 0
    x_aruco_2 = y_aruco_2 = x_aruco_3 = y_aruco_3 = 0

    # Early return if there are not enough corners to process
    if len(corners) <= 1:
        # Return None or 0 for all values indicating the function cannot proceed with calculations
        return (None, None, None, None, None, None, None, None, None, None, None, None, None, None)

    # Processing starts here because there are more than 1 corner
    index_aruco_0 = np.where(ids == 0)[0]
    index_aruco_1 = np.where(ids == 1)[0]
    index_aruco_2 = np.where(ids == 2)[0]
    index_aruco_3 = np.where(ids == 3)[0]

    if index_aruco_0.size > 0:
        x_aruco_0, y_aruco_0 = corners[index_aruco_0[0]][0][0][0], corners[index_aruco_0[0]][0][0][1]
    if index_aruco_1.size > 0:
        x_aruco_1, y_aruco_1 = corners[index_aruco_1[0]][0][1][0], corners[index_aruco_1[0]][0][1][1]
    if index_aruco_2.size > 0:
        x_aruco_2, y_aruco_2 = corners[index_aruco_2[0]][0][2][0], corners[index_aruco_2[0]][0][2][1]
    if index_aruco_3.size > 0:
        x_aruco_3, y_aruco_3 = corners[index_aruco_3[0]][0][3][0], corners[index_aruco_3[0]][0][3][1]

    # Calculate distances and ratios
    # Ensure there's a check to prevent division by zero
    if x_aruco_2 and x_aruco_3 and y_aruco_2 and y_aruco_3:
        pixel_distance_x = abs(x_aruco_2 - x_aruco_3)
        pixel_distance_y = abs(y_aruco_2 - y_aruco_3)

        if pixel_distance_x == 0 or pixel_distance_y == 0:
            # Handle the case where division by zero would occur
            return (None, None, None, None, None, None, None, None, None, None, None, None, None, None)

        mm_nbr_pixel_x = float(pixel_distance_x) / DISTANCE_COIN_ARUCO_X_MM
        pixel_nbr_mm_x = 1 / mm_nbr_pixel_x if mm_nbr_pixel_x else None
        mm_nbr_pixel_y = float(pixel_distance_y) / DISTANCE_COIN_Y_MM
        pixel_nbr_mm_y = 1 / mm_nbr_pixel_y if mm_nbr_pixel_y else None
    else:
        # If we can't calculate distances because markers are not detected, return Nones or zeros
        return (None, None, None, None, None, None, None, None, None, None, None, None, None, None)

    return pixel_distance_x, mm_nbr_pixel_x, pixel_nbr_mm_x, pixel_distance_y, mm_nbr_pixel_y, pixel_nbr_mm_y, x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3


def coordrobot(corners, ids):
    x_robot = y_robot = None  # Initialize with None to handle cases where the marker isn't detected
    if len(corners) < 1:
        return None, None  # Early return if there are no corners to process
    index_robot = np.where(ids == 137)[0]
    if index_robot.size > 0:
        # Calculate the center of the ArUco marker
        marker_corners = corners[index_robot[0]][0]
        x_robot = np.mean(marker_corners[:, 0])
        y_robot = np.mean(marker_corners[:, 1])
    return x_robot, y_robot


def aruco_display(corners, ids, image):
    if len(corners) > 0:
        ids = ids.flatten()

        for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))

            (topLeft, topRight, bottomRight, bottomLeft) = corners

            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            # Map ArUco marker coordinates to game card coordinates
            if markerID == 0:
                mapped_coordinates = (topLeft[0], topLeft[1])
                cv2.circle(image, mapped_coordinates, 4, (0, 0, 255), -1)
            elif markerID == 1:
                mapped_coordinates = (topRight[0], topRight[1])
                cv2.circle(image, mapped_coordinates, 4, (0, 0, 255), -1)
            elif markerID == 2:
                mapped_coordinates = (bottomRight[0], bottomRight[1])
                cv2.circle(image, mapped_coordinates, 4, (0, 0, 255), -1)
            elif markerID == 3:
                mapped_coordinates = (bottomLeft[0], bottomLeft[1])
                cv2.circle(image, mapped_coordinates, 4, (0, 0, 255), -1)
            else:
                mapped_coordinates = (cX, cY)
                cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

            cv2.putText(image, "ID: {}".format(markerID), (topLeft[0], topLeft[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)

            # Display mapped coordinates on the image
            cv2.putText(image, "Mapped: ({},{})".format(mapped_coordinates[0], mapped_coordinates[1]),
                        (topLeft[0], topLeft[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Print mapped coordinates in the console
            print("[Inference] ArUco marker ID: {}, Mapped Coordinates: {}".format(markerID, mapped_coordinates))

    return image


def cercle_calib(x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3, mm_nbr_pixel_x, mm_nbr_pixel_y, image):
    if pixel_distance_x is not None and pixel_distance_y is not None and mm_nbr_pixel_x is not None and mm_nbr_pixel_y is not None:

        # Dessin calib blanc jaune cyan vert magenta rouge bleu
        for i in range(1, 8):
            cv2.circle(image, (
                int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + i * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 )), 6,
                       (255, 255, 255), 1)  # -1 pour remplir le cercle


        # Dessin calib des blancs
        for i in range(1, 11):
            cv2.circle(image, (
                int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - i * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 6,
                       (255, 255, 255), 1)  # -1 pour remplir le cercle

    return image


def recup_mask_hsv(img, img_hsv, circle_centers):

    # Get the mean HSV values for each circle
    mean_hsv_values = []
    for center in circle_centers:
        x, y = center
        circle_mask = np.zeros_like(img_hsv[:, :, 0], dtype=np.uint8)
        cv2.circle(circle_mask, center, 2, 255, -1)
        mean_hsv = cv2.mean(img_hsv, mask=circle_mask)[:3]
        mean_hsv_values.append(mean_hsv)


    # Print the mean HSV values
    for i in range(4):
        print(f"Circle {i + 1}: Mean HSV = {mean_hsv_values[i][0]} {mean_hsv_values[i][1]} {mean_hsv_values[i][2]}")


    for i in range(4):
        if i == 0:
            # Blanc
            bound_lower = np.array([mean_hsv_values[0][0] - 8, mean_hsv_values[0][1] -10 , mean_hsv_values[0][2] -10])
            bound_upper = np.array([mean_hsv_values[0][0] + 8, 255, 190])
            mask_blanc = cv2.inRange(img_hsv, bound_lower, bound_upper)
        if i == 1:
            # Cyan
            bound_lower = np.array([mean_hsv_values[1][0] - 8, mean_hsv_values[1][1] -10 , mean_hsv_values[1][2] -10])
            bound_upper = np.array([mean_hsv_values[1][0] + 8, 255, 190])
            mask_cyan = cv2.inRange(img_hsv, bound_lower, bound_upper)
        elif i == 2:
            # Rouge
            bound_lower = np.array([mean_hsv_values[2][0] - 8, mean_hsv_values[2][1] - 100, mean_hsv_values[2][2] - 100])
            bound_upper = np.array([mean_hsv_values[2][0] + 8, 255, 255])
            mask_rouge = cv2.inRange(img_hsv, bound_lower, bound_upper)
        elif i == 3:
            # Gris
            bound_lower = np.array([mean_hsv_values[3][0] - 8, mean_hsv_values[3][1] - 100, mean_hsv_values[3][2] - 100])
            bound_upper = np.array([mean_hsv_values[3][0] + 8, 255, 255])
            mask_gris = cv2.inRange(img_hsv, bound_lower, bound_upper)

    kernel = np.ones((7, 7), np.uint8)


    mask_blanc = cv2.morphologyEx(mask_blanc, cv2.MORPH_CLOSE, kernel)
    mask_blanc = cv2.morphologyEx(mask_blanc, cv2.MORPH_OPEN, kernel)

    display_mask_blanc = cv2.bitwise_and(img, img, mask=mask_blanc)

    mask_cyan = cv2.morphologyEx(mask_cyan, cv2.MORPH_CLOSE, kernel)
    mask_cyan = cv2.morphologyEx(mask_cyan, cv2.MORPH_OPEN, kernel)

    display_mask_cyan = cv2.bitwise_and(img, img, mask=mask_cyan)

    mask_rouge = cv2.morphologyEx(mask_rouge, cv2.MORPH_CLOSE, kernel)
    mask_rouge = cv2.morphologyEx(mask_rouge, cv2.MORPH_OPEN, kernel)

    display_mask_rouge = cv2.bitwise_and(img, img, mask=mask_rouge)

    mask_gris = cv2.morphologyEx(mask_gris, cv2.MORPH_CLOSE, kernel)
    mask_gris = cv2.morphologyEx(mask_gris, cv2.MORPH_OPEN, kernel)

    display_mask_gris = cv2.bitwise_and(img, img, mask=mask_gris)


    return mean_hsv_values, display_mask_blanc, display_mask_cyan, display_mask_rouge, display_mask_gris




    #-----------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------
    #-----------------------------------------LANCEMENT DU CODE CI-DESSOUS--------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------


def recup_mask_bgr(img, circle_centers):

    # Get the mean BGR values for each circle
    mean_bgr_values = []
    for center in circle_centers:
        x, y = center
        circle_mask = np.zeros_like(img[:, :, 0], dtype=np.uint8)
        cv2.circle(circle_mask, center, 2, 255, -1)
        mean_bgr = cv2.mean(img, mask=circle_mask)[:3]
        mean_bgr_values.append(mean_bgr)

    # Print the mean BGR values
    for i in range(4):
        print(f"Circle {i + 1}: Mean BGR = {mean_bgr_values[i][0]} {mean_bgr_values[i][1]} {mean_bgr_values[i][2]}")

    tolerance = 30

    for i in range(4):
        if i == 0:
            # Blanc
            bound_lower = np.array([mean_bgr_values[0][0] - tolerance, mean_bgr_values[0][1] - tolerance , mean_bgr_values[0][2] -tolerance])
            bound_upper = np.array([mean_bgr_values[0][0] + tolerance, mean_bgr_values[0][1] + tolerance , mean_bgr_values[0][2] +tolerance])
            mask_blanc = cv2.inRange(img, bound_lower, bound_upper)
        if i == 1:
            # Cyan
            bound_lower = np.array([mean_bgr_values[1][0] - tolerance, mean_bgr_values[1][1] -tolerance , mean_bgr_values[1][2] -tolerance])
            bound_upper = np.array([mean_bgr_values[1][0] + tolerance, mean_bgr_values[1][1] +tolerance , mean_bgr_values[1][2] +tolerance])
            mask_cyan = cv2.inRange(img, bound_lower, bound_upper)
        elif i == 2:
            # Rouge
            bound_lower = np.array([mean_bgr_values[2][0] - tolerance, mean_bgr_values[2][1] - tolerance, mean_bgr_values[2][2] - tolerance])
            bound_upper = np.array([mean_bgr_values[2][0] + tolerance, mean_bgr_values[2][1] + tolerance, mean_bgr_values[2][2] + tolerance])
            mask_rouge = cv2.inRange(img, bound_lower, bound_upper)
        elif i == 3:
            # Gris
            bound_lower = np.array([mean_bgr_values[3][0] - tolerance, mean_bgr_values[3][1] - tolerance, mean_bgr_values[3][2] - tolerance])
            bound_upper = np.array([mean_bgr_values[3][0] + tolerance, mean_bgr_values[3][1] + tolerance, mean_bgr_values[3][2] + tolerance])
            mask_gris = cv2.inRange(img, bound_lower, bound_upper)

    kernel = np.ones((7, 7), np.uint8)


    mask_blanc = cv2.morphologyEx(mask_blanc, cv2.MORPH_CLOSE, kernel)
    mask_blanc = cv2.morphologyEx(mask_blanc, cv2.MORPH_OPEN, kernel)
    display_mask_blanc = cv2.bitwise_and(img, img, mask=mask_blanc)

    mask_cyan = cv2.morphologyEx(mask_cyan, cv2.MORPH_CLOSE, kernel)
    mask_cyan = cv2.morphologyEx(mask_cyan, cv2.MORPH_OPEN, kernel)
    display_mask_cyan = cv2.bitwise_and(img, img, mask=mask_cyan)

    mask_rouge = cv2.morphologyEx(mask_rouge, cv2.MORPH_CLOSE, kernel)
    mask_rouge = cv2.morphologyEx(mask_rouge, cv2.MORPH_OPEN, kernel)
    display_mask_rouge = cv2.bitwise_and(img, img, mask=mask_rouge)

    mask_gris = cv2.morphologyEx(mask_gris, cv2.MORPH_CLOSE, kernel)
    mask_gris = cv2.morphologyEx(mask_gris, cv2.MORPH_OPEN, kernel)
    display_mask_gris = cv2.bitwise_and(img, img, mask=mask_gris)


    return mean_bgr_values, display_mask_blanc, display_mask_cyan, display_mask_rouge, display_mask_gris



aruco_type = "DICT_ARUCO_ORIGINAL"

arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters()

if TEST != 1:
    cap = cv2.VideoCapture("./Videos/mapvideo.mp4")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_LONGUEUR)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_LARGEUR)



nomImages = ("./Images/mapframevideo.jpg", "./Images/map3adam.jpg", "./Images/map1.jpg", )
nbImages = len(nomImages)

img = cv2.imread(nomImages[0])

cpt = 0
comptagemask = 0

while True:
    if TEST == 0:
        ret, img = cap.read()
    elif TEST == 1:
        img = cv2.imread(nomImages[cpt])
        if cv2.waitKey(1) & 0xFF == ord('p'):
            cpt += 1
            if cpt == nbImages:
                cpt = 0


    h, w, _ = img.shape
    print("Lecture d'image réussie. Shape: {}".format((h, w)))

    width = IMAGE_LONGUEUR
    height = IMAGE_LARGEUR
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)




    #-------------------------------RECUPERATION PREMIERE IMAGE ET DETECTION DES COINS----------------------------------
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    corners, ids, rejected = detector.detectMarkers(img)
    #cv2.imshow("Original Image", img)
    x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3 = trouver_arucos_coins(corners, ids)






    #----------------------------------------------RECADREMENT DE L'IMAGE----------------------------------------------
    pts1 = np.float32([[x_aruco_0 - CONSTANTE_RECADRAGE, y_aruco_0 - CONSTANTE_RECADRAGE],[x_aruco_1 + CONSTANTE_RECADRAGE, y_aruco_1 - CONSTANTE_RECADRAGE],[x_aruco_3 - CONSTANTE_RECADRAGE, y_aruco_3 + CONSTANTE_RECADRAGE],[x_aruco_2 + CONSTANTE_RECADRAGE, y_aruco_2 + CONSTANTE_RECADRAGE]])
    pts2 = np.float32([[0, 0], [IMAGE_RECADRE_LONGUEUR, 0], [0, IMAGE_RECADRE_LARGEUR], [IMAGE_RECADRE_LONGUEUR, IMAGE_RECADRE_LARGEUR]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    img_recadre = cv2.warpPerspective(img, M, (IMAGE_RECADRE_LONGUEUR, IMAGE_RECADRE_LARGEUR))

    #Copie de l'image recadré pour y afficher des infos dessus
    img_recadre_copy = img_recadre.copy()






    #---------------------------------DETECTION ARUCOS COIN ET ROBOT IMAGE RECADRE------------------------------------
    #Recuperation des arucos
    corners_recadre, ids_recadre, rejected = detector.detectMarkers(img_recadre)




    #Affichage des arucos
    img_recadre_copy = aruco_display(corners_recadre, ids_recadre, img_recadre_copy)



    #Recuperations des coordonnées des arucos de coins
    x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3 = trouver_arucos_coins(corners_recadre, ids_recadre)
    #Recuperations des coordonnées de l'aruco du robot
    x_robot, y_robot = coordrobot(corners_recadre, ids_recadre)
    #Calcul de conversion pixel/mm et autre
    pixel_distance_x, mm_nbr_pixel_x, pixel_nbr_mm_x, pixel_distance_y, mm_nbr_pixel_y, pixel_nbr_mm_y = calcul_pixel_mm(x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3)

    # Dessin hitbox robot (inutile pour l'instant)
    if x_robot is not None and y_robot is not None:
        cv2.circle(img_recadre_copy, (int(x_robot), int(y_robot)), int(RADIUS_ROBOT*(mm_nbr_pixel_x+mm_nbr_pixel_y)/2), (234,	158,	236), 3)
    else:
        print("ArUco marker 137 not detected.")



    #Affichage de cercles autour de calibrations de couleurs (utiles quand test de nouvelles images pour check si ok)
    #img_recadre_copy = cercle_calib(x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3, mm_nbr_pixel_x, mm_nbr_pixel_y, img_recadre_copy)





    #---------------------------------DETECTIONS DES COULEURS------------------------------------

    # Coordonnées des couleurs de calibrations nous intéressant
    pixel_blanc = (int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 1 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 ))
    pixel_cyan = (int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 3 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 ))
    pixel_rouge = (int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 6 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 ))
    pixel_gris =  (int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 9 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 ))


    #Affichage de cercle pour check si bons endroits
    cv2.circle(img_recadre_copy, pixel_blanc, 8, (255,255,255), 1)
    cv2.circle(img_recadre_copy, pixel_cyan, 8, (255,255,255), 1)
    cv2.circle(img_recadre_copy, pixel_rouge, 8, (255,255,255), 1)
    cv2.circle(img_recadre_copy, pixel_gris, 8, (255,255,255), 1)


    cv2.imshow("Image Recadre Copy avec Calib couleurs", img_recadre_copy)


    #Image en HSV pour y afficher des infos
    img_recadre_hsv = cv2.cvtColor(img_recadre, cv2.COLOR_BGR2HSV)
    #Copie de l'image recadré HSV pour y afficher des infos dessus
    img_recadre_hsv_copy = img_recadre_hsv.copy()



    # Define the centers of the circles (blanc, cyan, rouge, gris )
    circle_centers = [pixel_blanc, pixel_cyan, pixel_rouge, pixel_gris]
    circle_radius = 5


    print("comptagemask = ", comptagemask)
    if cv2.waitKey(1) & 0xFF == ord('n'):
        comptagemask += 1
        print("comptagemask = ", comptagemask)
        if comptagemask == 5:
            comptagemask = 0



            #------------------------PARTIE HSV---------------------------------

    mean_hsv_values, display_mask_blanc, display_mask_cyan, display_mask_rouge, display_mask_gris = recup_mask_hsv(img_recadre, img_recadre_hsv, circle_centers)

    #Affichage de cercles pour check si bonne couleurs
    for i in range(len(circle_centers)):
        cv2.circle(img_recadre_hsv_copy, (circle_centers[i][0], circle_centers[i][1] - 20), circle_radius, (mean_hsv_values[i][0],mean_hsv_values[i][1], mean_hsv_values[i][2]), -1)  # Draw filled circle

    #cv2.imshow("Image Recadre HSV Copy avec cercle couleurs", img_recadre_hsv_copy)

    top_row = cv2.hconcat([display_mask_blanc, display_mask_cyan])
    bottom_row = cv2.hconcat([display_mask_rouge, display_mask_gris])
    all_mask_hsv = cv2.vconcat([top_row, bottom_row])
    all_mask_hsv = cv2.resize(all_mask_hsv, (width, height), interpolation=cv2.INTER_CUBIC)
    cv2.imshow("All Mask HSV", all_mask_hsv)

    #Afficher les mask
    if comptagemask == 1:
        cv2.imshow("Masque Blanc HSV", display_mask_blanc)
    elif comptagemask == 2:
        cv2.imshow("Masque Cyan HSV", display_mask_cyan)
    elif comptagemask == 3:
        cv2.imshow("Masque Rouge HSV", display_mask_rouge)
    elif comptagemask == 4:
        cv2.imshow("Masque Gris HSV", display_mask_gris)




            #------------------------PARTIE BGR---------------------------------


    mean_bgr_values, mask_blanc, mask_cyan, mask_rouge, mask_gris = recup_mask_bgr(img_recadre, circle_centers)

    #Affichage de cercles pour check si bonne couleurs
    for i in range(len(circle_centers)):
        cv2.circle(img_recadre_copy, (circle_centers[i][0], circle_centers[i][1] - 20), circle_radius, (mean_bgr_values[i][0],mean_bgr_values[i][1], mean_bgr_values[i][2]), -1)  # Draw filled circle

    #cv2.imshow("Image Recadre Copy avec cercle couleurs", img_recadre_copy)

    top_row = cv2.hconcat([mask_blanc, mask_cyan])
    bottom_row = cv2.hconcat([mask_rouge, mask_gris])
    all_mask_bgr = cv2.vconcat([top_row, bottom_row])
    all_mask_bgr = cv2.resize(all_mask_bgr, (width, height), interpolation=cv2.INTER_CUBIC)

    cv2.imshow("All Mask BGR", all_mask_bgr)
    #Afficher les mask
    if comptagemask == 1:
        cv2.imshow("Masque Blanc BGR", mask_blanc)
    elif comptagemask == 2:
        cv2.imshow("Masque Cyan BGR", mask_cyan)
    elif comptagemask == 3:
        cv2.imshow("Masque Rouge BGR", mask_rouge)
    elif comptagemask == 4:
        cv2.imshow("Masque Gris BGR", mask_gris)




    print("")
    print("----------------------------------------------------------------------------------------------------------")
    print("")


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if TEST != 1:
    cap.release()
cv2.destroyAllWindows()