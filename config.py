import yaml

import dropboxconn

class Config:
  def __init__(self, filename="config.yaml"):
    with open(filename, 'r') as f:
     self.doc = yaml.load(f)

  def get_connectors(self, connector=None):
    if connector is not None:
      return self.doc['connectors'][connector]
    else:
      return self.doc['connectors'].keys()


def flatten(l):
  return [item for sublist in l for item in sublist]

def init_connectors(config):
  conns = flatten([map(lambda t: dropboxconn.DropboxConnector(t),
    config.get_connectors(connector)) for connector in config.get_connectors()])
  map(lambda conn: conn.validate(), conns)
  return conns
