from mapgen.map import Map
import load_json

# TODO specify json name?
# TODO Fixed map gen options
if __name__ == "__main__":
    # Generate Map
    m = Map(7, 5, 6)

    # Convert to JSON
    load_json.save_map_to_file("gamerunner/map.json", m.convert_to_json())
    # Print graph using networkx
    # m.draw_graph()
