from django.shortcuts import render, redirect
from youtubesearchpython import VideosSearch
from .models import ToDo, Notes, Homework
import requests
import wikipedia


def home(request):
    return render(request, 'home.html')


def youtube_view(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')  
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
                'published': i['publishedTime']
            }
            desc = ''
            if 'descriptionSnippet' in i and i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        
        context = {
            'results': result_list
        }
        return render(request, 'youtube.html', context)
    else:
        print('An error')
        return render(request, 'youtube.html')


def notes(request):
    notes = Notes.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title and description:
            Notes.objects.create(title=title, description=description)
            return redirect('notes') 

    context = {
        'notes': notes,
    }
    return render(request, 'notes.html', context)


def note_detail(request, pk):
    note = Notes.objects.get(pk=pk)
    context ={
        "note":note
    }

    return render(request, 'notes-details.html', context)


def delete_note(request, pk):
    note = Notes.objects.get(pk=pk)
    note.delete()
    return redirect('notes')


def homework(request):
    homeworks = Homework.objects.all()
    context = {
        'homeworks': homeworks
    }

    if request.method == 'POST':
        subject = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        due = request.POST.get('due')
        is_finished = request.POST.get('is_finished', False)
        
        homework = Homework.objects.create(
            subject=subject,
            title=title,
            description=description,
            due=due,
            is_finished=is_finished
        )
        return redirect('homework')

    return render(request, 'homework.html', context)


def delete_homework(request, homework_id):
    homework = Homework.objects.get(id=homework_id)
    homework.delete()
    return redirect('homework')


def dictionary_view(request):
    input_word = None
    phonetics = None
    definition = None
    example = None
    audio = None

    input_word = None
    word_data = None

    if request.method == 'POST':
        input_word = request.POST.get('word')
        if input_word:
            api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{input_word}"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    word_data = data[0]

    context = {
        'input': input_word,
        'word_data': word_data,
    }
    return render(request, 'dictionary.html', context)

from django.shortcuts import render
import wikipedia

def wikipedia_view(request):
    context = {}
    
    if request.method == 'POST':
        text = request.POST.get('search_query')
        if text:
            try:
                search = wikipedia.page(text)
                context = {
                    'title': search.title,
                    'link': search.url,
                    'details': search.summary
                }
            except wikipedia.exceptions.DisambiguationError as e:
                options = e.options  # List of possible options
                context = {
                    'error_message': 'Ambiguous search term. Please specify more precisely.',
                    'options': options
                }
            except wikipedia.exceptions.PageError:
                context = {'error_message': 'Page not found.'}
            except Exception as e:
                context = {'error_message': f'An error occurred: {e}'}
        else:
            context = {'error_message': 'Please enter a search query.'}
    
    return render(request, 'wikipedia.html', context)


def todo(request):
    todos = ToDo.objects.all()
    todos_done = todos.filter(is_finished=True)
    return render(request, 'todo.html', {'todos': todos, 'todos_done': todos_done})

def create_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        ToDo.objects.create(title=title)
    return redirect('todo')

def delete_todo(request, todo_id):

    if request.method == 'POST':
        todo = ToDo.objects.get(id=todo_id)
        todo.delete()
    return redirect('todo')


def conversion(request):
    if request.method == 'POST':
        measurement = request.POST.get('measurement')
        
        if measurement == 'length':
            input = True
            measure1 = request.POST.get('measure1')
            measure2 = request.POST.get('measure2')
            input_value = request.POST.get('input')
            answer = ''
            if input_value and int(input_value) >= 0:
                if measure1 == 'yard' and measure2 == 'foot':
                    answer = f'{input_value} yard = {int(input_value) * 3} foot'
                elif measure1 == 'foot' and measure2 == 'yard':
                    answer = f'{input_value} foot = {int(input_value) / 3} yard'
            context = {'answer': answer, "input": input, "measurement":measurement}
            return render(request, 'conversion.html', context)

        if measurement == 'mass':
            input = True
            measure1 = request.POST.get('measure1')
            measure2 = request.POST.get('measure2')
            input_value = request.POST.get('input')
            answer = ''
            if input_value and int(input_value) >= 0:
                if measure1 == 'pound' and measure2 == 'kilogram':
                    answer = f'{input_value} pound = {int(input_value) * 0.453592} kilogram'
                elif measure1 == 'kilogram' and measure2 == 'pound':
                    answer = f'{input_value} kilogram = {int(input_value) * 2.20462} pound'
            context = {'answer': answer, "input": input, "measurement":measurement}
            return render(request, 'conversion.html', context)
    else:
        return render(request, 'conversion.html', {'input':False})

def books(request):
    if request.method == 'GET' and 'book_name' in request.GET:
        book_name = request.GET['book_name']
        results = search_books(book_name)
    else:
        results = []  

    context = {
        'results': results,
    }
    return render(request, 'books.html', context)

def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=10"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])

        results = []
        for item in items:
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', 'Unknown Title')
            subtitle = volume_info.get('subtitle', '')
            description = volume_info.get('description', 'No description available.')
            thumbnail = volume_info.get('imageLinks', {}).get('thumbnail', '')
            categories = volume_info.get('categories', [])
            pageCount = volume_info.get('pageCount', '')
            averageRating = volume_info.get('averageRating', '')

            book_data = {
                'title': title,
                'subtitle': subtitle,
                'description': description,
                'thumbnail': thumbnail,
                'categories': categories,
                'pageCount': pageCount,
                'averageRating': averageRating,
                'preview': volume_info.get('previewLink', ''),
            }
            results.append(book_data)
        
        return results
    else:
        return [] 
    

def contact_us(request):
    return render(request, 'contact.html')






