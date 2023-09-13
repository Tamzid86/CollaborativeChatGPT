from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
import openai
# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def getResponse(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    openai.api_key = "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"
    # Call the ChatGPT API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",  # Specify the ChatGPT engine
        prompt=f"You are in room {room_id}. User {username}: {message}\n",
        max_tokens=50,  # Adjust this based on your desired response length
    )

    generated_message = response.choices[0].text.strip()

    # Create a new Message object with the generated response
    new_message = Message.objects.create(value=generated_message, user="ChatGPT", room=room_id)
    new_message.save()
    
    return HttpResponse(generated_message)