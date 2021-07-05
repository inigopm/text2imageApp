from flask import Flask, render_template, url_for, send_from_directory, request
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
from werkzeug.utils import secure_filename
from util import texts
import random
import time

app = Flask(__name__)


@app.route('/')
def index():
    """
    This function generates an overview.
    """
    return render_template("index.html")


@app.route('/text_image')
def application():
    """
    This function genererates the text to image page.
    """
    return render_template("predictor.html", texts = texts.random_texts(5, texts.retrieve_texts_names_in_folder("static/randomTexts"), "static/randomTexts"))

@app.route('/text_image/output', methods=['POST'])
def output():
    """
    This function handles the input that the user gives (file uploaded by a user or random text) and gives an output.
    """
    # Form data
    data = request.form
    
    if data.get("custom-inputAttn-GAN") == '':
    	f = open("static/randomTexts/" + data.get("randomTextAttn-GAN"), "r")
    	text = f.readline()
    	f.close()
    else:
	text = data.get("custom-inputAttn-GAN")
	
    f = open("attngan/data/coco/webapp.txt", "w")
    f.write(text)
    f.close()
    
    os.chdir("attngan/code")
    os.system('python main.py')
    os.chdir("../../")
    files = os.listdir("static/pictures/Attn-GAN")
    for filename in files:
    	os.remove("static/pictures/Attn-GAN/"+filename)
    	if "0_s_0_g" in filename:
    		num = int(filename[7:9])+1
    		if num == 100:
    			num = 10
    		os.rename("attngan/models/coco_AttnGAN2/webapp/0_s_0_g2.png", "static/pictures/Attn-GAN/0_s_0_g"+str(num)+".png")
    		path1 = "../static/pictures/Attn-GAN/0_s_0_g"+str(num)+".png"
    	else:
    		num = int(filename[7:9])+1
    		if num == 100:
    			num = 10
    		os.rename("attngan/models/coco_AttnGAN2/webapp/0_s_0_a1.png", "static/pictures/Attn-GAN/0_s_0_a"+str(num)+".png")
    		path2 = "../static/pictures/Attn-GAN/0_s_0_a"+str(num)+".png"
    		
    
    return render_template("output.html", texts = text, paths = [path1,path2])

@app.errorhandler(404)
def page_not_found(e):

    """
    This function handles 404 errors.
    """
    return render_template("404.html")

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port=5000)
