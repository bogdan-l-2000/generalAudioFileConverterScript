# generalAudioFileConverterScript
High-level script to convert audio files between formats, introduction to audio programming

Main library used: pydub (https://pypi.org/project/pydub/)

If pydub cannot find the specified file, run the following command:
`conda install -c conda-forge ffmpeg`


In the process of creating a server that converts files and sends the converted files to clients, along with a sample client for the server.
Currently, the server is able to convert the client's files to a `.wav` format and sends the updated file content to the client. 

Next step in the process is creating sample clients for different applications. 
Might be possible to create a web application here as well.
