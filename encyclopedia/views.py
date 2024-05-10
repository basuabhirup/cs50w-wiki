from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import util
from random import choice
from markdown2 import markdown


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
        "entry": markdown(entry)
    })
    
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
    
        if not title or not content:
            return render(request, "encyclopedia/create.html", {
            "error": "Please fill out both title and content fields."
            })
        
        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
            "error": "An encyclopedia entry with that title already exists."
            })
        
        util.save_entry(title, content)
        
        return HttpResponseRedirect(f"wiki/{title}")
    
    else:
        return render(request, "encyclopedia/create.html")
    
def random(request):
    entries = util.list_entries()
    print(entries)
    entry = choice(entries)
    print(entry)
    return HttpResponseRedirect(f"wiki/{entry}")
    
    
    