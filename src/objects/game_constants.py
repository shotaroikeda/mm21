#NodeType enum (NodeType.Small = 1)
class NodeType:

    processing0 = {'Map': 0,
                  'Small': 100,
                  'Medium': 200,
                  'Large': 500,
                  'ISP': 2000,
                  'Datacenter': 0
                  }

    networking0 = {'Map': 0,
                  'Small': 100,
                  'Medium': 200,
                  'Large': 500,
                  'ISP': 0,
                  'Datacenter': 2000
                  }

    processing = [processing0]
    networking = [networking0]