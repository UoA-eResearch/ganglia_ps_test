import config
import xml.sax
import socket

class GmondCollector():

  gmond_xml_blob = ''

  def __init__(self):
    ''' read data from the gmond collector '''
    bufsize = 100000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config.gmond_host, config.gmond_port))
    incoming = s.recv(bufsize)
    while (incoming != ""):
      self.gmond_xml_blob += incoming;
      incoming = s.recv(bufsize)
    s.close()
    if not self.gmond_xml_blob:
      raise Exception('Failed to read data from gmond collector')

  def get_hosts_with_outdated_processes(self):
    handler = AgeHandler()
    xml.sax.parseString(self.gmond_xml_blob, handler)
    return handler.hosts


class AgeHandler(xml.sax.ContentHandler):
  hosts = {}
  hosttmp = ''

  def startElement(self, name, attrs):
    if name == "HOST":
      self.hosttmp = str(attrs.getValue("NAME"))
      if self.hosttmp.endswith('-p'):
        self.hosttmp = self.hosttmp[0:-2]
      self.hosts[self.hosttmp] = -1

    if name == "METRIC" and self.hosttmp in self.hosts:
      attrname = attrs.getValue("NAME")
      if "ps-" in attrname:
        lifetime = attrs.getValue("TN")
        if lifetime:
          self.hosts[self.hosttmp] = max(int(lifetime), self.hosts[self.hosttmp])

  def endDocument(self):
    ''' clean up at the end '''
    if self.hosts:
      for hostname in self.hosts.keys():
        if self.hosts[hostname] <= config.gmond_process_age_limit:
          del(self.hosts[hostname])

if __name__ == '__main__':
  print GmondCollector().get_hosts_with_outdated_processes()

