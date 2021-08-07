# face-match
face-recognition powered matching artificial inteligence

# Usage
```
python3 detector.py <path_to_img> <difference_value>

ex.) python3 detector.py ./face_to_check/ayami.jpg 0.5
```

- path_to_img: path to the face image file you want to match.
- difference value: indicates how close you want the matched faces to be. 0: exactly the same, 1: totally different person. Range 0.4 ~ 0.6 is frequently used.
