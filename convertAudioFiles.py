import pydub
import sys, os

accepted_input_formats = ['wav', 'mp3', 'ogg', 'flv', 'mp4', 'wma', 'aac', 'm4a']
accepted_output_formats = ['wav', 'mp3', 'ogg', 'flv']

old_file_path = None
while old_file_path is None or not (os.path.isfile(old_file_path) and os.path.splitext(old_file_path)[-1][1:].lower() in accepted_input_formats):
    old_file_path = input("Enter a path to a file that you would like to convert. This must be an audio file: ")

new_file_format = None

while new_file_format not in accepted_output_formats:
    new_file_format = input("Enter the file format you wish to convert this to. File format must be one of type wav, mp3, ogg, flv: ")

old_file_format = os.path.splitext(old_file_path)[-1][1:].lower()

if old_file_format == new_file_format:
    print("New file format is the same as the old format: exiting program")
    sys.exit(1)

audio = pydub.AudioSegment.from_file(old_file_path, format=old_file_format)

new_file_path = os.path.splitext(os.path.basename((old_file_path)))[0] + '.' + new_file_format
audio.export(new_file_path, format=new_file_format)
