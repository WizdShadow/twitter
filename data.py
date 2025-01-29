from PIL import Image

# Путь к изображению
image_path = 'rengoku.jpg'

# Открываем изображение
with Image.open(image_path) as img:
    # Преобразуем изображение в байты
    with open(image_path, 'rb') as f:
        binary_data = f.read()

# Теперь binary_data содержит изображение в бинарном формате
print(binary_data)  #