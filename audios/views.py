from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Audios



def try_recent_audio(request):
    example_audio = Audios.objects.get(pk=1)
    working_example = {}
    working_example['profile_photo_url'] = 'https://www.pexels.com/photo/crop-woman-setting-up-microphone-before-podcasting-6953868/'
    working_example['card_image_url'] = 'https://www.pexels.com/photo/woman-standing-on-a-podium-6172613/'
    working_example['card_audio_url'] = example_audio.url
    working_example['card_audio_hint'] = example_audio.hint
    working_example['text'] = 'This from Android App "Hi-Q MP3 Recorder running 96 kbps recording MP3'

    test_audio = Audios.objects.get(pk=2)
    to_test = {}
    to_test['profile_photo_url'] = 'https://www.pexels.com/photo/man-in-suit-giving-speech-3880204/'
    to_test['card_image_url'] = 'https://www.pexels.com/photo/man-with-fireworks-769525/'
    to_test['card_audio_url'] = test_audio.url
    to_test['card_audio_hint'] = test_audio.hint
    to_test['text'] = test_audio.text

    data_items = {'to_test': to_test, 'working_example': working_example}
    return render(request, 'audio_test2.html', {'data_items': data_items})

@csrf_exempt
def accept_media(request):
    try:
        error_message, from_tel, text, media_hint, media_url = cleaner(request)
        if error_message:
            return error_message
        else:
            pk = 1 if from_tel=='+16502196500' else 2  
            try:
                needed = Audios.objects.get(pk=pk)
                needed.text = text
                needed.url = media_url
                needed.hint = media_hint
            except Audios.DoesNotExist:
                needed = Audios(from_tel=from_tel, text=text, hint=media_hint, url=media_url)
            needed.save()
            message = f'Received type {media_hint}. See at https://salty-plains-25907.herokuapp.com/'
            return HttpResponse(content=f"<Response><Message>'{message}'</Message></Response>")  
    except Exception as E:
        return HttpResponse(content=f"<Response><Message>Have a problem {repr(E)}. Contact Steve</Message></Response>")  
        


def cleaner(request):
    error_message = None
    blanks = ('',)*6
    if request.method!='POST':
        return HttpResponse(status=405), *blanks 
    postdata = request.POST
    from_tel = postdata['From']
    text = postdata['Body']    
    if text:
        text = f'{from_tel} sent: {text.lower().strip()}'
    else:
        text = f'{from_tel} sent no text'
    media_quantity_as_string = postdata["NumMedia"]
    if media_quantity_as_string != '1':
        error_message =  HttpResponse(content=f'<Response><Message>Please send one audio file. Got {media_quantity_as_string} files.</Message></Response>')
        return error_message, text, ' ', ' '
    else:
        media_hint = postdata['MediaContentType0']
        media_type  = media_hint.split('/')[0]
        media_url = postdata['MediaUrl0']
        if media_type != 'audio':
            error_message =  HttpResponse(content=f'<Response><Message>This test site does not use {media_type} files. Please send audio only.</Message></Response>')
        return error_message, from_tel, text, media_hint, media_url