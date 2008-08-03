# Create your views here.

def home(request):
    """The site's home page."""
    return render_to_response('index.html', {
    
    }, context_instance=RequestContext(request))
