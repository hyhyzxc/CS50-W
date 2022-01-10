from logging import PlaceHolder
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from markdown2 import Markdown
import markdown2
import random
from . import util

class NewTaskForm(forms.Form):
    search = forms.CharField(label = "Search Encyclopedia")

class NewWikiForm(forms.Form):
    title = forms.CharField(label = "New Wiki Title")
    textcontent = forms.CharField(widget=forms.Textarea())

class NewEditForm(forms.Form):
    editcontent = forms.CharField(widget=forms.Textarea())


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_content(request, entry):
    content = util.get_entry(entry)
    if content != None:
        markdowner = Markdown()
        contents = markdowner.convert(content)
        return render(request, "encyclopedia/content.html", {
            "content": contents,
            "title": entry
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "entry" : entry
        })


def search(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            if search in util.list_entries():
                return HttpResponseRedirect(f"wiki/{search}")
            else:
                entries = []
                for entry in util.list_entries():
                    if search.lower() in entry.lower():
                        entries.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "entries" : entries
                })
        else:
            return render(request, "encyclopedia/index.html")
    else:
        return render(request, "encyclopedia/index.html")

def create(request):
    if request.method == 'POST':
        form = NewWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textcontent = form.cleaned_data["textcontent"]
            if title in util.list_entries():
                return render(request, "encyclopedia/titleerror.html", {
                    "title":title
                })
            else:
                util.save_entry(title, textcontent)
                return HttpResponseRedirect(f"wiki/{title}")
        else:
            return render(request, "encyclopedia/create.html", {
                'form': form
            })
    else:
        return render(request, "encyclopedia/create.html",{
            'form':NewWikiForm()
        })

def edit(request, entry):
    if request.method == 'POST':
        form = NewEditForm(request.POST)
        if form.is_valid():
            editcontent = form.cleaned_data["editcontent"]
            util.save_entry(entry, editcontent)
            return render(request, "encyclopedia/content.html", {
                'title' : entry,
                'content' :markdown2.markdown(editcontent)
            })
        else:
            return render(request, "encyclopedia/edit.html",{
                'form':NewEditForm(initial={'editcontent':util.get_entry(entry)}),
                'title':entry
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            'form':NewEditForm(initial = {'editcontent':util.get_entry(entry)}),
            'title':entry
        })

def random_page(request):
    page = random.choice(util.list_entries())
    return HttpResponseRedirect(f"wiki/{page}")