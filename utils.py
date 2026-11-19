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
