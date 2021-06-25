import os 
import sys
import face_recognition
import cv2 as cv 
import pickle


def get_frame(video_path, frame_number):
    cap = cv.VideoCapture(video_path) 
    count = 0 
    if not cap.isOpened():
        print("Не удается открыть видео")
        exit()
    while True:
        ret, frame = cap.read()
        if count % frame_number == 0:
            cv.imwrite(f'out_frames/reframe_{int((count + 1)/frame_number)}.jpg', frame)
        count += 1
        if not ret:
            print(f"Видео раскадированно")
            break
    cv.destroyAllWindows()


def person_on_frame(id):

    if not os.path.exists('out_frames'):
        print('[ОШИБКА] не найдена папка с кадрами')
        sys.exit()

    known_encoding = []
    images = os.listdir('out_frames')

    for(i, image) in enumerate(images):
        print(f'Обробатываемый кадр{i + 1}/{len(images)}')
        face_img = face_recognition.load_image_file(f'out_frames/{image}')
        if len(face_recognition.face_encodings(face_img)) == 0:
                print('На этом кадре лиц не обнаруженно')
                continue
        else:
            encodings = face_recognition.face_encodings(face_img)[0] 
            if len(known_encoding) == 0:
                known_encoding.append(encodings)
            else:
                for item in range(0, len(known_encoding)):
                    result = face_recognition.compare_faces([encodings], known_encoding[item])
                    if result[0]:
                        known_encoding.append(encodings)
                        print('На кадре один и тот же человек')
                        break
                    else:
                        print('На кадре больше 1-го человека')
# создадим словарь с кодировкой обнаруженного на нем человеком  
    data = {
    'id' : id,
    'encodings' : known_encoding
    }
    
    #записываем получениые данные в файл
    with open(f'{id}_encodings.pickle', 'wb') as file:
        file.write(pickle.dumps('data'))
    return f'Файл {id}_encodings.pickle успешно сохранен'


def main():
    get_frame('video\example_1.mp4', 15)
    person_on_frame(123)


if __name__ == '__main__':
    main()