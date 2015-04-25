from map import Map
import pprint

if __name__ == "__main__":
    m = Map(2, 4, 3)
    pp = pprint.PrettyPrinter()
    pp.pprint(m.convert_to_json())
    m.draw_graph()
