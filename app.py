import cv2
import pytesseract
import re
import os  # Biblioteca para interagir com o sistema operacional

# --- CONFIGURAÇÕES ---
# FIXME: Adicione aqui o caminho para o executável do Tesseract no seu computador.
# Exemplo para Windows: r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# No macOS (se instalado com Homebrew), geralmente não é necessário.
# TESSERACT_PATH = r'/opt/homebrew/bin/tesseract'
# if os.name == 'nt': # Verifica se o sistema é Windows
#     pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

# Caminho para o nosso banco de dados mock
DB_FILE_PATH = 'database.txt'


# --- FUNÇÕES DE OCR ---

def preprocess_image(image_path):
    """Lê e pré-processa a imagem para melhorar a leitura do OCR."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem em '{image_path}'")
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Um threshold mais adaptativo pode ajudar em diferentes iluminações
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return img, thresh


def extract_plate_text(image_path):
    """Extrai o texto de uma imagem usando OCR e limpa o resultado."""
    original, processed = preprocess_image(image_path)
    if original is None:
        return ""

    # Configuração do Tesseract para focar em caracteres de placas (Mercosul)
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text = pytesseract.image_to_string(processed, config=custom_config)

    # Limpa o texto extraído para manter apenas letras e números
    cleaned_text = re.sub(r'[^A-Z0-9]', '', text).upper()
    return cleaned_text


# --- LÓGICA DE BANCO DE DADOS E VERIFICAÇÃO ---

def check_plate_authorization(plate):
    """
    Verifica no 'banco de dados' (database.txt) se a placa tem status 'LIBERADO'.
    Retorna: (Status, Cliente) ou (None, None) se não encontrar.
    """
    print(f"\nVerificando autorização para a placa: {plate}...")
    try:
        with open(DB_FILE_PATH, 'r', encoding='utf-8') as db:
            for line in db:
                if not line.strip():
                    continue

                parts = line.strip().split(',')
                if len(parts) == 3:
                    db_plate, db_status, db_client = parts
                    if plate == db_plate:
                        print(f"Placa encontrada! Status: {db_status}, Cliente: {db_client}")
                        return db_status, db_client

        print("Placa não encontrada no sistema.")
        return "NAO_ENCONTRADO", None
    except FileNotFoundError:
        print(f"ERRO: Arquivo de banco de dados '{DB_FILE_PATH}' não encontrado.")
        return "ERRO_DB", None


# --- FLUXO PRINCIPAL DA APLICAÇÃO ---

def main():
    """Função principal que orquestra a execução do programa."""
    # FIXME: Altere aqui para o caminho da imagem que você quer testar
    image_file_to_test = "/Users/leonardofinsbd/Downloads/image2.png"

    if not os.path.exists(image_file_to_test):
        print(f"ERRO: A imagem de teste '{image_file_to_test}' não existe.")
        return

    # 1. Extrair a placa da imagem
    extracted_plate = extract_plate_text(image_file_to_test)
    print(f"Texto extraído e limpo pelo OCR: '{extracted_plate}'")

    if not extracted_plate:
        print("Nenhuma placa pôde ser lida da imagem.")
        return

    # 2. Verificar a placa no banco de dados
    status, client = check_plate_authorization(extracted_plate)

    # 3. Tomar a decisão com base no status
    if status == 'LIBERADO':
        print(f"\n>>> RESULTADO: ACESSO LIBERADO para {client}!")
        # Futuramente, aqui será o comando para o Arduino
    elif status == 'BLOQUEADO':
        print(f"\n>>> RESULTADO: ACESSO NEGADO. Veículo com restrição (Cliente: {client}).")
    elif status == 'MANUTENCAO':
        print(f"\n>>> RESULTADO: ACESSO NEGADO. Veículo em manutenção (Cliente: {client}).")
    else:
        print("\n>>> RESULTADO: ACESSO NEGADO. Placa não reconhecida ou sem autorização.")


if __name__ == "__main__":
    main()