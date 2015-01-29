import argparse

def get_args():
    parser = argparse.ArgumentParser(description="simple Media Center - a simple Media Center application")
    parser.add_argument("-i", "--ip", nargs="?", default="127.0.0.1", help="ip address on which to serve [127.0.0.1]")
    parser.add_argument("-p", "--port", nargs="?", type=int, default=5000, help="port on which to serve [5000]")
    return parser.parse_args()