from .forms import UserRegistrationForm 
from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.views import generic
from .models import *
from .forms import HomeworkForm  # Replace '.forms' with the correct path to your forms module
from .models import Homework,Todo 
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests 
from youtubesearchpython import VideosSearch
from .forms import DashboardFom 
import wikipedia
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Authentication failed, add an error message to the form
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'your_template.html', {'form': form})



# Create your views here.
def home(request):
    dt=Card.objects.all()
    data={'data':dt}
    return render(request,'home.html',data)

def notes(request):
    if request.method=='POST':
        form= NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"notes add from {request.user.username}successfully")
    else:


        form=NotesForm()
    notes=Notes.objects.filter(user=request.user)#loginuser
    context={"notes":notes,'form':form}
    return render(request,'notes.html',context)

def delete_notes(request,pk=None):#primarykey means id uniqueness
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

class NotesDetailView(generic.DetailView):
    model=Notes
    template_name='notes_detail.html'


def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            # Process the form data and save the Homework instance
            homework = form.save(commit=False)
            homework.user = request.user
            if 'is_finished' in request.POST:
                homework.is_finished = True
            homework.save()
            messages.success(request, f'Homework added from {request.user.username}!!')
            return redirect('homework')  # Redirect to the homework view (change 'homework' to your actual URL name)
        else:
            # Handle form validation errors here if needed
            messages.error(request, 'Form submission error. Please check your input.')
            return redirect('homework')  # Redirect to the homework view if form validation fails

    else:
        homework = Homework.objects.filter(user=request.user)
        if len(homework) == 0:
            homework_done = True
        else:
            homework_done = False
        
        context = {'homeworks': homework, 'homeworks_done': homework_done, 'form': HomeworkForm()}
        return render(request, 'homework.html', context)

def update_homework_status(request, homework_id):
    # Retrieve the Homework object
    homework = get_object_or_404(Homework, pk=homework_id)

    # Update the homework status logic here (for example, toggle the 'is_finished' field)
    homework.is_finished = not homework.is_finished
    homework.save()

    # Redirect to a specific URL after updating the status (optional)
    return redirect('homework')  # Replace 'homework' with your desired URL name




def delete_homework(request, pk=None):
    # Retrieve the Homework object or return a 404 error if not found
    homework = get_object_or_404(Homework, pk=pk)
    
    # Delete the homework object
    homework.delete()

    # Redirect to a specific URL after deleting the object (for example, redirect to the homework list)
    return HttpResponseRedirect(reverse('homework'))  # Replace 'homework' with your actual URL name



def youtube(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            video = VideosSearch(text, limit=10)
            result_list = []
            for i in video.result()['result']:
                result_dict = {
                    'input': text,
                    'title': i['title'],
                    'duration': i['duration'],
                    'thumbnail': i['thumbnails'][0]['url'],
                    'channel': i['channel']['name'],
                    'link': i['link'],
                    'views': i['viewCount']['short'],
                    'published': i['publishedTime'],
                }
                desc = ''
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        desc += j['text']
                result_dict['description'] = desc
                result_list.append(result_dict)
                
            context = {
                'form': form,
                'results': result_list,
            }
            return render(request, 'youtube.html', context)
    else:
        form = DashboardFom()
    
    context = {'form': form}
    return render(request, 'youtube.html', context)

def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished =request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished=False
                
            except:
                finished = False
                todos = Todo(
                    user = request.user,
                    title = request.POST['title'],
                    is_finished = finished
                    
                )
                todos.save()
                messages.success(request,f'todo added from {request.user.username}!!')
    else:
        form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done= True
    else:
        todos_done = False
    context={
        'form':form,
        'todos':todo,
        'todos_done':todos_done

    }
    return render(request,'todo.html',context)

def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
        todo.save()
        return redirect('todo')
    
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")

def books(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = 'https://www.googleapis.com/books/v1/volumes?q=' + text
            r = requests.get(url)
            if r.status_code == 200:
                answer = r.json()
                result_list = []
                items = answer.get('items', [])
                for item in items[:10]:  # Limit to the first 10 results
                    volume_info = item.get('volumeInfo', {})
                    result_dict = {
                        'title': volume_info.get('title', 'No Title'),
                        'subtitle': volume_info.get('subtitle', ''),
                        'description': volume_info.get('description', ''),
                        'count': volume_info.get('pageCount', ''),
                        'categories': volume_info.get('categories', []),
                        'rating': volume_info.get('pageRating', ''),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                        'preview': volume_info.get('previewLink', ''),
                    }
                    result_list.append(result_dict)
                
                context = {
                    'form': form,
                    'results': result_list,
                }
                return render(request, 'books.html', context)
            else:
                # Handle API request failure
                error_message = f"Failed to fetch data. Status code: {r.status_code}"
                context = {
                    'form': form,
                    'error_message': error_message,
                }
                return render(request, 'books.html', context)
    else:
        form = DashboardFom()
    
    context = {'form': form}
    return render(request, 'books.html', context)

import requests

def dictionary(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            url = f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}'  # Corrected URL formation
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    answer = r.json()
                    phonetics = answer[0]['phonetics'][0]['text']
                    audio = answer[0]['phonetics'][0]['audio']
                    definition = answer[0]['meanings'][0]['definitions'][0]['definition']
                    example = answer[0]['meanings'][0]['definitions'][0]['example']
                    synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']

                    context = {
                        'form': form,
                        'input': text,
                        'phonetics': phonetics,
                        'audio': audio,
                        'definition': definition,
                        'example': example,
                        'synonyms': synonyms
                    }
                else:
                    context = {
                        'form': form,
                        'input': text,
                        'error_message': 'Failed to fetch data from the API. Please try again later.'
                    }
            except Exception as e:
                print(e)  # Handle exceptions appropriately
                context = {
                    'form': form,
                    'input': '',
                    'error_message': 'An error occurred. Please try again later.'
                }
        else:
            context = {'form': form, 'input': ''}
    else:
        form = DashboardFom()
        context = {'form': form}

    return render(request,'dictionary.html',context)

def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardFom(request.POST)
        search= wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary

        }
        return render(request,'wiki.html',context)
    else:

        form= DashboardFom()
        context={
        'form':form
    }
    return render(request,'wiki.html',context)

def conversion(request):
    if request.method =='POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement']== 'length':
            measurement_form= ConversionLengthForm()
            context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True
                }
            if 'input' in request.POST:
                first =request.POST['measure1']
                second =request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input)>=0:
                    if first == 'yard' and second=='foot':
                        answer = f'{input} yard={int(input)*3} foot'
                    if first == 'foot' and second=='yard':
                        answer = f'{input} yard={int(input)/3} foot'
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
        else:
            if request.POST['measurement']== 'mass':
                measurement_form= ConversionMassForm()
                context = {
                    'form':form,
                    'm_form':measurement_form,
                    'input':True
                }
            if 'input' in request.POST:
                first =request.POST['measure1']
                second =request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input)>=0:
                    if first == 'pound' and second=='kilogram':
                        answer = f'{input} pound={int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second=='pound':
                        answer = f'{input} kilogram={int(input)*2.20462} pound'
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
                

            
    else:
            form = ConversionForm()
            context ={
        'form':form,
        'input':False
    }
    return render(request,'conversion.html',context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created For {username}!!')
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to 'home' upon successful login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    # Redirect to a specific URL after logout (such as the login page)
    return redirect('login')  # Replace 'login' with your actual login URL name



def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)


    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False

    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False

    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todos_done': todos_done,
    }

    return render(request, "profile.html", context)


