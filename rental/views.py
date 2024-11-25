from django.shortcuts import render, get_object_or_404
from .models import Platform, Game, Peminjaman
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
import locale

# Set locale untuk format mata uang rupiah
locale.setlocale(locale.LC_ALL, 'id_ID')

def home(request):
    nama = request.GET.get('game')
    if nama:
        games = Game.objects.filter(nama__icontains=nama)
    else:
        games = Game.objects.all()
    return render(request, 'home.html', {'nama': nama, 'games': games})

def about(request):
    return render(request, 'about.html')

def detail(request, game_id):
    # Mengambil objek Game
    game = get_object_or_404(Game, pk=game_id)
    pesan_berhasil = None
    jumlah_bayar = None
    
    if request.method == 'POST':
        # Ambil data dari form POST
        nik = request.POST.get('nik')
        nama_peminjam = request.POST.get('nama_peminjam')
        tanggal_pinjam = datetime.strptime(request.POST.get('tanggal_pinjam'), "%Y-%m-%d")
        tanggal_kembali = datetime.strptime(request.POST.get('tanggal_kembali'), "%Y-%m-%d")
        
        # Menghitung durasi peminjaman
        durasi_peminjaman = (tanggal_kembali - tanggal_pinjam).days
        
        # Periksa apakah durasi peminjaman valid (harus lebih dari 0)
        if durasi_peminjaman <= 0:
            pesan_berhasil = "Tanggal kembali harus lebih besar dari tanggal peminjaman."
            context = {'game': game, 'pesan_berhasil': pesan_berhasil}
            return render(request, 'detail.html', context)
        
        # Hitung jumlah yang harus dibayar
        jumlah_bayar = game.harga_per_hari * durasi_peminjaman
        jumlah_bayar_rupiah = locale.currency(jumlah_bayar, grouping=True)
        
        # Buat objek peminjaman baru
        peminjaman = Peminjaman(
            nik=nik,
            nama_peminjam=nama_peminjam,
            game=game,
            tanggal_pinjam=tanggal_pinjam,
            tanggal_kembali=tanggal_kembali,
            jumlah_bayar=jumlah_bayar,  # Menyimpan jumlah yang harus dibayar
        )
        
        # Simpan peminjaman
        peminjaman.save()
        
        # Kurangi stok
        game.stok -= 1
        game.save()  # Simpan perubahan stok game
        
        # Set pesan sukses
        pesan_berhasil = f"Terima kasih telah melakukan pemesanan. Silakan datang ke tempat untuk mengambil game. Total Bayar: {jumlah_bayar_rupiah}"
        
    context = {
        'game': game,
        'pesan_berhasil': pesan_berhasil,  # Pesan yang akan ditampilkan di template
        'jumlah_bayar': jumlah_bayar  # Menampilkan jumlah yang harus dibayar
    }
    
    # Render halaman detail dengan context
    return render(request, 'detail.html', context)
