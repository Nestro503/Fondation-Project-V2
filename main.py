import numpy as np
import time
import cv2

ARUCO_DICT = {
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
}

# Constantes
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

        # Dessin calib jaune
        cv2.circle(image, (
            int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 2 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib cyan
        cv2.circle(image, (
            int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 3 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib vert
        cv2.circle(image, (
            int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 4 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib magenta
        cv2.circle(image, (
            int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 5 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib rouge
        cv2.circle(image, (
            int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 6 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib bleu
        cv2.circle(image, (
            int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 7 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle



        ####################Dessins calib blancs !!
        # Dessin calib blanc 1
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 1 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib blanc 2
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 2 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib blanc 3
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 3 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib blanc 4
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 4 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib blanc 5
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 5 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib blanc 6
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 6 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib blanc 7
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 7 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib blanc 8
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 8 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib blanc 9
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 9 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle

        # Dessin calib blanc 10
        cv2.circle(image, (
            int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 10 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 )), 4,
                   (255, 255, 255), 2)  # -1 pour remplir le cercle


    return image




aruco_type = "DICT_ARUCO_ORIGINAL"

arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters()

# cap = cv2.VideoCapture("./Images/mapvideoframe.jpg")

cap = cv2.VideoCapture("./Videos/mapvideo.mp4")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_LONGUEUR)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_LARGEUR)



while cap.isOpened():

    ret, img = cap.read()

    h, w, _ = img.shape
    print("Lecture d'image réussie. Shape: {}".format((h, w)))

    '''
    width = 1920
    height = int(width * (h / w))
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    '''



    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

    corners, ids, rejected = detector.detectMarkers(img)



    cv2.imshow("Original Image", img)


    x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3 = trouver_arucos_coins(corners, ids)



    pts1 = np.float32([[x_aruco_0 - CONSTANTE_RECADRAGE, y_aruco_0 - CONSTANTE_RECADRAGE],[x_aruco_1 + CONSTANTE_RECADRAGE, y_aruco_1 - CONSTANTE_RECADRAGE],[x_aruco_3 - CONSTANTE_RECADRAGE, y_aruco_3 + CONSTANTE_RECADRAGE],[x_aruco_2 + CONSTANTE_RECADRAGE, y_aruco_2 + CONSTANTE_RECADRAGE]])
    pts2 = np.float32([[0, 0], [IMAGE_RECADRE_LONGUEUR, 0], [0, IMAGE_RECADRE_LARGEUR], [IMAGE_RECADRE_LONGUEUR, IMAGE_RECADRE_LARGEUR]])

    M = cv2.getPerspectiveTransform(pts1, pts2)


    img_recadre = cv2.warpPerspective(img, M, (IMAGE_RECADRE_LONGUEUR, IMAGE_RECADRE_LARGEUR))

    corners_recadre, ids_recadre, rejected = detector.detectMarkers(img_recadre)

    img_recadre = aruco_display(corners_recadre, ids_recadre, img_recadre)


    x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3 = trouver_arucos_coins(corners_recadre, ids_recadre)
    x_robot, y_robot = coordrobot(corners_recadre, ids_recadre)

    pixel_distance_x, mm_nbr_pixel_x, pixel_nbr_mm_x, pixel_distance_y, mm_nbr_pixel_y, pixel_nbr_mm_y = calcul_pixel_mm(x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3)

    # Check if coordinates are not None and draw the circle
    if x_robot is not None and y_robot is not None:
        cv2.circle(img_recadre, (int(x_robot), int(y_robot)), int(RADIUS_ROBOT*(mm_nbr_pixel_x+mm_nbr_pixel_y)/2), (234,	158,	236), 3)
    else:
        print("ArUco marker 137 not detected.")


    img_recadre = cercle_calib(x_aruco_0, y_aruco_0, x_aruco_1, y_aruco_1, x_aruco_2, y_aruco_2, x_aruco_3, y_aruco_3, mm_nbr_pixel_x, mm_nbr_pixel_y, img_recadre)








    # Coordonnées des pixels à vérifier
    pixel_rouge = (int(x_aruco_3 + TAILLE_ARUCO_COIN * mm_nbr_pixel_x + 6 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_3 ))
    pixel_gris =  (int(x_aruco_1 - TAILLE_ARUCO_COIN * mm_nbr_pixel_x - 9 * LONGUEUR_CALIBRATION * mm_nbr_pixel_x), int(y_aruco_1 ))

    # Obtenez la valeur BGR du pixel
    bgr_pixel_rouge = img_recadre[pixel_rouge[1], pixel_rouge[0]]
    bgr_pixel_gris = img_recadre[pixel_gris[1], pixel_gris[0]]

    # Dessinez un cercle avec la couleur du pixel
    cv2.circle(img_recadre, (int(IMAGE_RECADRE_LONGUEUR/2), int(IMAGE_RECADRE_LARGEUR/2)),
               10,
               (int(bgr_pixel_rouge[0]), int(bgr_pixel_rouge[1]), int(bgr_pixel_rouge[2])), -1)
    cv2.circle(img_recadre, (int(IMAGE_RECADRE_LONGUEUR/2 + 20), int(IMAGE_RECADRE_LARGEUR/2 + 20)),
               10,
               (int(bgr_pixel_gris[0]), int(bgr_pixel_gris[1]), int(bgr_pixel_gris[2])), -1)

    cv2.imshow("Image recadre", img_recadre)






    
    
    # Définir une tolérance pour la plage de couleur rouge autour du pixel de référence
    tolerance = 25  # Tolérance pour le rgb


    # Créer les bornes inférieure et supérieure pour le masque
    gris_lower = np.array(bgr_pixel_gris) - tolerance
    gris_upper = np.array(bgr_pixel_gris) + tolerance

    # Créer un masque qui détecte tous les pixels dans la plage de rouge définie
    mask_gris = cv2.inRange(img_recadre, gris_lower, gris_upper)

    # Remplacer la couleur rouge par du noir dans l'image originale
    img_recadre[mask_gris > 0] = [120, 120, 0]

    # Afficher l'image modifiée
    cv2.imshow("Image avec couleur de référence remplacée par du noir", img_recadre)




    '''
    # Convertir l'image BGR en HSV
    img_recadre_hsv = cv2.cvtColor(img_recadre, cv2.COLOR_BGR2HSV)

    # Obtenez la valeur HSV du pixel
    hsv_pixel_rouge = img_recadre_hsv[pixel_rouge[1], pixel_rouge[0]]

    # Définir des tolérances
    tolerance_hue = 10  # Tolérance pour la teinte
    tolerance_sat_val = 40  # Tolérance pour la saturation et la valeur

    teinte_rouge = hsv_pixel_rouge[0]
    saturation_rouge = hsv_pixel_rouge[1]
    valeur_rouge = hsv_pixel_rouge[2]


    # Bornes basées sur la teinte, la saturation, et la valeur du pixel rouge 
    rouge_lower_hsv = np.array([max(teinte_rouge - tolerance_hue, 0), max(saturation_rouge - tolerance_sat_val, 100), max(valeur_rouge - tolerance_sat_val, 100)])
    rouge_upper_hsv = np.array([min(teinte_rouge + tolerance_hue, 180), min(saturation_rouge + tolerance_sat_val, 255), min(valeur_rouge + tolerance_sat_val, 255)])


    # Créer un masque HSV qui détecte tous les pixels dans la plage définie
    mask_rouge_hsv = cv2.inRange(img_recadre_hsv, rouge_lower_hsv, rouge_upper_hsv)

    # Remplacer la couleur détectée par une couleur spécifique (par exemple, noir avec une teinte jaune)
    img_recadre[mask_rouge_hsv > 0] = [120, 120, 0]  # BGR

    # Afficher l'image modifiée
    cv2.imshow("Image HSV avec couleur de référence remplacée par du noir ", img_recadre)
    '''










    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()
