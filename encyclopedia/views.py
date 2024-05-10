from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util


def index(request):    
    if not request.GET.get("q"):   
        return render(request, "encyclopedia/index.html", {
            "heading": "All Pages",
            "entries": util.list_entries()
        })
        
    query = request.GET["q"]
    
    if (util.get_entry(query) is not None):
        return HttpResponseRedirect(f"wiki/{query}")
    else:
        entries = []
        for entry in util.list_entries():
            if query in entry:
                entries.append(entry)
        
        return render(request, "encyclopedia/index.html", {
            "heading": f"Search results for '{query}'",
            "entries": entries
        })

def wiki(request, title):
    entry = util.get_entry(title)
    
    if entry == None:
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "entry": entry
    })