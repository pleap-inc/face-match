import face_recognition
import matplotlib.pyplot as plt
import glob
import json
import array 
import sys
from tqdm import tqdm

args = sys.argv
# フォルダ内の全画像ファイルのパスを取得
file_paths = []

files = glob.glob("./tokyo_hot/*")
bar_analyze_img = tqdm(total = len(files))
print("____________________start appending file paths__________________")
for file in files:
    file_paths.append(file)
    bar_analyze_img.update(1)
print("____________________appending file paths ends__________________")
# 保存されている人物の顔の画像を読み込む。
known_face_imgs = []
print("____________________start appending img files__________________")
i = 0

file_names = []

for path in file_paths:
    img = face_recognition.load_image_file(path)
    file_names.append(path)
    known_face_imgs.append(img)
    if i % 10 == 0:
      print("###")
    print("###", end="")
    i = i + 1
    
print("\n____________________appending img files end__________________")

# 認証する人物の顔の画像を読み込む。
face_img_to_check = face_recognition.load_image_file(args[1])

# 顔の画像から顔の領域を検出する。

known_face_locs = [] 

bar_analyze_img = tqdm(total = len(known_face_imgs))

for img in known_face_imgs:
    loc = face_recognition.face_locations(img, model="cnn")
    # assert len(loc) == 1, "画像から顔の検出に失敗したか、2人以上の顔が検出されました"
    # if len(loc) == 0: 
      # continue
    # print(len(loc))
    known_face_locs.append(loc)
    bar_analyze_img.update(1)

face_loc_to_check = face_recognition.face_locations(face_img_to_check, model="cnn")
assert len(face_loc_to_check) == 1, "画像から顔の検出に失敗したか、2人以上の顔が検出されました"

def draw_face_locations(img, locations):
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.set_axis_off()
    for i, (top, right, bottom, left) in enumerate(locations):
        # 長方形を描画する。
        w, h = right - left, bottom - top
        ax.add_patch(plt.Rectangle((left, top), w, h, ec="r", lw=2, fill=None))
    plt.show()

draw_face_locations(face_img_to_check, face_loc_to_check)

# 顔の領域から特徴量を抽出する。
known_face_encodings = []
for img, loc in zip(known_face_imgs, known_face_locs):
    if len(loc) != 1: 
      continue
    (encoding,) = face_recognition.face_encodings(img, loc)
    known_face_encodings.append(encoding)

(face_encoding_to_check,) = face_recognition.face_encodings(
    face_img_to_check, face_loc_to_check
)

# 顔を認識する
matches = face_recognition.compare_faces(known_face_encodings, face_encoding_to_check)
print(matches)  # [True, False, False]

dists = face_recognition.face_distance(known_face_encodings, face_encoding_to_check)
print(dists)
list = []
n = 0

for i in dists: 
  if i < 0.35: 
    draw_face_locations(known_face_imgs[n], known_face_locs[n])
    print(file_names[n])
  n = n + 1
