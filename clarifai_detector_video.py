from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

def main():
    # Определяем канал связи 
    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

    # Открываем видео файл 
    with open("double_pairs.mp4", "rb") as f: # Название видео 
        file_bytes = f.read()

    # Авторизация
    metadata = (('authorization', 'Key 9fec68715ce9438eacb2bc994babaa9a'),)

    #Запрос
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            model_id="5750faf62ed9d514b9ee9d2d163f172e", # ID модели для обнаружения
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        video=resources_pb2.Video(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    #Если запрос провалился, то выдать статус ошибки 
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Получаем данные ответа 
    output_data = post_model_outputs_response.outputs[0].data

    #Выводим на экран инвормацию по каждому кадру (1 кадр в 1 сек.) для каждого объекта 
    for item in output_data.frames:
        print(f'Кадр №{item.frame_info.index}\n')
        for concept in item.data.regions:
            print(f'Уникальный номер объекта (ID): {concept.id}')
            print(f'На кадре изображен: {concept.data.concepts[0].name} с вероятностью {concept.data.concepts[0].value}\n')
            print(f'Координаты объекта на кадре:{concept.region_info.bounding_box}\n\n')
            print('___________________________________________________________')
    
if __name__ == '__main__':
    main()
        