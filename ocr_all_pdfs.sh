DIR_INPUT="vanilla pdfs copy/"

ls "$DIR_INPUT" | xargs -I{} -P 4 -n 1 ocrmypdf --force-ocr "$DIR_INPUT"{} ocr\ forced/{}

