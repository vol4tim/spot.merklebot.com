from spot_controller import SpotController

with SpotController("admin", "2zqa8dgw7lor", "192.168.50.3") as sc:
    yaws = [(-1) ** (j % 2) * i / 10 for j in range(8) for i in range(-5, 6, 1)]
    pitches = [i / 10 for i in range(-5, 3, 1) for j in range(11)]
    rolls = [0] * len(yaws)
    sc.move_head_in_points(yaws, pitches, rolls)