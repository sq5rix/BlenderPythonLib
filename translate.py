import openai
from PIL import Image
import pytesseract

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

def translate_polish_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img, lang='pol')

    # Translate the extracted text using OpenAI's GPT-4 model
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Translate the following Polish text to English:\n\n{text}"}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Get the translation from the response
    translation = response['choices'][0]['message']['content'].strip()
    return translation

# Example usage
image_path = 'path_to_your_image.jpeg'
translation = translate_polish_image(image_path)
print(translation)