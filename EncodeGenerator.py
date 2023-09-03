import cv2 as cv
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-81e4e-default-rtdb.firebaseio.com/",
    'storageBucket': 'faceattendacerealtime-81e4e.appspot.com'
})


pathList = os.listdir('Images')
imgList = []
studentIDs = []
for path in pathList:
    imgList.append(cv.imread(os.path.join('Images', path)))
    studentIDs.append(os.path.splitext(path)[0])

    fileName = f'{"images"}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
def findEncoding(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print('Encoding Started ...')
encodedListKnown = findEncoding(imgList)
encodedListKnownWithIDs = [encodedListKnown, studentIDs]
print('Encoding Complete')

file = open('EncodeFile.p', 'wb')
pickle.dump(encodedListKnownWithIDs, file)
file.close()
print('File Saved')