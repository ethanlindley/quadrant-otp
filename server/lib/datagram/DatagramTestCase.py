from Datagram import Datagram
from DatagramIterator import DatagramIterator

datagram = Datagram()
datagram.add_be_float64(60)
datagram.add_bool(True)
datagram.add_string("test")

dgi = DatagramIterator(datagram)
int8 = dgi.get_be_float64()
boolean = dgi.get_bool()
string = dgi.get_string()

print "int: %s\nbool: %s\nstring: %s" % (str(int8), str(boolean), str(string))
