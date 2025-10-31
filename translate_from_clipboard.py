import pyperclip
import time
import asyncio
import os
from googletrans import Translator
from PyMultiDictionary import MultiDictionary

dictionary = MultiDictionary()

async def translate(word, src='en', dest='tr'):
    async with Translator() as translator:
        try:
            result = await translator.translate(word, dest=dest, src=src)
            if not result.extra_data:
                return None
            return result.extra_data
        except Exception as e:
            print(f"Translation error for '{word}': {e}")
            return None

async def definite(word):
    try:
        meaning = dictionary.meaning('en', word)
        if meaning and len(meaning) > 2:
            return meaning[2]
        return None
    except Exception as e:
        print(f"Definition error for '{word}': {e}")
        return None

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def log(translation, definition, src='en', dest='tr'):
    if translation is None:
        print("No translation available.")
        return
    
    try:
        data = translation
        
        word = data['translation'][0][0]  
        translated_word = data['translation'][0][1]
        
        confidence = data.get('confidence', 0)
        if confidence is None:
            confidence = 0.0
        
        all_translations = data.get('all-translations', [])
        
        synonyms_src = []
        synonyms_dest = []
        
        if all_translations and len(all_translations) > 0:
            try:
                first_category = all_translations[0]
                if len(first_category) > 2 and len(first_category[2]) > 1:
                    synonyms_data = first_category[2][1][1] if len(first_category[2][1]) > 1 else []
                    synonyms_src = synonyms_data[:5] if isinstance(synonyms_data, list) else []
                
                if len(first_category) > 1:
                    synonyms_dest = first_category[1][:5] if isinstance(first_category[1], list) else []
            except:
                pass
        
        print("\n" + ("=" * 50))
        print(f"Word ({src}): {translated_word}")
        print(f"Translation ({dest}): {word}")
        print(f"Precise: {confidence:.4f}")
        print("-" * 50)
        
        print(f"Word Synonyms ({src}): {', '.join(synonyms_src) if synonyms_src else 'N/A'}")
        print(f"Translation Synonyms ({dest}): {', '.join(synonyms_dest) if synonyms_dest else 'N/A'}")
        
        print("-" * 50)
        print('Definition:')
        if definition:
            print(definition)
        else:
            print("No definition available.")
        
    except Exception as e:
        print(f"Error formatting output: {e}")

last_copied = pyperclip.paste().strip()
print("Clipboard tracker started. Ctrl + c to exit.")

try:
    while True:
        current = pyperclip.paste().strip()
        if current and current != last_copied:
            clear_screen()
            print(f"Processing: {current}")
            
            translation = asyncio.run(translate(current, src='en', dest='tr'))
            
            if translation is None:
                print(f"Skipping '{current}' - translation failed.")
                last_copied = current
                time.sleep(1)
                continue
            
            definition = asyncio.run(definite(current))
            
            log(translation, definition)
            
            last_copied = current
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExited...")
