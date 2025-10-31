# Clipboard Translator & Dictionary

**Clipboard Translator & Dictionary** is a Python application that automatically detects text copied to your clipboard, translates it from English to Turkish, and provides its dictionary meaning. It also displays synonyms for both the original word and its translation.

---

## Features

- Automatically detects copied text.
- English → Turkish translation using Google Translate.
- Fetches dictionary meanings with PyMultiDictionary.
- Shows synonyms for the word and its translation.
- Clean and readable terminal output.
- Lightweight and fast.

---

## Requirements

- Python 3.8 or higher
- Required Python packages:

```bash
pip install pyperclip googletrans==4.0.0-rc1 PyMultiDictionary
