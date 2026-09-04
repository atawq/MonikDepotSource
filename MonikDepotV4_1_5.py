# -*- coding: utf-8 -*-
"""
MonikDepot V4.1.5 Sources
Author: atawq & KuzeyMonik
====================================================================================================
"""

import os
import sys
import json
import time
import shutil
import zipfile
import io
import re
import ctypes
import logging
import subprocess
import webbrowser
import threading
import socket
import ssl
import tempfile
import urllib.request
import urllib.parse
import urllib.error
import traceback
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional, Tuple, Union

# ====================================================================================================
# [0] KÜTÜPHANE DOĞRULAMA (PYWEBVIEW KONTROLÜ)
# ====================================================================================================
try:
    import webview
except ImportError:
    print("[CRITICAL] 'pywebview' kütüphanesi sistemde bulunamadı!")
    print("[BİLGİ] Yüklemek için terminale şu komutu yazın: pip install pywebview")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview"])
        import webview
        print("[SİSTEM] 'pywebview' başarıyla kuruldu.")
    except Exception as e:
        print(f"[HATA] Otomatik kurulum başarısız. Detay: {e}")
        time.sleep(5)
        sys.exit(1)


# ====================================================================================================
# [1] ÖZEL HATA SINIFLARI (CUSTOM EXCEPTIONS)
# ====================================================================================================

class MonikException(Exception):
    """
    MonikDepot sisteminin temel hata sınıfı. 
    Diğer tüm özel hatalar bu sınıftan türer.
    """
    pass

class SteamDetectionError(MonikException):
    """
    Steam dizini kayıt defterinde veya varsayılan yollarda 
    bulunamadığında fırlatılan özel hata sınıfı.
    """
    pass

class NetworkBypassError(MonikException):
    """
    Ağ isteği güvenlik duvarı, SSL sertifikası veya antivirüs 
    tarafından engellendiğinde fırlatılan özel hata sınıfı.
    """
    pass

class DependencyError(MonikException):
    """
    Gerekli sistem DLL'leri veya üçüncü parti kütüphaneler 
    indirilemediğinde fırlatılan özel hata sınıfı.
    """
    pass

class TargetedBypassError(MonikException):
    """
    Hedef odaklı Bypass paketlerinin (GameBypasses) ayıklanması 
    esnasında oluşan spesifik hataları belirtir.
    """
    pass

class VaultSecurityException(MonikException):
    """
    Kredi kasanız (Vault) bozulduğunda veya okuma/yazma izni 
    alınamadığında fırlatılan güvenlik katmanı hatası.
    """
    pass


# ====================================================================================================
# [2] GLOBAL KONFİGÜRASYON VE VERİ SETLERİ (MONIKCONFIG)
# ====================================================================================================
class MonikConfig:
    """
    Uygulamanın küresel yapılandırma parametrelerini, API yollarını, 
    Shopier kodlarını ve sabitlerini içerir.
    """
    
    APP_NAME: str = "MonikDepot"
    VERSION: str = "4.1.5"
    BUILD_TAG: str = "Open-Source Version"
    SHOP_URL: str = "SHOPIER_URL"
    
    # Ağ Maskelemesi İçin Özel User-Agent
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    HEADERS: Dict[str, str] = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Connection": "keep-alive"
    }
    
    # API ve Bağlantı Noktaları
    MANIFEST_SOURCE: str = "MANIFEST_SOURCE"
    STEAM_FEATURED_API: str = "https://store.steampowered.com/api/featured/"
    STEAM_SEARCH_API: str = "https://store.steampowered.com/api/storesearch/?term={query}&l=turkish&cc=TR"
    TARGETED_BYPASS_BASE_URL: str = "YOUR_BYPASS_FILES_SOURCE_URL"
    
    # ==================================================
    # YENİ ALTYAPI BAĞIMLILIKLARI (3 KRİTİK DOSYA)
    # Tamamen yerli ve güvenli entegrasyonlar
    # ==================================================
    DEPENDENCIES: List[Dict[str, str]] = [
        {
            "name": "dwmapi.dll",
            "url": "YOUR_DWMAPI_URL"
        },
        {
            "name": "OpenSteamTool.dll",
            "url": "YOUR_OPENSTEAMTOOL_URL"
        },
        {
            "name": "xinput1_4.dll",
            "url": "YOUR_XINPUT14_URL"
        }
    ]

    # ==================================================
    # YÜKSEK GÜVENLİKLİ 16 HANELİ SHOPIER KODLARI
    # Dikey genişletilmiş PEP-8 uyumlu veri yapısı
    # ==================================================
    SHOP_CODES: Dict[str, int] = {
        # --- 5 KREDİLİK KODLAR (20 Adet) ---
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,
        "5CRD": 5,

        # --- 10 KREDİLİK KODLAR (50 Adet) ---
        
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,
    "10CR": 10,

        # --- 30 KREDİLİK KODLAR (20 Adet) ---
        "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30,
    "30CR": 30
    }

    # ==================================================
    # HEDEF ODAKLI BYPASS (TARGETED) OYUN LİSTESİ
    # Dikey genişletilmiş PEP-8 uyumlu veri yapısı
    # ==================================================
    SUPPORTED_GAMES: Dict[int, str] = {
        12210: "Grand Theft Auto IV: The Complete Edition",
        33230: "Assassin's Creed II",
        39140: "FINAL FANTASY VII (2013)",
        47790: "Medal of Honor(TM) Single Player",
        48190: "Assassin's Creed Brotherhood",
        50300: "Spec Ops: The Line",
        110800: "L.A. Noire",
        220240: "Far Cry 3",
        221910: "The Stanley Parable",
        234080: "Castlevania: Lords of Shadow - Ultimate Edition",
        239250: "Castlevania: Lords of Shadow 2",
        242050: "Assassin's Creed IV Black Flag",
        243470: "Watch_Dogs",
        256290: "Child of Light",
        289650: "Assassin's Creed Unity",
        298110: "Far Cry 4",
        311560: "Assassin's Creed Rogue",
        315210: "Suicide Squad: Kill the Justice League",
        368500: "Assassin's Creed Syndicate",
        371660: "Far Cry Primal",
        447040: "Watch_Dogs 2",
        466130: "White Day: A Labyrinth Named School",
        552520: "Far Cry 5",
        582160: "Assassin's Creed Origins",
        646910: "The Crew 2",
        678950: "DRAGON BALL FighterZ",
        916440: "Anno 1800",
        939960: "Far Cry New Dawn",
        1114150: "CarX Street",
        1174180: "Red Dead Redemption 2",
        1196590: "Resident Evil Village",
        1222680: "Need for Speed Heat",
        1222730: "STAR WARS: Squadrons",
        1237320: "Sonic Frontiers",
        1238000: "Mass Effect: Andromeda",
        1313860: "EA SPORTS FIFA 21",
        1328660: "Need for Speed Hot Pursuit Remastered",
        1328670: "Mass Effect Legendary Edition",
        1413480: "Shin Megami Tensei III Nocturne HD Remaster",
        1506830: "FIFA 22",
        1677280: "Company of Heroes 3",
        1693980: "Dead Space",
        2050650: "Resident Evil 4",
        2055290: "Sonic Colors: Ultimate",
        2172010: "Until Dawn",
        2208920: "Assassin's Creed Valhalla",
        2215260: "Scott Pilgrim vs The World",
        2239550: "Watch Dogs: Legion",
        2369390: "Far Cry 6",
        2668510: "Red Dead Redemption",
        2807960: "Battlefield 6",
        3017860: "DOOM: The Dark Ages",
        3035570: "Assassin's Creed Mirage",
        3764200: "Resident Evil Requiem",
        3800340: "ScootX"
    }

    # Dizin Yapılandırmaları
    APPDATA: Path = Path(os.getenv('APPDATA', os.path.expanduser("~")))
    ROOT_DIR: Path = APPDATA / APP_NAME
    LOG_DIR: Path = ROOT_DIR / "Logs"
    TEMP_DIR: Path = ROOT_DIR / "Temp"
    VAULT_FILE: Path = ROOT_DIR / "vault_v4.1.json"
    LOG_FILE: Path = LOG_DIR / "system.log"

    @classmethod
    def ensure_directories(cls):
        """Uygulamanın çalışması için gerekli tüm veri klasörlerini oluşturur."""
        for directory in [cls.ROOT_DIR, cls.LOG_DIR, cls.TEMP_DIR]:
            directory.mkdir(parents=True, exist_ok=True)


# ====================================================================================================
# [3] KORUMALI WINDOWS UAC YÖNETİCİ YETKİLENDİRMESİ
# ====================================================================================================
def is_admin() -> bool:
    """Uygulamanın yönetici haklarıyla çalışıp çalışmadığını doğrular."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def elevate_privileges() -> bool:
    """Yetki yoksa UAC penceresi tetikler ve yeniden başlatır."""
    if is_admin():
        return True
        
    print("[SİSTEM] Yönetici izni talep ediliyor, lütfen açılan pencereyi onaylayın...")
    try:
        executable = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        safe_script_path = f'"{script_path}"'
        arguments = " ".join([safe_script_path] + sys.argv[1:])
        working_directory = os.getcwd()
        
        result = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", executable, arguments, working_directory, 1
        )
        
        if result <= 32:
            print(f"[HATA] Kullanıcı yönetici iznini reddetti. Hata Kodu: {result}")
            return False
            
        sys.exit(0) 
    except Exception as e:
        print(f"[KRİTİK] Yönetici yetkisi yükseltilirken yapısal hata oluştu: {e}")
        return False


# ====================================================================================================
# [4] GELİŞMİŞ LOGLAMA VE BAĞLAM AKIŞ MOTORU (MONIKLOGGER)
# ====================================================================================================
class MonikLogger:
    """Arayüzü kitlemeyen, terminale ve dosyaya eşzamanlı yazan gelişmiş loglama sınıfı."""
    _lock = threading.Lock()
    _logger: Optional[logging.Logger] = None

    @classmethod
    def initialize(cls):
        """Sistemin loglama mimarisini yapılandırır ve dosyaları hazırlar."""
        MonikConfig.ensure_directories()
        with cls._lock:
            if os.name == 'nt':
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            
            cls._logger = logging.getLogger(MonikConfig.APP_NAME)
            cls._logger.setLevel(logging.DEBUG)
            
            if cls._logger.hasHandlers():
                cls._logger.handlers.clear()
                
            file_handler = logging.FileHandler(MonikConfig.LOG_FILE, encoding="utf-8")
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            file_handler.setFormatter(formatter)
            cls._logger.addHandler(file_handler)
            
            cls.info(f"=== {MonikConfig.APP_NAME} v{MonikConfig.VERSION} Loglama Sistemi Başlatıldı ===")

    @classmethod
    def _log_to_terminal(cls, level: str, color_code: str, message: str):
        """Mesajları renkli bir şekilde backend konsoluna basar. UI'a log gönderimi kaldırıldı."""
        now = datetime.now().strftime("%H:%M:%S")
        formatted = f"\033[{color_code}m[{level}] [{now}] {message}\033[0m"
        print(formatted, flush=True)

    @classmethod
    def info(cls, msg: str): 
        """Standart bilgi mesajlarını kaydeder (Mavi renk)."""
        if cls._logger: cls._logger.info(msg)
        cls._log_to_terminal("BİLGİ", "34", msg)
        
    @classmethod
    def warn(cls, msg: str): 
        """Uyarı mesajlarını kaydeder (Sarı renk)."""
        if cls._logger: cls._logger.warning(msg)
        cls._log_to_terminal("UYARI", "33", msg)
        
    @classmethod
    def error(cls, msg: str): 
        """Kritik hata mesajlarını kaydeder (Kırmızı renk)."""
        if cls._logger: cls._logger.error(msg)
        cls._log_to_terminal("HATA", "31", msg)
        
    @classmethod
    def debug(cls, msg: str): 
        """Geliştirici modu ayıklama mesajlarını kaydeder."""
        if cls._logger: cls._logger.debug(msg)
        cls._log_to_terminal("AYIKLA", "36", msg)
        
    @classmethod
    def success(cls, msg: str):
        """İşlem başarılarını kaydeder (Yeşil renk)."""
        if cls._logger: cls._logger.info(msg)
        cls._log_to_terminal("BAŞARI", "32", msg)
        
    @classmethod
    def thought(cls, msg: str):
        """Sistem mantığını ve kararları kaydeder (Mor renk)."""
        if cls._logger: cls._logger.debug(msg)
        cls._log_to_terminal("SİSTEM", "35", msg)


# ====================================================================================================
# [5] GİZLİ VE DÜŞÜK SEVİYELİ AĞ MOTORU (STEALTH NETWORK ENGINE)
# ====================================================================================================
class StealthNetwork:
    """Anti-Bot korumalarını aşmak için özel SSL ve chunk indirme yapısına sahip ağ modülü."""
    
    @staticmethod
    def get_secure_context() -> ssl.SSLContext:
        """Güvensiz HTTPS istekleri için sertifika doğrulamasını atlar."""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    @classmethod
    def fetch(cls, url: str, is_json: bool = False, timeout: int = 15, retries: int = 3) -> Any:
        """Hafif boyutlu verileri (JSON, Text) çekmek için kullanılır."""
        MonikLogger.debug(f"Ağ İsteği Başlatıldı: {url}")
        delay = 1
        
        for attempt in range(retries):
            try:
                request = urllib.request.Request(url, headers=MonikConfig.HEADERS)
                ctx = cls.get_secure_context()
                with urllib.request.urlopen(request, context=ctx, timeout=timeout) as response:
                    data = response.read()
                    if is_json:
                        try: return json.loads(data.decode('utf-8'))
                        except json.JSONDecodeError as je:
                            MonikLogger.error(f"JSON Parse Hatası ({url}): {je}")
                            return None
                    return data
            except urllib.error.URLError as e:
                MonikLogger.warn(f"Bağlantı Hatası ({url}) - Deneme {attempt+1}/{retries}: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2
            except Exception as e:
                MonikLogger.error(f"Beklenmeyen Ağ Çökmesi ({url}): {e}")
                break
        return None

    @classmethod
    def download_chunked(cls, url: str, dest_path: str, progress_callback=None) -> bool:
        """Büyük bypass ZIP paketlerini bozulmadan (chunk) indiren güvenli yapı."""
        ctx = cls.get_secure_context()
        temp_dest = dest_path + ".tmp"
        
        req = urllib.request.Request(url, headers=MonikConfig.HEADERS)
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
                total_size = int(response.info().get('Content-Length', 0))
                downloaded = 0
                block_size = 65536 # 64KB buffer
                
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                with open(temp_dest, 'wb') as f:
                    while True:
                        chunk = response.read(block_size)
                        if not chunk: break
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0 and progress_callback:
                            percent = int((downloaded / total_size) * 100)
                            progress_callback(percent, downloaded, total_size)
                            
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.rename(temp_dest, dest_path)
            return True
            
        except urllib.error.HTTPError as he:
            MonikLogger.error(f"Sunucu Hatası ({he.code}): Bypass ZIP dosyası henüz yüklenmemiş olabilir.")
            if os.path.exists(temp_dest): os.remove(temp_dest)
            return False
        except Exception as e:
            MonikLogger.error(f"İndirme esnasında ağ hatası: {str(e)}")
            if os.path.exists(temp_dest): os.remove(temp_dest)
            return False


# ====================================================================================================
# [6] BAĞIMLILIK YÖNETİCİSİ (DEPENDENCY MANAGER)
# ====================================================================================================
class DependencyManager:
    """Projenin tamamen yerli ve güvenli DLL bağımlılıklarını yönetir."""
    
    def __init__(self, steam_path: Optional[Path], network: StealthNetwork):
        self.steam_path = steam_path
        self.network = network

    def enforce_dependencies(self):
        """
        Yeni Altyapı dosyalarını Steam klasörüne doğrudan yönetici izinleriyle indirir.
        False-positive antivirüs engellemelerini önlemek için güvenli entegrasyon.
        """
        if not self.steam_path or not self.steam_path.exists():
            MonikLogger.warn("Steam dizini bulunamadı. Yerli DLL entegrasyonu atlanıyor.")
            return

        for dep in MonikConfig.DEPENDENCIES:
            target_file = self.steam_path / dep["name"]
            if not target_file.exists():
                MonikLogger.info(f"Eksik altyapı modülü tespit edildi. İndiriliyor: {dep['name']}...")
                self._download_and_place(dep["url"], target_file)

    def _download_and_place(self, url: str, target: Path):
        """Bağımlılıkları Github'dan çeker ve hedefe yazar."""
        MonikLogger.thought(f"Yönetici yetkileri kullanılarak '{target.name}' sisteme gömülüyor...")
        data = self.network.fetch(url, timeout=30)
        if data:
            try:
                if target.exists():
                    os.chmod(target, 0o777)
                target.write_bytes(data)
                MonikLogger.success(f"Yerli kütüphane başarıyla sisteme yerleştirildi: {target.name}")
            except Exception as e:
                MonikLogger.error(f"Kütüphane yazılamadı ({target.name}): {e}")

    @staticmethod
    def clean_temp_files():
        """Geçici indirme klasörünü uygulama kapanırken güvenle temizler."""
        if MonikConfig.TEMP_DIR.exists():
            try:
                shutil.rmtree(MonikConfig.TEMP_DIR, ignore_errors=True)
                MonikLogger.info("[TEMİZLİK] Geçici sistem klasörleri boşaltıldı.")
            except Exception as ce:
                MonikLogger.warn(f"Geçici klasör temizlenirken ufak bir sorun oluştu: {ce}")


# ====================================================================================================
# [7] TARGETED BYPASS MOTORU (HEDEF ODAKLI YENİ SİSTEM)
# ====================================================================================================
class TargetedBypassEngine:
    """Eski generic_fix mantığını çöpe atan, oyun başına özel ZIP çeken muazzam bypass motoru."""
    
    def __init__(self, network: StealthNetwork):
        self.network = network

    def apply_bypass(self, appid: int, game_install_path: str) -> Dict[str, Any]:
        """files.luatools.work üzerinden ilgili AppID'ye ait bypass zipini çeker ve oyun içine açar."""
        if appid not in MonikConfig.SUPPORTED_GAMES:
            return {"status": "error", "msg": "Bu oyun henüz yeni Bypass sisteminde desteklenmiyor!"}
            
        if not os.path.isdir(game_install_path): 
            return {"status": "error", "msg": "Hedef oyun klasörü bilgisayarda bulunamadı."}
            
        download_url = MonikConfig.TARGETED_BYPASS_BASE_URL.format(app_id=appid)
        MonikLogger.info(f"Bypass İsteği: {download_url}")
        
        zip_target_path = ""
        try:
            # İşletim sisteminin geçici dizinini kullan (Zero-Dir Policy)
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file: 
                zip_target_path = tmp_file.name
            
            # Kendi yazdığımız sağlam ağ motorunu kullanarak indir
            success = self.network.download_chunked(download_url, zip_target_path, None)
            if not success:
                return {"status": "error", "msg": "Bypass paketi sunucudan indirilemedi (ZIP bulunamadı veya ağ koptu)."}
                
            # Orijinal DLL'leri yedekleme havuzu
            backup_dir = os.path.join(game_install_path, ".monik_backup", str(appid))
            os.makedirs(backup_dir, exist_ok=True)
            
            extracted_files = []
            backed_up_files = []
            
            # ZIP Dosyasını ayıklama ve Zero-Dir yönetimi
            with zipfile.ZipFile(zip_target_path, 'r') as z:
                all_names = z.namelist()
                
                # Klasör hiyerarşisi analizi (Gereksiz kök klasörleri atlama)
                top_levels = set(n.split("/")[0] for n in all_names if n.split("/")[0])
                appid_folder = f"{appid}/"
                
                has_root_folder = len(top_levels) == 1 and appid_folder.rstrip("/") in top_levels
                
                for member in all_names:
                    if member.endswith('/'): continue # Klasörleri atla
                    
                    # Hedef yolun hesaplanması
                    if has_root_folder and member.startswith(appid_folder):
                        target_subpath = member[len(appid_folder):]
                        if not target_subpath: continue
                    else:
                        target_subpath = member
                        
                    target_full_path = os.path.join(game_install_path, target_subpath)
                    
                    # Orijinali Yedekle
                    if os.path.exists(target_full_path):
                        b_path = os.path.join(backup_dir, target_subpath)
                        os.makedirs(os.path.dirname(b_path), exist_ok=True)
                        shutil.copy2(target_full_path, b_path)
                        backed_up_files.append(target_subpath)
                        
                    # Fix'i Çıkart
                    os.makedirs(os.path.dirname(target_full_path), exist_ok=True)
                    
                    # ZipArchive'den direkt stream ile hedefe yazma (Zero-Dir kuralı)
                    with z.open(member) as source, open(target_full_path, "wb") as target:
                        shutil.copyfileobj(source, target)
                        
                    extracted_files.append(target_subpath.replace("\\", "/"))
            
            # Başarılı Enjeksiyon Sonrası Loglama
            game_name = MonikConfig.SUPPORTED_GAMES[appid]
            self._write_manifest_log(game_install_path, appid, game_name, extracted_files, backed_up_files, backup_dir)
            
            MonikLogger.success(f"{game_name} için Nokta Atışı Bypass başarıyla sağlandı!")
            return {"status": "success", "msg": f"Bypass dosyaları ({len(extracted_files)} adet) başarıyla oyuna entegre edildi."}
            
        except zipfile.BadZipFile:
            return {"status": "error", "msg": "İndirilen paket bozuk bir ZIP dosyası!"}
        except Exception as e:
            MonikLogger.error(f"Bypass Hatası: {e}")
            return {"status": "error", "msg": str(e)}
        finally:
            if zip_target_path and os.path.exists(zip_target_path):
                try: os.remove(zip_target_path)
                except: pass

    def _write_manifest_log(self, install_path: str, appid: int, game_name: str, files: list, backed_up: list, backup_dir: str):
        """Uygulanan yamaları geri alabilmek için manifest tutar."""
        log_path = os.path.join(install_path, f"monik-bypass-manifest-{appid}.log")
        
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f'[TARGETED_BYPASS]\nDate: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nGame: {game_name}\nBackup Dir: {backup_dir}\nFiles:\n')
            for fp in files: f.write(f'{fp}\n')
            if backed_up:
                f.write('---\nBackedUp:\n')
                for fp in backed_up: f.write(f'{fp}\n')
            f.write('[/TARGETED_BYPASS]\n')

    def restore_original_files(self, appid: int, game_install_path: str) -> Dict[str, Any]:
        """Uygulanan bypass'ı temizler ve orijinal dosyaları yerine koyar."""
        if not os.path.isdir(game_install_path): 
            return {"status": "error", "msg": "Oyun klasörü bulunamadı."}
            
        log_path = os.path.join(game_install_path, f"monik-bypass-manifest-{appid}.log")
        backup_dir = os.path.join(game_install_path, ".monik_backup", str(appid))
        
        if not os.path.exists(log_path): 
            return {"status": "error", "msg": "Sistemde uygulanmış bir bypass manifesti bulunamadı."}
            
        try:
            with open(log_path, 'r', encoding='utf-8') as f: 
                content = f.read()
                
            files_to_delete, backed_up_files, log_backup_dir = [], [], None
            
            if "[TARGETED_BYPASS]" in content:
                for block in content.split("[TARGETED_BYPASS]"):
                    if not block.strip(): continue
                    lines = block.split("\n")
                    in_files = in_backed_up = False
                    for line in lines:
                        line = line.strip()
                        if line == "[/TARGETED_BYPASS]": break
                        if line == "---": 
                            in_files = False; in_backed_up = True
                        elif line == "Files:": 
                            in_files = True
                        elif line == "BackedUp:": 
                            in_backed_up = True; in_files = False
                        elif line.startswith("Backup Dir:"): 
                            log_backup_dir = line.split("Backup Dir:", 1)[1].strip()
                        elif in_files and line: 
                            files_to_delete.append(line)
                        elif in_backed_up and line: 
                            backed_up_files.append(line)
                        
            restored, deleted = 0, 0
            actual_backup = log_backup_dir if (log_backup_dir and os.path.exists(log_backup_dir)) else backup_dir
            
            # Geri Yükleme
            if backed_up_files and os.path.exists(actual_backup):
                for fp in backed_up_files:
                    source, target = os.path.join(actual_backup, fp), os.path.join(game_install_path, fp)
                    if os.path.exists(source):
                        os.makedirs(os.path.dirname(target), exist_ok=True)
                        shutil.copy2(source, target)
                        restored += 1
                        
            # Bypass Dosyalarını Silme
            for fp in files_to_delete:
                full_path = os.path.join(game_install_path, fp)
                if os.path.exists(full_path): 
                    os.remove(full_path)
                    deleted += 1
                    
            try: os.remove(log_path)
            except: pass
            
            if os.path.exists(backup_dir):
                try: shutil.rmtree(backup_dir)
                except: pass
                
            return {"status": "success", "msg": f"{restored} orijinal dosya geri yüklendi, {deleted} bypass dosyası temizlendi."}
        except Exception as e: 
            MonikLogger.error(f"Geri yükleme hatası: {str(e)}")
            return {"status": "error", "msg": f"Geri yükleme hatası: {str(e)}"}

    def check_status(self, appid: int, game_install_path: str) -> bool:
        """Belirtilen oyunda bypass kurulup kurulmadığını kontrol eder."""
        return os.path.exists(os.path.join(game_install_path, f"monik-bypass-manifest-{appid}.log"))


# ====================================================================================================
# [8] STEAM INTEGRATION CORE (THE HEART)
# ====================================================================================================

class SteamCore:
    """Steam kayıt defterini ve oyun klasörlerini (depotcache/manifest) yöneten ana birim."""
    def __init__(self, network: StealthNetwork):
        self.network = network
        self.steam_path = self._detect_steam_installation()
        DependencyManager(self.steam_path, self.network).enforce_dependencies()

    def _detect_steam_installation(self) -> Optional[Path]:
        import winreg
        for hkey, subkey in [(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"), (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")]:
            try:
                with winreg.OpenKey(hkey, subkey) as key:
                    try: path_str, _ = winreg.QueryValueEx(key, "SteamPath")
                    except OSError: path_str, _ = winreg.QueryValueEx(key, "InstallPath")
                    fp = Path(path_str.replace("/", "\\"))
                    if fp.exists(): return fp
            except Exception: continue
        return None

    def write_app_manifest(self, app_id: str, game_name: str) -> bool:
        """Kütüphane entegrasyonu için yapay bir Steam ACF dosyası yazar."""
        if not self.steam_path: return False
        mf = self.steam_path / "steamapps" / f"appmanifest_{app_id}.acf"
        safe_name = re.sub(r'[\\/*?:"<>|]', "", game_name).strip()
        cnt = f""""AppState"\n{{\n\t"appid"\t\t"{app_id}"\n\t"Universe"\t\t"1"\n\t"name"\t\t"{game_name}"\n\t"StateFlags"\t\t"4"\n\t"installdir"\t\t"{safe_name}"\n\t"LastUpdated"\t\t"{int(time.time())}"\n\t"UpdateResult"\t\t"0"\n\t"SizeOnDisk"\t\t"0"\n\t"buildid"\t\t"0"\n\t"LastOwner"\t\t"0"\n\t"AutoUpdateBehavior"\t\t"0"\n\t"AllowOtherDownloadsWhileRunning"\t\t"0"\n\t"ScheduledAutoUpdate"\t\t"0"\n}}"""
        try: 
            mf.write_text(cnt, encoding="utf-8")
            return True
        except: return False

    def clear_app_cache(self):
        """Yeni eklenen oyunların tanınması için Steam appcache temizlenir."""
        if not self.steam_path: return
        cd = self.steam_path / "appcache"
        if cd.exists():
            try: shutil.rmtree(cd, ignore_errors=True)
            except: pass

    def deploy_zip_payload(self, zip_bytes: bytes, app_id: str) -> Tuple[bool, str]:
        """
        Kullanıcının seçtiği veya sunucudan inen manifest paketlerini Steam'e entegre eder.
        DİKKAT: .lua uzantılı dosyalar yeni kural gereği config/lua klasörüne açılır.
        DİKKAT: Steam restart özelliği yama/ekleme işlemleri için iptal edilmiştir.
        """
        if not self.steam_path: 
            return False, "Sistemde Steam yolu bulunamadı."
            
        extract_temp = None
        try:
            extract_temp = MonikConfig.TEMP_DIR / f"payload_{app_id}"
            if extract_temp.exists(): 
                shutil.rmtree(extract_temp, ignore_errors=True)
            extract_temp.mkdir(parents=True)
            
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive: 
                archive.extractall(extract_temp)

            dc = self.steam_path / "depotcache"
            dc.mkdir(exist_ok=True)
            for m_file in extract_temp.rglob("*.manifest"): 
                shutil.copy2(m_file, dc / m_file.name)
            
            # GÜNCEL KURAL: .lua dosyaları 'config/lua' klasörüne aktarılacak
            lp = self.steam_path / "config" / "lua"
            lp.mkdir(parents=True, exist_ok=True)
            for l_file in extract_temp.rglob("*.lua"): 
                shutil.copy2(l_file, lp / l_file.name)

            MonikLogger.thought("Steam kapatılıp açılmadan (restart iptal) veriler diske işlendi.")
            return True, "Manifest dosyaları Steam'e hatasız entegre edildi."
        except Exception as e: 
            return False, f"Steam entegrasyon hatası: {str(e)}"
        finally:
            if extract_temp and extract_temp.exists(): 
                shutil.rmtree(extract_temp, ignore_errors=True)


# ====================================================================================================
# [9] KASA (VAULT) VE SHOPIER LİSANS DOĞRULAMA SİSTEMİ
# ====================================================================================================

class MonikVault:
    """Kullanıcının Shopier kredi miktarını, kütüphanesini ve kod geçmişini tutan güvenli JSON cüzdanı."""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.load_vault()

    def load_vault(self) -> None:
        try:
            if MonikConfig.VAULT_FILE.exists():
                raw = MonikConfig.VAULT_FILE.read_text(encoding="utf-8")
                self.data = json.loads(raw)
                
                # Sürüm Geçiçi: Yeni politika ile kredi 3 olarak başlatılmalı (Eğer önceden yoksa)
                if "credits" not in self.data: self.data["credits"] = 3
                if "used_codes" not in self.data: self.data["used_codes"] = []
                if "games" not in self.data: self.data["games"] = []
                if "user_name" not in self.data: self.data["user_name"] = "Misafir"
                if "settings" not in self.data: self.data["settings"] = {"create_acf": True, "language": "tr"}
            else:
                self.reset_to_default()
        except Exception as e:
            MonikLogger.error(f"Vault okuma hatası, sıfırlanıyor: {e}")
            self.reset_to_default()

    def reset_to_default(self) -> None:
        """Başlangıçta 3 kredilik ücretsiz kullanım hakkı sunulur."""
        self.data = {
            "user_name": "Misafir",
            "credits": 3,
            "used_codes": [],
            "games": [],
            "settings": {"create_acf": True, "language": "tr"},
            "registered_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_vault()

    def save_vault(self) -> None:
        try:
            MonikConfig.VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(MonikConfig.VAULT_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            MonikLogger.error(f"Kasa (Vault) diske kaydedilemedi: {e}")

    def consume_credit(self) -> bool:
        """İndirme veya aktarım işlemi yapıldığında 1 kredi düşer."""
        if self.data["credits"] > 0:
            self.data["credits"] -= 1
            self.save_vault()
            MonikLogger.info(f"[-] 1 Kredi harcandı. Kalan Cüzdan: {self.data['credits']}")
            return True
        return False

    def add_credits_via_code(self, code: str) -> Tuple[bool, str, int]:
        """Kullanıcının girdiği kodu denetler ve bakiyeye yansıtır."""
        clean_code = code.strip().upper()
        
        if clean_code in self.data["used_codes"]:
            return False, "HATA: Bu Shopier kodu daha önce bilgisayarınızda aktive edilmiş!", self.data["credits"]
            
        if clean_code in MonikConfig.SHOP_CODES:
            reward = MonikConfig.SHOP_CODES[clean_code]
            self.data["credits"] += reward
            self.data["used_codes"].append(clean_code)
            self.save_vault()
            MonikLogger.success(f"[SHOPIER] Kod aktive edildi! Kod: {clean_code} -> +{reward} Kredi.")
            return True, f"Tebrikler! Shopier kodu onaylandı. Hesabınıza +{reward} Kredi eklendi!", self.data["credits"]

        return False, "HATA: Girdiğiniz kod geçersiz veya sistemde bulunmuyor!", self.data["credits"]


# ====================================================================================================
# [10] ANA ÇEKİRDEK KÖPRÜSÜ (MONIKENGINE - BACKEND API INTERFACE)
# ====================================================================================================
class MonikEngine:
    """JS ile Python arasındaki iletişimi kuran, Multi-Threaded ana motor."""
    
    def __init__(self):
        MonikLogger.info(f"{MonikConfig.APP_NAME} Backend API köprüsü başlatılıyor...")
        self.network = StealthNetwork()
        self.steam = SteamCore(self.network)
        self.bypass_engine = TargetedBypassEngine(self.network)
        self.vault = MonikVault()
        self.thread_pool = ThreadPoolExecutor(max_workers=8)

    # ------------------------------------------------------------------------------------------------
    # UI JAVASCRIPT EXPOSED API METOTLARI
    # ------------------------------------------------------------------------------------------------
    
    def get_initial_state(self) -> Dict[str, Any]:
        return self.vault.data

    def update_user_name(self, name: str) -> bool:
        clean = name.strip()
        if clean:
            self.vault.data["user_name"] = clean
            self.vault.save_vault()
            return True
        return False

    def update_setting(self, key: str, value: Union[str, bool]):
        if "settings" not in self.vault.data: 
            self.vault.data["settings"] = {}
        self.vault.data["settings"][key] = value
        self.vault.save_vault()

    def redeem_shopier_code(self, code: str) -> Dict[str, Any]:
        # Kodun stringe çevrilip boşluklarının temizlenmesi sağlanır
        if not code or len(str(code).strip()) == 0:
            return {"status": "error", "msg": "Kod alanı boş bırakılamaz!"}
            
        # add_credits_via_code fonksiyonuna da str() biçiminde güvenle gönderilir
        success, message, current_credits = self.vault.add_credits_via_code(str(code))
        if success:
            return {"status": "success", "msg": message, "credits": current_credits}
        return {"status": "error", "msg": message}

    def open_shopier_link(self) -> None:
        try:
            webbrowser.open(MonikConfig.SHOP_URL)
        except: pass

    def fetch_featured_games(self) -> List[Dict[str, Any]]:
        raw = self.network.fetch(MonikConfig.STEAM_FEATURED_API, is_json=True)
        return [{"id": str(g['id']), "name": g['name'], "img": g['large_capsule_image']} for g in raw.get('featured_win', [])] if raw else []

    def search_steam_database(self, query: str) -> List[Dict[str, Any]]:
        safe_query = urllib.parse.quote(query)
        url = MonikConfig.STEAM_SEARCH_API.format(query=safe_query)
        raw = self.network.fetch(url, is_json=True)
        return [{"id": str(i['id']), "name": i['name'], "img": f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{i['id']}/header.jpg"} for i in raw.get('items', [])] if raw else []

    def get_library(self) -> List[Dict[str, Any]]: 
        return self.vault.data.get("games", [])

    def get_bypass_catalog(self) -> Dict[str, Any]:
        """Arayüz için yeni 55 Oyunluk Bypass Kataloğunu hazırlar."""
        catalog_data = []
        for appid, name in MonikConfig.SUPPORTED_GAMES.items():
            catalog_data.append({
                "appid": appid, 
                "name": name, 
                "type": "Bypass", 
                "category": "1 Kredi"
            })
        return {"status": "success", "data": catalog_data}

    def run_auto_injection(self, app_id: str, name: str, img: str) -> Dict[str, Any]:
        """Steam Manifest İndirme ve Enjeksiyon (Kredi Harcar). Steam artık kapanmıyor."""
        MonikLogger.info(f"Oyun Ekleme İsteği: {name} (AppID: {app_id})")
        
        if self.vault.data["credits"] <= 0:
            return {"status": "error", "msg": "Krediniz tükenmiştir. Lütfen Shopier üzerinden lisans kodu satın alın."}

        url = MonikConfig.MANIFEST_SOURCE.format(app_id=app_id)
        zip_bytes = self.network.fetch(url, timeout=40)
        if not zip_bytes: 
            return {"status": "error", "msg": "Oyun sunucuda bulunamadı."}

        # DİKKAT: Steam restart özelliği iptal edildi. Kullanıcıya zaman kazandırıyoruz.
        success, msg = self.steam.deploy_zip_payload(zip_bytes, app_id)
        
        if success:
            if self.vault.data["settings"].get("create_acf", True): 
                self.steam.write_app_manifest(app_id, name)
            
            self.steam.clear_app_cache()
            
            self.vault.data["games"].append({
                "id": app_id, 
                "name": name, 
                "img": img, 
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            self.vault.consume_credit() # Krediyi düş ve kaydet
            
            return {"status": "success", "msg": f"{name} sisteme işlendi. (1 Kredi düşüldü)", "credits": self.vault.data["credits"]}
            
        return {"status": "error", "msg": msg}

    def run_manual_import(self, app_id: str, name: str) -> Dict[str, Any]:
        """Yerel ZIP ile Manuel İndirme (Kredi Harcar). Steam artık kapanmıyor."""
        if not app_id or not name: 
            return {"status": "error", "msg": "Lütfen gerekli oyun bilgilerini doldurun."}
        
        if self.vault.data["credits"] <= 0:
            return {"status": "error", "msg": "Krediniz tükenmiştir. İşlem yapılamıyor."}

        dialog = webview.windows[0].create_file_dialog(webview.OPEN_DIALOG, file_types=('ZIP Arşivleri (*.zip)',))
        if not dialog: 
            return {"status": "error", "msg": "Herhangi bir ZIP dosyası seçilmedi."}

        try:
            with open(dialog[0], 'rb') as f: 
                zip_bytes = f.read()
                
            # DİKKAT: Steam restart özelliği iptal edildi.
            success, msg = self.steam.deploy_zip_payload(zip_bytes, app_id)
            
            if success:
                if self.vault.data["settings"].get("create_acf", True): 
                    self.steam.write_app_manifest(app_id, name)
                
                self.steam.clear_app_cache()
                
                self.vault.data["games"].append({
                    "id": app_id, 
                    "name": name, 
                    "img": "https://via.placeholder.com/460x215/1c1c1e/ffffff?text=MANUAL", 
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                self.vault.consume_credit()
                
                return {"status": "success", "msg": "Yerel ZIP arşivi sisteme işlendi. (1 Kredi düşüldü)", "credits": self.vault.data["credits"]}
                
            return {"status": "error", "msg": msg}
        except Exception as e: 
            return {"status": "error", "msg": f"ZIP Okuma Hatası: {str(e)}"}

    def check_bypass_status(self, app_id: str) -> Dict[str, Any]:
        """Bir klasörde Bypass yüklü olup olmadığını denetler."""
        try: appid_int = int(app_id)
        except: return {"status": "error", "msg": "Uygulama ID'si geçersiz."}

        dialog = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        if not dialog: return {"status": "warning", "msg": "Dizin seçimi iptal edildi."}
        
        target_dir = dialog[0]
        installed = self.bypass_engine.check_status(appid_int, target_dir)
        
        return {
            "status": "success", 
            "installed": installed, 
            "msg": "Uyumlu Bypass Mevcut" if installed else "Bypass Henüz Yüklenmemiş",
            "path": target_dir
        }

    def apply_targeted_bypass(self, app_id: str) -> Dict[str, Any]:
        """
        Yeni Bypass sistemini tetikler. 
        DİKKAT: Yeni kurala göre bu işlem artık 1 KREDİ bedelindedir.
        """
        try: appid_int = int(app_id)
        except: return {"status": "error", "msg": "Uygulama ID'si geçersiz."}

        if self.vault.data["credits"] <= 0:
            return {"status": "error", "msg": "Krediniz tükenmiştir. Bypass işlemi 1 Kredi gerektirir."}

        dialog = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        if not dialog: return {"status": "warning", "msg": "Oyun dizini seçilmedi."}
        
        target_dir = dialog[0]
        res = self.bypass_engine.apply_bypass(appid_int, target_dir)
        
        if res.get("status") == "success":
            self.vault.consume_credit() # Krediyi tahsil et
            return {"status": "success", "msg": res.get("msg") + " (1 Kredi Düşüldü)", "credits": self.vault.data["credits"]}
            
        return {"status": "error", "msg": res.get("msg")}

    def remove_targeted_bypass(self, app_id: str, path: str) -> Dict[str, Any]:
        """Uygulanmış bypass'ı silip oyunu orijinal ayarlarına döndürür."""
        try: appid_int = int(app_id)
        except: return {"status": "error", "msg": "Uygulama ID'si geçersiz."}
            
        res = self.bypass_engine.restore_original_files(appid_int, path)
        if res.get("status") == "success":
            return {"status": "success", "msg": res.get("msg")}
        return {"status": "error", "msg": res.get("msg")}


# ====================================================================================================
# [11] MODERN VE ULTRA PROFESYONEL FRONTEND (UI_HTML) - DARK PREMIUM TEMASI (LOG EKRANI KALDIRILDI)
# ====================================================================================================

UI_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MonikDepot Enterprise v4.1.5</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        /* CSS Değişkenleri ve Reset */
        :root {
            --bg-deep: #050507;
            --bg-surface: #0f0f13;
            --bg-card: #15151a;
            --bg-hover: #1e1e24;
            --border-color: #22222a;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --accent: #a855f7;
            --text-pure: #ffffff;
            --text-main: #e4e4e7;
            --text-muted: #71717a;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --gold: #facc15;
            --transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; user-select: none; }
        body { background-color: var(--bg-deep); color: var(--text-main); display: flex; height: 100vh; overflow: hidden; }

        /* Kaydırma Çubuğu Optimizasyonu */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

        /* Sol Navigasyon (Sidebar) */
        .sidebar { width: 280px; background-color: var(--bg-surface); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; padding: 25px 20px; z-index: 10; }
        .logo-area { display: flex; align-items: center; gap: 12px; margin-bottom: 40px; padding-left: 10px; }
        .logo-icon { width: 32px; height: 32px; background: linear-gradient(135deg, var(--primary), var(--accent)); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
        .logo-text { font-size: 20px; font-weight: 700; letter-spacing: 0.5px; color: var(--text-pure); }
        .logo-text span { color: var(--primary); }
        
        .nav-menu { display: flex; flex-direction: column; gap: 6px; }
        .nav-item { display: flex; align-items: center; padding: 14px 16px; color: var(--text-muted); text-decoration: none; border-radius: 10px; cursor: pointer; font-size: 14px; font-weight: 500; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
        .nav-item:hover { background-color: rgba(255, 255, 255, 0.03); color: var(--text-pure); }
        .nav-item.active { background-color: rgba(59, 130, 246, 0.1); color: var(--primary); border: 1px solid rgba(59, 130, 246, 0.2); }
        
        .sidebar-footer { margin-top: auto; padding: 15px 10px 0 10px; border-top: 1px solid var(--border-color); font-size: 11px; color: var(--text-muted); display: flex; flex-direction: column; gap: 4px; }

        /* Kredi ve Cüzdan Görünümü */
        .wallet-widget { background: linear-gradient(135deg, rgba(250, 204, 21, 0.1), transparent); border: 1px solid rgba(250, 204, 21, 0.3); border-radius: 12px; padding: 15px; margin-bottom: 20px; cursor: pointer; transition: var(--transition); display: flex; align-items: center; justify-content: space-between; }
        .wallet-widget:hover { border-color: var(--gold); box-shadow: 0 0 15px rgba(250, 204, 21, 0.2); transform: translateY(-2px); }
        .wallet-info { display: flex; flex-direction: column; }
        .wallet-lbl { font-size: 11px; color: var(--text-muted); text-transform: uppercase; font-weight: 600; margin-bottom: 2px; }
        .wallet-val { font-size: 18px; font-weight: 800; color: var(--gold); }
        .wallet-icon { font-size: 24px; }

        .user-widget { background-color: var(--bg-deep); border: 1px solid var(--border-color); border-radius: 12px; padding: 12px; display: flex; align-items: center; gap: 12px; }
        .user-avatar { width: 34px; height: 34px; background: linear-gradient(135deg, var(--primary), var(--accent)); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 14px; color: white; }

        /* Ana İçerik ve Çalışma Alanı */
        .main-panel { flex: 1; display: flex; flex-direction: column; height: 100%; position: relative; }
        .top-bar { height: 70px; background-color: var(--bg-surface); border-bottom: 1px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; padding: 0 40px; }
        .top-title { font-size: 16px; font-weight: 600; color: var(--text-pure); }
        
        .search-wrapper { display: flex; position: relative; width: 350px; }
        .search-input { width: 100%; background-color: var(--bg-deep); border: 1px solid var(--border-color); border-radius: 10px; padding: 12px 16px; color: var(--text-pure); font-size: 13px; transition: var(--transition); }
        .search-input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); outline: none;}

        .content-container { flex: 1; padding: 40px; overflow-y: auto; display: none; animation: slideUp 0.3s ease-out forwards; }
        .content-container.active { display: block; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }

        /* Oyun Kartları */
        .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 24px; }
        .game-card { background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 15px; transition: var(--transition); display: flex; flex-direction: column; }
        .game-card:hover { transform: translateY(-5px); border-color: var(--primary); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        .game-card img { width: 100%; aspect-ratio: 16/9; object-fit: cover; border-radius: 10px; margin-bottom: 15px; background-color: #27272a; }
        .game-card h4 { font-size: 14px; font-weight: 700; color: var(--text-pure); margin-bottom: 15px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        /* Düğmeler ve İnteraktifler */
        .btn { background-color: var(--primary); color: white; border: none; border-radius: 10px; padding: 12px 20px; font-size: 13px; font-weight: 600; cursor: pointer; transition: var(--transition); display: inline-flex; align-items: center; justify-content: center; width: 100%; }
        .btn:hover { background-color: var(--primary-hover); transform: translateY(-1px); }
        .btn:active { transform: translateY(1px); }
        .btn-ghost { background-color: transparent; border: 1px solid var(--border-color); color: var(--text-main); }
        .btn-ghost:hover { background-color: var(--bg-hover); color: white; border-color: var(--text-muted); }
        .btn-gold { background: linear-gradient(90deg, #ca8a04, #eab308); color: #422006; font-weight: 800; border: none; box-shadow: 0 4px 15px rgba(234, 179, 8, 0.3); }
        .btn-gold:hover { filter: brightness(1.1); }

        /* Ayar Panelleri */
        .panel-card { background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 25px; max-width: 700px; }
        .panel-card h3 { font-size: 18px; font-weight: 700; color: var(--text-pure); margin-bottom: 20px; }
        .form-row { margin-bottom: 16px; display: flex; flex-direction: column; gap: 8px;}
        .form-label { display: block; font-size: 12px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; }
        
        .switch-container { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-top: 1px solid var(--border-color); }
        .toggle-switch { position: relative; display: inline-block; width: 46px; height: 24px; }
        .toggle-switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; inset: 0; background-color: var(--bg-deep); border: 1px solid var(--border-color); border-radius: 24px; transition: 0.3s; }
        .slider:before { position: absolute; content: ""; height: 16px; width: 16px; left: 3px; bottom: 3px; background-color: var(--text-muted); border-radius: 50%; transition: 0.3s; }
        input:checked + .slider { background-color: var(--primary); border-color: var(--primary); }
        input:checked + .slider:before { transform: translateX(22px); background-color: white; }

        /* Modal ve Yükleme Ekranları (Loader) */
        .overlay-bg { position: fixed; inset: 0; background-color: rgba(5, 5, 7, 0.95); backdrop-filter: blur(10px); z-index: 9000; display: none; align-items: center; justify-content: center; flex-direction: column; }
        .modal-box { background-color: var(--bg-surface); border: 1px solid var(--border-color); padding: 40px; border-radius: 24px; width: 100%; max-width: 500px; text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.6); }
        
        .spinner { width: 50px; height: 50px; border: 3px solid var(--border-color); border-top-color: var(--primary); border-radius: 50%; animation: spin 0.8s linear infinite; }
        @keyframes spin { 100% { transform: rotate(360deg); } }

        /* Dinamik Toast Bildirimleri */
        #toast-zone { position: fixed; bottom: 30px; right: 30px; z-index: 9999; display: flex; flex-direction: column; gap: 12px; }
        .toast { background-color: var(--bg-card); border: 1px solid var(--border-color); border-left: 4px solid var(--primary); padding: 16px 20px; border-radius: 12px; color: var(--text-pure); font-size: 13px; font-weight: 500; box-shadow: 0 10px 25px rgba(0,0,0,0.4); display: flex; align-items: center; gap: 10px; transform: translateX(120%); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
    </style>
</head>
<body>

    <div id="loader-screen" class="overlay-bg" style="z-index: 10000;">
        <div class="spinner"></div>
        <p id="loader-message" style="margin-top: 25px; font-size: 14px; font-weight: 600; color: var(--text-muted);">Sistem Protokolleri Başlatılıyor...</p>
    </div>

    <div id="setup-screen" class="overlay-bg">
        <div class="modal-box">
            <div class="logo-area" style="justify-content: center; margin-bottom: 20px;">
                <div class="logo-icon" style="width: 40px; height: 40px; font-size: 20px;">M</div>
                <div class="logo-text" style="font-size: 28px;">MONIK<span>DEPOT</span></div>
            </div>
            <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 35px;">Bağlantı kurmak için bir yönetici profili tanımlayın.</p>
            <div class="form-row">
                <input type="text" id="setup-username" class="search-input" placeholder="Profil İsminiz" style="text-align: center; font-weight: 600; font-size: 16px;" autocomplete="off">
            </div>
            <button class="btn" style="padding: 15px; font-size: 14px;" onclick="finalizeSetup()">Sistemi Başlat</button>
        </div>
    </div>

    <div id="shop-screen" class="overlay-bg">
        <div class="modal-box">
            <h2 style="color: var(--gold); margin-bottom: 15px; font-size: 24px;">Kredi Cüzdanı</h2>
            <p style="color: var(--text-muted); font-size: 13px; margin-bottom: 30px; line-height: 1.5;">Oyun eklemeye veya Bypass yapmaya devam etmek için kredi satın alın ve size verilen 16 haneli lisans kodunu aşağıya girin.</p>
            
            <button class="btn btn-gold" style="margin-bottom: 30px; padding: 15px;" onclick="pywebview.api.open_shopier_link()">🛒 Shopier'den Kredi Satın Al</button>
            
            <div style="border-top: 1px solid var(--border-color); padding-top: 30px;">
                <label class="form-label" style="text-align: left;">Lisans Kodunuzu Girin</label>
                <input type="text" id="shop-code-input" class="search-input" placeholder="Örn: 5CRD-A1B2-C3D4-E5F6" style="text-align: center; text-transform: uppercase; letter-spacing: 2px; font-weight: bold;">
                <button class="btn" style="margin-top: 15px;" onclick="redeemShopierCode()">Kodu Doğrula ve Yükle</button>
            </div>
            
            <button class="btn btn-ghost" style="margin-top: 15px;" onclick="document.getElementById('shop-screen').style.display='none'">Pencereyi Kapat</button>
        </div>
    </div>

    <div id="toast-zone"></div>

    <aside class="sidebar">
        <div class="logo-area">
            <div class="logo-icon">M</div>
            <div class="logo-text">MONIK<span>DEPOT</span></div>
        </div>
        
        <nav class="nav-menu">
            <div class="nav-item active" data-view="explore" onclick="switchView(this)">Oyunları Keşfet</div>
            <div class="nav-item" data-view="library" onclick="switchView(this)">Steam Kütüphanem</div>
            <div class="nav-item" data-view="manual" onclick="switchView(this)">Manuel ZIP Aktarım</div>
            <div class="nav-item" data-view="bypass" onclick="switchView(this)">Bypass</div>
            <div class="nav-item" data-view="settings" onclick="switchView(this)">Sistem Ayarları</div>
        </nav>

        <div class="wallet-widget" onclick="document.getElementById('shop-screen').style.display='flex'">
            <div class="wallet-info">
                <span class="wallet-lbl">Mevcut Bakiye</span>
                <span class="wallet-val" id="ui-credits">0 Kredi</span>
            </div>
            <div class="wallet-icon">💎</div>
        </div>

        <div class="user-widget">
            <div class="user-avatar" id="ui-avatar">U</div>
            <div style="display:flex; flex-direction:column; overflow:hidden;">
                <div id="ui-username" style="font-size:13px; font-weight:bold; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">User</div>
                <div style="font-size:11px; color:var(--text-muted);">MTA Development</div>
            </div>
        </div>

        <div class="sidebar-footer">
            <div>Sürüm: v4.1.5</div>
            <div>MTA Development &copy; 2026</div>
        </div>
    </aside>

    <main class="main-panel">
        <header class="top-bar">
            <div class="top-title" id="active-title">Keşfet Modülü</div>
            <div class="search-wrapper">
                <input type="text" id="steam-search" class="search-input" placeholder="Steam Veritabanında ara..." onkeydown="if(event.key==='Enter') executeSearch()">
            </div>
        </header>

        <div class="content-container active" id="view-explore">
            <div class="card-grid" id="grid-explore"></div>
        </div>

        <div class="content-container" id="view-library">
            <div class="card-grid" id="grid-library"></div>
        </div>

        <div class="content-container" id="view-manual">
            <div class="panel-card">
                <h3>Yerel ZIP Enjeksiyonu</h3>
                <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 25px;">Sunucuda bulunmayan oyunları, elinizdeki yerel .ZIP dosyaları üzerinden kütüphanenize entegre edebilirsiniz. Bu işlem 1 Kredi harcar.</p>
                
                <div class="form-row">
                    <label class="form-label">Steam AppID (Zorunlu)</label>
                    <input type="text" id="manual-id" class="search-input" placeholder="Örn: 1091500">
                </div>
                <div class="form-row">
                    <label class="form-label">Oyun Tam Adı (Zorunlu)</label>
                    <input type="text" id="manual-name" class="search-input" placeholder="Örn: Cyberpunk 2077">
                </div>
                
                <button class="btn" style="margin-top: 10px;" onclick="triggerManualImport()">ZIP Arşivi Seç ve Başlat</button>
            </div>
        </div>

        <div class="content-container" id="view-bypass">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
                <div>
                    <h2 style="font-size: 22px; margin-bottom: 5px;">Bypass</h2>
                    <p style="font-size: 13px; color: var(--text-muted);">Sunucularımız üzerinden sadece seçili oyuna özel bypass dosyasını indirir. Bu işlemler <strong>1 Krediye maal olur</strong>.</p>
                </div>
            </div>
            
            <div class="panel-card" style="max-width: 100%; margin-bottom: 25px;">
                <div class="form-row" style="display: flex; gap: 15px; align-items: flex-end; flex-direction:row;">
                    <div style="flex: 1;">
                        <label class="form-label">Durum Kontrolü İçin Hedef AppID</label>
                        <input type="text" id="bypass-appid-check" class="search-input" placeholder="Desteklenen bir AppID girin">
                    </div>
                    <button class="btn btn-ghost" style="width: auto; height: 42px;" onclick="checkBypassStatus()">Durum Sorgula</button>
                </div>
                
                <div id="bypass-status-area" style="margin-top: 15px; padding: 15px; background: var(--bg-deep); border: 1px dashed var(--border-color); border-radius: 10px; font-size: 13px; display: none;">
                    <span id="bypass-status-text" style="font-weight: bold;">Durum: Bekleniyor</span><br>
                    <span id="bypass-path-text" style="color: var(--text-muted); font-size: 11px;"></span>
                    <div style="margin-top:10px;">
                        <button class="btn" style="background: var(--danger); padding: 8px 12px; font-size: 11px; width:auto;" onclick="removeTargetedBypass()">Bypass'ı Kaldır (Orijinale Dön)</button>
                    </div>
                </div>
            </div>
            
            <div class="card-grid" id="grid-bypass"></div>
        </div>

        <div class="content-container" id="view-settings">
            <div class="panel-card">
                <h3>Profil Konfigürasyonu</h3>
                <div class="form-row" style="display: flex; gap: 15px; flex-direction:row;">
                    <input type="text" id="setting-username" class="search-input" style="flex: 1;">
                    <button class="btn" style="width: 140px;" onclick="saveProfileName()">Kaydet</button>
                </div>
            </div>

            <div class="panel-card">
                <h3>Sistem Tercihleri</h3>
                <div class="switch-container">
                    <div>
                        <div style="font-size: 14px; font-weight: 600;">AppManifest (.acf) Entegrasyonu</div>
                        <div style="font-size: 12px; color: var(--text-muted); margin-top: 4px;">Dağıtım sırasında Steam'in oyunu algılaması için sahte manifest oluşturur.</div>
                    </div>
                    <label class="toggle-switch">
                        <input type="checkbox" id="setting-acf-toggle" onchange="modifySetting('create_acf', this.checked)">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
        </div>
    </main>

    <script>
        let currentBypassPath = '';

        // --- İLK YÜKLEME ---
        window.addEventListener('pywebviewready', async () => {
            const state = await pywebview.api.get_initial_state();
            
            if (state.first_boot || state.user_name === "Misafir" || !state.user_name) {
                document.getElementById('setup-screen').style.display = 'flex';
                document.getElementById('setup-username').focus();
            } else {
                syncUIWithState(state);
                loadStoreGrid();
            }
        });

        // --- UI GÜNCELLEME VE SENKRONİZASYON ---
        function syncUIWithState(state) {
            const name = state.user_name || "Misafir";
            document.getElementById('ui-username').innerText = name;
            document.getElementById('ui-avatar').innerText = name.charAt(0).toUpperCase();
            document.getElementById('setting-username').value = name;
            
            // Cüzdan Bakiyesi
            document.getElementById('ui-credits').innerText = (state.credits || 0) + " Kredi";
            
            if(state.settings) {
                document.getElementById('setting-acf-toggle').checked = state.settings.create_acf;
            }
        }

        // --- PROFİL VE AYAR YÖNETİMİ ---
        async function finalizeSetup() {
            const name = document.getElementById('setup-username').value;
            if(!name.trim()) return showToast("Lütfen profil ismini boş bırakmayın.", "warning");
            
            const success = await pywebview.api.update_user_name(name);
            if (success) {
                document.getElementById('setup-screen').style.display = 'none';
                syncUIWithState(await pywebview.api.get_initial_state());
                loadStoreGrid();
                showToast("Sisteme giriş yapıldı.", "success");
            }
        }

        async function saveProfileName() {
            const name = document.getElementById('setting-username').value;
            if(name.trim()) {
                await pywebview.api.update_user_name(name);
                syncUIWithState(await pywebview.api.get_initial_state());
                showToast("Kullanıcı adı güncellendi.", "success");
            }
        }

        async function modifySetting(key, value) {
            await pywebview.api.update_setting(key, value);
            showToast("Ayarlar kaydedildi.", "success");
        }

        // --- KREDİ VE SHOPIER MODÜLÜ ---
        async function redeemShopierCode() {
            const code = document.getElementById('shop-code-input').value;
            if(!code) return showToast("Lütfen kodu girin.", "warning");
            
            setLoader(true, "Shopier lisansı doğrulanıyor...");
            const res = await pywebview.api.redeem_shopier_code(code);
            setLoader(false);
            
            showToast(res.msg, res.status);
            if(res.status === 'success') {
                document.getElementById('shop-code-input').value = '';
                document.getElementById('shop-screen').style.display = 'none';
                document.getElementById('ui-credits').innerText = res.credits + " Kredi";
            }
        }

        // --- MENÜ VE SEKME YÖNETİMİ ---
        function switchView(element) {
            const targetView = element.getAttribute('data-view');
            
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            element.classList.add('active');
            
            document.querySelectorAll('.content-container').forEach(v => v.classList.remove('active'));
            document.getElementById('view-' + targetView).classList.add('active');
            
            const titles = { explore: "Keşfet Modülü", library: "Steam Kütüphanem", manual: "Manuel ZIP Aktarım", bypass: "Bypass Motoru", settings: "Sistem Ayarları" };
            document.getElementById('active-title').innerText = titles[targetView];
            
            document.querySelector('.search-wrapper').style.visibility = targetView === 'explore' ? 'visible' : 'hidden';
            
            if (targetView === 'library') loadLibraryGrid();
            if (targetView === 'bypass') loadBypassCatalog();
        }

        // --- VERİ ÇEKME VE KART (GRID) SİSTEMLERİ ---
        async function loadStoreGrid() {
            setLoader(true, "Veritabanı senkronize ediliyor...");
            const games = await pywebview.api.fetch_featured_games();
            renderCardGrid('grid-explore', games, 'store');
            setLoader(false);
        }

        async function executeSearch() {
            const query = document.getElementById('steam-search').value;
            if (!query) return loadStoreGrid();
            
            setLoader(true, "Steam API sorgulanıyor...");
            const results = await pywebview.api.search_steam_database(query);
            renderCardGrid('grid-explore', results, 'store');
            setLoader(false);
        }

        async function loadLibraryGrid() {
            const games = await pywebview.api.get_library();
            renderCardGrid('grid-library', games, 'library');
        }

        async function loadBypassCatalog() {
            setLoader(true, "55 Oyunluk Bypass Kataloğu yükleniyor...");
            const res = await pywebview.api.get_bypass_catalog();
            if(res.status === 'success') {
                renderCardGrid('grid-bypass', res.data, 'bypass');
            } else {
                document.getElementById('grid-bypass').innerHTML = `<div style="color:var(--danger);">${res.msg}</div>`;
            }
            setLoader(false);
        }

        function renderCardGrid(containerId, itemsArray, type) {
            const container = document.getElementById(containerId);
            
            if (!itemsArray || itemsArray.length === 0) {
                container.innerHTML = `<div style="color:var(--text-muted); padding:20px; font-weight:500;">Gösterilecek öğe bulunamadı.</div>`;
                return;
            }
            
            container.innerHTML = itemsArray.map(item => {
                let actionHtml = '';
                
                if(type === 'store') {
                    actionHtml = `<button class="btn" onclick="triggerAutoInject('${item.id}', '${item.name.replace(/'/g, "")}', '${item.img}')">Kütüphaneye Ekle (1 Kredi)</button>`;
                } 
                else if(type === 'bypass') {
                    let appId = item.appid || item.id;
                    actionHtml = `<button class="btn" style="background:var(--accent);" onclick="triggerTargetedBypass('${appId}')">Bypass Uygula (1 Kredi)</button>`;
                } 
                else {
                    actionHtml = `<div style="font-size: 11px; font-weight: 700; color: var(--text-muted); margin-top: auto;">EKLENDİ: <span style="color: var(--success);">${item.timestamp}</span></div>`;
                }
                
                let imgSrc = item.img || `https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/${item.appid || item.id}/header.jpg`;
                
                return `
                <div class="game-card">
                    <img src="${imgSrc}" onerror="this.src='https://via.placeholder.com/460x215/1c1c1e/52525b?text=KAPAK+YOK'">
                    <h4 title="${item.name}">${item.name}</h4>
                    ${actionHtml}
                </div>
                `;
            }).join('');
        }

        // --- ENJEKSİYON EYLEMLERİ ---
        async function triggerAutoInject(id, name, img) {
            setLoader(true, `${name} kütüphaneye ekleniyor...`);
            const response = await pywebview.api.run_auto_injection(id, name, img);
            setLoader(false);
            
            showToast(response.msg, response.status);
            if(response.status === 'success' && response.credits !== undefined) {
                document.getElementById('ui-credits').innerText = response.credits + " Kredi";
            }
        }

        async function triggerManualImport() {
            const id = document.getElementById('manual-id').value;
            const name = document.getElementById('manual-name').value;
            
            if(!id || !name) return showToast("Lütfen zorunlu alanları doldurun.", "error");
            
            setLoader(true, "Dosya sistemi bekleniyor...");
            const response = await pywebview.api.run_manual_import(id, name);
            setLoader(false);
            
            if(response.status === 'success') {
                document.getElementById('manual-id').value = '';
                document.getElementById('manual-name').value = '';
                if(response.credits !== undefined) {
                    document.getElementById('ui-credits').innerText = response.credits + " Kredi";
                }
            }
            showToast(response.msg, response.status);
        }

        // --- YENİ TARGETED BYPASS MANTIĞI ---
        async function checkBypassStatus() {
            const id = document.getElementById('bypass-appid-check').value;
            if(!id) return showToast("Durum kontrolü için AppID girmelisiniz.", "warning");
            
            setLoader(true, "Oyun Klasörü Seçiniz...");
            const res = await pywebview.api.check_bypass_status(id);
            setLoader(false);
            
            if(res.status === "success") {
                currentBypassPath = res.path;
                document.getElementById('bypass-status-area').style.display = 'block';
                const stText = document.getElementById('bypass-status-text');
                stText.innerText = "Durum: " + res.msg;
                stText.style.color = res.installed ? "var(--success)" : "var(--warning)";
                document.getElementById('bypass-path-text').innerText = "Seçili Dizin: " + currentBypassPath;
            } else {
                showToast(res.msg, res.status);
            }
        }

        async function triggerTargetedBypass(id) {
            setLoader(true, "Uygulanacak oyun klasörünü seçiniz...");
            const response = await pywebview.api.apply_targeted_bypass(id);
            setLoader(false);
            
            showToast(response.msg, response.status);
            if(response.status === 'success' && response.credits !== undefined) {
                document.getElementById('ui-credits').innerText = response.credits + " Kredi";
            }
        }

        async function removeTargetedBypass() {
            const id = document.getElementById('bypass-appid-check').value;
            if(!id || !currentBypassPath) return showToast("Lütfen geçerli bir oyun seçin.", "error");
            
            setLoader(true, "Orijinal dosyalar geri yükleniyor...");
            const res = await pywebview.api.remove_targeted_bypass(id, currentBypassPath);
            setLoader(false);
            
            showToast(res.msg, res.status);
            if(res.status === 'success') {
                const stText = document.getElementById('bypass-status-text');
                stText.innerText = "Durum: Bypass YÜKLÜ DEĞİL";
                stText.style.color = "var(--warning)";
            }
        }

        // --- UI ANİMASYON VE YARDIMCILAR (HELPERS) ---
        function setLoader(show, textMessage) {
            document.getElementById('loader-screen').style.display = show ? 'flex' : 'none';
            if(textMessage) document.getElementById('loader-message').innerText = textMessage;
        }

        function showToast(message, type = 'info') {
            const zone = document.getElementById('toast-zone');
            const toast = document.createElement('div');
            toast.className = 'toast';
            
            let borderColor = "var(--primary)";
            if(type === 'success') borderColor = "var(--success)";
            if(type === 'error') borderColor = "var(--danger)";
            if(type === 'warning') borderColor = "var(--warning)";
            
            toast.style.borderLeftColor = borderColor;
            toast.innerHTML = `<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background-color:${borderColor};"></span> ${message}`;
            
            zone.appendChild(toast);
            setTimeout(() => { toast.style.transform = 'translateX(0)'; }, 10);
            
            setTimeout(() => {
                toast.style.transform = 'translateX(120%)';
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }
    </script>
</body>
</html>
"""

# ====================================================================================================
# [12] UYGULAMA BAŞLATICI VE FATAL HANDLER (BOOTSTRAPPER)
# ====================================================================================================

if __name__ == "__main__":
    # 1. Konsol Renk Kodlarını Aktifleştir
    os.system('color')
    
    # 2. Arka Plan Güvenli Log Sistemi
    MonikLogger.initialize()
    
    # 3. Yönetici Hakları (UAC) Kontrolü (Güvenlik Önlemi)
    # Bu blok sayesinde script'in devamındaki tüm dosya indirme 
    # ve yazma işlemleri otomatik olarak YÖNETİCİ yetkisiyle gerçekleşir.
    if not is_admin():
        MonikLogger.warn("Uygulama kısıtlı haklarla başlatıldı. UAC Yönetici izni ekranı çağrılıyor...")
        if not elevate_privileges():
            MonikLogger.error("Yönetici izni olmadan Bypass sistemleri ve Steam registry okunamaz. Sistem kapatılıyor.")
            sys.exit(1)
            
    # Eğer buraya geldiyse sistem %100 Administrator haklarına sahiptir.
    try:
        # 4. Ana Engine Objelerini ve Ağ Bağlantılarını Hazırla
        core_engine = MonikEngine()
        
        # 5. UI (WebView) Penceresini Konfigüre Et
        MonikLogger.info("MTA Development arayüz modülleri PyWebView üzerinden ayağa kaldırılıyor...")
        main_window = webview.create_window(
            title=f"{MonikConfig.APP_NAME} v{MonikConfig.VERSION}  {MonikConfig.BUILD_TAG}",
            html=UI_HTML,
            js_api=core_engine,
            width=1400,
            height=900,
            background_color='#050507',
            min_size=(1100, 700)
        )
        
        # 6. Bloklayıcı Döngüyü Başlat
        MonikLogger.success("Tüm sistemler kararlı durumda. UI ekranı aktif edildi.")
        webview.start(debug=False)
        
    except Exception as fatal_error:
        # 7. Görünmez çökmeleri (Silent Crashing) önleyen Fatal Handler
        error_trace = traceback.format_exc()
        MonikLogger.error(f"SİSTEM ÇÖKTÜ (FATAL ERROR):\n{error_trace}")
        
        # Hata Raporunu Diske Yazdır
        crash_report_path = MonikConfig.BASE_DIR / "crash_report.txt"
        try:
            crash_report_path.write_text(f"MonikDepot Crash Report\nDate: {datetime.now()}\n\n{error_trace}", encoding="utf-8")
        except:
            pass
            
        print(f"\n[SİSTEM ÇÖKTÜ] Beklenmeyen bir hata oluştu:\n{fatal_error}")
        print(error_trace)
        input("Çıkmak için ENTER tuşuna basın...")
    finally:
        # 8. Kapanışta Geçici Dosya (Temp) Temizliği
        DependencyManager.clean_temp_files()
        MonikLogger.info("=== MonikDepot Oturumu Güvenle Kapatıldı ===")