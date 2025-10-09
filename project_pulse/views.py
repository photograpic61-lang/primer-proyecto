from django.shortcuts import render

# Vista principal
def home(request):
    return render(request, 'index.html')
