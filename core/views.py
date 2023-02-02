from django.shortcuts import render
from tablib import Dataset
from .resources import PersonResource
from .models import Person


# Create your views here.


def importExcel(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_persons = request.FILES['my_file']
        imported_data = dataset.load(new_persons.read(), format= 'xlsx')
        for data in imported_data:
            value = Person(
                data[0],
                data[1],
                data[2],
                data[3]
            )
            value.save()


    return render(request, 'dashboard/form.html')