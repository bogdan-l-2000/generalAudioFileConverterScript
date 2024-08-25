import sys, os, time, socket, select

import pydub
import io


class SocketData:
    """
    Data associated with any given socket.

    ===Attributes===
    content: the string denoting the content that has been received or is
        to be sent
    content_bytes: the bytes object denoting the content that has been received
        or is to be sent
    read_complete: a flag to check whether the message is complete or not
    bytes_sent: denotes the number of bytes sent back to the client
    """
    content: str
    content_bytes: bytes
    read_complete: bool
    write_complete: bool
    output_file = io.BytesIO
    to_send: bytes
    bytes_sent: int

    def __init__(self):
        """
        Initialize a Socket Data object
        """
        self.content = ''
        self.content_bytes = b''
        self.read_complete = False
        self.write_complete = False
        self.to_send = b''
        self.bytes_sent = 0


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8000))


# Create a TCP/IP socket

# Listen for incoming connections
sock.listen(5)
# source: https://pymotw.com/3/socket/tcp.html

inputs = [sock]
outputs = []
msg_queue = {}
# Source: https://steelkiwi.com/blog/working-tcp-sockets/


while inputs:
    readable, writable, exceptional = select.select(inputs, outputs, inputs, 5)
    # source: https://pymotw.com/3/socket/tcp.html
    for read_from in readable:
        # Source: https://steelkiwi.com/blog/working-tcp-sockets/
        if read_from is sock:
            # Socket is the server, we accept a browser socket

            # Accept a socket
            connection, client_address = sock.accept()
            # source: https://pymotw.com/3/socket/tcp.html

            # Set the socket to nonblocking, add socket and create data object
            connection.setblocking(False)
            inputs.append(connection)
            msg_queue[connection] = SocketData()
            # source: https://steelkiwi.com/blog/working-tcp-sockets/
        else:
            if not msg_queue[read_from].read_complete:
                try:
                    # print("waiting...")
                    data = read_from.recv(16)

                    msg_queue[read_from].content_bytes += data
                    if len(msg_queue[read_from].content_bytes) >= 32 and b"EOF\r\n\r\n" in msg_queue[read_from].content_bytes[-32:]:
                        print("File read!")
                        msg_queue[read_from].read_complete = True

                        outputs.append(read_from)
                        inputs.remove(read_from)
                        request_list = msg_queue[read_from].content_bytes.split(b"\r\n")

                        content_index = request_list.index(b"CONTENT")
                        old_file_content = b"\r\n".join(request_list[content_index+1:-3])

                        received_file = io.BytesIO(old_file_content)
                        audio = pydub.AudioSegment.from_file(received_file,
                                                             format="m4a")
                        # audio.export("NEW_FILE_NAME.wav", format='wav')
                        msg_queue[read_from].output_file = io.BytesIO()
                        msg_queue[read_from].output_file = audio.export(msg_queue[read_from].output_file, 'wav')
                        msg_queue[read_from].output_file.seek(0)

                finally:
                    pass

    for write_to in writable:
        if not msg_queue[write_to].write_complete:
            try:
                # print("sending...")
                msg_queue[write_to].to_send = msg_queue[write_to].output_file.read(16)
                # print(msg_queue[write_to].to_send)
                write_to.send(msg_queue[write_to].to_send)
                msg_queue[write_to].bytes_sent += 16

                if not msg_queue[write_to].to_send:
                    msg_queue[write_to].write_complete = True
                    write_to.send(b"\r\nEOF\r\n\r\n")
            finally:
                pass

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del msg_queue[s]
    # Source: https://steelkiwi.com/blog/working-tcp-sockets/
