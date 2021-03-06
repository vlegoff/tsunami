complexe = importeur.salle.creer_etendue("complexe")
complexe.origine = (20, 20)
obstacle = importeur.salle.obstacles["falaise"]

coords = [
    (20, 20),
    (21, 20),
    (22, 20),
    (23, 20),
    (24, 20),
    (25, 20),
    (20, 21),
    (20, 22),
    (20, 23),
    (20, 24),
    (20, 25),
    (19, 25),
    (19, 26),
    (18, 26),
    (17, 26),
    (19, 27),
    (17, 27),
    (17, 28),
    (18, 28),
    (19, 28),
    (20, 28),
    (21, 28),
    (22, 28),
    (23, 28),
    (24, 28),
    (24, 27),
    (24, 26),
    (23, 26),
    (23, 25),
    (23, 24),
    (24, 24),
    (25, 24),
    (25, 23),
    (23, 23),
    (25, 22),
    (22, 22),
    (23, 22),
    (25, 21),
]

for coord in coords:
    complexe.ajouter_obstacle(coord, obstacle)

complexe.trouver_contour()
