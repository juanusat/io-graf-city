import argparse
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Genera un grafo y resuelve el MST.")
    parser.add_argument('-r', type=int, required=True, help="Número de filas")
    parser.add_argument('-c', type=int, required=True, help="Número de columnas")
    parser.add_argument('-f', type=float, required=True, help="Peso mínimo")
    parser.add_argument('-t', type=float, required=True, help="Peso máximo")
    parser.add_argument('-n', '--name', required=True, help="Nombre del test")
    args = parser.parse_args()

    generate_command = f"python random-city.py -r {args.r} -c {args.c} -f {args.f} -t {args.t} -n {args.name}"
    subprocess.run(generate_command, shell=True)

    kruskal_command = f"python mst_algorithms_no_lib.py -f city-test-{args.name}.txt -a kruskal -i city-test-{args.name}_mst_kruskal.png -r {args.r} -c {args.c}"
    subprocess.run(kruskal_command, shell=True)

    prim_command = f"python mst_algorithms_no_lib.py -f city-test-{args.name}.txt -a prim -i city-test-{args.name}_mst_prim.png -r {args.r} -c {args.c}"
    subprocess.run(prim_command, shell=True)

    delete_files = input("¿Desea borrar los archivos generados? (s/n): ")
    if delete_files.lower() == 's':
        os.remove(f"city-test-{args.name}.txt")
        os.remove(f"city-test-{args.name}.png")
        os.remove(f"city-test-{args.name}-mst_kruskal.png")
        os.remove(f"city-test-{args.name}-mst_prim.png")
        print("Archivos borrados.")

if __name__ == "__main__":
    main()