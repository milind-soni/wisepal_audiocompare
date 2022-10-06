import speechbrain as sb
from speechbrain.dataio.dataio import read_audio
from IPython.display import Audio
from speechbrain.pretrained import SpeakerRecognition
from flask import Flask 
from flask import request
from os import path
from pydub import AudioSegment

compareaudiofile = Flask(__name__)

@compareaudiofile.route('/greetings')
def greetings():
    return 'May the force be with you!'

@compareaudiofile.route('/audiofileCompare',methods=['POST'])
def compareAudioSpeakers():
    # files                                                                         
    
    basepath = "C:/code/pyaudio/FileCompare/"
    audioFile1 = request.files['file1']
    audioFile2 = request.files['file2']
    #print(audioFile.filename)
    audioFile1.save(basepath + audioFile1.filename)
    audioFile2.save(basepath + audioFile2.filename)
    file1name = audioFile1.filename.rsplit('.', 1)[0].lower()
    file2name = audioFile2.filename.rsplit('.', 1)[0].lower()
    print (audioFile1.mimetype)
    print (audioFile2.mimetype)
    # convert wav to mp3          
    if audioFile1.mimetype=='audio/mpeg':        
        (AudioSegment.from_mp3(basepath + audioFile1.filename)).export(basepath + file1name + ".wav", format="wav")
    if audioFile2.mimetype=='audio/mpeg':        
        (AudioSegment.from_mp3(basepath + audioFile2.filename)).export(basepath + file2name + ".wav", format="wav")
        
    verFile1 =basepath +  file1name + ".wav"
    verFile2 =basepath +  file2name + ".wav"
   
    verification = SpeakerRecognition.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="pretrained_models/spkrec-ecapa-voxceleb")
    score, prediction = verification.verify_files(verFile1, verFile2)
    print(prediction, score)   
    return str(score.item())

if __name__ == 'main':
    compareaudiofile.run()