from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Audios



def try_recent_audio(request):
    needed = Audios.objects.get(pk=1)
    data_items = {'text': needed.text, 'url': needed.url, 'hint': needed.hint}
    return render(request, 'audio_test.html', {'data_items': data_items})

@csrf_exempt
def accept_media(request):
    try:
        error_message, text, media_hint, media_url = cleaner(request)
        if error_message:
            return error_message
        else:
            needed = Audios.objects.get(pk=1)
            needed.text = text
            needed.url = media_url
            needed.hint = media_hint
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
    to_tel = postdata['To']
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
        return error_message, text, media_hint, media_url