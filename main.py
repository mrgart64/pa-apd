'''
Nama : Gabriel Ado Ramos Tukan
NIM : 2609106038

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
import time
from prettytable import PrettyTable
from utils import validasiMenu, validasiAngka, tampilJudul, tampilMenu, batangTeks
import requests
import matplotlib.pyplot as plt

bin_url = "https://satteliteworker.basis64.workers.dev/5t8eihgoto32gn6y"

def loadData():
    """Memuat data dari npoint.io ke app_data."""
    print("Memuat data dari npoint.io...")
    try:
        response = requests.get(bin_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("Data berhasil dimuat.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Gagal memuat data: {e}")
        raise


def saveData(retries=3, delay=1.5):
    """Prosedur untuk menyimpan data ke npoint.io."""
    print("Menyimpan data ke npoint.io...")
    for attempt in range(1, retries + 1):
        try:
            response = requests.put(bin_url, json=app_data, timeout=10)
            if response.status_code >= 500:
                raise requests.exceptions.HTTPError(
                    f"{response.status_code} Server Error: {response.text}",
                    response=response,
                )
            response.raise_for_status()
            print("Data berhasil disimpan.")
            return
        except requests.exceptions.RequestException as e:
            print(f"Percobaan {attempt}/{retries} gagal: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print("Gagal menyimpan data setelah beberapa percobaan.")
                raise


app_data = loadData()

penerima = app_data['tables']['penerima']
pengajuan = app_data['tables']['pengajuan']
blacklist = app_data['tables']['blacklist']


def reloadData():
    """Memuat ulang data terbaru dari server dan menyinkronkan variabel tabel."""
    global app_data, penerima, pengajuan, blacklist
    app_data = loadData()
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
Fungsi tanpa parameter untuk login
'''
def login():
    global is_admin, is_login, penerima, session
    tampilJudul('SISTEM PENCATATAN USAHA PENGGUNAAN LAHAN')
    print('Silakan login untuk melanjutkan\n')
    username = input('Masukkan username Anda (NIP) : ')
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
                    is_admin = False
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
    tampilJudul('TAMBAH PEMOHON / PENGELOLA LAHAN')
    nama = input('Masukkan nama : ')
    nip = input('Masukkan nip : ')
    if not validasiAngka(nip):
        return
    if nip in penerima:
        print(f'{warning_icon} NIP {nip} sudah terdaftar ({penerima[nip]["nama"]}) dan tidak bisa dipakai.')
        return
    alamat = input('Masukkan alamat : ')
    password = input('Masukkan password : ')
    reloadData() # untuk mencegah data tertimpa karena race condition saat 2 program menulis data secara bersamaan 
    penerima[nip] = {'nip': nip, 'nama': nama, 'alamat': alamat, 'password': password}
    saveData()
    print(f'{success_icon} Data pemohon berhasil dibuat')
    
'''
Prosedur adminLihatPenerima() menggunakan PrettyTable
'''
'''
Prosedur adminLihatPenerima() menggunakan PrettyTable
'''
def adminLihatPenerima():
    global penerima, blacklist
    tampilJudul('DAFTAR PEMOHON LAHAN')
    
    table = PrettyTable()
    table.field_names = ["No", "NIP", "Nama", "Alamat", "Status Akun"]
    
    j = 1
    for i in penerima.values():
        nip = i['nip']
        status_akun = "diblokir" if (nip in blacklist and blacklist[nip]) else "sehat"
        table.add_row([j, nip, i['nama'], i['alamat'], status_akun])
        j += 1
        
    print(table)
        
'''
Prosedur adminUbahStatus() menggunakan PrettyTable
'''
def adminUbahStatus():
    global penerima, pengajuan, blacklist
    tampilJudul('UBAH STATUS PENGAJUAN LAHAN')
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
    pilih = input('Pilih nomor pengajuan yang akan diproses : ')
    if not validasiMenu(pilih, len(pengajuan_menu)):
        return
    selected = pengajuan_menu[int(pilih)-1]
    
    clearScreen()
    
    tampilJudul('INFORMASI PENGAJUAN LAHAN')
    print(f'NIP                  : {selected["nip"]}')
    print(f'Nama                 : {selected["nama"]}')
    print(f'Alamat               : {selected["alamat"]}')
    print(f'Status pengajuan     : {selected["status"]}')
    print(f'Mau dipakai apa      : {selected["mau_dipakai_apa"]}')
    print(f'Cara pakai lahan     : {selected["cara_pakai"]}')
    
    print()
    tampilMenu('AKSI', [('Setujui', ''), ('Tolak', ''), ('Blokir', ''), ('Batal', '')])
    
    select_menu = input('Pilih menu : ')
    if not validasiMenu(select_menu, 4):
        return
    select_menu = int(select_menu)
    reloadData() # untuk mencegah data tertimpa karena race condition saat 2 program menulis data secara bersamaan 
    
    if select_menu == 1:
        pengajuan[selected['nip']]['status'] = 'disetujui'
        saveData()
        print('Pengajuan penggunaan lahan berhasil disetujui')
    elif select_menu == 2:
        desc = input('Masukkan alasan penolakan : ')
        pengajuan[selected['nip']]['status'] = 'ditolak'
        pengajuan[selected['nip']]['alasan'] = desc
        saveData()
        print('Pengajuan penggunaan lahan berhasil ditolak')
    elif select_menu == 3:
        desc = input('Masukkan alasan pemblokiran : ')
        pengajuan[selected['nip']]['status'] = 'ditolak'
        pengajuan[selected['nip']]['alasan'] = desc
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
    tampilJudul('UBAH DATA PEMOHON')
    
    table = PrettyTable()
    table.field_names = ["No", "NIP", "Nama", "Alamat"]
    
    j = 1
    for i in penerima.values():
        table.add_row([j, i['nip'], i['nama'], i['alamat']])
        j += 1
        
    print(table)
    pilih = input('Pilih pemohon : ')
    if not validasiMenu(pilih, len(penerima)):
        return None
    index = int(pilih)-1
    nama = input('Masukkan nama : ')
    alamat = input('Masukkan alamat : ')
    
    return (index, nama, alamat)

'''
Prosedur adminUbahPenerima() dengan 1 global variable dan beberapa local variables
'''
def adminUbahPenerima():
    global penerima
    hasil = getNewData()
    if hasil is None:
        return

    index, nama, alamat = hasil
    reloadData()  # untuk mencegah data tertimpa karena race condition saat 2 program menulis data secara bersamaan
    keys = list(penerima.keys())

    if index < 0 or index >= len(keys):
        print(f'{warning_icon} Data pemohon tidak ditemukan setelah memuat ulang data.')
        return

    nip_target = keys[index]
    penerima[nip_target] = {
        'nip': nip_target,
        'nama': nama,
        'alamat': alamat,
        'password': penerima[nip_target]['password']
    }
    saveData()
    print(f'{success_icon} Data pemohon berhasil diubah')

'''
Prosedur adminHapusPenerima() menggunakan PrettyTable
'''
def adminHapusPenerima():
    global penerima, blacklist, pengajuan
    tampilJudul('HAPUS PEMOHON')
    
    table = PrettyTable()
    table.field_names = ["No", "NIP", "Nama", "Alamat"]
    
    j = 1
    for i in penerima.values():
        table.add_row([j, i['nip'], i['nama'], i['alamat']])
        j += 1
        
    print(table)
    pilih = input('Pilih pemohon yang akan dihapus : ')
    if not validasiMenu(pilih, len(penerima)):
        return
    index = int(pilih)-1
    deleted = penerima.pop(list(penerima.keys())[index])
    if blacklist.get(deleted['nip']):
        blacklist.pop(deleted['nip'])
    if pengajuan.get(deleted['nip']):
        pengajuan.pop(deleted['nip'])
    saveData()
    print(f'{deleted["nama"]} ({deleted["nip"]}) berhasil dihapus')

def adminLihatStatistik():
    global pengajuan
    reloadData()  # Ambil data terbaru dari server sebelum membuat chart
    clearScreen()
    tampilJudul('STATISTIK PENGAJUAN PENGGUNAAN LAHAN')

    diterima = 0
    ditolak = 0
    pending = 0
    daftar_pending = []

    for nip, data in pengajuan.items():
        status = str(data.get('status', '')).strip().lower() if isinstance(data, dict) else ''

        if status in ('disetujui', 'diterima'):
            diterima += 1
        elif status == 'ditolak':
            ditolak += 1
        else:
            # Termasuk 'menunggu persetujuan', kosong, atau belum direspon
            pending += 1
            daftar_pending.append((nip, status if status else 'belum direspon'))

    total = diterima + ditolak + pending
    maks = max(diterima, ditolak, pending)

    # Ringkasan dan bar chart di terminal
    print(f'Total pengajuan : {total}\n')
    print(batangTeks('Diterima', diterima, maks))
    print(batangTeks('Ditolak', ditolak, maks))
    print(batangTeks('Pending', pending, maks))

    if daftar_pending:
        table = PrettyTable()
        table.field_names = ["NIP", "Nama", "Status"]
        for nip, st in daftar_pending:
            table.add_row([nip, penerima.get(nip, {}).get('nama', '-'), st])
        print('\nPengajuan yang masih pending:')
        print(table)

    # Bar chart matplotlib
    kategori = ['Diterima', 'Ditolak', 'Pending']
    jumlah = [diterima, ditolak, pending]
    warna = ['green', 'red', 'gold']

    plt.figure(figsize=(7, 5))
    bars = plt.bar(kategori, jumlah, color=warna, edgecolor='black', width=0.55)

    for bar in bars:
        tinggi = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, tinggi + 0.1,
                 str(int(tinggi)), ha='center', va='bottom', fontweight='bold')

    plt.title('Statistik Status Pengajuan Penggunaan Lahan')
    plt.xlabel('Status Pengajuan')
    plt.ylabel('Jumlah Pengajuan')
    plt.ylim(0, maks + 1)
    plt.yticks(range(0, maks + 2))
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()
    
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
    
    tampilJudul('FORM PENGAJUAN PENGGUNAAN LAHAN')
    mau_dipakai_apa = input('Lahan mau dipakai untuk usaha apa? : ')
    cara_pakai = input('Bagaimana cara pakai / metode pengelolaan lahannya? : ')
    reloadData() # untuk mencegah data tertimpa karena race condition saat 2 program menulis data secara bersamaan 
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
    
    tampilJudul('STATUS PENGAJUAN PENGGUNAAN LAHAN')
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
    elif data_pengajuan['status'] == 'ditolak' and not kena_banned:
        print(f'Status akun : SEHAT {success_icon}')
        print(f'{warning_icon} Pengajuan ditolak, masih dapat membuat pengajuan lagi')
        print(f'Alasan: \n{pengajuan[session["nip"]].get("alasan")}')
    else:
        print(f'Status akun : SEHAT {success_icon}')

'''
Prosedur menu admin
'''
def adminMenu():
    global is_login
    tampilMenu('MENU ADMIN', [
        ('Tambah pemohon', 'CREATE'),
        ('Lihat pemohon', 'READ'),
        ('Proses pengajuan', 'UPDATE'),
        ('Ubah data pemohon', 'UPDATE'),
        ('Hapus pemohon', 'DELETE'),
        ('Lihat statistik', 'CHART'),
        ('Keluar', ''),
    ])
    menu = input('Pilih menu : ')
    clearScreen()
    if not validasiMenu(menu, 7):
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
        adminLihatStatistik()
    elif menu == 7:
        is_login = False

'''
Prosedur menu pengguna biasa
'''
def userMenu():
    global is_login
    reloadData()
    print(f'Halo, {session["nama"]}')
    print('Verifikasi pengajuan bisa memakan waktu beberapa minggu sampai bulan.')
    print('Jika akun terblokir, datangi kantor pengelolaan lahan.\n')
    tampilMenu('MENU PEMOHON', [
        ('Buat pengajuan', 'CREATE'),
        ('Lihat status', 'READ'),
        ('Keluar', ''),
    ])
    menu = input('Pilih menu : ')
    clearScreen()
    if not validasiMenu(menu, 3):
        return
    
    menu = int(menu)
    
    if menu == 1:
        userBuatPengajuan()
    elif menu == 2:
        userLihatStatus()
    elif menu == 3:
        is_login = False

'''
Prosedur menu
'''
def mainMenu():
    global is_login
    while is_login:
        clearScreen()
        tampilJudul('SISTEM PENCATATAN USAHA PENGGUNAAN LAHAN')
        print('"Pencatatan tertib, pemanfaatan lahan tepat guna dan berkelanjutan"\n')
        if is_admin:
            adminMenu()
        else:
            userMenu()
        input('\nTekan enter untuk melanjutkan...\n')
      


def main():
    while True:
        while True:
            if login():
                break
            
        mainMenu()
    
main()






