import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
import petl as etl
import csv
from .forms import FetchStarWarsData
from .models import Character, DataSet
import uuid

# Create your views here.

def landing_page(request):
    return render(request, 'landing.html')


def home_screen_view(request):
    global header
    sw_collect = DataSet.objects.all().order_by('downloaded_time').reverse()

    if request.method == 'POST':
        form = FetchStarWarsData(request.POST)
        if form.is_valid():
            url = 'https://swapi.dev/api/people/'
            url_planets = 'https://swapi.dev/api/planets/'

            characters = []
            planets = []
            while url:
                response = requests.get(url)
                data = response.json()
                characters.extend(data['results'])
                url = data['next']

            while url_planets:
                response_planet = requests.get(url_planets)
                data_planet = response_planet.json()
                planets.extend(data_planet['results'])
                url_planets = data_planet['next']

            unique_filename = str(uuid.uuid4())

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{unique_filename}.csv"'
            writer = csv.writer(response)

            dataset = DataSet.objects.create(filename=unique_filename)

            for character in characters:
                Character.objects.create(
                    name=character['name'],
                    height=character['height'],
                    mass=character['mass'],
                    hair_color=character['hair_color'],
                    skin_color=character['skin_color'],
                    eye_color=character['eye_color'],
                    birth_year=character['birth_year'],
                    gender=character['gender'],
                    edited=character['edited']
                    # homeworld=planets[character['name'][-1]]
                    # TODO: resolve from external endpoint
                )

                csv_writer = csv.writer(response)

                count = 0

                for emp in characters:
                    if count == 0:
                        # header = emp.keys()
                        header = ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year',
                                  'gender', 'homeworld', 'date']
                        csv_writer.writerow(header)
                        count += 1
                        # Writing data of CSV file
                        # csv_writer.writerow(emp.values())
                    planet_number = int(emp['homeworld'].rsplit('/', 2)[1])

                    csv_writer.writerow([emp['name'], emp['height'], emp['mass'], emp['hair_color'],
                                         emp['skin_color'], emp['eye_color'], emp['birth_year'],
                                         emp['gender'], planets[planet_number-1]['name'],
                                         emp['edited'][0:10]])

                    if not os.path.exists('stored_csv'):
                        os.mkdir('stored_csv/')
                    else:
                        with open(os.path.join('stored_csv/', unique_filename + '.csv'), 'wb') as f:
                            f.write(response.content)


                else:
                    break

            return response

    else:
        form = FetchStarWarsData()


    return render(request, 'content.html', {"sw_collect": sw_collect, "form": form})


def preview_downloaded_csv(request, filename):
    if DataSet.objects.filter(filename=filename).exists():
        filename = filename + '.csv'
    else:
        filename = 'File does not exist!'

    offset = int(request.GET.get('offset', 0))
    table = etl.fromcsv(f'stored_csv/{filename}', encoding='utf-8')[1:offset + 11]

    header = ['name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color', 'birth_year',
              'gender', 'homeworld', 'date']

    context = {
        'filename': filename,
        'table': table,
        'offset': offset,
        'header': header
    }

    return render(request, "csv_preview.html", context)


def load_more(request):
    offset = int(request.GET.get('offset'))
    limit = int(request.GET.get('limit'))
    table = etl.fromcsv('stored_csv/3e8be355-f1cc-4f26-840e-91c91780fe66.csv')
    return render(request, 'csv_preview.html', {'table': table})
