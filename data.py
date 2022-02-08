'''
Declare your Traits
and there Data Attributes here

    file: points to the Name of the actual image file [no need for extentsion in name, file must be .png]
    label: Call it what you want
    weight: Weigt Distribution of randomly choosing this trait [Sum of all Traits has to be 100]
'''

background = [
    {
        "file": "background_1",
        "label": "Checker",
        "weight": 30,
    },
    {
        "file": "background_2",
        "label": "Gradient",
        "weight": 10,
    },
    {
        "file": "background_3",
        "label": "Solid",
        "weight": 60,
    },

]

body = [
    {
        "file": "body_1",
        "label": "Green",
        "weight": 45,
    },
    {
        "file": "body_2",
        "label": "Blue",
        "weight": 25,
    },
    {
        "file": "body_3",
        "label": "Purple",
        "weight": 30,
    },
]

face = [
    {
        "file": "face_1",
        "label": "Bold Smile",
        "weight": 10,
    },
    {
        "file": "face_2",
        "label": "Happy",
        "weight": 25,
    },
    {
        "file": "face_3",
        "label": "Smiley",
        "weight": 60,
    },
    {
        "file": "face_4",
        "label": "Teeth Smile",
        "weight": 5,
    },
]

hat = [
    {
        "file": "",
        "label": "No Hat",
        "weight": 60,
    },
    {
        "file": "hat_1",
        "label": "Cylinder",
        "weight": 25,
    },
    {
        "file": "hat_2",
        "label": "Joker",
        "weight": 15,
    },
]