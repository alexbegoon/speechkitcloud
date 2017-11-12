from asrclient.voiceproxy_pb2 import AddDataResponse as AsrResponse

"""
use it like
./asrclient-cli.py -k <your-key> --callback-module advanced_callback_example --silent <path-to-your-sound.wav>
"""

session_id = "not-set"

def advanced_callback(asr_response, correction = 0, start_time = 0):
    print("Got response:")
    print("end-of-utterance = {}".format(asr_response.endOfUtt))
    r_count = 0
    last_words = []
    for r in asr_response.recognition:
        print("recognition[{}] = {}; confidence = {}".format(r_count, r.normalized.encode("utf-8"), r.confidence))
        print("utterance timings: from {} to {}".format(r.align_info.start_time+correction,r.align_info.end_time+correction))
        w_count = 0
        last_words = r.words
        for w in r.words:
            print("word[{}] = {}; confidence = {}".format(w_count, w.value.encode("utf-8"), w.confidence))
            print("word timings: from {} to {}".format(w.align_info.start_time+correction,w.align_info.end_time+correction))
            w_count += 1
        r_count += 1
    requests.post("http://happybox.omadonex.com/api/data/speech", data={'recognition': recognition[r_count], 'words': last_words, 'start_time': start_time})

def advanced_utterance_callback(asr_response, data_chunks):
    data_length = 0
    for chunk in data_chunks:
        data_length += len(chunk) if chunk else 0
    print("Got complete utterance, for {0} data_chunks, session_id = {1}".format(len(data_chunks), session_id))
    print("Metainfo", asr_response.metainfo.minBeam, asr_response.metainfo.maxBeam)
    print("Data length = {0}".format(data_length))
