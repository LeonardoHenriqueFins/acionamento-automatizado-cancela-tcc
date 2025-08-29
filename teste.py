from PIL import Image
import pytesseract

# Set the path to the Tesseract executable (if not in PATH)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract" # Example for Windows
def extract_text_from_image(image_path):
    """
    Extracts text from an image using Tesseract OCR.
    Args:
        image_path (str): The path to the image file.
    Returns:
        str: The extracted text from the image.
    """
    try:
        # Open the image using Pillow
        img = Image.open(image_path)
        # Perform OCR on the image
        text = pytesseract.image_to_string(img)
        return text
    except FileNotFoundError:
        return "Error: Image file not found."
    except pytesseract.TesseractNotFoundError:
        return "Error: Tesseract-OCR is not installed or not in your system's PATH."
    except Exception as e:
        return f"An error occurred: {e}"
# Example usage
image_file = "/Users/leonardofinsbd/Downloads/image4.png"  # Replace with your image file path
extracted_content = extract_text_from_image(image_file)
print(extracted_content)
