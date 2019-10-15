from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
import os
from wsgiref.util import FileWrapper
from wsgiref.util import FileWrapper
import json
from .models import Video
import ntpath
import youtube_dl
import random
from glob import glob

from .forms import UploadFileForm

script_path = os.path.dirname(os.path.abspath(__file__))
video_dir_name = 'video'
video_dir = os.path.join(script_path, video_dir_name)


def show_downloader(request):
    return render(request, 'tube_download.html', {})


def download_video_return_path(youtube_url):
    while True:
        temp_dir = os.path.join(video_dir, str(random.randint(10 ** 10, 10 ** 15)))
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            break

    ydl_opts = {'outtmpl': f'{temp_dir}/%(extractor_key)s/%(extractor)s-%(id)s-%(title)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    files = []
    start_dir = temp_dir
    pattern = "*.mp4"

    for dir, _, _ in os.walk(start_dir):
        files.extend(glob(os.path.join(dir, pattern)))

    if files:
        return files[0]
    return None


def create_or_check_video_dir():
    if not os.path.exists(video_dir):
        os.makedirs(video_dir, exist_ok=True)


def download_video(request, video_id):
    video = Video.objects.get(id=video_id)

    file = FileWrapper(open(video.video_path, 'rb'))
    filename = ntpath.basename(video.video_path)
    response = HttpResponse(file, content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def convert_video(request):
    print(request)
    if request.method == 'POST':
        body = json.loads(request.body.decode('UTF-8'))

        youtube_url = [x for x in body['form'] if x['name'] == 'YouTubeURL']
        youtube_url = youtube_url[0]['value']
        if not youtube_url:
            youtube_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        create_or_check_video_dir()
        video_path = download_video_return_path(youtube_url)
        video = Video(video_path=video_path)
        video.save()
        return HttpResponse(video.id)
