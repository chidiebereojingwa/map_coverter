import os

from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import folium

from image_converter.image_converter import settings


def convert_image_to_map(request):
    # Load the input image
    #image = Image.open('input_image.jpg')
    image = Image.open(os.path.join(settings.MEDIA_ROOT, 'input_image.jpg'))
    width, height = image.size

    # Convert image to map
    map_object = folium.Map(location=[0, 0], zoom_start=1, control_scale=True)

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            lat = (r - 128) / 256 * 90
            lon = (g - 128) / 256 * 180
            folium.Marker([lat, lon]).add_to(map_object)

    # Save the map as an HTML file
    map_file_path = 'media/output_map.html'
    map_object.save(map_file_path)

    # Return a download link to the generated map
    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename="output_map.html"'
    with open(map_file_path, 'rb') as f:
        response.write(f.read())

    return response

