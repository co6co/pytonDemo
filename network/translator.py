# encoding= utf-8
from googletrans import Translator

translator=Translator()
text ="Hello"
translated=translator.translate(text,dest='zh-CN')
print(translated.text)