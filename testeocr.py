import cv2
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt

# Caminho do Tesseract.exe
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def preprocess_image(image_path):
    # Lê a imagem em escala de cinza
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aumenta contraste + binariza
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Remover ruídos (blur opcional)
    blur = cv2.medianBlur(thresh, 3)

    return img, blur

def extract_text_from_image(image_path):
    # Pré-processar
    original, processed = preprocess_image(image_path)

    # Salvar imagem processada temporariamente
    temp_path = "processed.png"
    cv2.imwrite(temp_path, processed)

    # Extrair texto
    text = pytesseract.image_to_string(Image.open(temp_path), config='--psm 7')

    # Mostrar imagens lado a lado
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axs[0].set_title("Original")
    axs[0].axis("off")

    axs[1].imshow(processed, cmap="gray")
    axs[1].set_title("Pré-processada")
    axs[1].axis("off")

    plt.show()

    return text

# Exemplo de uso
image_file = '/Users/leonardofinsbd/Downloads/image2.png'
resultado = extract_text_from_image(image_file)
print("Texto extraído:", resultado)

