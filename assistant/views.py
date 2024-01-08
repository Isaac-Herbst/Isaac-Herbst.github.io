from django.shortcuts import render, redirect
from openai import OpenAI
from openai import RateLimitError, BadRequestError
from .secret_key import API_KEY
from .models import ChatLog
import time

import os
from django.http import HttpResponse
from wsgiref.util import FileWrapper


client = OpenAI(api_key=API_KEY)

def home(request):
    try:
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "You are now chatting with a user, provide them with comprehensive, short and concise answers."},
            ]

        if request.method == 'POST':
            prompt = request.POST.get('prompt')
            # probably not needed
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": prompt})
            request.session.modified = True
            #ChatLog.objects.create(user=request.user, content=message.content)

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=request.session['messages'],
                    max_tokens=1000,
                )
            except RateLimitError:
                # handle rate limit error
                print("Rate limit exceeded. Please slow down your requests.")
                #time.sleep(60) # wait for 60 seconds before retrying
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=request.session['messages'],
                    max_tokens=1000,
                )
            except BadRequestError:
                # handle invalid request error
                print("Bad request. Please check your parameters.")
            except Exception as e:
                # handle all other exceptions
                print(f"An error occurred: {e}")
                return redirect('error_handler')

            # format the response
            formatted_response = response['choices'][0]['message']['content']
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
            }
            return render(request, 'assistant/home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
            }
            return render(request, 'assistant/home.html', context)
    except Exception as e:
        print(e)
        return redirect('error_handler')


def new_chat(request):
    request.session.pop('messages', None)
    return redirect('home')

def error_handler(request):
    return render(request, 'assistant/404.html')

from django.http import HttpResponse
from .models import ChatLog

def download_file(request):
   filename = 'whatever_in_absolute_path__or_not.pdf'
   content = FileWrapper(filename)
   response = HttpResponse(content, content_type='application/pdf')
   response['Content-Length'] = os.path.getsize(filename)
   response['Content-Disposition'] = 'attachment; filename=%s' % 'whatever_name_will_appear_in_download.pdf'
   return response

def user_profile(request):
   return render(request, 'user_profile.html')