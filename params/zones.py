
ZONES = [
    {
        "name": "P1",
        "corners": (  # cols, rows
            (140, 0),  # top left
            (30, 485),  # bottom left
            (200, 485),  # bottom right
            (265, 0),  # top right
        ),
        "key_idx": [0, 3], # idx of dominant point in bbox
        "bottom_level": 460,
        "top_level": 50,
        "ruler": [102, 125, 148, 173, 198],
        "ruler_step": 150,
        "ruler_equation": [-2.15, 6.27, -4.65e-3],
        "text_box": (10, 50),
        "photocells": (110, 380),
    },
    {
        "name": "P2",
        "corners": (  # cols, rows
            (360, 0),  # top left
            (465, 485),  # bottom left
            (650, 485),  # bottom right
            (490, 0),  # top right
        ),
        "key_idx": [0, 1],  # idx of dominant point in bbox
        "bottom_level": 460,
        "top_level": 170,
        "ruler": [212, 240, 270, 303, 338],
        "ruler_step": 150,
        "ruler_equation": [-0.907, 4.81, -5.82e-3],
        "text_box": (400, 50),
        "photocells": (170, 440)
    },
]
