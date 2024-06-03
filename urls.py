from django.urls import path
from . import views   # . dot is define current application
from django.conf import settings
from django.conf.urls.static import static



urlpatterns=[
    path('',views.home, name='home'),
    path('notes',views.notes, name='notes'),
    path('delete_notes/<int:pk>',views.delete_notes,name='delete_note'),
    path('notes_detail/<int:pk>',views.NotesDetailView.as_view(),name='notes_details'),
    path('homework/',views.homework,name='homework'),
    path('update_homework/<int:homework_id>/', views.update_homework_status, name='update_homework_status'),
    path('delete_homework/<int:pk>/', views.delete_homework, name='delete_homework'),
    path('youtube',views.youtube,name="youtube"),
    path('todo',views.todo,name='todo'),
    path('update_todo/<int:pk>/', views.update_todo, name='update_todo'),
    path('delete_todo/<int:pk>',views.delete_todo,name='delete_todo'),
    path('books',views.books,name='books'),
    path('dictionary',views.dictionary,name='dictionary'),
    path('wiki',views.wiki,name='wiki'),
    path('conversion',views.conversion,name='conversion'),
    path('logout/', views.logout_view, name='logout'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     