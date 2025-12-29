# days of week
DAYS_OF_WEEK = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

# name of activities
BAND_ACTIVITIES = [
    # production
    "REKAMAN VOCAL", "REKAMAN INSTRUMEN", "MIXING & MASTERING", 
    "PRODUKSI MUSIK", "WORKSHOP LAGU BARU", "PENGEMBANGAN LIRIK", 
    "ARRANGEMENT MUSIK", "DEMO TRACKING",
    # practice needs
    "LATIHAN STUDIO", "LATIHAN RUTIN", "SOUNDCHECK", 
    "TECHNICAL MEETING", "GLADIKERSIK (GR)", "PEMBERSIHAN ALAT",
    # perform & stage
    "KONSER LIVE", "PERFORMANCE FESTIVAL", "GIGS CAFE", 
    "AKUSTIK SESSION", "CHESTRIG PREPARATION", "LOAD IN ALAT", "LOAD OUT ALAT",
    # media & promotion
    "INTERVIEW RADIO", "PODCAST SESSION", "FOTO PRE-RELEASE", 
    "SYUTING VIDEO KLIP", "PRESS CONFERENCE", "MEETING VENDOR", 
    "PROMOSI MEDIA SOSIAL", "SIGNING SESSION", "MEETING MANAJEMEN",
    # etc
    "TOUR BUS TRAVEL", "EVALUASI MINGGUAN", "MEETING SPONSOR", "CONTENT CREATOR COLLAB"
]

# mandatory default schedule
DEFAULT_MANDATORY_SCHEDULE = [
    {"day": "Senin", "activity": "LATIHAN RUTIN", "start": "10:00", "end": "13:00"},
    {"day": "Selasa", "activity": "PRODUKSI MUSIK", "start": "14:00", "end": "17:00"},
    {"day": "Rabu", "activity": "MEETING MANAJEMEN", "start": "11:00", "end": "12:30"},
    {"day": "Kamis", "activity": "WORKSHOP LAGU BARU", "start": "13:00", "end": "16:00"},
    {"day": "Jumat", "activity": "SOUNDCHECK", "start": "16:00", "end": "18:00"},
    {"day": "Sabtu", "activity": "KONSER LIVE", "start": "19:00", "end": "22:00"},
    {"day": "Minggu", "activity": "EVALUASI MINGGUAN", "start": "20:00", "end": "21:30"}
]