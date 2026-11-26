'''
Fungsi digunakan agar logika validasi menu tidak perlu diketik ulang dan lebih efisien
'''
def validasiMenu (menu, max):
    '''
    Penanganan input kosong
    '''
    if len(menu) == 0:
        print ('[\033[1;31mX\033[0m] Input harus diisi.\n')
        return False

    '''
    Poin plus: Penanganan input bukan angka dengan error handling (try/except)
    '''
    try:
        menu = int (menu) # ubah ke angka
    except:
        print ('[\033[1;31mX\033[0m] Input harus angka.\n')
        return False



    '''
    Penanganan input tidak valid
    '''
    if menu < 1 or menu > max:
        print ('[\033[1;31mX\033[0m] Input tidak valid.\n')
        return False

    return True

'''
Fungsi digunakan agar logika validasi angka tidak perlu diketik ulang dan lebih efisien
'''
def validasiAngka (num):
    '''
    Penanganan input kosong
    '''
    if len(num) == 0:
        print ('[\033[1;31mX\033[0m] Input harus diisi.\n')
        return False

    '''
    Poin plus: Penanganan input bukan angka dengan error handling (try/except)
    '''
    try:
        num = int (num) # ubah ke angka
    except:
        print ('[\033[1;31mX\033[0m] Input harus angka.\n')
        return False

    return True

'''
Fungsi untuk menampilkan judul dalam kotak agar tampilan lebih rapi
'''
def tampilJudul (teks, lebar = 60):
    print ('+' + '-' * (lebar - 2) + '+')
    print ('|' + teks.center (lebar - 2) + '|')
    print ('+' + '-' * (lebar - 2) + '+')

'''
Fungsi untuk menampilkan daftar menu bernomor
daftar berisi pasangan (nama menu, keterangan)
'''
def tampilMenu (judul, daftar, lebar = 60):
    tampilJudul (judul, lebar)
    for no, (nama, ket) in enumerate (daftar, 1):
        print (f'  [{no}] {nama:<28}{ket}')
    print ('-' * lebar)

'''
Fungsi untuk membuat diagram batang sederhana di terminal
'''
def batangTeks (label, jumlah, maks, panjang = 30):
    isi = int (jumlah / maks * panjang) if maks > 0 else 0
    return f'  {label:<10} {"█" * isi:<{panjang}} {jumlah}'
