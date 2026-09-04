UI_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MonikDepot v3.3.1 UI</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #9333ea; --primary-hover: #a855f7; --bg-base: #0f172a; --glass-bg: rgba(30, 41, 59, 0.4); --glass-border: rgba(168, 85, 247, 0.2); --text-main: #f8fafc; --text-muted: #cbd5e1; --danger: #ef4444; --success: #22c55e; --warning: #f59e0b; }
        [data-theme="light"] { --bg-base: #f1f5f9; --glass-bg: rgba(255, 255, 255, 0.6); --glass-border: rgba(147, 51, 234, 0.4); --text-main: #0f172a; --text-muted: #475569; }
        * { box-sizing: border-box; font-family: 'Outfit', sans-serif; margin: 0; padding: 0; user-select: none; }
        body { background: radial-gradient(circle at top right, #3b0764 0%, var(--bg-base) 60%); color: var(--text-main); height: 100vh; overflow: hidden; display: flex; flex-direction: column; transition: background 0.3s ease; }
        [data-theme="light"] body { background: radial-gradient(circle at top right, #e9d5ff 0%, var(--bg-base) 60%); }
        ::-webkit-scrollbar { width: 8px; } ::-webkit-scrollbar-track { background: transparent; } ::-webkit-scrollbar-thumb { background: rgba(168, 85, 247, 0.3); border-radius: 4px; } ::-webkit-scrollbar-thumb:hover { background: var(--primary); }
        header { display: flex; justify-content: space-between; align-items: center; padding: 20px 40px; background: var(--glass-bg); backdrop-filter: blur(16px); border-bottom: 1px solid var(--glass-border); z-index: 50; position: relative; }
        .greeting { font-size: 26px; font-weight: 800; letter-spacing: -0.5px; } .greeting span { color: #c084fc; text-shadow: 0 0 10px rgba(168, 85, 247, 0.5); } [data-theme="light"] .greeting span { color: var(--primary); text-shadow: none; }
        .menu-trigger { display: flex; flex-direction: column; gap: 5px; cursor: pointer; padding: 10px; border-radius: 8px; transition: 0.3s; } .menu-trigger:hover { background: rgba(147, 51, 234, 0.1); } .menu-trigger div { width: 30px; height: 3px; background: var(--text-main); border-radius: 2px; transition: 0.3s; }
        #sidebar-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.6); backdrop-filter: blur(5px); z-index: 99; opacity: 0; pointer-events: none; transition: 0.4s ease; } #sidebar-overlay.active { opacity: 1; pointer-events: all; }
        #sidebar { position: fixed; top: 0; right: -380px; width: 350px; height: 100vh; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(20px); border-left: 1px solid var(--glass-border); z-index: 100; transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1); display: flex; flex-direction: column; padding: 30px 0; box-shadow: -10px 0 40px rgba(0,0,0,0.5); overflow-y: auto;}
        [data-theme="light"] #sidebar { background: rgba(248, 250, 252, 0.85); } #sidebar.open { right: 0; }
        .sidebar-header { padding: 0 30px 30px 30px; border-bottom: 1px solid var(--glass-border); display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; } .sidebar-header h2 { font-weight: 800; font-size: 24px; color: var(--primary); } .close-btn { font-size: 32px; cursor: pointer; color: var(--text-muted); line-height: 1; } .close-btn:hover { color: var(--danger); }
        .menu-list { display: flex; flex-direction: column; gap: 5px; padding: 0 20px; } .menu-item { padding: 16px 20px; border-radius: 12px; cursor: pointer; font-size: 16px; font-weight: 600; color: var(--text-muted); transition: 0.2s; display: flex; align-items: center; gap: 15px; } .menu-item:hover { background: rgba(147, 51, 234, 0.1); color: var(--text-main); transform: translateX(5px); } .menu-item.active { background: var(--primary); color: white; box-shadow: 0 4px 15px rgba(147, 51, 234, 0.4); }
        main { flex: 1; position: relative; overflow: hidden; display: flex; flex-direction: column; }
        .search-container { padding: 20px 40px; background: transparent; z-index: 10; } .search-input { width: 100%; max-width: 600px; background: var(--glass-bg); border: 1px solid var(--glass-border); padding: 16px 25px; border-radius: 20px; color: var(--text-main); font-size: 16px; outline: none; box-shadow: 0 4px 30px rgba(0,0,0,0.1); backdrop-filter: blur(10px); transition: 0.3s; } .search-input:focus { border-color: var(--primary); box-shadow: 0 0 0 4px rgba(147, 51, 234, 0.2); }
        .view { position: absolute; inset: 0; padding: 20px 40px 40px 40px; overflow-y: auto; opacity: 0; pointer-events: none; transition: 0.3s ease; transform: translateY(10px); display: flex; flex-direction: column; } .view.active { opacity: 1; pointer-events: all; transform: translateY(0); } .view-title { font-size: 32px; font-weight: 800; margin-bottom: 30px; letter-spacing: -1px; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 25px; } .card { background: var(--glass-bg); border-radius: 20px; padding: 16px; border: 1px solid var(--glass-border); transition: 0.3s; display: flex; flex-direction: column; backdrop-filter: blur(10px); } .card:hover { transform: translateY(-8px); border-color: var(--primary); box-shadow: 0 10px 30px rgba(147, 51, 234, 0.2); } .card img { width: 100%; border-radius: 14px; margin-bottom: 15px; object-fit: cover; aspect-ratio: 16/7; } .card h4 { font-size: 16px; font-weight: 700; margin-bottom: 15px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .btn { background: var(--primary); color: white; border: none; padding: 12px 20px; border-radius: 12px; font-weight: 700; font-size: 14px; cursor: pointer; transition: 0.2s; text-transform: uppercase; letter-spacing: 0.5px; width: 100%; } .btn:hover { background: var(--primary-hover); transform: scale(1.02); box-shadow: 0 4px 15px rgba(147, 51, 234, 0.3); }
        #blocker-screen, #intro-screen { position: fixed; inset: 0; background: rgba(0,0,0,0.85); backdrop-filter: blur(15px); z-index: 10000; display: none; align-items: center; justify-content: center; text-align: center; padding: 20px; } [data-theme="light"] #blocker-screen, [data-theme="light"] #intro-screen { background: rgba(255,255,255,0.85); } .block-box, .intro-box { background: var(--glass-bg); padding: 50px; border-radius: 30px; border: 2px solid var(--danger); max-width: 600px; box-shadow: 0 0 50px rgba(239, 68, 68, 0.2); } .intro-box { border-color: var(--primary); box-shadow: 0 0 50px rgba(147, 51, 234, 0.2); width: 450px;} .intro-input { width: 100%; padding: 15px 20px; border-radius: 12px; border: 1px solid var(--glass-border); background: var(--glass-bg); color: var(--text-main); font-size: 18px; margin: 25px 0; outline: none; text-align: center; } .intro-input:focus { border-color: var(--primary); }
        #toast-container { position: fixed; bottom: 30px; right: 30px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; } .toast { background: var(--bg-base); color: var(--text-main); border-left: 4px solid var(--primary); padding: 15px 25px; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); font-weight: 600; transform: translateX(120%); animation: slideIn 0.3s forwards; border: 1px solid var(--glass-border); } @keyframes slideIn { to { transform: translateX(0); } }
        #loader { position: fixed; inset: 0; background: rgba(0,0,0,0.7); z-index: 9500; display: none; flex-direction: column; align-items: center; justify-content: center; backdrop-filter: blur(8px); color:white;} .spinner { width: 60px; height: 60px; border: 5px solid rgba(255,255,255,0.2); border-top-color: var(--primary); border-radius: 50%; animation: spin 1s infinite linear; margin-bottom: 20px; } @keyframes spin { 100% { transform: rotate(360deg); } }
        .info-card { background: var(--glass-bg); padding: 30px; border-radius: 20px; border: 1px solid var(--glass-border); margin-bottom: 20px; line-height: 1.7; color: var(--text-muted); font-size: 16px; max-width: 800px; backdrop-filter: blur(10px); } .setting-row { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid var(--glass-border); } .setting-row:last-child { border-bottom: none; }
        .switch { position: relative; display: inline-block; width: 50px; height: 28px; } .switch input { opacity: 0; width: 0; height: 0; } .slider { position: absolute; cursor: pointer; inset: 0; background-color: rgba(147, 51, 234, 0.2); transition: .4s; border-radius: 34px; border: 1px solid var(--glass-border); } .slider:before { position: absolute; content: ""; height: 20px; width: 20px; left: 4px; bottom: 3px; background-color: white; transition: .4s; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.2);} input:checked + .slider { background-color: var(--primary); border-color: var(--primary); } input:checked + .slider:before { transform: translateX(20px); }
        select.custom-select { padding: 10px 15px; border-radius: 10px; background: var(--glass-bg); color: var(--text-main); border: 1px solid var(--glass-border); outline: none; cursor: pointer;} select.custom-select option { background: var(--bg-base); color: var(--text-main); }
    </style>
</head>
<body>
    <script>
        const i18n = {
            tr: {
                m_home: "🏠 Ana Sayfa", m_lib: "📚 Kütüphanem", m_man: "📝 Manuel Ekle", 
                m_ofix: "🌐 Online Fix", m_bfix: "🛡️ Bypass Fix", m_fix: "🔧 Lisans Fix", 
                m_don: "❤️ Bağış Yap", m_abt: "ℹ️ Hakkımızda", m_st: "📡 Sunucu Durumu", m_set: "⚙️ Ayarlar",
                t_home: "Öne Çıkanlar", t_lib: "Kütüphanem", t_man: "Manuel Oyun Ekle", 
                t_ofix: "Online Fix Kurulumu", t_bfix: "Bypass Fix Kurulumu",
                t_don: "Bağış Yap", t_abt: "Hakkımızda", t_st: "Sunucu Durumu", t_set: "Ayarlar",
                search_ph: "Steam'de oyun ara... (Enter'a bas)", btn_add: "KÜTÜPHANEYE EKLE", added: "EKLENME",
                man_desc: "Sunucumuzda bulunmayan oyunları, elinizdeki .ZIP dosyası ile kütüphanenize kolayca ekleyebilirsiniz.", man_id: "Oyun ID'si (Zorunlu):", man_name: "Oyun Adı (Zorunlu):", man_img: "Kapak Görseli URL (Opsiyonel):", man_btn: "ZIP DOSYASI SEÇ VE ENJEKTE ET",
                fix_desc: "Oyunun AppID'sini girin. Eğer sunucuda fix mevcutsa, oyun klasörünü seçmeniz istenecektir.",
                fix_btn: "FİX DOSYASINI ARA VE KUR",
                set_acf: "AppManifest (.acf) Üretimi", set_acf_d: "Oyun eklenirken appmanifest dosyalarının otomatik oluşturulmasını sağlar.",
                set_lang: "Dil Seçimi / Language", set_lang_d: "Uygulamanın dilini değiştirin.",
                set_thm: "Tema Rengi", set_thm_d: "Açık veya koyu arayüz temasını seçin.",
                set_name: "İsim Değiştir", set_name_d: "Uygulamanın size hitap edeceği ismi güncelleyin.", btn_save: "KAYDET",
                greet: "Hoş Geldin, "
            },
            en: {
                m_home: "🏠 Home", m_lib: "📚 My Library", m_man: "📝 Manual Add", 
                m_ofix: "🌐 Online Fix", m_bfix: "🛡️ Bypass Fix", m_fix: "🔧 License Fix", 
                m_don: "❤️ Donate", m_abt: "ℹ️ About Us", m_st: "📡 Server Status", m_set: "⚙️ Settings",
                t_home: "Featured Games", t_lib: "My Library", t_man: "Manual Game Add", 
                t_ofix: "Online Fix Installation", t_bfix: "Bypass Fix Installation",
                t_don: "Donate", t_abt: "About Us", t_st: "Server Status", t_set: "Settings",
                search_ph: "Search games on Steam... (Press Enter)", btn_add: "ADD TO LIBRARY", added: "ADDED",
                man_desc: "Easily add games not available on our server using a .ZIP file containing the required files.", man_id: "Game ID (Required):", man_name: "Game Name (Required):", man_img: "Cover Image URL (Optional):", man_btn: "SELECT ZIP FILE AND INJECT",
                fix_desc: "Enter the AppID of the game. If the fix is available, you will be prompted to select the game folder.",
                fix_btn: "SEARCH AND INSTALL FIX",
                set_acf: "AppManifest (.acf) Generation", set_acf_d: "Automatically generates appmanifest files when adding a game.",
                set_lang: "Language / Dil Seçimi", set_lang_d: "Change the application language.",
                set_thm: "Theme Color", set_thm_d: "Select light or dark interface theme.",
                set_name: "Change Name", set_name_d: "Update the name the application uses to greet you.", btn_save: "SAVE",
                greet: "Welcome, "
            }
        };
        let currentLang = 'tr';
    </script>

    <div id="blocker-screen">
        <div class="block-box">
            <h1 style="color:var(--danger); font-size:36px; margin-bottom:15px; font-weight:800;">ZORUNLU GÜNCELLEME!</h1>
            <p style="font-size:16px; color:var(--text-muted); margin-bottom:30px; line-height: 1.5;">MonikDepot'un yeni sürümü mevcut. Lütfen güncelleyin.</p>
            <button class="btn" style="padding: 15px 30px; font-size: 16px; width: auto;" onclick="pywebview.api.open_update_website()">Hemen İndir</button>
        </div>
    </div>

    <div id="intro-screen">
        <div class="intro-box">
            <h1 style="font-weight:800; font-size:32px; margin-bottom:10px;">Hoş Geldin! 👋</h1>
            <p style="color:var(--text-muted); font-size:16px;">Sana nasıl hitap etmemizi istersin?</p>
            <input type="text" id="intro-name-input" class="intro-input" placeholder="İsminizi yazın..." autocomplete="off">
            <button class="btn" onclick="saveUserName()">Maceraya Başla 🚀</button>
        </div>
    </div>

    <div id="loader"><div class="spinner"></div><h2 id="loader-text" style="font-weight:600;">İşlem yapılıyor...</h2></div>
    <div id="toast-container"></div>

    <header>
        <div class="greeting" id="header-greeting">Hoş Geldin, <span id="user-display-name">Oyuncu</span></div>
        <div class="menu-trigger" onclick="toggleSidebar()"><div></div><div></div><div></div></div>
    </header>

    <div id="sidebar-overlay" onclick="toggleSidebar()"></div>
    <div id="sidebar">
        <div class="sidebar-header">
            <h2>Menü</h2><div class="close-btn" onclick="toggleSidebar()">&times;</div>
        </div>
        <div class="menu-list">
            <div class="menu-item active" data-i18n="m_home" onclick="switchView('home', this)">🏠 Ana Sayfa</div>
            <div class="menu-item" data-i18n="m_lib" onclick="switchView('library', this)">📚 Kütüphanem</div>
            <div class="menu-item" data-i18n="m_man" onclick="switchView('manual', this)">📝 Manuel Ekle</div>
            <div class="menu-item" data-i18n="m_ofix" onclick="switchView('onlinefix', this)">🌐 Online Fix</div>
            <div class="menu-item" data-i18n="m_bfix" onclick="switchView('bypassfix', this)">🛡️ Bypass Fix</div>
            <div class="menu-item" data-i18n="m_fix" onclick="triggerLicenseFix(this)">🔧 Lisans Fix</div>
            <div class="menu-item" data-i18n="m_don" onclick="switchView('donate', this)">❤️ Bağış Yap</div>
            <div class="menu-item" data-i18n="m_abt" onclick="switchView('about', this)">ℹ️ Hakkımızda</div>
            <div class="menu-item" data-i18n="m_st" onclick="switchView('status', this)">📡 Sunucu Durumu</div>
            <div class="menu-item" data-i18n="m_set" onclick="switchView('settings', this)">⚙️ Ayarlar</div>
        </div>
    </div>

    <main>
        <div class="search-container" id="search-section">
            <input type="text" id="search-input" data-i18n-ph="search_ph" class="search-input" placeholder="Steam'de oyun ara..." onkeydown="if(event.key=='Enter')searchGame()">
        </div>

        <div id="view-home" class="view active" style="top: 80px;">
            <h2 class="view-title" id="home-title" data-i18n="t_home">Öne Çıkanlar</h2>
            <div id="market-grid" class="grid"></div>
        </div>

        <div id="view-library" class="view">
            <h2 class="view-title" data-i18n="t_lib">Kütüphanem</h2>
            <div id="library-grid" class="grid"></div>
        </div>

        <div id="view-manual" class="view">
            <h2 class="view-title" data-i18n="t_man">Manuel Oyun Ekle</h2>
            <div class="info-card" style="max-width: 600px;">
                <p style="margin-bottom: 20px;" data-i18n="man_desc">Sunucumuzda bulunmayan oyunları .ZIP dosyası ile kolayca ekleyin.</p>
                <input type="text" id="man-id" class="search-input" placeholder="AppID (Zorunlu)" style="margin-bottom:20px; width:100%; border-radius:10px;">
                <input type="text" id="man-name" class="search-input" placeholder="Oyun Adı (Zorunlu)" style="margin-bottom:20px; width:100%; border-radius:10px;">
                <input type="text" id="man-img" class="search-input" placeholder="Kapak Görseli URL (Opsiyonel)" style="margin-bottom:30px; width:100%; border-radius:10px;">
                <button class="btn" style="padding: 15px;" data-i18n="man_btn" onclick="doManualInject()">ZIP DOSYASI SEÇ VE ENJEKTE ET</button>
            </div>
        </div>

        <div id="view-onlinefix" class="view">
            <h2 class="view-title" data-i18n="t_ofix">Online Fix Kurulumu</h2>
            <div class="info-card" style="max-width: 600px;">
                <p style="margin-bottom: 20px;" data-i18n="fix_desc">Oyunun AppID'sini girin. Eğer sunucuda fix mevcutsa, oyun klasörünü seçmeniz istenecektir.</p>
                <input type="text" id="ofix-id" class="search-input" placeholder="AppID (Örn: 730)" style="margin-bottom:30px; width:100%; border-radius:10px;">
                <button class="btn" style="padding: 15px;" data-i18n="fix_btn" onclick="doOnlineFix()">FİX DOSYASINI ARA VE KUR</button>
            </div>
        </div>

        <div id="view-bypassfix" class="view">
            <h2 class="view-title" data-i18n="t_bfix">Bypass Fix Kurulumu</h2>
            <div class="info-card" style="max-width: 600px;">
                <p style="margin-bottom: 20px;" data-i18n="fix_desc">Oyunun AppID'sini girin. Eğer sunucuda fix mevcutsa, oyun klasörünü seçmeniz istenecektir.</p>
                <input type="text" id="bfix-id" class="search-input" placeholder="AppID (Örn: 730)" style="margin-bottom:30px; width:100%; border-radius:10px;">
                <button class="btn" style="padding: 15px;" data-i18n="fix_btn" onclick="doBypassFix()">FİX DOSYASINI ARA VE KUR</button>
            </div>
        </div>

        <div id="view-donate" class="view">
            <h2 class="view-title" data-i18n="t_don">Bağış Yap</h2>
            <div class="info-card" style="text-align:center; padding:50px 30px;">
                <div style="font-size:72px; font-weight:800; color:var(--primary); margin:20px 0;" id="donation-counter">0</div>
                <p style="font-size:12px; text-transform:uppercase; letter-spacing:1px; margin-bottom:30px;">TOTAL DONATIONS</p>
                <button class="btn" style="max-width:300px; padding:15px; font-size:16px;" onclick="executeDonation()">DONATE ❤️</button>
            </div>
        </div>

        <div id="view-about" class="view">
            <h2 class="view-title" data-i18n="t_abt">Hakkımızda</h2>
            <div class="info-card">
                <p>Biz Türk oyuncu topluluğunun yardımı için geldik. Sizlere ücretsiz olarak oyun oynamanıza imkan sunan MonikDepot projemizi gururla sunarız.</p><br>
                <p>Ücretsiz oyun oynamak her oyuncunun hakkı. İyi oyunlar dileriz.</p>
            </div>
        </div>

        <div id="view-status" class="view">
            <h2 class="view-title" data-i18n="t_st">Sunucu Durumu</h2>
            <div class="info-card" style="text-align:center; padding:60px 30px;">
                <p style="margin-bottom:20px; font-size:18px;">API Bağlantısı:</p>
                <div id="server-status-text" style="font-size:32px; font-weight:800; padding:20px; background:rgba(0,0,0,0.3); border-radius:15px; display:inline-block;">Bağlanıyor...</div>
            </div>
        </div>

        <div id="view-settings" class="view">
            <h2 class="view-title" data-i18n="t_set">Ayarlar</h2>
            <div class="info-card">
                <div class="setting-row">
                    <div style="flex:1;">
                        <h4 style="color:var(--text-main); font-size:18px; margin-bottom:5px;" data-i18n="set_name">İsim Değiştir</h4>
                        <p style="font-size:14px;" data-i18n="set_name_d">Uygulamanın size hitap edeceği ismi güncelleyin.</p>
                    </div>
                    <div style="display:flex; gap:10px;">
                        <input type="text" id="set-name-input" class="search-input" style="padding:10px; width:150px; font-size:14px;" placeholder="Yeni İsim">
                        <button class="btn" style="width:auto; padding:10px 20px;" data-i18n="btn_save" onclick="updateName()">KAYDET</button>
                    </div>
                </div>
                <div class="setting-row">
                    <div>
                        <h4 style="color:var(--text-main); font-size:18px; margin-bottom:5px;" data-i18n="set_lang">Dil Seçimi / Language</h4>
                        <p style="font-size:14px;" data-i18n="set_lang_d">Uygulamanın dilini değiştirin.</p>
                    </div>
                    <select id="set-lang-select" class="custom-select" onchange="changeLanguage(this.value)">
                        <option value="tr">Türkçe</option><option value="en">English</option>
                    </select>
                </div>
                <div class="setting-row">
                    <div>
                        <h4 style="color:var(--text-main); font-size:18px; margin-bottom:5px;" data-i18n="set_thm">Tema Rengi</h4>
                        <p style="font-size:14px;" data-i18n="set_thm_d">Açık veya koyu arayüz temasını seçin.</p>
                    </div>
                    <select id="set-theme-select" class="custom-select" onchange="changeTheme(this.value)">
                        <option value="dark">Dark Mode</option><option value="light">Light Mode</option>
                    </select>
                </div>
                <div class="setting-row" style="border:none;">
                    <div>
                        <h4 style="color:var(--text-main); font-size:18px; margin-bottom:5px;" data-i18n="set_acf">AppManifest (.acf) Üretimi</h4>
                        <p style="font-size:14px;" data-i18n="set_acf_d">Oyun eklenirken appmanifest dosyalarının otomatik oluşturulmasını sağlar.</p>
                    </div>
                    <label class="switch">
                        <input type="checkbox" id="setting-acf" onchange="pywebview.api.update_setting('create_acf', this.checked)">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
        </div>
    </main>

    <script>
        window.addEventListener('pywebviewready', async function() {
            const vData = await pywebview.api.check_version_block();
            if (!vData.is_valid) { document.getElementById('blocker-screen').style.display = 'flex'; return; }

            const state = await pywebview.api.get_initial_state();
            if (state.is_first_boot || !state.user_name) {
                document.getElementById('intro-screen').style.display = 'flex';
                document.getElementById('intro-name-input').focus();
            } else { setupApp(state); }
        });

        function setupApp(state) {
            document.getElementById('user-display-name').innerText = state.user_name;
            document.getElementById('setting-acf').checked = state.acf_enabled;
            currentLang = state.language; document.getElementById('set-lang-select').value = currentLang; applyTranslations();
            const theme = state.theme; document.getElementById('set-theme-select').value = theme; document.documentElement.setAttribute('data-theme', theme);
            loadMarketGames();
        }

        function applyTranslations() {
            const dict = i18n[currentLang];
            document.querySelectorAll('[data-i18n]').forEach(el => { const key = el.getAttribute('data-i18n'); if(dict[key]) el.innerText = dict[key]; });
            document.querySelectorAll('[data-i18n-ph]').forEach(el => { const key = el.getAttribute('data-i18n-ph'); if(dict[key]) el.placeholder = dict[key]; });
            const name = document.getElementById('user-display-name').innerText;
            document.getElementById('header-greeting').innerHTML = dict['greet'] + `<span id="user-display-name">${name}</span>`;
        }

        async function changeLanguage(lang) { currentLang = lang; applyTranslations(); await pywebview.api.update_setting("language", lang); showToast(lang === 'tr' ? "Dil güncellendi." : "Language updated.", "success"); }
        async function changeTheme(theme) { document.documentElement.setAttribute('data-theme', theme); await pywebview.api.update_setting("theme", theme); }

        async function updateName() {
            const newName = document.getElementById('set-name-input').value;
            if(!newName.trim()) return showToast("Geçerli isim girin!", "warning");
            const ok = await pywebview.api.save_user_greeting(newName);
            if(ok) { document.getElementById('user-display-name').innerText = newName; document.getElementById('set-name-input').value = ''; showToast("İsim güncellendi!", "success"); }
        }

        async function saveUserName() {
            const nameInput = document.getElementById('intro-name-input').value;
            if (!nameInput.trim()) return showToast("Geçerli isim giriniz!", "error");
            const ok = await pywebview.api.save_user_greeting(nameInput);
            if (ok) { document.getElementById('intro-screen').style.display = 'none'; setupApp(await pywebview.api.get_initial_state()); showToast("Giriş yapıldı!", "success"); }
        }

        function toggleSidebar() { document.getElementById('sidebar').classList.toggle('open'); document.getElementById('sidebar-overlay').classList.toggle('active'); }

        function switchView(viewId, menuItem) {
            toggleSidebar();
            document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active')); menuItem.classList.add('active');
            document.querySelectorAll('.view').forEach(el => el.classList.remove('active')); document.getElementById(`view-${viewId}`).classList.add('active');
            document.getElementById('search-section').style.display = (viewId === 'home') ? 'block' : 'none';
            if(viewId !== 'home') document.getElementById('view-' + viewId).style.top = '0px';
            if (viewId === 'home') loadMarketGames(); if (viewId === 'library') loadLibraryGames(); if (viewId === 'status') checkServerStatus(); if (viewId === 'donate') fetchDonationCount();
        }
        
        async function triggerLicenseFix(el) {
            document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active')); el.classList.add('active');
            document.getElementById('sidebar').classList.remove('open'); document.getElementById('sidebar-overlay').classList.remove('active');
            showLoader(true, "Oyun klasörünü seçin...");
            try {
                const res = await pywebview.api.run_license_fix(); showLoader(false);
                if (res.status === "success") showToast(res.msg, "success"); else if (res.status === "warning") showToast(res.msg, "warning"); else showToast(res.msg, "error");
            } catch (err) { showLoader(false); showToast("Hata: " + err, "error"); }
        }

        async function doOnlineFix() {
            const appId = document.getElementById('ofix-id').value;
            if(!appId) return showToast("AppID giriniz!", "warning");
            showLoader(true, "Sunucu sorgulanıyor...");
            const res = await pywebview.api.run_online_fix(appId);
            showLoader(false);
            if (res.status === "success") { showToast(res.msg, "success"); document.getElementById('ofix-id').value = ''; }
            else if (res.status === "warning") showToast(res.msg, "warning");
            else showToast(res.msg, "error");
        }

        async function doBypassFix() {
            const appId = document.getElementById('bfix-id').value;
            if(!appId) return showToast("AppID giriniz!", "warning");
            showLoader(true, "Sunucu sorgulanıyor...");
            const res = await pywebview.api.run_bypass_fix(appId);
            showLoader(false);
            if (res.status === "success") { showToast(res.msg, "success"); document.getElementById('bfix-id').value = ''; }
            else if (res.status === "warning") showToast(res.msg, "warning");
            else showToast(res.msg, "error");
        }

        async function searchGame() {
            const q = document.getElementById('search-input').value;
            if(!q) return loadMarketGames();
            showLoader(true, "Aranıyor..."); const results = await pywebview.api.search_steam_games(q); showLoader(false);
            document.getElementById('home-title').innerText = "Arama Sonuçları"; renderGrid('market-grid', results, true);
        }

        async function loadMarketGames() {
            document.getElementById('home-title').innerText = i18n[currentLang]['t_home'];
            document.getElementById('market-grid').innerHTML = '<p style="color:var(--text-muted);">Yükleniyor...</p>';
            renderGrid('market-grid', await pywebview.api.fetch_featured_games(), true);
        }

        async function loadLibraryGames() {
            const games = await pywebview.api.get_library_games();
            if(games.length === 0) document.getElementById('library-grid').innerHTML = '<p style="color:var(--text-muted);">Boş.</p>'; else renderGrid('library-grid', games, false);
        }

        function renderGrid(targetId, data, isStore) {
            const grid = document.getElementById(targetId);
            if(data.length === 0) { grid.innerHTML = '<p>Bulunamadı.</p>'; return; }
            const btnText = i18n[currentLang]['btn_add']; const addText = i18n[currentLang]['added'];
            grid.innerHTML = data.map(g => `
                <div class="card"><img src="${g.img}" alt="Kapak"><h4>${g.name}</h4>
                    ${isStore ? `<button class="btn" style="margin-top:auto;" onclick="injectGame('${g.id}', '${g.name.replace(/'/g, "\\'")}', '${g.img}')">${btnText}</button>` : `<p style="font-size:12px; color:var(--success); font-weight:700; margin-top:auto;">${addText}: ${g.added_at}</p>`}
                </div>`).join('');
        }

        async function injectGame(appId, name, img) {
            showLoader(true, "Oyun indiriliyor...");
            const res = await pywebview.api.inject_steam_game(appId, name, img); showLoader(false);
            if (res.status === "success") showToast(res.msg, "success"); else showToast(res.msg, "error");
        }

        async function doManualInject() {
            const appId = document.getElementById('man-id').value; const name = document.getElementById('man-name').value; const img = document.getElementById('man-img').value;
            if(!appId || !name) return showToast("Zorunlu alanları doldurun!", "warning");
            showLoader(true, "ZIP dosyası seçimi bekleniyor...");
            const res = await pywebview.api.manual_inject_game(appId, name, img); showLoader(false);
            if (res.status === "success") { showToast(res.msg, "success"); document.getElementById('man-id').value = ''; document.getElementById('man-name').value = ''; document.getElementById('man-img').value = ''; } 
            else if (res.status === "warning") showToast(res.msg, "warning"); else showToast(res.msg, "error");
        }

        async function checkServerStatus() {
            const el = document.getElementById('server-status-text'); el.innerText = "Sorgulanıyor..."; el.style.color = "var(--text-main)";
            const isOnline = await pywebview.api.fetch_server_status();
            if (isOnline) { el.innerText = "Durum: Online"; el.style.color = "var(--success)"; } else { el.innerText = "Durum: Offline"; el.style.color = "var(--danger)"; }
        }

        async function fetchDonationCount() { document.getElementById('donation-counter').innerText = await pywebview.api.fetch_donation_count(); }

        async function executeDonation() {
            showLoader(true, "Bağlanıyor..."); const res = await pywebview.api.trigger_donation(); showLoader(false);
            if (res.status === "success") { showToast(res.msg, "success"); document.getElementById('donation-counter').innerText = res.new_count; } 
            else if (res.status === "already_donated") alert("Zaten bağış yaptınız!"); else showToast(res.msg, "error");
        }

        function showLoader(show, text = "") { document.getElementById('loader').style.display = show ? 'flex' : 'none'; document.getElementById('loader-text').innerText = text; }
        function showToast(message, type = "info") {
            const container = document.getElementById('toast-container'); const toast = document.createElement('div'); toast.className = 'toast';
            let color = "var(--primary)"; if (type === "success") color = "var(--success)"; if (type === "error") color = "var(--danger)"; if (type === "warning") color = "var(--warning)"; 
            toast.style.borderLeftColor = color; toast.innerHTML = `<span>${message}</span>`; container.appendChild(toast);
            setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateX(120%)'; setTimeout(() => toast.remove(), 300); }, 4000);
        }
    </script>
</body>
</html>
"""
