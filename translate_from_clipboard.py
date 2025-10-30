import pyperclip
import time
import asyncio
from googletrans import Translator
from PyMultiDictionary import MultiDictionary
dictionary = MultiDictionary()

async def translate(word, src='en', dest='tr'):
    async with Translator() as translator:
        result = await translator.translate(word, dest=dest, src=src)
        return result.extra_data
        
async def definite(word):
    dictionary = MultiDictionary()
    meaning = dictionary.meaning('en', word)
    return meaning[2]
    
def log(translation, definition, src='en', dest='tr'):
    data = translation
    # Main translation
    main_translation = data['translation'][0][0]  
    target_translation = data['translation'][0][1] 
    
    # Alternatives
    all_translations = data['all-translations'][0]
    word_type = all_translations[0]  # "isim"
    synonyms_src = all_translations[2][1][1]  # ['şeytan', 'iblis']
    synonyms_dest = all_translations[1]  # ['şeytan', 'iblis']
    
    print("=" * 50)
    
    print(f"Word ({src}): {main_translation}")
    print(f"Translation ({dest}): {target_translation}")
    print(f"Precise: {data['confidence']:.4f}")

    print("-" * 50)
    
    print(f"Word Synonyms ({src}): {', '.join(synonyms_src)}")
    print(f"Translation Synonyms ({dest}): {', '.join(synonyms_dest)}")
    
    print("-" * 50)
    
    print('Definition:')
    print(definition)

last_copied = ""
print("Clipboard tracker started. Ctrl + c to exit.")

try:
    while True:
        current = pyperclip.paste().strip()
        if current and current != last_copied:
            try:
                translation = asyncio.run(translate(current, src='en', dest='tr'))
                definition =  asyncio.run(definite(current))
                if not translation and not definition:
                    print('No data')
                    continue
                
                log(translation, definition)
            except Exception as e:
                print(f"Translation error: {e}")
            last_copied = current
        time.sleep(1)
except KeyboardInterrupt:
    print("Exited...")
    



