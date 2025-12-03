import csv
import datetime

# =====================================
# GÜVENLİ DRONE FİLO YÖNETİM SİSTEMİ
# =====================================

class DroneFiloSistemi:
    """Tüm hafta öğrendiklerimizi kullanan kapsamlı sistem"""
    
    def __init__(self):
        self.dronlar = []
        self.log_dosyasi = "sistem_log.txt"
        self.csv_dosyasi = "filo_rapor.csv"
        self._csv_hazirla()
        self.log("🚁 Sistem başlatıldı")
    
    def _csv_hazirla(self):
        """CSV dosyasını hazırla"""
        try:
            with open(self.csv_dosyasi, "w", newline='', encoding='utf-8') as f:
                yazici = csv.writer(f)
                yazici.writerow(["Zaman", "Drone_ID", "Olay", "Batarya", "Durum"])
        except Exception as e:
            print(f"❌ CSV hazırlama hatası: {e}")
    
    def log(self, mesaj):
        """Zaman damgalı log kaydı"""
        try:
            zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.log_dosyasi, "a", encoding='utf-8') as f:
                f.write(f"[{zaman}] {mesaj}\n")
            print(f"📝 {mesaj}")
        except Exception as e:
            print(f"❌ Log hatası: {e}")
    
    def drone_ekle(self, drone_id, model):
        """Yeni drone ekle"""
        try:
            # Aynı ID var mı kontrol et
            for drone in self.dronlar:
                if drone["id"] == drone_id:
                    print(f"⚠️ {drone_id} zaten mevcut!")
                    return False
            
            # Yeni drone oluştur
            yeni_drone = {
                "id": drone_id,
                "model": model,
                "batarya": 100,
                "yukseklik": 0,
                "durum": "Hazır"
            }
            
            self.dronlar.append(yeni_drone)
            self.log(f"✅ {drone_id} ({model}) filoya eklendi")
            return True
        
        except Exception as e:
            self.log(f"❌ Drone ekleme hatası: {e}")
            return False
    
    def drone_bul(self, drone_id):
        """ID'ye göre drone bul"""
        for drone in self.dronlar:
            if drone["id"] == drone_id:
                return drone
        return None
    
    def kalkis(self, drone_id, hedef_yukseklik):
        """Güvenli kalkış"""
        try:
            drone = self.drone_bul(drone_id)
            
            if drone is None:
                print(f"❌ {drone_id} bulunamadı!")
                return False
            
            if drone["batarya"] < 20:
                print(f"❌ {drone_id} batarya yetersiz!")
                return False
            
            # Kalkış simülasyonu
            for yukseklik in range(0, hedef_yukseklik + 1, 10):
                drone["yukseklik"] = yukseklik
                drone["batarya"] -= 2
            
            drone["durum"] = "Havada"
            self.log(f"🚀 {drone_id} {hedef_yukseklik}m yüksekliğe çıktı")
            self._csv_kaydet(drone_id, "Kalkış", drone["batarya"], drone["durum"])
            return True
        
        except Exception as e:
            self.log(f"❌ Kalkış hatası: {e}")
            return False
    
    def inis(self, drone_id):
        """Güvenli iniş"""
        try:
            drone = self.drone_bul(drone_id)
            
            if drone is None:
                print(f"❌ {drone_id} bulunamadı!")
                return False
            
            # İniş simülasyonu
            while drone["yukseklik"] > 0:
                drone["yukseklik"] -= 10
                drone["batarya"] -= 1
                if drone["yukseklik"] < 0:
                    drone["yukseklik"] = 0
            
            drone["durum"] = "Yerde"
            self.log(f"⬇️ {drone_id} iniş yaptı")
            self._csv_kaydet(drone_id, "İniş", drone["batarya"], drone["durum"])
            return True
        
        except Exception as e:
            self.log(f"❌ İniş hatası: {e}")
            return False
    
    def _csv_kaydet(self, drone_id, olay, batarya, durum):
        """CSV'ye kayıt ekle"""
        try:
            zaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.csv_dosyasi, "a", newline='', encoding='utf-8') as f:
                yazici = csv.writer(f)
                yazici.writerow([zaman, drone_id, olay, batarya, durum])
        except Exception as e:
            print(f"❌ CSV kayıt hatası: {e}")
    
    def durum_raporu(self):
        """Filo durumu"""
        print("\n" + "=" * 70)
        print("📊 FİLO DURUM RAPORU")
        print("=" * 70)
        
        if not self.dronlar:
            print("❌ Filoda drone yok!")
            return
        
        for drone in self.dronlar:
            print(f"🚁 {drone['id']} ({drone['model']})")
            print(f"   🔋 Batarya: %{drone['batarya']}")
            print(f"   📍 Yükseklik: {drone['yukseklik']}m")
            print(f"   ✅ Durum: {drone['durum']}")
            print()
        
        print("=" * 70)
    
    def csv_raporu(self):
        """CSV raporunu göster"""
        try:
            print("\n📋 UÇUŞ GEÇMİŞİ (CSV)")
            print("=" * 80)
            
            with open(self.csv_dosyasi, "r", encoding='utf-8') as f:
                okuyucu = csv.reader(f)
                for i, satir in enumerate(okuyucu):
                    if i == 0:
                        print(f"{satir[0]:20} | {satir[1]:10} | {satir[2]:10} | {satir[3]:10} | {satir[4]}")
                        print("-" * 80)
                    else:
                        print(f"{satir[0]:20} | {satir[1]:10} | {satir[2]:10} | {satir[3]:10} | {satir[4]}")
            
            print("=" * 80)
        
        except FileNotFoundError:
            print("❌ Henüz kayıt yok!")
        except Exception as e:
            print(f"❌ Rapor hatası: {e}")

# =====================================
# TEST SİSTEMİ
# =====================================

def test_sistemi():
    """Sistemi test et"""
    print("🚁 DRONE FİLO YÖNETİM SİSTEMİ TEST EDİLİYOR...")
    print("=" * 70)
    
    # Sistem oluştur
    sistem = DroneFiloSistemi()
    
    # Drone'ları ekle
    sistem.drone_ekle("ALFA-1", "Bayraktar TB2")
    sistem.drone_ekle("ALFA-2", "Akıncı")
    sistem.drone_ekle("ALFA-3", "Bayraktar TB2")
    
    print()
    
    # Kalkışlar
    sistem.kalkis("ALFA-1", 50)
    sistem.kalkis("ALFA-2", 75)
    sistem.kalkis("ALFA-3", 100)
    
    print()
    
    # Durum raporu
    sistem.durum_raporu()
    
    # İnişler
    sistem.inis("ALFA-1")
    sistem.inis("ALFA-2")
    sistem.inis("ALFA-3")
    
    print()
    
    # Final durum
    sistem.durum_raporu()
    
    # CSV raporu
    sistem.csv_raporu()
    
    print(f"\n📁 Dosyalar oluşturuldu:")
    print(f"   - {sistem.log_dosyasi}")
    print(f"   - {sistem.csv_dosyasi}")

# Çalıştır
test_sistemi()