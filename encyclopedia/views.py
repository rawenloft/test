from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse
from django import forms
import markdown as mark
import random
from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": 'form-control'}), label="Page Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5,"cols":20, 'class':'form-control'}), label="Page Content")


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def add_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        pages = util.list_entries()
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in pages:
                print(title)
                messages.error(request, 'Page already exist! Create another page or update existed.')
                return render(request, "encyclopedia/form.html", {
                    "form": form,
                    "title": title,
                    "action": "Add"
                })
            util.save_entry(title, content)
            messages.success(request, "Page successfully created!")
            return redirect(reverse('wiki:page', kwargs={'title': title}))
    return render(request, "encyclopedia/form.html", {
        "form": NewPageForm(),
        "title": "New",
        "action": "Add"
    })

def edit_page(request, title):
    header = title
    title = util.get_entry(title)
    form = NewPageForm(initial={'title': header, 'content': title})
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            messages.success(request, "Page update successfully saved!")
            return redirect(reverse('wiki:page', kwargs={'title': title}))
    return render(request, 'encyclopedia/form.html', {
        "form": form,
        "title": header,
        "action": "Update",
    })

def search(request):
    query = request.GET["q"]
    files = util.list_entries()
    entries = []
    for item in filter(lambda x: query.lower() in x.lower(), files):
        entries.append(item)
    if not entries:
        messages.error(request,"No matching pages found!")
    for page in files:
        if query.lower() == page.lower():
            get_page(request, page)
            return redirect(reverse('wiki:page', kwargs={'title': page}))
    return HttpResponse(render(request, 'encyclopedia/index.html',{
        "entries": entries,
    }))

def convert(title):
    converted = mark.markdown(title)
    return converted

def get_random_page(request):
    page_list = util.list_entries()
    title = random.choice(page_list)
    return redirect('wiki:page', title=title)

def get_page(request, title):
    head = title
    title = util.get_entry(title)
    if title:
        return render(request, "encyclopedia/page.html", {
            "title": convert(title),
            "header": head,
            "edit": head
        })
    else:   
        return render(request, "encyclopedia/page404.html")
