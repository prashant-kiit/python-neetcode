"""
A minimal single-threaded, asynchronous TCP server using epoll (Linux).
This mirrors the Go implementation described in the transcript:
  - one socket for the server, set to non-blocking
  - one epoll instance
  - server fd registered for EPOLLIN (new connection ready)
  - each accepted client fd also registered for EPOLLIN (data ready to read)
  - a single infinite loop calls epoll.poll() and dispatches events

Run:  python3 async_tcp_epoll.py
Test: redis-cli -p 7379   (or) nc localhost 7379
"""

import socket
import select

HOST = "0.0.0.0"
PORT = 7379
MAX_CLIENTS = 20000  # backlog size, same role as "max clients" in the transcript


def eval_and_respond(cmd: bytes, conn: socket.socket):
    """Very small command evaluator -- only PING is implemented,
    exactly like the state of the DiceDB server at this point in the video."""
    command = cmd.strip().upper()
    if command == b"PING":
        conn.send(b"+PONG\r\n")
    elif command == b"":
        pass
    else:
        conn.send(b"-ERR unknown command\r\n")


def read_command(conn: socket.socket) -> bytes:
    """Blocking-looking read, but the fd itself is non-blocking;
    epoll only calls us when data is actually available."""
    return conn.recv(1024)


def run_async_tcp_server():
    print(f"Starting an asynchronous TCP server on {HOST}:{PORT}")

    # ---- 1. Create the listening socket (raw, non-blocking, stream) ----
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(False)          # non-blocking mode
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)          # start listening, with backlog
    server_fd = server_socket.fileno()

    # ---- 2. Create the epoll instance and register the server fd ----
    epoll = select.epoll()                     # epoll_create1()
    epoll.register(server_fd, select.EPOLLIN)   # epoll_ctl(ADD, server_fd, EPOLLIN)

    # Keep a lookup from fd -> socket object, since epoll only deals in fds
    fd_to_socket = {server_fd: server_socket}

    try:
        while True:  # the "gigantic for loop" -- our actual event loop
            # epoll_wait(): blocks here (not on accept/recv) until *something*
            # is ready. Returns a list of (fd, event) pairs.
            events = epoll.poll()

            for fd, event in events:
                if fd == server_fd:
                    # Server fd is ready for IO => a new client wants to connect
                    client_socket, addr = server_socket.accept()
                    client_socket.setblocking(False)
                    client_fd = client_socket.fileno()

                    # Register this new client fd too, so epoll also
                    # notifies us when *this* client sends data
                    epoll.register(client_fd, select.EPOLLIN)
                    fd_to_socket[client_fd] = client_socket
                    print(f"Accepted new client: fd={client_fd}, addr={addr}")

                else:
                    # An already-connected client fd is ready for IO
                    # => the client has sent us a command
                    client_socket = fd_to_socket[fd]
                    try:
                        data = read_command(client_socket)
                        if not data:
                            # Client disconnected: unregister and clean up
                            epoll.unregister(fd)
                            client_socket.close()
                            del fd_to_socket[fd]
                            print(f"Client disconnected: fd={fd}")
                            continue

                        eval_and_respond(data, client_socket)

                    except (ConnectionResetError, BrokenPipeError):
                        epoll.unregister(fd)
                        client_socket.close()
                        del fd_to_socket[fd]

    finally:
        epoll.unregister(server_fd)
        epoll.close()
        server_socket.close()


if __name__ == "__main__":
    run_async_tcp_server()