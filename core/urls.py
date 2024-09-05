from django.urls import path
from .views import home, youtube_view, create_todo, delete_todo, todo, books, dictionary_view, wikipedia_view, notes, note_detail, homework, delete_homework, delete_note, conversion, contact_us

urlpatterns = [
    path('', home, name='home'),
    path('books/', books, name="books"),
    path('contact/', contact_us, name="contactus"),
    path('dict/', dictionary_view, name="dictionary"),
    path('youtube-search/', youtube_view, name='youtube-search'),
    path('todo/', todo, name='todo'),
    path('create-todo/', create_todo, name='create-todo'),
    path('conversation/', conversion, name='conversation'),
    path('delete-todo/<int:todo_id>', delete_todo, name='delete-todo'),
    path('notes/', notes, name='notes'),
    path('notes-detail/<int:pk>', note_detail, name='notedetail'),
    path('notes-delete/<int:pk>', delete_note, name='notedelete'),
    path('wiki/', wikipedia_view, name="wikipedia"),
    path('homework/', homework, name='homework'),
    path('homework/delete/<int:homework_id>/', delete_homework, name='delete_homework'),
]