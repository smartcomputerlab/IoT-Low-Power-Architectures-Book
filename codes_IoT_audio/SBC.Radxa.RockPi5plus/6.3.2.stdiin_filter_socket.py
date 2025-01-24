import socket

destination_ip = "192.168.1.47"
#destination_ip = "127.0.0.1"         # to test locally
destination_port = 8888

def send_udp_message(message,ip_address,port):
    try:
        udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_socket.sendto(message.encode(),(ip_address, port))
        udp_socket.close()
        print("UDP package sent")

    except Exception as e:
        print("Error sending UDP package")

def main():
    while True:
        result=input("Write a message: ")
        send_udp_message(result,destination_ip,destination_port)

if __name__ == "__main__":
    main()
    
    
