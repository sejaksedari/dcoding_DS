
'''
# impor fungsi dan variabel secara TIDAK SPESIFIK dari modul dcoding_hello
print("impor modul saja tanpa fungsi dan variabel = TIDAK SPESIFIK")
import dcoding_hello

persegi_panjang_pertama = dcoding_hello.mencari_luas_persegi_panjang(5,10)
print(persegi_panjang_pertama)

print(dcoding_hello.nama) #manggil variabel nama dari dcoding_hello.py
# Terlihat pada kode di atas bahwa untuk menampilkan variabel kita tidak menggunakan kurung tutup "()" seperti pada saat pemanggilan fungsi. Namun, kita tetap menggunakan "hello" sebagai modul yang telah kita impor sebelumnya.



# impor fungsi dan variabel secara SPESIFIK dari modul dcoding_hello
print("\nimpor fungsi dan variabel = SPESIFIK")
from dcoding_hello import mencari_luas_persegi_panjang, nama

persegi_panjang_pertama = mencari_luas_persegi_panjang(5,10)
print(persegi_panjang_pertama)

print(nama) #manggil variabel nama dari dcoding_hello.py tapi GA PERLU pake nama modulnya sebelum nama variabel
'''





# # KUIS CODING: OOP //////////////////////////////

# """
# # TODO:
# 1. Buatlah class bernama Animal dengan ketentuan:
#     - Memiliki properti:
#       - name: string
#       - age: int
#       - species: string
#     - Memiliki constructor untuk menginisialisasi properti:
#       - name
#       - age
#       - species
# 2. Buatlah class bernama Cat dengan ketentuan:
#     - Merupakan turunan dari class Animal
#     - Memiliki method:
#       - bernama "deskripsi" yang mengembalikan nilai string berikut ini.
#         "{self.name} adalah kucing berjenis {self.species} yang sudah berumur {self.age} tahun"
#       - bernama "suara" yang akan mengembalikan nilai string "meow!"
#  3. Buatlah instance dari kelas Cat bernama "myCat" dengan ketentuan:
#     - Atribut name bernilai: "Neko"
#     - Atribut age bernilai: 3
#     - Atribut species bernilai: "Persian".
# """

# # 1
# # Animal punya properti name, age, species
# class Animal:
#     def __init__ (self, name, age, species):
#         self.name = name
#         self.age = age
#         self.species = species

# # Call constructor to initiate name, age, species
# gajah_1 = Animal("Gajah", 15, "Loxodonta")
# print(f"Aku {gajah_1.name} berumur {gajah_1.age} dengan nama spesies {gajah_1.species}")

# #2
# # bikin class Cat turunan dari class Animal dan punya method deskripsi & suara
# class Cat(Animal):
#     def deskripsi(self):
#         return f"{self.name} adalah kucing berjenis {self.species} yang sudah berumur {self.age} tahun"

#     def suara(self):
#         return "meow!"

# #3
# # bikin instance dari Cat bernama myCat dengan nama Neko, 3 tahun, Persian
# # make instance of cat
# myCat = Cat('Neko', 3, 'Persian')

# # Access attributes directly, not as methods
# print(myCat.name)
# print(myCat.age)
# print(myCat.species)

# # Print the description and sound
# print(myCat.deskripsi())
# print(myCat.suara())





# # NUMPY ////////////////////////////////////////////
# import numpy as np
# array_1 = np.array([2, 3, 6, 5])
# # print(array_1)
# print(array_1)



# # PANDAS ////////////////////////////////////////////
# import pandas as pd
# data = {
#     'Nama': ['Lulu', 'Lala', 'Lili'],
#     'Age': [23, 45, 53]
# }

# df = pd.DataFrame(data)
# print(df)



# # SCIPY ////////////////////////////////////////////
# import scipy
# print('scipy version: ' + scipy.__version__)



# # MATPLOTLIB ////////////////////////////////////////////
# import matplotlib
# print('matplotlib version: ' + matplotlib.__version__)



# SEABORN ////////////////////////////////////////////
import seaborn
print('seaborn version: ' + seaborn.__version__)