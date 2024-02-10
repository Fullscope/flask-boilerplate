from flask import Flask, abort, request
from flask_cors import CORS
from openai import OpenAI, OpenAIError
import os
import logging
import config
from pydub import AudioSegment

client = OpenAI(api_key="sk-ipsos-facto-insights-service-account-3jyoCwdPMq4ebQMGPWHQT3BlbkFJfcJQT3RrNcX3MDmSQCc0")
if not os.path.isdir("./uploads"):
    try:
        os.mkdir("./uploads")        
    except FileExistsError:
        pass 
upload_path = "./uploads"
if not os.path.isdir("./downloads"):
    try:
        os.mkdir("./downloads")        
    except FileExistsError:
        pass 
download_path = "./downloads"
# Set the OpenAI API key.

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Send a POST request to /whisper with a file attached to transcribe it."


@app.route('/whisper', methods=['POST'])
def handler():
    if not request.files:
        # If the user didn't submit any files, return a 400 (Bad Request) error.
        abort(400)

    # For each file, let's store the results in a list of dictionaries.
    results = []
    

    if request.files: 
        #Get the audio Byte data, and save it to a file in the uploads folder 
        audio_bytes = request.files['file'].read()  # Access the uploaded file        
        with open(os.path.join(upload_path, request.files['file'].filename), "wb") as f:
            f.write(audio_bytes)
        output_audio_file = request.files['file'].filename.split('.')[0] + '.mp3'
        #send the file to the to_mp3 function to convert it to mp3
        try:
            output_audio_file = to_mp3(request.files['file'], output_audio_file)
        except:
            app.logger.error("Error: File not converted to mp3")
            return "Error: File not converted to mp3"
        # Open the file for reading.
        audio_file = open(os.path.join(download_path, output_audio_file), "rb")
        # Let's get the transcript of the temporary file.
        try:
            result = client.audio.transcriptions.create (model="whisper-1", file=audio_file)
        except OpenAIError as e:
            app.logger.error(f"Error: {e}")
            remove_file(os.path.join(download_path, output_audio_file))
            return (f"Error: {e}")

        # Now we can store the result object for this file.
        results.append({
        'transcript': result.text,
        })
        remove_file(os.path.join(download_path, output_audio_file))
        # This will be automatically converted to JSON.
        return {'results': results}

def to_mp3(audio_file, output_audio_file):
    try:
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.filename))
    except TypeError:
        app.logger.error("Error: File type not supported")
        return "Error: File type not supported"
    except:
        app.logger.error("Error: File not found")
        return "Error: File not found"
    audio_data.export(os.path.join(
            download_path, output_audio_file), format="mp3")
    remove_file(os.path.join(upload_path, audio_file.filename))
    return output_audio_file

def remove_file(file_path):
    try:
        os.remove(os.path.abspath(file_path))
    except OSError:
        pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
