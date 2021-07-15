import cv2 as cv


def main():
    # Set path to classifier
    casc_path = cv.data.haarcascades + "haarcascade_frontalface_alt.xml"
    face_cascade = cv.CascadeClassifier(casc_path)

    # Capture video stream
    video_capture = cv.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        small_frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)
        gray = cv.cvtColor(small_frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv.CASCADE_SCALE_IMAGE
        )
        font = cv.FONT_HERSHEY_SIMPLEX

        print(faces)

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv.rectangle(small_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Add face counter to the frame
        cv.putText(small_frame, 'People detected: ' + str(len(faces)), (15, 15), font, 0.5, (0, 0, 0), 2, cv.LINE_4)

        # Display the resulting frame
        cv.imshow('Video', small_frame)

        # Exit if 'q' pressed
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
