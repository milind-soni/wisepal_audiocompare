import base64
import speechbrain as sb
from speechbrain.dataio.dataio import read_audio
from IPython.display import Audio
from speechbrain.pretrained import SpeakerRecognition
from flask import Flask
from flask import request
from os import path
from pydub import AudioSegment

app = Flask(__name__)


@app.route('/greetings')
def greetings():
    return 'May the force be with you!'


@app.route('/getpostexample', methods=['GET', 'POST'])
def GetPostExample():
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                  <h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Language: <input type="text" name="language"></label></div>
               <div><label>Framework: <input type="text" name="framework"></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['language']
    framework = request_data['framework']

    # two keys are needed because of the nested object
    python_version = request_data['version_info']['python']

    # an index is needed because of the array
    example = request_data['examples'][0]

    boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)


@app.route('/audiobyteupload', methods=['POST', 'OPTIONS'])
def audioByteUpload():
    request_data = request.get_json()
    file = request_data['file']
    print(file)
    return {"ok": True}


@app.route('/audiofileupload', methods=['POST'])
def audioFileUpload():
    audioFile1 = request.files['file1']
    audioFile2 = request.files['file2']
    # print(audioFile.filename)
    audioFile1.save(audioFile1.filename)
    audioFile2.save(audioFile2.filename)
    return 'true'


@app.route('/audiofilebase64upload', methods=['POST'])
def audioFilebase64Upload():
    request_data = request.get_json()
    audiofile = request_data['file']
    decode_string = base64.b64decode(audiofile)
    # print(decode_string)
    savefiletolocal('test1.mp3', decode_string)
    return 'true'


def savefiletolocal(uploaded_file, some_bytes):
    binary_file = open(uploaded_file, "wb")

    # Write bytes to file
    binary_file.write(some_bytes)

    # Close file
    binary_file.close()


@app.route('/audiofileCompare', methods=['POST'])
def compareAudioSpeakers():
    # files

    basepath = "/home/milindsoni/Downloads/audiocompare-master/FileCompare/"
    audioFile1 = request.files['file1']
    audioFile2 = request.files['file2']
    # print(audioFile.filename)
    audioFile1.save(basepath + audioFile1.filename)
    audioFile2.save(basepath + audioFile2.filename)
    file1name = audioFile1.filename.rsplit('.', 1)[0].lower()
    file2name = audioFile2.filename.rsplit('.', 1)[0].lower()
    # convert wav to mp3
    if audioFile1.mimetype == 'mp3':
        (AudioSegment.from_mp3(basepath + audioFile1.filename)
         ).export(basepath + file1name + ".wav", format="wav")
    if audioFile2.mimetype == 'mp3':
        (AudioSegment.from_mp3(basepath + audioFile2.filename)
         ).export(basepath + file2name + ".wav", format="wav")

    verFile1 = basepath + file1name + ".wav"
    verFile2 = basepath + file2name + ".wav"

    verification = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
    score, prediction = verification.verify_files(verFile1, verFile2)
    print(prediction, score)
    return str(score.item())


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
