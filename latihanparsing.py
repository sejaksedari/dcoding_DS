import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', action='store_true', help="tampilkan output")
parser.add_argument('-n', '--nama', required=True, help="Masukkan Nama Anda")
parser.add_argument('-t', '--tanggallahir', required=True, help="Masukkan Tanggal Lahir Anda (DD-MM-YYYY)")
args = parser.parse_args()

if args.output:
    print("Halo, ini merupakan sebuah output dari panggildicoding.py")

print("Terima kasih telah menggunakan panggildicoding.py, "+ args.nama + " " + args.tanggallahir)