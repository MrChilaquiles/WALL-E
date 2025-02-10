import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pdf2image import convert_from_path

# Configuración del bot
TOKEN = os.environ.get("TOKEN")  # Lee el token desde variables de entorno
DOWNLOAD_PATH = "temp_pdf"
OUTPUT_PATH = "temp_jpg"

# Configurar logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "¡Hola! Envíame un archivo PDF y lo convertiré en imágenes JPG."
    )

def convert_pdf_to_jpg(pdf_path: str, output_path: str):
    images = convert_from_path(pdf_path, dpi=200, fmt="jpeg")
    saved_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_path, f"page_{i+1}.jpg")
        image.save(image_path, "JPEG")
        saved_paths.append(image_path)
    return saved_paths

def handle_document(update: Update, context: CallbackContext):
    user = update.message.from_user
    document = update.message.document

    # Verificar si es un PDF
    if document.mime_type != "application/pdf":
        update.message.reply_text("❌ Por favor, envía un archivo PDF.")
        return

    # Crear carpetas temporales
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    # Descargar el PDF
    file = context.bot.get_file(document.file_id)
    pdf_path = os.path.join(DOWNLOAD_PATH, document.file_name)
    file.download(pdf_path)

    update.message.reply_text("🔄 Convirtiendo PDF a JPG...")

    try:
        # Convertir PDF a JPG
        jpg_paths = convert_pdf_to_jpg(pdf_path, OUTPUT_PATH)

        # Enviar las imágenes
        for path in jpg_paths:
            with open(path, "rb") as img_file:
                update.message.reply_photo(img_file)

        # Eliminar archivos temporales
        os.remove(pdf_path)
        for path in jpg_paths:
            os.remove(path)

    except Exception as e:
        logger.error(f"Error: {e}")
        update.message.reply_text("❌ Ocurrió un error al procesar el PDF.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Comandos y manejadores
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_document))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()