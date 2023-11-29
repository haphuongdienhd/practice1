# chat/views.py

from django.shortcuts import render, redirect
 
 
def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    return render(request, "chat/chatpage.html", context)