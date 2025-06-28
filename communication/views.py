from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message
from .forms import MessageForm
from django.urls import reverse

@login_required
def inbox(request):
    messages_list = Message.objects.filter(recipient=request.user)
    return render(request, 'communication/inbox.html', {'messages': messages_list})

@login_required
def sent_messages(request):
    messages_list = Message.objects.filter(sender=request.user)
    return render(request, 'communication/sent_messages.html', {'messages': messages_list})

@login_required
def new_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Message envoyé avec succès.')
            return redirect('communication:inbox')
    else:
        form = MessageForm()
    return render(request, 'communication/new_message.html', {'form': form})

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'communication/message_detail.html', {'message': message}) 