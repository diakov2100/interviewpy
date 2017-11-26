"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import request
from FlaskWebProject1 import app
import os
from ffmpy import FFmpeg
import argparse
import requests
import sys
import xml.etree.ElementTree
import json
import base64

@app.route('/')
@app.route('/home')
def home():
    

    """Renders the home page."""
    return render_template('index.html',
        title='Home Page',
        year=datetime.now().year,)

@app.route('/video', methods=['POST'])
def video_processing():
    data = request.data
    print(data)
    with open("video.webm", "wb") as fh:
        fh.write(base64.decodebytes(data))
    ff = FFmpeg(inputs={'video.webm': None},
        outputs={'audio.mp3': None})
    ff.cmd
    ff.run() 
    api_key = 'f246426f-d49c-4958-bb26-dae6d49042cb'
    uuid = '01ae13cb74d628b58fb536d496daa1e6'
    headers = {'Content-Type': 'audio/x-mpeg-3'}
    data = open('audio.mp3', 'rb').read()
    r = requests.post(url='https://asr.yandex.net/asr_xml?key=%s&uuid=%s&topic=notes' % (api_key, uuid),
                      data=data, headers=headers)

    recognized_strings = map(lambda item: item.text, xml.etree.ElementTree.fromstring(r.text))
    st='';
    for word in recognized_strings:
        st=word;
        break
    os.remove("video.webm")
    os.remove('audio.mp3')
    return (st)

@app.route('/contact')
def contact():
    ff = FFmpeg(inputs={'small.webm': None},
        outputs={'small.ogg': None})
    ff.cmd
    ff.run() 
    """Renders the contact page."""
    return render_template('contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')
