from django.http import HttpResponse
import json

def wrap_response(json_object, content_type='application/json'):
    return HttpResponse(json.dumps(json_object), content_type=content_type)
