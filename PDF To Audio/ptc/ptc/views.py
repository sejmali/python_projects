import os
import io
from django.shortcuts import render
from gtts import gTTS
import PyPDF2
from translate import Translator
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
from django.urls import reverse_lazy, reverse
from django.core.files.storage import FileSystemStorage


def nothing(request):
    return render(request, 'index.html')


def output(request):
    language = 'en'

    uploaded_pdf_file = request.FILES['pdffile']
    print(uploaded_pdf_file.name)
    print(uploaded_pdf_file.size)

    pdf_Reader = PyPDF2.PdfFileReader(uploaded_pdf_file)
    count = pdf_Reader.numPages  # counts number of pages in pdf
    textList = []

    for i in range(count):
        try:
            page = pdf_Reader.getPage(i)
            textList.append(page.extractText())

        except:
            pass

    # Converting multiline text to single line text
    textString = " ".join(textList)

    print(textString)

    # Set language to english (en)
    language = 'en'

    # Call GTTS
    myAudio = gTTS(text=textString, lang=language, slow=False)
    myAudio.save("Audio.mp3")
    os.system("Audio.mp3")

    return render(request, 'index.html', {'show_text': textString})


def text_translator(request):

    text = request.POST.get('text')
    print(text)
    from_lang = request.POST.get('from_lang')
    print(from_lang)
    to_lang = request.POST.get('to_lang')
    print(to_lang)
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translated_text = translator.translate(text)

    return render(request, 'index.html', {'data': translated_text})
