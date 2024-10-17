from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("AntiNSFWv0.2.pt")

def process_image(image_path):
    results = model.predict(image_path)

    # Извлекаем предсказанный класс (индекс класса с наивысшей вероятностью)
    predicted_class_index = results[0].probs.top1
    predicted_class_possibly = ((str(results[0].probs.top1conf)).split("("))[1].split(",")

    # Извлекаем имя предсказанного класса
    predicted_class = results[0].names[predicted_class_index]

    return predicted_class + " с примерной вероятностью " + predicted_class_possibly[0]
