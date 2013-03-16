from django.shortcuts import *

def home(request):
    if request.method=='POST':
        question=request.POST['question']
        print "comes here"
    return render_to_response('home.html',locals(),context_instance=RequestContext(request))

