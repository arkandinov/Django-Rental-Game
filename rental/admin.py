from django.contrib import admin
from .models import Platform, Game, Peminjaman

# Register your models here.

@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('nama',)  # Menampilkan hanya nama platform
    search_fields = ('nama',)  # Pencarian berdasarkan nama platform
    ordering = ('nama',)  # Mengurutkan berdasarkan nama platform


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('nama', 'platform', 'harga_per_hari', 'stok')  # Menampilkan nama game, platform, harga per hari, dan stok
    list_filter = ('platform',)  # Filter berdasarkan platform game
    search_fields = ('nama', 'platform__nama')  # Pencarian berdasarkan nama game atau platform
    ordering = ('nama',)  # Mengurutkan berdasarkan nama game

    def save_model(self, request, obj, form, change):
        """Opsional: Dapat ditambahkan logika khusus ketika game disimpan"""
        super().save_model(request, obj, form, change)


@admin.register(Peminjaman)
class PeminjamanAdmin(admin.ModelAdmin):
    list_display = ('nik', 'nama_peminjam', 'game', 'tanggal_pinjam',
                    'tanggal_kembali', 'status', 'jumlah_bayar')  # Menampilkan informasi peminjaman
    list_filter = ('status',)  # Filter berdasarkan status peminjaman
    search_fields = ('nik', 'nama_peminjam', 'game__nama')  # Pencarian berdasarkan NIK, nama peminjam, atau nama game
    ordering = ('-tanggal_pinjam',)  # Mengurutkan berdasarkan tanggal peminjaman terbaru

    def save_model(self, request, obj, form, change):
        """Jika status peminjaman berubah menjadi 'DIKEMBALIKAN', kembalikan stok game."""
        if obj.status == 'DIKEMBALIKAN':
            obj.game.stok += 1  # Mengembalikan stok game
            obj.game.save()  # Simpan perubahan stok game
        super().save_model(request, obj, form, change)
