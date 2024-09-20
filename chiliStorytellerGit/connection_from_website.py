from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from multiprocessing.connection import Listener




#Connection with the other node


print ('\n\nStarting... Waiting for conenction\n\n')
address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'secret password')
conn = listener.accept()
print ('Connection accepted from', listener.last_accepted)




@inlineCallbacks
def main(session, details):
    
    
    yield session.call("rie.dialogue.say",
    text="Hello, I am successfully connected!")


    print("Robot running and waiting for messages")

    yield sleep(0.01) 
    
    print("\n\nWaiting messages!")

    while True:
        
        msg = conn.recv()
        # msg = input("type")
        # do something with msg
        print("\n\nMessage received:" + str(msg))

        if msg == 'close':
            # conn.close()
            break

        else:
            yield session.call("rie.dialogue.say",
            text=msg)

        yield sleep(0.01) 


    # listener.close()

    session.leave() # Sluit de verbinding met de robot

# Create wamp connection
wamp = Component(
transports=[{
    "url": "ws://wamp.robotsindeklas.nl",
    "serializers": ["json"]
    }],
    realm="rie.66b5f83389e0147f994f5e85",
)

wamp.on_join(main)

if __name__ == "__main__":
    run([wamp])