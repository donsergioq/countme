import face_recognition
import cv2
import datetime


class Camera:

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.known_face_encodings = []
        self.known_face_ids = []
        self.face_locations = []
        self.face_encodings = []
        self.face_id = 0
        self.recognize_timestamp = 0
        self.scale_factor = 0.5

    def __del__(self):
        self.video.release()

    def __recognize(self, face_encodings):
        face_ids = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            current_face_id = ""
            if True in matches:
                first_match_index = matches.index(True)
                current_face_id = self.known_face_ids[first_match_index]
            else:
                self.known_face_encodings.append(face_encoding)
                self.known_face_ids.append(str(self.face_id))
                self.face_id += 1
                self.recognize_timestamp = int(datetime.datetime.now().timestamp())
            face_ids.append(current_face_id)
        return face_ids

    def __scale(self, x):
        return x * int(1 / self.scale_factor)

    def get_recognized_ids(self):
        return [self.recognize_timestamp, self.known_face_ids]

    def get_frame(self):
        ret, frame = self.video.read()
        small_frame = cv2.resize(frame, (0, 0), fx=self.scale_factor, fy=self.scale_factor)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), name in zip(face_locations, self.__recognize(face_encodings)):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top = self.__scale(top)
            right = self.__scale(right)
            bottom = self.__scale(bottom)
            left = self.__scale(left)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, jpeg = cv2.imencode('.jpg', cv2.resize(frame, (0, 0), fx=self.scale_factor, fy=self.scale_factor))
        return jpeg.tobytes()
