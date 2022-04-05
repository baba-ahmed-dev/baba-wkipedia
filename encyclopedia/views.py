from urllib import request
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
import markdown2
from markdown2 import markdown
from . import util
from .forms import search_form, add_form ,edit_form
from django.core.files.storage import default_storage
from random import choice


def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries":util.list_entries(),
        "form":search_form()
    })

def get_page(request, pagename):
    page = util.get_entry(pagename)
    if page is None:
        return render(request,"encyclopedia/error.html",{
            "pagename":pagename,
            "form":search_form()
        })
    html = markdown2.markdown(page)
    return render(request, "encyclopedia/display.html",{
        "page":html,
        "form":search_form(),
        "title":pagename
    })

def search_page(request):
    if request.method == "GET":
        form = search_form(request.GET)
        if form.is_valid():
            q = form.cleaned_data["search"]
            all_entries = util.list_entries()
            result = [entry for entry in all_entries if q.lower() in entry.lower()]
            if len(result) == 0:
                return render(request,"encyclopedia/error.html",{
                    "pagename":q,
                    "form":search_form()
                })
            elif len(result) == 1 and result[0].lower() == q.lower():
                return get_page(request, result[0])
            else:
                pages = [title for title in result if title.lower() == q.lower() ]
                if len(pages)>0:
                    return get_page(request, pages[0])
                else:
                    return render(request, "encyclopedia/result.html",{
                        "pages":result,
                        "form":search_form()
                    })
        else:
            return HttpResponseRedirect(reverse('index'))
    
    return HttpResponseRedirect(reverse('index'))       
        
        

def create_page(request):
    if request.method == "POST":
        form = add_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            pages = util.list_entries()
            for page in pages:
                if page.upper() != title.upper():
                    util.save_entry(title,body)
                    return get_page(request, title)
                else:
                    return render(request,"encyclopedia/createPage.html",{
                        "form":search_form(),
                        "addForm":add_form(),
                        "error": f'{title} already exist'
                    })
                
        else:
            return render(request,"encyclopedia/createPage.html",{
                "form":search_form(),
                "addForm":add_form()
            })
    else:
        return render(request,"encyclopedia/createPage.html",{
                "form":search_form(),
                "addForm":add_form()
            })


def edit_page(request):
    title = request.POST.get("edit")
    body = util.get_entry(title)
    form = edit_form(initial={'title':title, 'body':body})
    if form.is_valid():
        return render(request,"encyclopedia/editPage.html",{
            "form":search_form(),
            "editForm":edit_form(),
            "title":title
        })
    return render(request,"encyclopedia/editPage.html",{
            "form":search_form(),
            "editForm":form,
            "title":title
        })
    

def save_page(request):
    form = edit_form(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        body = form.cleaned_data["body"]
        util.save_entry(title,body)
        return get_page(request,title)
    else:
        return render(request,"encyclopedia/editPage.html",{
            "form":search_form(),
            "editForm":edit_form()
        })

def random_page(request):
    randomPage = choice(util.list_entries())
    return get_page(request, randomPage)

