import face_recognition
import matplotlib.pyplot as plt
import glob
from tqdm import tqdm
import os
import sys
import numpy as np

args = sys.argv

file_paths = []

known_face_encodings = []



def draw_face_locations(img, locations):
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_axis_off()
    for i, (top, right, bottom, left) in enumerate(locations):
        # 長方形を描画する。
        w, h = right - left, bottom - top
        ax.add_patch(plt.Rectangle((left, top), w, h, ec="r", lw=2, fill=None))
    plt.show()


# 名前と特徴量をjsonファイルから読み取る

import json

# Opening JSON file

with open('tokyo_hot_full.json') as f:
    print("loading database...")
    data = json.load(f)
    file_paths = list(data.keys())
    known_face_encodings = list(data.values())

print("database loading over.")


'''
# 名前と特徴量をcsvファイルから読み取る

import csv

csv_file = "./210806_features.csv"

with open(csv_file, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        file_names.append(row[0]) #取得したい列番号を指定（0始まり）
        known_face_encodings.append(np.array(row[1].replace( '\n' , '').strip("[]").split(), dtype="float64"))

'''



# 認証する人物の顔の画像を読み込む。

face_img_to_check = face_recognition.load_image_file(args[1])

# 顔の領域を取得し、出力
face_loc_to_check = face_recognition.face_locations(face_img_to_check, model="cnn")
assert len(face_loc_to_check) == 1, "画像から顔の検出に失敗したか、2人以上の顔が検出されました"
# draw_face_locations(face_img_to_check, face_loc_to_check)

# 顔の領域から特徴量を抽出する: 認識する人物
(face_encoding_to_check,) = face_recognition.face_encodings(
    face_img_to_check, face_loc_to_check
)



'''
# 顔を認識する
matches = face_recognition.compare_faces(known_face_encodings, face_encoding_to_check)
print(matches)
'''

dists = face_recognition.face_distance(known_face_encodings, face_encoding_to_check)
print(dists)


# 合致する顔を記録
matched_names = []
n = 0
print("faces with difference smaller than {}: ".format(args[2]))
for i in dists:
  if i < float(args[2]):
    print(str(n) + ". " + file_paths[n])
    matched_names.append(file_paths[n])
  n = n + 1

# 合致する顔を出力
for matched_name in matched_names:
    img = face_recognition.load_image_file(matched_name)
    loc = face_recognition.face_locations(img, model="cnn")
    draw_face_locations(img, loc)
