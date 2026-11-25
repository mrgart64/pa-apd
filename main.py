'''
Nama    : Gabriel Ado Ramos Tukan
NIM     : 2609106038

Lihat data.json untuk mendapatkat informasi login yang lebih lengkap atau lihat inforasi login di bawah ini

Login admin: {"username": "admin", "password": "Admin#1234"}

Login penerima:
[
  {"username": "067", "password": "asepasep123"},
  {"username": "068", "password": "testing67"},
  {"username": "069", "password": "barbershop66"},
  {"username": "070", "password": "gatau"},
  {"username": "306", "password": "hydrant"}
]
'''
import os
import json
from prettytable import PrettyTable
from utils import validasiMenu, validasiAngka

# 6 variabel global digunakan
app_data = json.load(open('data.json', 'r', encoding='utf-8'))

penerima = app_data['tables']['penerima']
pengajuan = app_data['tables']['pengajuan']
blacklist = app_data['tables']['blacklist']

session = {}
is_admin = False
is_login = False

success_icon = '[\033[1;32m✓\033[0m]'
warning_icon = '[\033[1;33m!\033[0m]'
failed_icon = '[\033[1;31mX\033[0m]'

# 2 fungsi memakai parameter: validasiMenu(), validasiAngka()
# 2 fungsi tanpa parameter: login(), getNewData()

def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

clearScreen()

'''
Prosedur untuk menyimpan data
'''
def saveData():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(app_data, f, indent=4)

'''
Fungsi tanpa parameter untuk login
'''
def login():
    global is_admin, penerima, session
    print('Selamat datang di aplikasi Sistem Pencatatan Usaha Penggunaan Lahan')
    username = input('Masukkan username Anda : ')
    password = input('Masukkan password Anda : ')
    if username == 'admin':
        if password == 'Admin#1234':
            print(f'{success_icon} Berhasil login sebagai admin')
            is_admin = True
            is_login = True
            return True
        else:
            print('[X] Password admin salah.')
            return False
    else:
        for i in penerima.values():
            if username == i['nip']:
                if password == i['password']:
                    print(f'{success_icon} Berhasil login sebagai {i["nama"]}')
                    session = i
                    is_login = True
                    return True
                else:
                    print(f'{failed_icon} Password pengguna salah.')
                    return False
        
        print(f'{failed_icon} Pengguna tidak ditemukan.')
        return False

'''
Prosedur adminTambahPenerima() dengan 1 global variable dan 4 local variables
'''
def adminTambahPenerima():
    global penerima
    print('=== Tambah Pemohon / Pengelola Lahan ===')
    nama = input('Masukkan nama : ')
    nip = input('Masukkan nip : ')
    if not validasiAngka(nip):
        return
    alamat = input('Masukkan alamat : ')
    password = input('Masukkan password : ')
    penerima[nip] = {'nip': nip, 'nama': nama, 'alamat': alamat, 'password': password}
    saveData()
    print('Data pemohon berhasil dibuat')
    
'''
Prosedur adminLihatPenerima() menggunakan PrettyTable
'''
def adminLihatPenerima():
    global penerima
    print('=== Lihat Semua Pemohon Lahan ===')
    
    table = PrettyTable()
    table.field_names = ["No", "NIP", "Nama", "Alamat"]
    
    j = 1
    for i in penerima.values():
        table.add_row([j, i['nip'], i['nama'], i['alamat']])
        j += 1
        
    print(table)
        
'''
Prosedur adminUbahStatus() menggunakan PrettyTable
'''
def adminUbahStatus():
    global penerima, pengajuan, blacklist
    print('=== Ubah Status Pengajuan Penggunaan Lahan ===')
    print('Pilih pengajuan yang akan diubah statusnya')
    
    table = PrettyTable()
    table.field_names = ["No", "NIP", "Nama", "Alamat", "Status", "Mau Dipakai Apa", "Cara Pakai"]
    
    pengajuan_menu = []
    for i in penerima.values():
        data_pengajuan = pengajuan.get(i['nip'])
        if data_pengajuan and data_pengajuan.get('status') == 'menunggu persetujuan':
            mau_dipakai_apa = data_pengajuan.get('mau_dipakai_apa', data_pengajuan.get('desc', '-'))
            cara_pakai = data_pengajuan.get('cara_pakai', '-')
            pengajuan_menu.append({
                'nip': i['nip'], 
                'nama': i['nama'], 
                'alamat': i['alamat'], 
                'status': data_pengajuan['status'], 
                'mau_dipakai_apa': mau_dipakai_apa,
                'cara_pakai': cara_pakai
            })
            table.add_row([
                len(pengajuan_menu), 
                i['nip'], 
                i['nama'], 
                i['alamat'], 
                data_pengajuan['status'], 
                mau_dipakai_apa,
                cara_pakai
            ])
                
    if not pengajuan_menu:
        print("Tidak ada pengajuan yang menunggu persetujuan.")
        return

    print(table)
    selected = pengajuan_menu[int(input('Pilih nomor pengajuan yang akan diproses : '))-1]
    
    clearScreen()
    
    print('=== Informasi Pengajuan Lahan ===')
    print(f'NIP                  : {selected["nip"]}')
    print(f'Nama                 : {selected["nama"]}')
    print(f'Alamat               : {selected["alamat"]}')
    print(f'Status pengajuan     : {selected["status"]}')
    print(f'Mau dipakai apa      : {selected["mau_dipakai_apa"]}')
    print(f'Cara pakai lahan     : {selected["cara_pakai"]}')
    
    print('\n=== Menu ===')
    print('[1] Setujui')
    print('[2] Tolak')
    print('[3] Blokir')
    print('[4] Keluar')
    
    select_menu = int(input('Pilih menu : '))
    
    if select_menu == 1:
        pengajuan[selected['nip']]['status'] = 'disetujui'
        saveData()
        print('Pengajuan penggunaan lahan berhasil disetujui')
    elif select_menu == 2:
        pengajuan[selected['nip']]['status'] = 'ditolak'
        saveData()
        print('Pengajuan penggunaan lahan berhasil ditolak')
    elif select_menu == 3:
        desc = input('Masukkan alasan pemblokiran : ')
        pengajuan[selected['nip']]['status'] = 'ditolak'
        blacklist[selected['nip']] = {'desc': desc}
        saveData()
        print('Pemohon berhasil diblokir')
    else:
        print('Dibatalkan')

'''
Fungsi tanpa parameter getNewData() menggunakan PrettyTable
'''
def getNewData():
    global penerima
    print('=== Ubah Data Pemohon ===')
    
    table = PrettyTable()
    table.field_names = ["No", "NIP", "Nama", "Alamat"]
    
    j = 1
    for i in penerima.values():
        table.add_row([j, i['nip'], i['nama'], i['alamat']])
        j += 1
        
    print(table)
    index = int(input('Pilih pemohon : '))-1
    nama = input('Masukkan nama : ')
    alamat = input('Masukkan alamat : ')
    
    return (index, nama, alamat)

'''
Prosedur adminUbahPenerima() dengan 1 global variable dan beberapa local variables
'''
def adminUbahPenerima():
    global penerima
    (index, nama, alamat) = getNewData()
    keys = list(penerima.keys())
    penerima[keys[index]] = {'nip': keys[index], 'nama': nama, 'alamat': alamat, 'password': penerima[keys[index]]['password']}
    saveData()
    print('Data pemohon berhasil diubah')

'''
Prosedur adminHapusPenerima() menggunakan PrettyTable
'''
def adminHapusPenerima():
    global penerima, blacklist, pengajuan
    print('=== Hapus Pemohon ===')
    
    table = PrettyTable()
    table.field_names = ["No", "NIP", "Nama", "Alamat"]
    
    j = 1
    for i in penerima.values():
        table.add_row([j, i['nip'], i['nama'], i['alamat']])
        j += 1
        
    print(table)
    index = int(input('Pilih pemohon yang akan dihapus : '))-1
    deleted = penerima.pop(list(penerima.keys())[index])
    if blacklist.get(deleted['nip']):
        blacklist.pop(deleted['nip'])
    if pengajuan.get(deleted['nip']):
        pengajuan.pop(deleted['nip'])
    saveData()
    print(f'{deleted["nama"]} ({deleted["nip"]}) berhasil dihapus')
    
'''
Prosedur userBuatPengajuan() dengan 2 global variables dan beberapa local variables
'''
def userBuatPengajuan():
    global blacklist, pengajuan
    if blacklist.get(session['nip']):
        print('Akun Anda terblokir atau kena banned, silakan datangi kantor pengelolaan lahan secara offline untuk verifikasi dan klarifikasi lebih lanjut.')
        return
    
    if pengajuan.get(session['nip']):
        if pengajuan.get(session['nip'])['status'] == 'menunggu persetujuan':
            print('Anda telah mengirim pengajuan penggunaan lahan dan petugas akan memverifikasi lebih lanjut\ndalam waktu beberapa minggu sampai beberapa bulan sesuai regulasi dan birokrasi\nwilayah Kalimantan Timur.')
            return
    
    print('=== Form Pengajuan Penggunaan Lahan ===')
    mau_dipakai_apa = input('Lahan mau dipakai untuk usaha apa? : ')
    cara_pakai = input('Bagaimana cara pakai / metode pengelolaan lahannya? : ')
    pengajuan[session['nip']] = {
        'mau_dipakai_apa': mau_dipakai_apa,
        'cara_pakai': cara_pakai,
        'status': 'menunggu persetujuan'
    }
    saveData()
    print('Pengajuan penggunaan lahan berhasil dibuat.')
    
    
'''
Prosedur userLihatStatus() dengan 2 global variables dan beberapa local variable
'''
def userLihatStatus():
    global pengajuan, blacklist
    data_pengajuan = pengajuan.get(session['nip'])
    if not data_pengajuan:
        print('Anda belum membuat pengajuan penggunaan lahan.')
        return
    
    kena_banned = blacklist.get(session['nip'])
    mau_dipakai_apa = data_pengajuan.get('mau_dipakai_apa', data_pengajuan.get('desc', '-'))
    cara_pakai = data_pengajuan.get('cara_pakai', '-')
    
    print('=== STATUS PENGAJUAN PENGGUNAAN LAHAN ===')
    print('Proses verifikasi mungkin memakan waktu beberapa minggu sampai\nbeberapa bulan bergantung pada regulasi dan birokrasi wilayah Kalimantan Timur.')
    print('[!] Cek secara berkala status pengajuan di aplikasi ini.\n')
    print(f'Status pengajuan : {data_pengajuan["status"]}')
    print(f'Mau dipakai apa  : {mau_dipakai_apa}')
    print(f'Cara pakai lahan  : {cara_pakai}\n')
    
    if data_pengajuan['status'] == 'disetujui':
        print('Selamat, pengajuan usaha penggunaan lahan Anda telah disetujui dan terverifikasi.\n')
        
    if data_pengajuan['status'] == 'ditolak' and kena_banned:
        print('Akun Anda terkena banned, Anda tidak dapat membuat\nulang pengajuan penggunaan lahan.\nSilakan datangi kantor pengelolaan lahan untuk verifikasi data dan klarifikasi\nlalu Anda membuat kembali pengajuan melalui aplikasi ini dan melewati prosedur birokrasi sesuai protokol')
    
    if data_pengajuan['status'] == 'ditolak' and not kena_banned:
        print('Pengajuan ditolak, Anda dapat membuat ulang pengajuan dan\nkembali melewati prosedur birokrasi sesuai protokol')
    
    if kena_banned:
        print(f'Status akun : TIDAK SEHAT / KENA BANNED {failed_icon}')
        print(f'{warning_icon} Akun Anda terkena banned')
        print(f'Alasan pemblokiran: \n{blacklist[session["nip"]]["desc"]}')
    else:
        print(f'Status akun : SEHAT {success_icon}')

'''
Prosedur menu admin
'''
def adminMenu():
    print('=== Admin Menu ===')
    print('[1] Tambah pemohon       | CREATE')
    print('[2] Lihat pemohon        | READ')
    print('[3] Setujui pengajuan    | UPDATE')
    print('[4] Ubah data pemohon    | UPDATE')
    print('[5] Hapus pemohon        | DELETE')
    print('[6] Keluar')
    menu = input('Pilih menu : ')
    clearScreen()
    if not validasiMenu(menu, 6):
        return
    
    menu = int(menu)
    
    if menu == 1:
        adminTambahPenerima()
    elif menu == 2:
        adminLihatPenerima()
    elif menu == 3:
        adminUbahStatus()
    elif menu == 4:
        adminUbahPenerima()
    elif menu == 5:
        adminHapusPenerima()
    elif menu == 6:
        exit()

'''
Prosedur menu pengguna biasa
'''
def userMenu():
    print('=== User Menu ===')
    print('PERHATIAN: Proses verifikasi mungkin memakan waktu beberapa minggu sampai\nbeberapa bulan bergantung pada regulasi dan birokrasi wilayah Kalimantan Timur.\nDatangi kantor pengelolaan lahan secara offline untuk verifikasi dan klarifikasi lebih lanjut jika akun Anda terblokir.')
    print('[1] Buat pengajuan   | CREATE')
    print('[2] Lihat status     | READ')
    print('[3] Keluar')
    menu = input('Pilih menu : Pilihlah menu di atas: ')
    clearScreen()
    if not validasiMenu(menu, 3):
        return
    
    menu = int(menu)
    
    if menu == 1:
        userBuatPengajuan()
    elif menu == 2:
        userLihatStatus()
    elif menu == 3:
        exit()

'''
Prosedur menu
'''
def mainMenu():
    while (1):
        clearScreen()
        print('Sistem Pencatatan Usaha Penggunaan Lahan')
        print('"Pencatatan tertib, pemanfaatan lahan tepat guna dan berkelanjutan"')
        if is_admin:
            adminMenu()
        else:
            userMenu()
        input('\nTekan enter untuk melanjutkan...\n')


def main():
    while True:
        if login():
            break
        
    mainMenu()
    
main()