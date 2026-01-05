# cv-parser-py-llm

This project does not aim to parse a cv in its entirety, as it would be too hard and tedious.

The goal is to extract a person’s educational background from a dataset of heterogeneous curricula vitae


---

### DISCLAIMER
**This is poorly suited for any use other than mine at the moment.**

I'm using it to build a personal dataset so without paying much attention to code readability and state of the art

---
# How it works

OCRmyPDF(PDFS) -> pdftotext(OCRED_PDFS) -> keyword_extractor(TEXTS) -> LLM(TEXT_FRAGMENTS)

We take advantage of the ability of LLMs to understand text even if it contains spelling errors 

## Requirements 

These are the libraries (they're high quality) that are mandatory to run this repo

[pdftotext](https://www.xpdfreader.com/download.html) 

[OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) 

[ollama](https://ollama.com/download) 

## LLMs

I've used ```qwen3:8b``` but you can use anything else, possibly 8b or more.. 

## License

GNU General Public License v3.0 (**GNU GPLv3.0**)
