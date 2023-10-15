import openai
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .models import ErrorReport, Message, Room


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
        max_tokens=1000,  # Adjust this based on your desired response length
    )

    generated_message = response.choices[0].text.strip()

    # Create a new Message object with the generated response
    new_message = Message.objects.create(value=generated_message, user="ChatGPT", room=room_id)
    new_message.save()
    
    return HttpResponse(generated_message)

def reportError(request):
    if request.method == 'POST':
        error_types = request.POST.getlist('errorTypes')  # Get the list of error types
        main_message = request.POST.get('mainMessage', '')
        user_remarks = request.POST.get('userRemarks', '')
        print(f"Error_types: {error_types}")
        print(f"Main_message: {main_message}")
        print(f"User_remarks: {user_remarks}")

        if error_types and main_message:
            # Process the list of error types here
            for error_type in error_types:
                error_report = ErrorReport(error_type=error_type, main_message=main_message, user_remarks=user_remarks)
                error_report.save()
            
            return JsonResponse({'message': 'Error reported successfully'})
        else:
            return JsonResponse({'message': 'Error report data incomplete'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
