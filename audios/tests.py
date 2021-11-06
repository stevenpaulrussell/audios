from django.http import request
from django.test import TestCase
from django.test.client import RequestFactory

from .views import accept_media, cleaner

 

twilio_no_media_keys = ('From', 'To', 'Body', 'NumMedia')
twilio_single_media_keys = ('From', 'To', 'Body', 'NumMedia', 'MediaContentType0', 'MediaUrl0') 
twilio_two_media_keys = ('From', 'To', 'Body', 'NumMedia', 'MediaContentType0', 'MediaUrl0', 'MediaContentType1', 'MediaUrl1')

sender_keys = ('status', 'profile_photo_url', 'name' )  # from_tel is dictionary key for each sender

from_0, from_1, from_2  = '+1test0000', '+1test0001', '+1test0002'
to_0, to_1 = '+1test9990', '+1test9991'
audio_type = 'audio/ogg'
image_type = 'image/jpeg'
url0, url1, url2, url3 = 'url_string_zero', 'url_string_one', 'url_string_two', 'url_string_three'
a_sample_connector = '1234'

post_dict_image_only = dict(zip(twilio_single_media_keys, (from_0, to_0, '', '1', image_type, url1)))
post_dict_comment_command_and_audio = dict(zip(twilio_single_media_keys, (from_0, to_0, 'com ment', '1', audio_type, url2)))
post_dict_audio_only = dict(zip(twilio_single_media_keys, (from_0, to_0, '', '1', audio_type, url0)))
post_dict_two_media = dict(zip(twilio_two_media_keys, (from_0, to_0, '', '2', audio_type, url0, image_type, url1)))
post_dict_empty = dict(zip(twilio_no_media_keys, (from_0, to_0, '', '0')))





class ViewAcceptMediaErrorFromEstablishedSendersCaseTest(TestCase):

    def test_accept_media_view_function_returns_proper_media_request_with_text(self):
        request = RequestFactory().post('/accept_media/', post_dict_comment_command_and_audio)
        error_message, text, media_hint, media_url = cleaner(request)
        self.assertIn('+1test0000 sent: com ment', text)

    def test_accept_media_view_function_returns_proper_media_request_with_no_text(self):
        request = RequestFactory().post('/accept_media/', post_dict_audio_only)
        error_message, text, media_hint, media_url = cleaner(request)
        self.assertIn('+1test0000 sent no text', text)

    def test_accept_media_view_function_detects_wrong_media_type(self):
        request = RequestFactory().post('/accept_media/', post_dict_image_only)
        resp = accept_media(request)
        self.assertIn('This test site does not use image files. Please send audio only', str(resp.content))

    def test_accept_media_view_function_detects_too_many_media(self):
        request = RequestFactory().post('/accept_media/', post_dict_two_media)
        resp = accept_media(request)
        self.assertIn('Please send one audio file. Got 2 files.', str(resp.content))


