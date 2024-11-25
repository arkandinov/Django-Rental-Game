from django.db import models
from django.utils.timezone import now
# Create your models here.

class Platform(models.Model):
    nama = models.CharField(max_length=250)
    deskripsi = models.TextField(blank=True,null=True)
    
    def __str__(self) -> str:
        return self.nama
    
class Game(models.Model):
    nama = models.CharField(max_length=250)
    deskripsi = models.TextField(blank=True,null=True)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE,default=1)
    stok = models.PositiveIntegerField(default=0)
    harga_per_hari = models.DecimalField(max_digits=10, decimal_places=0)
    gambar = models.ImageField(upload_to='book/images/')

    def __str__(self) -> str:
        return self.nama
    
class Peminjaman(models.Model):
    STATUS_CHOICES = [
        ('DIPESAN', 'Dipesan'),
        ('DIPINJAM', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
    ]
    
    nik = models.CharField(max_length=17)
    nama_peminjam = models.CharField(max_length=250)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="peminjaman")
    tanggal_pinjam = models.DateField(default=now)
    tanggal_kembali = models.DateField()
    jumlah_bayar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sudah_bayar = models.BooleanField(default=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DIPESAN')
    
    def __str__(self):
        return f"{self.nama_peminjam} - {self.game.nama} - ({self.status})"