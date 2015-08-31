from mapgen.map import Map
import argparse
import load_json

parser = argparse.ArgumentParser(
    description="Launches the visualizer")
parser.add_argument(
    "-c", "--num_continents",
    help="Number of continents to use",
    default="3")
parser.add_argument(
    "-ipc", "--isp_per_continents",
    help="Number of isps per continents",
    default="5")
parser.add_argument(
    "-cpi", "--cities_per_isp",
    help="Number of cities per isp",
    default="6")
args = parser.parse_args()  # parse args

if __name__ == "__main__":
    # Generate Map
    # m = Map(7, 5, 6)  # Original settings
    m = Map(3, 5, 2)  # Ace's test settings
    # m = Map(int(args.num_continents), int(args.isp_per_continents), int(args.cities_per_isp))

    # Convert to JSON
    load_json.save_map_to_file("gamerunner/map.json", m.convert_to_json())
    # Print graph using networkx
    # m.draw_graph()
