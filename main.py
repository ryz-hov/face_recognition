import cv2 as cv
import os
import pickle
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-81e4e-default-rtdb.firebaseio.com/",
    'storageBucket': 'faceattendacerealtime-81e4e.appspot.com'
})

bucket = storage.bucket()
cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv.imread('Resources/background.png')
# folderModePath = 'Resources/Modes'
modePathList = os.listdir('Resources/Modes')
imgModeList = []
for path in modePathList:
    imgModeList.append(cv.imread(os.path.join('Resources/Modes', path)))

# Load the encoding file
print('Loading Encode File...')
file = open('EncodeFile.p', 'rb')
encodedListKnownWithIDs = pickle.load(file)
file.close()
encodedListKnown, studentIDs = encodedListKnownWithIDs
print('Encode File Loaded')

modeType = 0
counter = 0
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    for encodeFace, faceLoc, in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodedListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodedListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            print("Known Face Detected")
            print(studentIDs[matchIndex])

            id = studentIDs[matchIndex]
            if counter == 0:
                counter = 1
                modeType = 1

    if counter != 0:
        if counter == 1:
            # Get the Data
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)
            # Get the Image from the storage
            blob = bucket.get_blob(f'{"images"}/{id}.png')
            print(type(blob))
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv.imdecode(array, cv.COLOR_BGRA2BGR)

        if 10 < counter < 20:
            modeType = 2
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        if counter <= 10:
            cv.putText(imgBackground, str(studentInfo['group']), (858, 123),
                       cv.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)

            cv.putText(imgBackground, str(studentInfo['speciality']), (1006, 550),
                       cv.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 1)

            cv.putText(imgBackground, str(id), (1006, 493),
                       cv.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 50), 1)

            cv.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                       cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

            cv.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                       cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

            cv.putText(imgBackground, str(studentInfo['room']), (910, 625),
                       cv.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

            (w, h), _ = cv.getTextSize(studentInfo['name'], cv.FONT_HERSHEY_COMPLEX, 1, 1)
            offset = (414 - w)//2
            cv.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                       cv.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

            imgBackground[175:175+216, 909:909+216] = imgStudent
        counter += 1

        if counter >= 20:
            counter = 0
            modeType = 0
            studentInfo = []
            imgStudent = []
    cv.imshow('Webcam', img)
    cv.imshow('Face attendance', imgBackground)
    cv.waitKey(1)
