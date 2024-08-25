import os.path
import socket
import pydub

FILENAME = "FILE_NAME.m4a"

s = socket.socket()
s.connect(("localhost", 8000))
filetosend = open(FILENAME, "rb")
s.send(b"FILESIZE\r\n")
print(os.path.getsize(FILENAME))
s.send(str(os.path.getsize(FILENAME)).encode() + b"\r\n")
s.send(b"FILENAME\r\n")
s.send(FILENAME.encode("utf-8") + b"\r\n")
s.send(b"CONTENT\r\n")
data = filetosend.read(1024)
print(data)
while data:
    # print("Sending...")
    s.send(data)
    data = filetosend.read(1024)
filetosend.close()
s.send(b"\r\n")
s.send(b"EOF\r\n\r\n")
print("Done Sending.")
print(os.path.getsize(FILENAME))
print(str(os.path.getsize(FILENAME)).encode())
content = b""
file_read = False
while not file_read:
    # print("Reading...")
    response = s.recv(16)
    content += response
    if len(content) > 32 and b"\r\nEOF\r\n\r\n" in content[-32:]:
        file_read = True
print("Done Reading.")
print(content)
s.shutdown(2)
s.close()

output_file = open(FILENAME[:-4] + ".wav", 'wb')
output_file.write(content[:-9])
output_file.close()
