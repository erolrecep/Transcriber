#!/usr/bin/env python


# import required libraries
import shlex
import subprocess
import sys
import json
import os
import numpy as np
from deepspeech import Model
import wave
from timeit import default_timer as timer


cwd = os.getcwd()
MODEL_FILE = cwd + "/models/deepspeech-0.7.4-models.pbmm"
SCORER_FILE = cwd + "/models/deepspeech-0.7.4-models.scorer"
AUDIO_FILE = cwd + "/audio_files/deneme.wav"
TXT_OUTPUT_FOLDER = cwd + "/output"

# I don't know yet what this is but I am going to find
candidate_transcripts = 3


# Custom functions
def convert_samplerate(audio_path, desired_sample_rate):
    sox_cmd = 'sox {} --type raw --bits 16 --channels 1 --rate {} --encoding signed-integer --endian little ' \
              '--compression 0.0 --no-dither - '.format(shlex.quote(audio_path), desired_sample_rate)
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('SoX returned non-zero status: {}'.format(e.stderr))
    except OSError as e:
        raise OSError(e.errno,
                      'SoX not found, use {}hz files or install it: {}'.format(desired_sample_rate, e.strerror))

    return desired_sample_rate, np.frombuffer(output, np.int16)


def words_from_candidate_transcript(metadata):
    word = ""
    word_list = []
    word_start_time = 0
    # Loop through each character
    for i, token in enumerate(metadata.tokens):
        # Append character to word if it's not a space
        if token.text != " ":
            if len(word) == 0:
                # Log the start time of the new word
                word_start_time = token.start_time

            word = word + token.text
        # Word boundary is either a space or the last character in the array
        if token.text == " " or i == len(metadata.tokens) - 1:
            word_duration = token.start_time - word_start_time

            if word_duration < 0:
                word_duration = 0

            each_word = dict()
            each_word["word"] = word
            each_word["start_time "] = round(word_start_time, 4)
            each_word["duration"] = round(word_duration, 4)

            word_list.append(each_word)
            # Reset
            word = ""
            word_start_time = 0

    return word_list


def metadata_to_string(metadata):
    return ''.join(token.text for token in metadata.tokens)


def metadata_json_output(metadata, filename):
    json_result = dict()
    json_result["transcripts"] = [{
        "confidence": transcript.confidence,
        "words": words_from_candidate_transcript(transcript),
    } for transcript in metadata.transcripts]

    with open(filename, 'w') as fp:
        json.dump(json_result, fp)

    # return json.dumps(json_result, indent=2)


# Write inference result to a txt file
def write2txt(filename, text):
    txt_file = open(filename, "w")
    txt_file.write(text)
    txt_file.close()


# Transcribe single file
def transcribe_(audio_file):
    pass


# Transcribe many files from a list
def transcribe_many(list_of_files):
    pass


def load_model(model_file, scorer_file):
    ds = Model(model_file)

    ds.enableExternalScorer(scorer_file)
    return ds


if __name__ == '__main__':
    print(MODEL_FILE)
    print(SCORER_FILE)

    # load DeepSpeech model
    print('Loading model and scorer files {}'.format(MODEL_FILE), file=sys.stderr)
    model_load_start = timer()
    # sphinx-doc: python_ref_model_start
    # ds = Model(MODEL_FILE)
    ds = load_model(MODEL_FILE, SCORER_FILE)
    # sphinx-doc: python_ref_model_stop
    model_load_end = timer() - model_load_start
    print('Loaded model and in {:.3}s.'.format(model_load_end), file=sys.stderr)

    desired_sample_rate = ds.sampleRate()

    # print('Loading scorer from files {}'.format(SCORER_FILE), file=sys.stderr)
    # scorer_load_start = timer()
    # ds.enableExternalScorer(SCORER_FILE)
    # scorer_load_end = timer() - scorer_load_start
    # print('Loaded scorer in {:.3}s.'.format(scorer_load_end), file=sys.stderr)

    # TODO: lm_alpha and lm_beta are omitted because they are being used from scorer

    # read video_urls or video_locs file and transcribe one by one
    with open(cwd + "/audio_locations.txt", "r") as f:
        locations = f.read()

    locations = locations.split("\n")

    for audio_loc in locations:
        print(f"audio location: {audio_loc}")

        fin = wave.open(audio_loc, 'rb')
        fs_orig = fin.getframerate()
        if fs_orig != desired_sample_rate:
            print(
                'Warning: original sample rate ({}) is different than {}hz. Resampling might produce erratic speech '
                'recognition.'.format(
                    fs_orig, desired_sample_rate), file=sys.stderr)
            fs_new, audio = convert_samplerate(audio_loc, desired_sample_rate)
        else:
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

        audio_length = fin.getnframes() * (1 / fs_orig)
        fin.close()

        print('Running inference.', file=sys.stderr)
        inference_start = timer()
        # sphinx-doc: python_ref_inference_start

        # Write inference output as a string to a txt file
        output_text = metadata_to_string(ds.sttWithMetadata(audio, 1).transcripts[0])
        # print(output_text)

        # Write output txt to a txt file
        audio_file = audio_loc
        text_filename = audio_file[:-4] + "_DeepSpeech_output.txt"
        print(f"TXT Inference result is being written to {text_filename}")
        write2txt(filename=text_filename, text=output_text)

        # Also write output with other metadata to a json file
        json_filename = audio_file[:-4] + "_DeepSpeech_output.json"
        print(f"JSON Inference result is being written to {json_filename}")
        metadata_json_output(ds.sttWithMetadata(audio, candidate_transcripts), filename=json_filename)

        inference_end = timer() - inference_start
        print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length), file=sys.stderr)