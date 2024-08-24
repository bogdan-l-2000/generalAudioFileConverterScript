# generalAudioFileConverterScript
High-level script to convert audio files between formats, introduction to audio programming

Main library used: pydub (https://pypi.org/project/pydub/)

If pydub cannot find the specified file, run the following command:
`conda install -c conda-forge ffmpeg`


In the process of creating a server that converts files and sends the converted files to clients, along with a sample client for the server.
Currently, the server is able to convert the client's file from an `.m4a` to a `.wav` format and saves the file in the local directory. 

Next steps are to send the updated file content back to the client.
