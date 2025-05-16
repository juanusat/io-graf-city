import osmnx as ox
import argparse

def convert_graphml_to_txt(graphml_file, txt_file):
    G = ox.load_graphml(graphml_file)
    with open(txt_file, 'w') as f:
        for u, v, data in G.edges(data=True):
            weight = data.get('length', 1.0)  # usa 1.0 si no hay longitud
            f.write(f"{u} {v} {weight:.2f}\n")
    print(f"Archivo generado: {txt_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help="Archivo .graphml de entrada")
    parser.add_argument('-o', '--output', required=True, help="Archivo .txt de salida (lista de aristas)")
    args = parser.parse_args()
    convert_graphml_to_txt(args.input, args.output)
