from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
import time as tim

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def homepage():
    return render_template("index.html")


@app.route("/youtube/api", methods = ['POST', 'GET'])
def youtube():
    global file_type
    global link_input
    global title
    global video1
    global video2
    
    if request.method == "POST":
        file_type = request.form.get("file_type")
        link_input = request.form.get("link_input")
    
        video = YouTube(link_input)
    
        thumbnail_url = YouTube(link_input).thumbnail_url
        title = YouTube(link_input).title
        description = YouTube(link_input).description
        author = YouTube(link_input).author
        length = tim.strftime("%H:%M:%S", tim.gmtime(YouTube(link_input).length))
        time = str(YouTube(link_input).publish_date)
        
        
        videos = video.streams.filter(progressive=True)
        
        video1 = videos[1]
        video2 = videos[2]
        
        video1_filesize = int(video1.filesize/1048576)
        video2_filesize = int(video2.filesize/1048576)
        
        
        
        if file_type == "mp3":
            return render_template("index2.html",
            thumbnail_url = thumbnail_url,
            title = title,
            description = description[:300],
            author = author,
            time = time[:10],
            length = length,)
        
        
        return render_template("index1.html",
            thumbnail_url = thumbnail_url,
            title = title,
            description = description[:300],
            author = author,
            time = time[:10],
            length = length,
            video1 = video1,
            video2 = video2,
            video1_filesize = video1_filesize,
            video2_filesize = video2_filesize)
    
    else:
        return redirect(url_for("homepage"))


@app.route("/downloadmp3", methods = ['POST', 'GET'])
def downloadmp3():
    global file_type
    global link_input
    global title
        
    video = YouTube(link_input).streams.filter(only_audio=True).first()
    video.download(filename=title+".mp3")

    return render_template("downloaded.html")

@app.route("/download360p", methods = ['POST', 'GET'])
def download360p():
    global file_type
    global link_input
    global title
    global video1
    
    video1.download(filename=title+"_360p"+".mp4")

    return render_template("downloaded.html")

@app.route("/download720p", methods = ['POST', 'GET'])
def download720p():
    global file_type
    global link_input
    global title
    global video2
    
    video2.download(filename=title+"_720p"+".mp4")
    
    return render_template("downloaded.html")



if __name__ == "__main__":
    app.run(debug=True)