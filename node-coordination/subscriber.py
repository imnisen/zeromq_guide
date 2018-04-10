#
#  Synchronized subscriber
#
import time

import zmq

def main():
    context = zmq.Context()

    # First, connect our subscriber socket
    subscriber = context.socket(zmq.SUB)
    subscriber.connect('tcp://localhost:5561')
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')

    time.sleep(1)

    # Second, synchronize with publisher
    syncclient = context.socket(zmq.REQ)
    syncclient.connect('tcp://localhost:5562')

    # send a synchronization request
    syncclient.send(b'')

    # wait for synchronization reply
    syncclient.recv()

    # Third, get our updates and report how many we got
    nbr = 0
    while True:
        msg = subscriber.recv()
        if msg == b'END':
            break
        nbr += 1

    print ('Received %d updates' % nbr)

if __name__ == '__main__':
    main()

#     We can't assume that the SUB connect will be finished by the time the REQ/REP dialog is complete. There are no guarantees that outbound connects will finish in any order whatsoever, if you're using any transport except inproc. So, the example does a brute force sleep of one second between subscribing, and sending the REQ/REP synchronization.

# A more robust model could be:

# Publisher opens PUB socket and starts sending "Hello" messages (not data).
# Subscribers connect SUB socket and when they receive a Hello message they tell the publisher via a REQ/REP socket pair.
# When the publisher has had all the necessary confirmations, it starts to send real data.
