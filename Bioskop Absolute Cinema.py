import flet as ft
from datetime import datetime
import random
import os

class Film:
    def __init__(self, judul, sutradara, genre, durasi, tahun_rilis, deskripsi, rating, jadwal_penayangan, poster):
        self.__judul = judul
        self.__sutradara = sutradara
        self.__genre = genre
        self.__durasi = durasi
        self.__tahun_rilis = tahun_rilis
        self.__deskripsi = deskripsi
        self.__rating = rating
        self.__jadwal_penayangan = jadwal_penayangan
        self.__poster = poster

    def get_judul(self):
        return self.__judul
    def get_sutradara(self):
        return self.__sutradara
    def get_genre(self):
        return self.__genre
    def get_durasi(self):
        return self.__durasi
    def get_tahun_rilis(self):
        return self.__tahun_rilis
    def get_deskripsi(self):
        return self.__deskripsi
    def get_rating(self):
        return self.__rating
    def get_jadwal_penayangan(self):
        return self.__jadwal_penayangan
    def get_poster(self):
        return self.__poster

    def set_judul(self, judul):
        self.__judul = judul
    def set_sutradara(self, sutradara):
        self.__sutradara = sutradara
    def set_genre(self, genre):
        self.__genre = genre
    def set_durasi(self, durasi):
        self.__durasi = durasi
    def set_tahun_rilis(self, tahun_rilis):
        self.__tahun_rilis = tahun_rilis
    def set_deskripsi(self, deskripsi):
        self.__deskripsi = deskripsi
    def set_rating(self, rating):
        self.__rating = rating
    def set_jadwal_penayangan(self, jadwal_penayangan):
        self.__jadwal_penayangan = jadwal_penayangan
    def set_poster(self, poster):
        self.__poster = poster

    def get_jadwal_list(self):
        """Mengubah string jadwal menjadi list waktu"""
        return [waktu.strip() for waktu in self.__jadwal_penayangan.split(',')]

class ListFilm:
    def __init__(self):
        self.films = []
        self.muat_film_dari_file()
        
        if len(self.films) == 0 or all(f.get_judul() == "" for f in self.films):
            self.tambah_film_default()
            self.simpan_ke_file()
    
    def muat_film_dari_file(self, nama_file="daftar1.txt"):
        try:
            with open(nama_file, 'r', encoding='utf-8') as file:
                for baris in file:
                    data = baris.strip().split('|')
                    if len(data) >= 9:
                        film = Film(
                            judul=data[0],
                            sutradara=data[1],
                            genre=data[2],
                            durasi=int(data[3]),
                            tahun_rilis=int(data[4]),
                            deskripsi=data[5],
                            rating=data[6],
                            jadwal_penayangan=data[7],
                            poster=data[8]
                        )
                        self.films.append(film)
        except FileNotFoundError:
            print("File daftar1.txt tidak ditemukan, akan dibuat saat menyimpan.")
        except Exception as e:
            print(f"Error membaca file: {e}")
    
    def tambah_film_default(self):
        default_films = [
            Film("The Shawshank Redemption", "Frank Darabont", "Drama", 142, 1994, 
                 "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", 
                 "9.3/10", "10:00, 14:00, 18:00", "shaw.jpg"),
            Film("The Godfather", "Francis Ford Coppola", "Crime", 175, 1972, 
                 "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", 
                 "9.2/10", "11:00, 15:00, 19:00", "shaw.jpg"),
            Film("Pulp Fiction", "Quentin Tarantino", "Crime", 154, 1994, 
                 "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", 
                 "8.9/10", "12:00, 16:00, 20:00", "shaw.jpg")
        ]
        self.films.extend(default_films)
    
    def simpan_ke_file(self, nama_file="daftar1.txt"):
        try:
            with open(nama_file, 'w', encoding='utf-8') as file:
                for film in self.films:
                    line = "|".join([
                        film.get_judul(),
                        film.get_sutradara(),
                        film.get_genre(),
                        str(film.get_durasi()),
                        str(film.get_tahun_rilis()),
                        film.get_deskripsi(),
                        film.get_rating(),
                        film.get_jadwal_penayangan(),
                        film.get_poster()
                    ])
                    file.write(line + "\n")
        except Exception as e:
            print(f"Error menyimpan file: {e}")

class TheaterKursi:
    EMPTY = 0
    TAKEN = 1
    SELECTED = 2
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Ubah struktur data untuk menyimpan kursi per jadwal
        self.seats_by_schedule = {}  # Format: {jadwal: [[kursi_status]]}
    
    def get_or_create_schedule(self, jadwal):
        """Mendapatkan atau membuat grid kursi untuk jadwal tertentu"""
        if jadwal not in self.seats_by_schedule:
            self.seats_by_schedule[jadwal] = [[self.EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        return self.seats_by_schedule[jadwal]
    
    def pesan_kursi(self, baris, kolom, jadwal):
        r, c = baris - 1, kolom - 1
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        
        seats = self.get_or_create_schedule(jadwal)
        if seats[r][c] == self.TAKEN:
            return False
        seats[r][c] = self.TAKEN
        return True
    
    def batal_pesan(self, baris, kolom, jadwal):
        r, c = baris - 1, kolom - 1
        seats = self.get_or_create_schedule(jadwal)
        if seats[r][c] == self.EMPTY:
            return False
        seats[r][c] = self.EMPTY
        return True
    
    def toggle_pilih(self, baris, kolom, jadwal):
        r, c = baris - 1, kolom - 1
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        
        seats = self.get_or_create_schedule(jadwal)
        if seats[r][c] == self.TAKEN:
            return False
        seats[r][c] = self.SELECTED if seats[r][c] == self.EMPTY else self.EMPTY
        return True
    
    def get_selected_seats(self, jadwal):
        selected = []
        seats = self.get_or_create_schedule(jadwal)
        for r in range(self.rows):
            for c in range(self.cols):
                if seats[r][c] == self.SELECTED:
                    selected.append((r+1, c+1))
        return selected
    
    def confirm_selection(self, jadwal):
        seats = self.get_or_create_schedule(jadwal)
        for r in range(self.rows):
            for c in range(self.cols):
                if seats[r][c] == self.SELECTED:
                    seats[r][c] = self.TAKEN
    
    def get_seat_status(self, baris, kolom, jadwal):
        """Mendapatkan status kursi untuk jadwal tertentu"""
        r, c = baris - 1, kolom - 1
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return None
        
        seats = self.get_or_create_schedule(jadwal)
        return seats[r][c]


class Studio:
    def __init__(self, jumlah_kursi, fasilitas):
        self.jumlah_kursi = jumlah_kursi
        self.fasilitas = fasilitas
        self.kursi = TheaterKursi(10, 15)
        self.film = None

    def get_tipe(self):
        return "Biasa"

    def get_fasilitas(self):
        return list(self.fasilitas)

class Premiere(Studio):
    def __init__(self, jumlah_kursi):
        super().__init__(jumlah_kursi, {"kursi premium", "selimut", "snack eksklusif", "recliner"})

    def get_tipe(self):
        return "Premiere"

    def get_fasilitas(self):
        return list(self.fasilitas) + ["layanan ekstra"]

class Konsumsi:
    def __init__(self):
        self.makanan = {
            "1": ("Popcorn Caramel", {"Diet": 15000, "Medium": 30000, "Jumbo": 50000 },"https://drive.google.com/uc?export=view&id=1UnKrYNUlwTyhdbcb2WY9302tG67PhxbA"),
            "2": ("Popcorn Butter", {"Diet": 14000, "Medium": 28000, "Jumbo": 48000},"https://drive.google.com/uc?export=view&id=1DvpRh1dQwsiUfB8YNSIYM7VPAnCt5p_a"),
            "3": ("Popcorn Cheese", {"Diet": 16000, "Medium": 32000, "Jumbo": 52000},"https://drive.google.com/uc?export=view&id=1pMaL3X5mlks3BixlywF06LPBHedWj-Mc"),
            "4": ("Popcorn Spicy", {"Diet": 16000, "Medium": 32000, "Jumbo": 52000},"https://drive.google.com/uc?export=view&id=1ZYqbjewJO6DwS7NEBL8H2GLo7AIzPPfQ"),
            "5": ("Kentang Goreng Spicy", {"Diet": 17000, "Medium": 31000, "Jumbo": 45000},"https://drive.google.com/uc?export=view&id=15royya-7Uz3lDwkwq1vjgCDa0ZnFQOr1"),
            "6": ("Kentang Goreng Umami", {"Diet": 17000, "Medium": 31000, "Jumbo": 45000},"https://drive.google.com/uc?export=view&id=1lJNEpmdXKBFFYEHZJxtl_kbJH3lgh2V8"),
            "7": ("Blood Dragon Hotdog", {"Diet": 20000, "Medium": 35000, "Jumbo": 50000},"https://drive.google.com/uc?export=view&id=1I0Fda2qnl4FzRFZRscoCbB7pPsFqERQB"), #tambah url==========================================
        }
        self.minuman = {
            "1": ("Lemon Soda", {"Diet": 12000, "Medium": 20000, "Jumbo": 30000},"https://drive.google.com/uc?export=view&id=1yTc5T0xFirdMM7Hq9AbgUtcxEia42hiy"),
            "2": ("Blood Demon Soda", {"Diet": 15000, "Medium": 23000, "Jumbo": 33000},"https://drive.google.com/uc?export=view&id=17Gs1pASBwvMaAC6hLaLLN3KqtWerTrQz"),
            "3": ("Ice Tea", {"Diet": 10000, "Medium": 18000, "Jumbo": 25000},"https://drive.google.com/uc?export=view&id=1YDr4vV0ffnlRgJ19Ebf4Q3KR7B9UFCcb"),
            "4": ("Heavenly Ice Cream", {"Diet": 18000, "Medium": 25000, "Jumbo": 35000},"https://drive.google.com/uc?export=download&id=1q38-zi7IuWUioFp5NXh610-9R_y4Z6Xj"),
        }

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Konsumen:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.transaksi_history = []

class Transaksi:
    def __init__(self, username, film, tanggal_pemesanan, no_kursi, studio, tipe_tiket, konsumsi=None, voucher=None, waktu_tayang = None):
        self.id_transaksi = f"TRX{random.randint(1000, 9999)}"
        self.username = username
        self.film = film
        self.tanggal_pemesanan = tanggal_pemesanan
        self.no_kursi = no_kursi
        self.studio = studio
        self.tipe_tiket = tipe_tiket
        self.konsumsi = konsumsi if konsumsi else []
        self.voucher = voucher
        self.waktu_tayang = waktu_tayang
        self.harga_tiket = 100000 if tipe_tiket.lower() == "premiere" else 50000
        self.diskon = 0.2 if voucher and voucher.lower() == "diskon20" else 0
        self.status = "Pending"
    
    def hitung_total(self):
        total = self.harga_tiket * len(self.no_kursi)  # Total harga berdasarkan jumlah kursi
        
        # Weekend surcharge
        if self.tanggal_pemesanan.strftime("%A").lower() in ["saturday", "sunday"]:
            total += 20000 * len(self.no_kursi)
        
        # Add consumables
        for item in self.konsumsi:
            total += item["harga"]
        
        # Apply discount
        total -= total * self.diskon
        
        return total
    
    def confirm_payment(self):
        self.status = "Paid"
        return True
    
    def get_fasilitas(self, studios_dict):
        studio_obj = studios_dict.get(self.studio)
        if studio_obj:
            return studio_obj.get_fasilitas()
        return ["(fasilitas tidak diketahui)"]

class CinemaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Absolute Cinema"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window_width = 1000
        self.page.window_height = 700
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.selected_consumables = []
        
        # Initialize data
        self.konsumen_db = [
            Konsumen("budi", "123"),
            Konsumen("alya", "password1")
        ]
        self.admin_db = [
        Admin("admin", "admin123")
        ]
        self.available_genres = [
            "Action", "Adventure", "Animation", "Comedy", "Crime",
            "Documentary", "Drama", "Fantasy", "Horror", "Mystery",
            "Romance", "Sci-Fi", "Thriller", "Western", "Biography",
            "Family", "History", "Musical", "Sport", "War"
        ]
        self.current_user = None
        self.is_admin = False 
        self.list_film = ListFilm()
        self.studios = {
            "Studio 1": Studio(150, {"kursi standar"}),
            "Studio 2": Studio(150, {"kursi standar"}),
            "Studio Premiere": Premiere(100)
        }
        self.konsumsi = Konsumsi()
        self.current_transaction = None
        self.selected_seats = []
        self.selected_consumables = []
        
        # UI Components
        self.create_login_ui()

    def open_date_picker(self):
        self.date_picker.open = True
        self.page.update()

    def update_date_display(self, e):
        if self.date_picker.value:
            self.selected_date.value = self.date_picker.value.strftime("%d/%m/%Y")
            self.page.update()

    def pick_date(self, e):
        if self.date_picker.value:
            self.selected_date.value = self.date_picker.value.strftime("%d/%m/%Y")
            self.page.update()
    
    def create_login_ui(self):
        self.user_type = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="consumer", label="Konsumen"),
                ft.Radio(value="admin", label="Admin")
            ]),
            value="consumer"
        )
        
        self.username_field = ft.TextField(label="Username", width=300, autofocus=True)
        self.password_field = ft.TextField(label="Password", width=300, password=True, can_reveal_password=True)
        
        login_button = ft.ElevatedButton(
            "Login",
            on_click=self.handle_login,
            width=300
        )
        
        register_button = ft.TextButton(
            "Belum punya akun? Daftar disini",
            on_click=self.show_register_dialog
        )
        
        self.login_form = ft.Column(
        [
            ft.Text("Welcome to Absolute Cinema", size=24, weight="bold"),
            ft.Text("Silakan login untuk melanjutkan"),
            self.user_type,  # Tambahkan radio group untuk memilih tipe user
            self.username_field,
            self.password_field,
            login_button,
            register_button
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        # Register dialog
        self.register_username = ft.TextField(label="Username")
        self.register_password = ft.TextField(label="Password", password=True)
        self.register_dialog = ft.AlertDialog(
            title=ft.Text("Daftar Akun Baru"),
            content=ft.Column([
                self.register_username,
                self.register_password
            ], tight=True),
            actions=[
                ft.TextButton("Daftar", on_click=self.handle_register),
                ft.TextButton("Batal", on_click=self.close_register_dialog)
            ]
        )
        
        self.page.clean()
        self.page.add(self.login_form)
    
    def show_register_dialog(self, e):
        self.page.dialog = self.register_dialog
        self.register_dialog.open = True
        self.page.update()
    
    def close_register_dialog(self, e):
        self.register_dialog.open = False
        self.page.update()
    
    def handle_register(self, e):
        username = self.register_username.value
        password = self.register_password.value
        
        if not username or not password:
            self.page.snack_bar = ft.SnackBar(ft.Text("Username dan password harus diisi"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        if any(user.username == username for user in self.konsumen_db):
            self.page.snack_bar = ft.SnackBar(ft.Text("Username sudah digunakan"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        self.konsumen_db.append(Konsumen(username, password))
        self.close_register_dialog(e)
        self.page.snack_bar = ft.SnackBar(ft.Text("Pendaftaran berhasil! Silakan login"))
        self.page.snack_bar.open = True
        self.page.update()
    
    def handle_login(self, e):
        username = self.username_field.value
        password = self.password_field.value
        user_type = self.user_type.value
        
        if user_type == "consumer":
            # Login sebagai konsumen
            user = next((u for u in self.konsumen_db if u.username == username and u.password == password), None)
            if user:
                self.current_user = user
                self.is_admin = False
                self.create_main_ui()
            else:
                self.show_snackbar("Username atau password salah")
        else:
            # Login sebagai admin
            admin = next((a for a in self.admin_db if a.username == username and a.password == password), None)
            if admin:
                self.current_user = admin
                self.is_admin = True
                self.create_admin_ui()  # Buat UI khusus admin
            else:
                self.show_snackbar("Username atau password admin salah")
        
        self.page.update()
    
    def logout(self, e):
        self.current_user = None
        self.is_admin = False
        self.create_login_ui()

    def update_schedule_options(self, e):
        """Update pilihan jadwal berdasarkan film yang dipilih"""
        self.schedule_dropdown.options.clear()
        self.schedule_dropdown.disabled = True
        self.schedule_dropdown.value = None
        self.studio_display.value = "Studio akan ditentukan otomatis setelah memilih waktu tayang"
        
        if self.film_dropdown.value:
            # Cari film yang dipilih
            selected_film = next((f for f in self.list_film.films if f.get_judul() == self.film_dropdown.value), None)
            if selected_film:
                # Ambil jadwal waktu dari film
                jadwal_list = selected_film.get_jadwal_list()
                
                # Buat options untuk dropdown jadwal
                self.schedule_dropdown.options = [
                    ft.dropdown.Option(waktu) for waktu in jadwal_list
                ]
                self.schedule_dropdown.disabled = False
        
        # Reset seat grid
        self.seat_grid.controls.clear()
        self.page.update()
    
    def update_studio_assignment(self, e):
        """Otomatis assign studio berdasarkan waktu yang dipilih"""
        if not self.schedule_dropdown.value:
            return
        
        # Logika penentuan studio berdasarkan waktu
        waktu = self.schedule_dropdown.value
        
        waktu_int = int(waktu.split(':')[0])  # Ambil jam saja
        
        # Cek jika tipe tiket Premiere, maka selalu gunakan Studio Premiere
        if self.ticket_type.value == "Premiere":
            assigned_studio = "Studio Premiere"
        else:
            # Tetapkan studio berdasarkan waktu
            if waktu_int <= 12:
                assigned_studio = "Studio 1"
            elif waktu_int <= 17:
                assigned_studio = "Studio 2"
            else:
                assigned_studio = "Studio 2"
        
        # Update display studio
        self.studio_display.value = f"Studio: {assigned_studio}"
        self.studio_display.color = ft.Colors.BLUE_600
        
        # Set studio yang dipilih (untuk keperluan internal)
        self.selected_studio = assigned_studio
        
        # Update seat grid dengan studio dan jadwal yang tepat
        self.update_seat_grid_with_studio(assigned_studio)
        self.page.update()

    def on_ticket_type_change(self, e):
        if self.ticket_type.value == "Premiere":
            self.selected_studio = "Studio Premiere"
            self.studio_display.value = "Studio: Studio Premiere"
            self.studio_display.color = ft.Colors.BLUE_600
            self.schedule_dropdown.disabled = False  # Allow user to choose time
            self.update_seat_grid_with_studio("Studio Premiere")

        else:  # Tiket Biasa
           self.schedule_dropdown.disabled = False
           self.studio_display.value = "Studio akan ditentukan otomatis setelah memilih waktu tayang"
           self.studio_display.color = ft.Colors.GREY_600

        # Jika jadwal sudah dipilih, tetapkan studio otomatis
        if self.schedule_dropdown.value:
            self.update_studio_assignment(None)

        self.page.update()

        self.page.update()
            
    def update_seat_grid_with_studio(self, studio_name):
        """Update seat grid berdasarkan studio yang dipilih"""
        self.seat_grid.controls.clear()
        
        if not studio_name or studio_name not in self.studios:
            return
        
        # Pastikan jadwal sudah dipilih
        if not hasattr(self, 'schedule_dropdown') or not self.schedule_dropdown.value:
            return
            
        studio = self.studios[studio_name]
        current_schedule = self.schedule_dropdown.value
        
        for row in range(1, studio.kursi.rows + 1):
            for col in range(1, studio.kursi.cols + 1):
                # Gunakan jadwal sebagai parameter untuk mendapatkan status kursi
                seat_status = studio.kursi.get_seat_status(row, col, current_schedule)
                
                if seat_status == TheaterKursi.EMPTY:
                    bgcolor = ft.Colors.GREEN_200
                elif seat_status == TheaterKursi.TAKEN:
                    bgcolor = ft.Colors.RED_200
                else:  # SELECTED
                    bgcolor = ft.Colors.BLUE_200
                
                seat = ft.Container(
                    content=ft.Text(f"{row}-{col}"),
                    width=40,
                    height=40,
                    bgcolor=bgcolor,
                    border_radius=5,
                    alignment=ft.alignment.center,
                    on_click=lambda e, r=row, c=col: self.toggle_seat_selection_new(r, c, studio_name)
                )
                self.seat_grid.controls.append(seat)
        
        self.page.update()
    
    def toggle_seat_selection_new(self, row, col, studio_name):
        """Toggle seat selection dengan studio dan jadwal yang sudah ditentukan"""
        if not hasattr(self, 'schedule_dropdown') or not self.schedule_dropdown.value:
            self.show_snackbar("Pilih jadwal terlebih dahulu")
            return
            
        studio = self.studios[studio_name]
        current_schedule = self.schedule_dropdown.value
        
        if studio.kursi.toggle_pilih(row, col, current_schedule):
            self.update_seat_grid_with_studio(studio_name)
        
    def create_admin_ui(self):
        # Tab untuk mengelola film
        self.admin_film_tab = self.create_admin_film_management_ui()
        self.admin_add_film_tab = self.create_admin_add_film_ui()
        
        self.admin_tabs = ft.Tabs(
            expand=True,
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Daftar Film",
                    icon=ft.Icons.LIST,
                    content=self.admin_film_tab,
                ),
                ft.Tab(
                    text="Tambah Film",
                    icon=ft.Icons.ADD,
                    content=self.admin_add_film_tab,
                ),
                ft.Tab(
                    text="Laporan",
                    icon=ft.Icons.ANALYTICS,
                    content=self.create_admin_statistics_ui()
                )
            ]
        )
        
        logout_button = ft.ElevatedButton(
            "Logout",
            on_click=self.logout,
            icon=ft.Icons.LOGOUT,
            color=ft.Colors.RED
        )
        
        self.page.clean()
        self.page.add(
            ft.Row(
                [
                    ft.Text(f"Admin Panel - Selamat datang, {self.current_user.username}", size=20, weight="bold"),
                    logout_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            self.admin_tabs
        )


    def create_admin_add_film_ui(self):
        # Input fields untuk film baru
        self.new_film_title = ft.TextField(label="Judul Film", width=400, autofocus=True)
        self.new_film_director = ft.TextField(label="Sutradara", width=400)
        self.new_film_genre = ft.TextField(label="Genre Terpilih", width=400, read_only=True, value="", hint_text="Pilih genre dari daftar di atas")
        self.genre_chips = ft.Row(
        wrap=True,
        spacing=5,
        run_spacing=5
        )

        for genre in self.available_genres:
            chip = ft.Chip(
                label=ft.Text(genre),
                on_select=lambda e, g=genre: self.toggle_genre_selection(e, g),
                selected=False
            )
            self.genre_chips.controls.append(chip)
    
        
        self.new_film_duration = ft.TextField(label="Durasi (menit)", width=400, input_filter=ft.NumbersOnlyInputFilter())
        self.new_film_year = ft.TextField(label="Tahun Rilis", width=400, input_filter=ft.NumbersOnlyInputFilter())
        self.new_film_description = ft.TextField(label="Deskripsi", width=400, multiline=True, min_lines=3)
        self.new_film_rating = ft.TextField(label="Rating", width=400)
        self.new_film_schedule = ft.TextField(label="Jadwal (pisahkan dengan koma)", width=400, hint_text="Contoh: 10:00, 14:00, 18:00")
        self.new_film_poster = ft.TextField(label="URL Poster", width=400)
        
        add_button = ft.ElevatedButton(
            "Tambah Film",
            icon=ft.Icons.ADD,
            on_click=self.add_new_film
        )
        
        return ft.Column(
            [
                ft.Text("Tambah Film Baru", size=18, weight="bold"),
                self.new_film_title,
                self.new_film_director,
                ft.Text("Pilih Genre:", size=14),
                self.genre_chips,
                self.new_film_genre,
                self.new_film_duration,
                self.new_film_year,
                self.new_film_description,
                self.new_film_rating,
                self.new_film_schedule,
                self.new_film_poster,
                add_button
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=15
        )
    
    def toggle_genre_selection(self, e, genre):
        print(f"Chip diklik: {genre}")  # Debug
        e.control.selected = e.control.selected
        print(f"Status baru: {e.control.selected}")  # Debug
        
        selected_genres = [
            chip.label.value
            for chip in self.genre_chips.controls
            if chip.selected
        ]
        print(f"Genre terpilih: {selected_genres}")  # Debug
        
        self.new_film_genre.value = ", ".join(selected_genres)
        self.page.update()
    
    def create_admin_statistics_ui(self):
        # Kumpulkan data dari semua konsumen
        film_sales = {}
        studio_sales = {}
        total_income = 0
        konsumsi_counter = {}
        voucher_usage = {}
    
        for konsumen in self.konsumen_db:
            for trx in getattr(konsumen, 'transaksi_history', []):
                if trx.status != "Paid":
                    continue
    
                # Jumlah penjualan tiket per film
                film_title = trx.film.get_judul()
                film_sales[film_title] = film_sales.get(film_title, 0) + len(trx.no_kursi)
    
                # Tiket terjual per studio
                studio_sales[trx.studio] = studio_sales.get(trx.studio, 0) + len(trx.no_kursi)
    
                # Total pendapatan
                total_income += trx.hitung_total()
    
                # Konsumsi paling laris
                for item in trx.konsumsi:
                    key = f"{item['nama']} ({item['ukuran']})"
                    konsumsi_counter[key] = konsumsi_counter.get(key, 0) + 1
    
                # Penggunaan voucher
                if trx.voucher:
                    voucher_usage[trx.voucher.lower()] = voucher_usage.get(trx.voucher.lower(), 0) + 1
    
        # Buat tampilan
        return ft.Column([
            ft.Text("Statistik Penjualan dan Transaksi", size=20, weight="bold"),
    
            ft.Text(f"Total Pendapatan: Rp {total_income:,.0f}", size=16, color=ft.Colors.GREEN),
            ft.Divider(),
    
            ft.Text("Jumlah Penjualan Tiket per Film", weight="bold"),
            *[ft.Text(f"• {judul}: {jumlah} tiket") for judul, jumlah in film_sales.items()],
    
            ft.Divider(),
            ft.Text("Tiket Terjual per Studio", weight="bold"),
            *[ft.Text(f"• {studio}: {jumlah} tiket") for studio, jumlah in studio_sales.items()],
    
            ft.Divider(),
            ft.Text("Konsumsi Paling Laris", weight="bold"),
            *[ft.Text(f"• {nama}: {jumlah}x") for nama, jumlah in sorted(konsumsi_counter.items(), key=lambda x: -x[1])],
    
            ft.Divider(),
            ft.Text("Penggunaan Voucher", weight="bold"),
            *[ft.Text(f"• {kode.upper()}: {jumlah}x") for kode, jumlah in voucher_usage.items()],
    
        ], scroll=ft.ScrollMode.AUTO)

    def create_admin_film_management_ui(self):
        # Buat list view untuk menampilkan film
        self.admin_film_list_view = ft.ListView(expand=True)
        self.update_admin_film_list()
        
        return ft.Column(
            [
                ft.Text("Daftar Film", size=18, weight="bold"),
                self.admin_film_list_view
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
    
    def update_admin_film_list(self):
        self.admin_film_list_view.controls.clear()
        
        if not self.list_film.films:
            self.admin_film_list_view.controls.append(ft.Text("Tidak ada film yang tersedia."))
            return
        
        for film in self.list_film.films:
            film_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.MOVIE),
                                title=ft.Text(film.get_judul(), weight="bold"),
                                subtitle=ft.Text(f"{film.get_genre()} | {film.get_durasi()} menit"),
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"Sutradara: {film.get_sutradara()}"),
                                    ft.Text(f"Rating: {film.get_rating()}"),
                                ],
                                spacing=20
                            ),
                            ft.Text(film.get_deskripsi(), size=12),
                            ft.Text(f"Jadwal: {film.get_jadwal_penayangan()}"),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Edit",
                                        on_click=lambda e, f=film: self.load_film_for_edit(f),
                                        icon=ft.Icons.EDIT
                                    ),
                                    ft.ElevatedButton(
                                        "Hapus",
                                        on_click=lambda e, f=film: self.delete_film(f),
                                        icon=ft.Icons.DELETE,
                                        color=ft.Colors.RED
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.END
                            )
                        ],
                        spacing=5
                    ),
                    padding=10,
                    width=400
                )
            )
            self.admin_film_list_view.controls.append(film_card)
        
        self.page.update()
    
    def load_film_for_edit(self, film):
        # Set tab ke "Tambah Film"
        self.admin_tabs.selected_index = 1
        self.page.update()
        
        # Isi form dengan data film
        self.new_film_title.value = film.get_judul()
        self.new_film_director.value = film.get_sutradara()
        
        # Set genre chips
        existing_genres = [g.strip() for g in film.get_genre().split(",")]
        for chip in self.genre_chips.controls:
            chip.selected = chip.label.value in existing_genres
        self.new_film_genre.value = film.get_genre()
        
        self.new_film_duration.value = str(film.get_durasi())
        self.new_film_year.value = str(film.get_tahun_rilis())
        self.new_film_description.value = film.get_deskripsi()
        self.new_film_rating.value = film.get_rating()
        self.new_film_schedule.value = film.get_jadwal_penayangan()
        self.new_film_poster.value = film.get_poster()
        
        # Simpan film yang sedang diedit
        self.editing_film = film
        self.page.update()

    def load_film_data_for_edit(self, e):
        selected_title = self.film_to_edit.value
        if not selected_title:
            return
        
        film = next((f for f in self.list_film.films if f.get_judul() == selected_title), None)
        if film:
            self.new_film_title.value = film.get_judul()
            self.new_film_director.value = film.get_sutradara()
            existing_genres = [g.strip() for g in film.get_genre().split(",")]
            for chip in self.genre_chips.controls:
                chip.selected = chip.label.value in existing_genres
            self.new_film_duration.value = str(film.get_durasi())
            self.new_film_year.value = str(film.get_tahun_rilis())
            self.new_film_description.value = film.get_deskripsi()
            self.new_film_rating.value = film.get_rating()
            self.new_film_schedule.value = film.get_jadwal_penayangan()
            self.new_film_poster.value = film.get_poster()
            self.page.update()
    
    def add_new_film(self, e):
        try:
            # Validasi input
            if not all([self.new_film_title.value, self.new_film_director.value,
                       self.new_film_genre.value, self.new_film_duration.value, 
                       self.new_film_year.value, self.new_film_schedule.value]):
                self.show_snackbar("Harap isi semua field yang diperlukan")
                return
            
            if hasattr(self, 'editing_film') and self.editing_film:
                # Mode edit film
                self.editing_film.set_judul(self.new_film_title.value)
                self.editing_film.set_sutradara(self.new_film_director.value)
                self.editing_film.set_genre(self.new_film_genre.value)
                self.editing_film.set_durasi(int(self.new_film_duration.value))
                self.editing_film.set_tahun_rilis(int(self.new_film_year.value))
                self.editing_film.set_deskripsi(self.new_film_description.value)
                self.editing_film.set_rating(self.new_film_rating.value)
                self.editing_film.set_jadwal_penayangan(self.new_film_schedule.value)
                self.editing_film.set_poster(self.new_film_poster.value)
                
                message = "Film berhasil diupdate"
                delattr(self, 'editing_film')
            else:
                # Mode tambah film baru
                new_film = Film(
                    judul=self.new_film_title.value,
                    sutradara=self.new_film_director.value,
                    genre=self.new_film_genre.value,
                    durasi=int(self.new_film_duration.value),
                    tahun_rilis=int(self.new_film_year.value),
                    deskripsi=self.new_film_description.value,
                    rating=self.new_film_rating.value,
                    jadwal_penayangan=self.new_film_schedule.value,
                    poster=self.new_film_poster.value if self.new_film_poster.value else "default_poster.jpg"
                )
                self.list_film.films.append(new_film)
                message = "Film berhasil ditambahkan"
            
            # Simpan ke file
            self.list_film.simpan_ke_file()
            
            # Reset form
            self.new_film_title.value = ""
            self.new_film_director.value = ""
            for chip in self.genre_chips.controls:
                chip.selected = False
            self.new_film_genre.value = ""
            self.new_film_duration.value = ""
            self.new_film_year.value = ""
            self.new_film_description.value = ""
            self.new_film_rating.value = ""
            self.new_film_schedule.value = ""
            self.new_film_poster.value = ""
            
            # Update daftar film
            self.update_admin_film_list()
            
            # Kembali ke tab daftar film
            self.admin_tabs.selected_index = 0
            
            self.show_snackbar(message)
            self.page.update()
            
        except Exception as ex:
            self.show_snackbar(f"Error: {str(ex)}")

    def create_main_ui(self):
        self.film_list_view = ft.ListView(expand=True)
        self.update_film_list()
        
        self.tab_menu = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Film",
                    icon=ft.Icons.MOVIE,
                    content=self.film_list_view
                ),
                ft.Tab(
                    text="Pesan Tiket",
                    icon=ft.Icons.CONFIRMATION_NUMBER,
                    content=self.create_booking_ui_sederhana()
                ),
                ft.Tab(
                    text="Tiket Saya",
                    icon=ft.Icons.RECEIPT_LONG,
                    content=self.create_ticket_ui()
                ),
                ft.Tab(
                    text="Transaksi",
                    icon=ft.Icons.HISTORY,
                    content=self.create_transaction_ui()
                ),
            ],
            expand=True
        )
        #==========================================================================================================================
        
        logout_button = ft.ElevatedButton(
            "Logout",
            on_click=self.logout,
            icon=ft.Icons.LOGOUT,
            color=ft.Colors.RED
        )
        
        self.page.clean()
        self.page.add(
            ft.Row(
                [
                    ft.Text(f"Selamat datang, {self.current_user.username}", size=20, weight="bold"),
                    logout_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            self.tab_menu
        )

    def update_film_list(self):
        self.film_list_view.controls.clear()
        
        if not self.list_film.films:
            self.film_list_view.controls.append(ft.Text("Tidak ada film yang tersedia."))
            return
        
        for film in self.list_film.films:
            film_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.MOVIE),
                                title=ft.Text(film.get_judul(), weight="bold"),
                                subtitle=ft.Text(f"{film.get_genre()} | {film.get_durasi()} menit"),
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"Sutradara: {film.get_sutradara()}"),
                                    ft.Text(f"Rating: {film.get_rating()}"),
                                ],
                                spacing=20
                            ),
                            ft.Text(film.get_deskripsi(), size=12),
                            ft.Text(f"Jadwal: {film.get_jadwal_penayangan()}"),
                            ft.Image(src=film.get_poster(), width=200, height=300, fit=ft.ImageFit.CONTAIN),
                        ],
                        spacing=5
                    ),
                    padding=10,
                    width=400
                )
            )
            self.film_list_view.controls.append(film_card)
        
        self.page.update()

    def update_film(self, e):
        try:
            selected_title = self.film_to_edit.value
            if not selected_title:
                self.show_snackbar("Pilih film terlebih dahulu")
                return
            
            film = next((f for f in self.list_film.films if f.get_judul() == selected_title), None)
            if not film:
                self.show_snackbar("Film tidak ditemukan")
                return
            
            # Update film
            film.set_judul(self.new_film_title.value)
            film.set_sutradara(self.new_film_director.value)
            film.set_genre(self.new_film_genre.value)
            film.set_durasi(int(self.new_film_duration.value))
            film.set_tahun_rilis(int(self.new_film_year.value))
            film.set_deskripsi(self.new_film_description.value)
            film.set_rating(self.new_film_rating.value)
            film.set_jadwal_penayangan(self.new_film_schedule.value)
            film.set_poster(self.new_film_poster.value)
            
            # Simpan perubahan
            self.list_film.simpan_ke_file()
            
            # Update dropdown
            self.film_to_edit.options = [ft.dropdown.Option(f.get_judul()) for f in self.list_film.films]
            self.film_to_edit.value = film.get_judul()
            
            self.show_snackbar("Film berhasil diupdate")
            self.page.update()
            
        except Exception as ex:
            self.show_snackbar(f"Error: {str(ex)}")
    
    def create_ticket_ui(self):
        self.ticket_list_view = ft.ListView(expand=True)
        self.update_ticket_display()
    
        return ft.Column([
        ft.Text("Tiket Saya", size=20, weight="bold"),
        self.ticket_list_view
    ], expand=True)

    def update_ticket_display(self):
        print("=== DEBUG update_ticket_display ===")
        self.ticket_list_view.controls.clear()
        
        # Debug: Cek apakah user memiliki transaksi_history
        if not hasattr(self.current_user, 'transaksi_history'):
            print("User tidak memiliki transaksi_history")
            self.ticket_list_view.controls.append(ft.Text("Belum ada tiket"))
            self.page.update()
            return
        
        print(f"Jumlah transaksi total: {len(self.current_user.transaksi_history)}")
        
        if not self.current_user.transaksi_history:
            print("transaksi_history kosong")
            self.ticket_list_view.controls.append(ft.Text("Belum ada tiket"))
            self.page.update()
            return
        
        # Hanya tampilkan transaksi yang sudah dibayar
        paid_transactions = [t for t in self.current_user.transaksi_history if t.status == "Paid"]
        print(f"Jumlah transaksi yang sudah dibayar: {len(paid_transactions)}")
        
        # Debug: Print detail setiap transaksi
        for i, t in enumerate(self.current_user.transaksi_history):
            print(f"Transaksi {i+1}: ID={t.id_transaksi}, Status={t.status}")
        
        if not paid_transactions:
            print("Tidak ada transaksi yang sudah dibayar")
            self.ticket_list_view.controls.append(ft.Text("Belum ada tiket yang dibayar"))
            self.page.update()
            return
        
        print(f"Membuat {len(paid_transactions)} kartu tiket...")
        
        for transaksi in reversed(paid_transactions):
            # Buat kartu tiket yang menarik
            ticket_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        # Header tiket
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.CONFIRMATION_NUMBER, color=ft.Colors.WHITE),
                                ft.Text("TIKET BIOSKOP", color=ft.Colors.WHITE, weight="bold", size=16),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            bgcolor=ft.Colors.BLUE_600,
                            padding=10,
                            border_radius=ft.BorderRadius(10, 10, 0, 0)
                        ),
                        
                        # Detail tiket
                        ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text("ID Tiket:", weight="bold"),
                                    ft.Text(transaksi.id_transaksi, color=ft.Colors.BLUE_600)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                
                                ft.Divider(height=1),
                                
                                ft.Row([
                                    ft.Text("Film:", weight="bold"),
                                    ft.Text(transaksi.film.get_judul())
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                
                                ft.Row([
                                    ft.Text("Studio:", weight="bold"),
                                    ft.Text(transaksi.studio)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                
                                ft.Row([
                                    ft.Text("Kursi:", weight="bold"),
                                    ft.Text(', '.join(transaksi.no_kursi))
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                
                                ft.Row([
                                    ft.Text("Tanggal:", weight="bold"),
                                    ft.Text(transaksi.tanggal_pemesanan.strftime('%d/%m/%Y'))
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                                ft.Row([
                                    ft.Text("Waktu:", weight="bold"),
                                    ft.Text(transaksi.waktu_tayang)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                
                                ft.Row([
                                    ft.Text("Tipe:", weight="bold"),
                                    ft.Text(transaksi.tipe_tiket),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                                ft.Row([
                                    ft.Text("Fasilitas:", weight="bold"),
                                    *[ft.Text(f"• {fasilitas}") for fasilitas in transaksi.get_fasilitas(self.studios)]
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                                ft.Row([
                                    ft.Text("Total Harga Tiket:", weight="bold"),
                                    ft.Text(transaksi.harga_tiket * int(len(transaksi.no_kursi)))
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                
                                ft.Divider(height=1),
                                
                                ft.Row([
                                    ft.Text("Total:", weight="bold", size=16),
                                    ft.Text(f"Rp {transaksi.hitung_total():,}", weight="bold", size=16, color=ft.Colors.GREEN_600)
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                
                                # Tampilkan konsumsi jika ada
                                *([ft.Divider(height=1), ft.Text("Konsumsi:", weight="bold")] + 
                                  [ft.Text(f"• {item['nama']} ({item['ukuran']}) - Rp {item['harga']:,}") 
                                   for item in transaksi.konsumsi] if transaksi.konsumsi else []),
                                
                            ], spacing=8),
                            padding=15,
                            bgcolor=ft.Colors.WHITE
                        ),
                        
                        # Footer dengan QR code placeholder
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.QR_CODE, size=30),
                                ft.Text("Tunjukkan tiket ini saat masuk bioskop", 
                                       style=ft.TextStyle(italic=True))
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            bgcolor=ft.Colors.GREY_100,
                            padding=10,
                            border_radius=ft.BorderRadius(0, 0, 10, 10)
                        )
                        
                    ], spacing=0),
                    width=400,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    border_radius=10
                ),
                elevation=5
            )
            self.ticket_list_view.controls.append(ticket_card)
        
        print(f"Berhasil menambahkan {len(self.ticket_list_view.controls)} kartu tiket")
        print("=== END DEBUG ===")
        self.page.update()
    
    def create_booking_ui_sederhana(self):
            # Dropdown Film
        film_options = [ft.dropdown.Option(film.get_judul()) for film in self.list_film.films]
        self.film_dropdown = ft.Dropdown(
            label="Pilih Film",
            options=film_options,
            width=300,
            on_change=self.update_schedule_options  # Tambahkan ini
        )
    
        # Dropdown Jadwal Waktu (akan diisi setelah pilih film)
        self.schedule_dropdown = ft.Dropdown(
            label="Pilih Waktu Tayang",
            options=[],
            width=300,
            on_change=self.update_studio_assignment,  # Tambahkan ini
            disabled=True
        )
    
        # Text untuk menampilkan studio yang otomatis dipilih
        self.studio_display = ft.Text(
            "Studio akan ditentukan otomatis setelah memilih waktu tayang",
            size=14,
            color=ft.Colors.GREY_600
        )
    
        # Tipe Tiket
        self.ticket_type = ft.Dropdown(
            label="Tipe Tiket",
            options=[
                ft.dropdown.Option("Biasa"),
                ft.dropdown.Option("Premiere")
            ],
            width=300,
            on_change=self.on_ticket_type_change  # Tambahkan ini

        )
        
        # Voucher Field
        self.voucher_field = ft.TextField(
            label="Kode Voucher",
            width=200,
            hint_text="Masukkan DISKON20 untuk diskon 20%"
        )
    
        # Date Picker
        self.date_picker = ft.DatePicker(
            first_date=datetime.now(),
            on_change=self.update_date_display
        )
        self.page.overlay.append(self.date_picker)
        self.date_button = ft.ElevatedButton(
            "Pilih Tanggal",
            on_click=lambda e: self.open_date_picker()
        )    
        self.selected_date = ft.Text()
    
        # Seat Grid
        self.seat_grid = ft.GridView(
            runs_count=10,
            max_extent=40,
            spacing=5,
            run_spacing=5,
        )
        
        # Konsumsi Section
        self.consumables_section = self.create_consumables_section()
    
        # Booking Button
        self.booking_button = ft.ElevatedButton(
            "Pesan Tiket",
            icon=ft.Icons.CHECK_CIRCLE,
            on_click=self.process_booking
        )
    
        return ft.Column([
            ft.Row([self.film_dropdown, self.schedule_dropdown, self.ticket_type], spacing=20),
            self.studio_display,
            ft.Row([self.date_button, self.selected_date], spacing=20),
            self.voucher_field,
            ft.Text("Pilih Kursi:", weight="bold"),
            self.seat_grid,
            ft.Divider(),
            ft.Text("Konsumsi (Opsional):", weight="bold"),
            self.consumables_section,
            ft.Divider(),
            self.booking_button
        ], spacing=20, scroll=ft.ScrollMode.AUTO)

    def create_consumables_section(self):
        # Reset selected consumables
        self.selected_consumables = []
        
        consumables_column = ft.Column(spacing=10)
        
        # Makanan Section
        consumables_column.controls.append(ft.Text("Makanan:", weight="bold", color=ft.Colors.BLUE_600))
        for key, (nama, ukuran_harga, gambar) in self.konsumsi.makanan.items(): #tambah gambar ==================================================
            food_row = ft.Row([
                ft.Image(src=gambar, width=50, height=50), #tambah ini==============================================================================
                ft.Text(nama, width=200),
                *[ft.ElevatedButton(
                    f"{ukuran} - Rp {harga:,}",
                    on_click=lambda e, n=nama, u=ukuran, h=harga: self.add_consumable(n, u, h),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                ) for ukuran, harga in ukuran_harga.items()]
            ], spacing=10)
            consumables_column.controls.append(food_row)
        
        # Minuman Section
        consumables_column.controls.append(ft.Text("Minuman:", weight="bold", color=ft.Colors.BLUE_600))
        for key, (nama, ukuran_harga,gambar) in self.konsumsi.minuman.items(): #tambah gambarr----------------------------------------------------
            drink_row = ft.Row([
                ft.Image(src=gambar, width=50, height=50), #tambah ini=====================================================
                ft.Text(nama, width=200),
                *[ft.ElevatedButton(
                    f"{ukuran} - Rp {harga:,}",
                    on_click=lambda e, n=nama, u=ukuran, h=harga: self.add_consumable(n, u, h),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
                ) for ukuran, harga in ukuran_harga.items()]
            ], spacing=10)
            consumables_column.controls.append(drink_row)
        
        # Selected consumables display
        self.selected_consumables_display = ft.Column(spacing=5)
        consumables_column.controls.extend([
            ft.Divider(),
            ft.Text("Konsumsi Dipilih:", weight="bold"),
            self.selected_consumables_display
        ])
        
        return ft.Container(
            content=consumables_column,
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10
        )

    def add_consumable(self, nama, ukuran, harga):
        # Tambahkan ke daftar konsumsi
        consumable = {
            "nama": nama,
            "ukuran": ukuran, 
            "harga": harga
        }
        self.selected_consumables.append(consumable)
        
        # Update display
        self.update_consumables_display()

    def update_consumables_display(self):
        self.selected_consumables_display.controls.clear()
        
        if not self.selected_consumables:
            self.selected_consumables_display.controls.append(
                ft.Text("Belum ada konsumsi dipilih", style=ft.TextStyle(italic=True))
            )
        else:
            total_consumables = 0
            for item in self.selected_consumables:
                total_consumables += item["harga"]
                consumable_row = ft.Row([
                    ft.Text(f"• {item['nama']} ({item['ukuran']}) - Rp {item['harga']:,}"),
                    ft.IconButton(
                        ft.Icons.DELETE,
                        on_click=lambda e, item=item: self.remove_consumable(item),
                        icon_color=ft.Colors.RED
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                self.selected_consumables_display.controls.append(consumable_row)
            
            # Total konsumsi
            self.selected_consumables_display.controls.append(
                ft.Text(f"Total Konsumsi: Rp {total_consumables:,}", weight="bold", color=ft.Colors.GREEN_600)
            )
        
        self.page.update()

    def remove_consumable(self, item_to_remove):
        self.selected_consumables = [item for item in self.selected_consumables if item != item_to_remove]
        self.update_consumables_display()

    
    def update_seat_grid(self, e=None):
        self.seat_grid.controls.clear()
        
        if not self.studio_dropdown.value:
            return
            
        studio = self.studios[self.studio_dropdown.value]
        
        for row in range(1, studio.kursi.rows + 1):
            for col in range(1, studio.kursi.cols + 1):
                seat_status = studio.kursi.seats[row-1][col-1]
                
                if seat_status == TheaterKursi.EMPTY:
                    bgcolor = ft.Colors.GREEN_200
                elif seat_status == TheaterKursi.TAKEN:
                    bgcolor = ft.Colors.RED_200
                else:  # SELECTED
                    bgcolor = ft.Colors.BLUE_200
                
                seat = ft.Container(
                    content=ft.Text(f"{row}-{col}"),
                    width=40,
                    height=40,
                    bgcolor=bgcolor,
                    border_radius=5,
                    alignment=ft.alignment.center,
                    on_click=lambda e, r=row, c=col: self.toggle_seat_selection(r, c)
                )
                self.seat_grid.controls.append(seat)
        
        self.page.update()
    
    def toggle_seat_selection(self, row, col):
        studio = self.studios[self.studio_dropdown.value]
        if studio.kursi.toggle_pilih(row, col):
            self.update_seat_grid()
    
    def process_booking(self, e):
        try:
            print("Tombol pesan tiket ditekan")
            
            # Validasi input
            if not self.film_dropdown.value:
                print("Film tidak dipilih")
                self.show_snackbar("Harap pilih film")
                return
            
            if not hasattr(self, 'selected_studio') or not self.selected_studio:
                print("Waktu tayang belum dipilih")
                self.show_snackbar("Harap pilih waktu tayang terlebih dahulu")
                return
            
            if not self.schedule_dropdown.value:
                print("Jadwal waktu tidak dipilih")
                self.show_snackbar("Harap pilih jadwal waktu tayang")
                return
            
            if not self.ticket_type.value:
                print("Tipe tiket tidak dipilih")
                self.show_snackbar("Harap pilih tipe tiket")
                return
            
            if not self.date_picker.value or not self.selected_date.value:
                print("Tanggal tidak dipilih")
                self.show_snackbar("Harap pilih tanggal")
                return
            
            # Dapatkan kursi yang dipilih dengan jadwal yang tepat
            studio = self.studios[self.selected_studio]
            current_schedule = self.schedule_dropdown.value
            selected_seats = studio.kursi.get_selected_seats(current_schedule)
            print(f"Kursi terpilih untuk jadwal {current_schedule}: {selected_seats}")

            
            if not selected_seats:
                print("Tidak ada kursi yang dipilih")
                self.show_snackbar("Harap pilih minimal satu kursi")
                return
            
            # Format nomor kursi
            seat_numbers = [f"{row}-{col}" for row, col in selected_seats]
            print(f"Nomor kursi: {seat_numbers}")
            
            # Dapatkan film yang dipilih
            selected_film = next(f for f in self.list_film.films if f.get_judul() == self.film_dropdown.value)
            print(f"Film terpilih: {selected_film.get_judul()}")
            
            # Buat transaksi dengan konsumsi
            self.current_transaction = Transaksi(
                username=self.current_user.username,
                film=selected_film,
                tanggal_pemesanan=self.date_picker.value,
                no_kursi=seat_numbers,
                studio=self.selected_studio,
                tipe_tiket=self.ticket_type.value,
                konsumsi=self.selected_consumables.copy() if self.selected_consumables else [],
                voucher=self.voucher_field.value if self.voucher_field.value else None,
                waktu_tayang=self.schedule_dropdown.value
            )
            
            print("Transaksi berhasil dibuat, menampilkan dialog pembayaran")
            
            # Tampilkan dialog konfirmasi
            self.show_payment_dialog()
        
        except Exception as ex:
            print(f"Error dalam process_booking: {ex}")
            self.show_snackbar(f"Terjadi kesalahan: {str(ex)}")



    def show_payment_dialog(self):
        try:
            print("Membuat dialog pembayaran...")
            print(f"Current transaction exists: {self.current_transaction is not None}")  # Tambahkan ini
            
            if not self.current_transaction:
                print("Error: current_transaction is None")
                self.show_snackbar("Error: Transaksi tidak ditemukan")
                return
            
            if hasattr(self.page, "dialog") and self.page.dialog and self.page.dialog.open:
               print("Menutup dialog sebelumnya")
               self.page.dialog.open = False
               self.page.update()
            # Hitung total
            total = self.current_transaction.hitung_total()
            print(f"Total pembayaran: Rp {total:,}")

            kursi_list = self.current_transaction.no_kursi
            if not all(isinstance(k, str) for k in kursi_list):
             kursi_list = [str(k) for k in kursi_list]
            
            # Format detail transaksi dengan lebih sederhana
            details_column = ft.Column([
                ft.Text(f"Film: {self.current_transaction.film.get_judul()}", size=14),
                ft.Text(f"Studio: {self.current_transaction.studio}", size=14),
                ft.Text(f"Tipe Tiket: {self.current_transaction.tipe_tiket}", size=14),
                ft.Text(f"Tanggal: {self.current_transaction.tanggal_pemesanan.strftime('%d/%m/%Y') + " " + str(self.current_transaction.waktu_tayang)}", size=14),
                ft.Text(f"Kursi: {', '.join(self.current_transaction.no_kursi)}", size=14),
                ft.Text(f"Harga: Rp {self.current_transaction.harga_tiket* int(len(self.current_transaction.no_kursi))}", size=14),
                ft.Divider(),
                ft.Text(f"Total: Rp {total:,}", size=16, weight="bold", color=ft.Colors.GREEN_600)
            ], spacing=8, tight=True)
            
            # Tambahkan detail konsumsi jika ada
            if self.current_transaction.konsumsi:
                details_column.controls.insert(-2, ft.Text("Konsumsi:", size=14, weight="bold"))
                for item in self.current_transaction.konsumsi:
                    details_column.controls.insert(-2, 
                        ft.Text(f"• {item['nama']} ({item['ukuran']}) - Rp {item['harga']:,}", size=12)
                    )
            
            # Tambahkan info voucher jika ada
            if self.current_transaction.voucher:
                details_column.controls.insert(-2, 
                    ft.Text(f"Voucher: {self.current_transaction.voucher} (Diskon {self.current_transaction.diskon*100}%)", 
                           size=12, color=ft.Colors.BLUE_600)
                )


            
            # Buat dialog dengan ukuran yang sesuai
            self.payment_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Konfirmasi Pembayaran", size=18, weight="bold"),
                content=ft.Container(
                    content=ft.Column(
                        controls=details_column.controls,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                        ),
                    width=400,
                    height=300
                ),
                actions=[
                    ft.ElevatedButton(
                        "Bayar Sekarang",
                        on_click=self.confirm_payment,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE
                        )
                    ),
                    ft.TextButton(
                        "Batal", 
                        on_click=self.cancel_payment,
                        style=ft.ButtonStyle(color=ft.Colors.RED_600)
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            
            if self.payment_dialog not in self.page.overlay:
               self.page.overlay.append(self.payment_dialog)
            print("Dialog berhasil dibuat, menampilkan ke user...")
            
            # Pastikan dialog ditampilkan
            self.page.dialog = self.payment_dialog
            self.payment_dialog.open = True
            self.page.update()
            
            print("Dialog pembayaran berhasil ditampilkan")
            
        except Exception as ex:
            print(f"Error dalam show_payment_dialog: {ex}")
            import traceback
            traceback.print_exc()
            self.show_snackbar(f"Error menampilkan dialog: {str(ex)}")

    def confirm_payment(self, e):
        try:
            print("Konfirmasi pembayaran...")
            
            if not self.current_transaction:
                print("Error: current_transaction is None")
                return
            
            # Konfirmasi pembayaran
            self.current_transaction.confirm_payment()
            print("Status transaksi diubah ke Paid")
            
            # Tambahkan ke history transaksi
            if not hasattr(self.current_user, 'transaksi_history'):
                self.current_user.transaksi_history = []
            self.current_user.transaksi_history.append(self.current_transaction)
            print(f"Transaksi ditambahkan ke history user: {self.current_user.username}")
            
            # Konfirmasi pemilihan kursi dengan jadwal yang tepat
            studio = self.studios[self.current_transaction.studio]
            current_schedule = self.current_transaction.waktu_tayang
            studio.kursi.confirm_selection(current_schedule)
            print(f"Kursi berhasil di-booking untuk jadwal {current_schedule}")
            
            # Tutup dialog terlebih dahulu
            self.payment_dialog.open = False
            self.page.dialog = None
            self.page.update()
            print("Dialog pembayaran ditutup")
            
            # Update data
            print("Updating transaction history...")
            self.update_transaction_history()
            
            print("Updating ticket display...")
            self.update_ticket_display()
            
            # Pindah ke tab tiket
            print("Switching to ticket tab...")
            self.tab_menu.selected_index = 2
            
            # Update UI
            self.page.update()
            
            # Tampilkan pesan sukses
            self.show_snackbar("Pembayaran berhasil! Tiket telah dipesan.")
            
            # Reset form
            self.reset_booking_form()
            
            print("Pembayaran berhasil diproses")
            
        except Exception as ex:
            print(f"Error dalam confirm_payment: {ex}")
            import traceback
            traceback.print_exc()
            self.show_snackbar(f"Error dalam pembayaran: {str(ex)}")
    
    def cancel_payment(self, e):
        try:
            print("Pembayaran dibatalkan")
            
            # Reset kursi yang dipilih dengan jadwal yang tepat
            if self.current_transaction and hasattr(self, 'schedule_dropdown') and self.schedule_dropdown.value:
                studio = self.studios[self.current_transaction.studio]
                current_schedule = self.schedule_dropdown.value
                
                # Reset hanya kursi yang SELECTED untuk jadwal ini
                seats = studio.kursi.get_or_create_schedule(current_schedule)
                for row in range(studio.kursi.rows):
                    for col in range(studio.kursi.cols):
                        if seats[row][col] == TheaterKursi.SELECTED:
                            seats[row][col] = TheaterKursi.EMPTY
                
                # Update seat grid dengan studio yang benar
                self.update_seat_grid_with_studio(self.current_transaction.studio)
                print("Kursi yang dipilih telah direset")
            
            # Reset konsumsi yang dipilih
            self.selected_consumables = []
            if hasattr(self, 'selected_consumables_display'):
                self.update_consumables_display()
            print("Konsumsi yang dipilih telah direset")
            
            # Tutup dialog
            self.payment_dialog.open = False
            self.page.dialog = None
            self.page.update()
            
            # Tampilkan pesan informasi
            self.show_snackbar("Pembayaran dibatalkan. Pilihan kursi dan konsumsi telah direset.")
            
            print("Dialog pembayaran ditutup, kursi dan konsumsi direset")
        except Exception as ex:
            print(f"Error dalam cancel_payment: {ex}")
    
    def show_snackbar(self, message):
        """Helper method untuk menampilkan snackbar"""
        try:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                action="OK"
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as ex:
            print(f"Error menampilkan snackbar: {ex}")
        
    def reset_booking_form(self):
        self.film_dropdown.value = None
        self.schedule_dropdown.value = None  # Tambahkan ini
        self.schedule_dropdown.disabled = True  # Tambahkan ini
        self.studio_display.value = "Studio akan ditentukan otomatis setelah memilih waktu tayang"  # Tambahkan ini
        self.studio_display.color = ft.Colors.GREY_600  # Tambahkan ini
        if hasattr(self, 'selected_studio'):  # Tambahkan ini
            delattr(self, 'selected_studio')
        self.ticket_type.value = None
        self.date_picker.value = None
        self.selected_date.value = ""
        self.voucher_field.value = ""
        self.selected_consumables = []  # Reset konsumsi
        
        # Update display konsumsi
        if hasattr(self, 'selected_consumables_display'):
            self.update_consumables_display()
        
        # Reset seat selection
        for studio in self.studios.values():
            for row in range(studio.kursi.rows):
                for col in range(studio.kursi.cols):
                    if studio.kursi.seats[row][col] == TheaterKursi.SELECTED:
                        studio.kursi.seats[row][col] = TheaterKursi.EMPTY
        
        self.update_seat_grid()
        self.page.update()
    
    def create_transaction_ui(self):
        self.transaction_list_view = ft.ListView(expand=True)
        self.update_transaction_history()
        
        return ft.Column([
            ft.Text("Riwayat Transaksi", size=20, weight="bold"),
            self.transaction_list_view
        ], expand=True)
    
    def update_transaction_history(self):
        self.transaction_list_view.controls.clear()
        
        if not hasattr(self.current_user, 'transaksi_history') or not self.current_user.transaksi_history:
            self.transaction_list_view.controls.append(ft.Text("Belum ada transaksi"))
            return
        
        for transaksi in reversed(self.current_user.transaksi_history):
            transaction_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            title=ft.Text(f"ID: {transaksi.id_transaksi}"),
                            subtitle=ft.Text(f"Status: {transaksi.status}"),
                        ),
                        ft.Text(f"Film: {transaksi.film.get_judul()}"),
                        ft.Text(f"Studio: {transaksi.studio}"),
                        ft.Text(f"Kursi: {', '.join(transaksi.no_kursi)}"),
                        ft.Text(f"Tanggal: {transaksi.tanggal_pemesanan.strftime('%d/%m/%Y')}"),
                        ft.Text(f"Waktu: {transaksi.waktu_tayang}"),
                        ft.Text(f"Total: Rp {transaksi.hitung_total():,}"),
                    ], spacing=5),
                    padding=10,
                    width=400
                )
            )
            self.transaction_list_view.controls.append(transaction_card)
        
        self.page.update()
        
    def delete_film(self, film):
        try:
            # Konfirmasi penghapusan
            print(f"[DEBUG] Tombol hapus ditekan untuk film: {film.get_judul()}")
            self.confirm_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Konfirmasi Penghapusan"),
                content=ft.Text(f"Apakah Anda yakin ingin menghapus film '{film.get_judul()}'?"),
                actions=[
                    ft.TextButton("Ya", on_click=lambda e, f=film: self.confirm_delete_film(f)),
                    ft.TextButton("Tidak", on_click=self.close_dialog),
                ]
            )

            if self.confirm_dialog not in self.page.overlay:
               self.page.overlay.append(self.confirm_dialog)
            
            self.page.dialog = self.confirm_dialog 
            self.confirm_dialog.open = True        
            self.page.update()                     
            print("[DEBUG] Dialog konfirmasi ditampilkan")
    
        except Exception as ex:
            print(f"[ERROR] Terjadi kesalahan saat menampilkan dialog: {ex}")
            self.show_snackbar(f"Error: {str(ex)}")
    
    def refresh_film_dropdown(self):
        if hasattr(self, 'film_dropdown'):
            self.film_dropdown.options = [ft.dropdown.Option(f.get_judul()) for f in self.list_film.films]
            self.page.update()

    def confirm_delete_film(self, film):
        # Normalisasi judul untuk membandingkan dengan lebih aman
        judul_target = film.get_judul().strip().lower()
        
        # Hapus dari list dengan mencocokkan judul (case-insensitive, tanpa spasi)
        self.list_film.films = [
            f for f in self.list_film.films if f.get_judul().strip().lower() != judul_target
        ]
        
        # Simpan perubahan ke file
        self.list_film.simpan_ke_file()
        
        # Update UI
        self.update_admin_film_list()
        self.refresh_film_dropdown()
        
        self.show_snackbar(f"Film '{film.get_judul()}' berhasil dihapus")
        self.close_dialog()


    def close_dialog(self, e=None):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

def main(page: ft.Page):
    # Set app theme and properties
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE
    )
    
    # Create and run the app
    app = CinemaApp(page)

if __name__ == "__main__":
    ft.app(target=main)