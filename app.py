import streamlit as st
import time
import pandas as pd
import matplotlib.pyplot as plt
from algorithms.iterative import get_conflict_free_activities_iterative, is_time_conflict_free_iterative
from algorithms.recursive import get_conflict_free_activities_recursive
from data.generator import generate_activities
from data.static import DEFAULT_MANDATORY_SCHEDULE, DAYS_OF_WEEK
import sys 
# set recursion limit to increase stability in high number of activities
sys.setrecursionlimit(2000)

# ==========================================
#   STATE MANAGEMENT (Agar data tidak hilang)
# ==========================================
if 'custom_mandatory' not in st.session_state:
    st.session_state.custom_mandatory = []
if 'custom_candidates' not in st.session_state:
    st.session_state.custom_candidates = []

# ===================
#   UI ENTRY POINT
# ===================
st.title("Analisis Kompleksitas Algoritma")
st.subheader("Algoritma Non-Overlapping-Intervals untuk Penjadwalan")
st.text("Project by:")
st.text("Achmad Baihaqie Wibowo - 103012400026\nRafi Dzaki Azhari - 103012400336\nJean Yudhistira Diva Waluyo - 103012400113")

if st.sidebar.button("Reset Jadwal Kustom"):
    st.session_state.custom_mandatory = []
    st.session_state.custom_candidates = []
    st.rerun()

# ==========================
#   MANDATORY ENTRY SET-UP
# ==========================
mandatory_schedule_choice = st.sidebar.radio("Jadwal Mandatory", ("Default", "Acak", "Customize"))
Mandatory = []
if mandatory_schedule_choice == "Default":
    Mandatory = DEFAULT_MANDATORY_SCHEDULE.copy()
elif mandatory_schedule_choice == "Customize":
    st.sidebar.subheader("Tambah Jadwal Mandatory")
    with st.sidebar.form("form_mandatory"):
        input_day = st.selectbox("Hari", DAYS_OF_WEEK)
        input_activity = st.text_input("Nama Aktivitas", "rapat")
        input_start = st.time_input("Jam Mulai", value=None, step=60)
        input_end = st.time_input("Jam Selesai", value=None, step=60)
        add_button = st.form_submit_button("Tambah ke Jadwal Mandatory")
        if add_button:
            if input_start and input_end and input_start < input_end:
                new_mandatory_activity = {
                    "day": input_day,
                    "activity": input_activity,
                    "start": input_start.strftime("%H:%M"),
                    "end": input_end.strftime("%H:%M")
                }
                input_start_minute = input_start.hour * 60 + input_start.minute
                input_end_minute = input_end.hour * 60 + input_end.minute
                if is_time_conflict_free_iterative(st.session_state.custom_mandatory, new_mandatory_activity, input_start_minute, input_end_minute):
                    st.session_state.custom_mandatory.append(new_mandatory_activity)
                    st.sidebar.success(f"Berhasil menambahkan {input_activity}")
                else:
                    st.sidebar.error("Bentrok dengan jadwal mandatory yang sudah ada!")
            else:
                st.sidebar.error("Waktu mulai harus lebih awal dari selesai.")
    Mandatory = st.session_state.custom_mandatory

# ==========================
#   CANDIDATE ENTRY SET-UP
# ==========================
candidate_schedule_choice = st.sidebar.radio("Jadwal Kandidat", ("Acak", "Customize"))
Candidate = []

if candidate_schedule_choice == "Customize":
    st.sidebar.subheader("Tambah Jadwal Kandidat")
    with st.sidebar.form("form_candidate"):
        input_day = st.selectbox("Hari", DAYS_OF_WEEK)
        input_activity = st.text_input("Nama Aktivitas", "olahraga")
        input_start = st.time_input("Jam Mulai", value=None, step=60)
        input_end = st.time_input("Jam Selesai", value=None, step=60)
        add_button = st.form_submit_button("Tambah ke Jadwal Kandidat")
        if add_button:
            if input_start and input_end and input_start < input_end:
                st.session_state.custom_candidates.append({
                    "day": input_day,
                    "activity": input_activity,
                    "start": input_start.strftime("%H:%M"),
                    "end": input_end.strftime("%H:%M")
                })
                st.sidebar.success(f"Berhasil menambahkan {input_activity}")
        Candidate = st.session_state.custom_candidates
        if len(Candidate) > 0:
            dataset_size = len(Candidate)
        else:
            dataset_size = 1
            st.sidebar.info(f"Jumlah data kandidat kustom: {len(Candidate)}")
else:
    st.sidebar.header("Settings")
    dataset_size = st.sidebar.slider("Candidate Dataset Size", min_value = 1, max_value = 1000, value = 10)

# ============================
#    nM GROWTH LOGIC SET-UP
# ============================
growth_mode = "Statis"
if mandatory_schedule_choice == "Acak":
    growth_mode = st.sidebar.selectbox("Mode Pertumbuhan nM", ("Statis", "Proporsional terhadap nC"))
    if growth_mode == "Statis":
        n_mandatory_random = st.sidebar.slider("Mandatory Dataset Size (nM konstan)", min_value = 1, max_value = 1000, value = 10)
    else:
        ratio = st.sidebar.slider("Rasio Pertumbuhan nM terhadap nC (%)", min_value = 1, max_value = 100, value = 20)
        st.sidebar.caption(f"nM akan selalu {ratio}% dari nC.")

# ========================
#     STEP SIZE SET-UP
# ========================
simulation_step = st.sidebar.slider("Simulation Step (Lompatan Data)", min_value = 1, max_value = 100, value = 10)
st.sidebar.caption("Semakin besar step, semakin cepat simulasi selesai.")

# ==================================
#       VIEW CURRENT INPUTS 
# ==================================
st.divider()
with st.expander("Lihat Daftar Jadwal Terinput Saat Ini"):
    col_m, col_c = st.columns(2)
    with col_m:
        st.write("**Jadwal Mandatory:**")
        if Mandatory:
            st.dataframe(pd.DataFrame(Mandatory), use_container_width=True)
        else:
            st.caption("Kosong")
    with col_c:
        st.write("**Jadwal Kandidat:**")
        if Candidate:
            st.dataframe(pd.DataFrame(Candidate), use_container_width=True)
        else:
            st.caption("Kosong")

# ==================================================
#    GENERATING DATA & EXECUTION TIME MEASUREMENT
# ==================================================
if st.button("Jalankan Simulasi"):

    # rule
    if not Mandatory and mandatory_schedule_choice == "Customize":
        st.warning("Jadwal Mandatory kustom masih kosong!")
        st.stop()
    if not Candidate and candidate_schedule_choice == "Customize":
        st.warning("Jadwal Kandidat kustom masih kosong!")
        st.stop()

    # initialization
    iterative_execution_times = []
    recursive_execution_times = []
    results_match = True
    progress_bar = st.progress(0)

    # fixed pools for data consistency in mandatory schedule
    if mandatory_schedule_choice == "Acak" and growth_mode == "Statis":
        current_mandatory_fixed = generate_activities(n_mandatory_random, True)
    else:
        current_mandatory_fixed = Mandatory
    # fixed pools for data consistency in candidate schedule
    if candidate_schedule_choice == "Acak":
        full_candidate_pool = generate_activities(dataset_size, False)

    # define the range of data points to be tested based on the simulation step
    steps = list(range(1, dataset_size + 1, simulation_step))
    total_steps = len(steps)

    # start simulation
    for i, size in enumerate(steps):
        # candidate data seeding
        if candidate_schedule_choice == "Acak":
            current_candidate = full_candidate_pool[:size]
        else:
            current_candidate = Candidate[:size]
        # mandatory data seeding
        if mandatory_schedule_choice == "Acak" and growth_mode == "Proporsional terhadap nC":
            current_nM_size = max(1, int(size * (ratio / 100)))
            current_mandatory = generate_activities(current_nM_size, True)
        else:
            current_mandatory = current_mandatory_fixed
        # iterative execution time
        start_time = time.time()
        iterative_result = get_conflict_free_activities_iterative(current_candidate, current_mandatory)
        iterative_execution_times.append(time.time() - start_time)
        # recursive execution time
        start_time = time.time()
        recursive_result = get_conflict_free_activities_recursive(current_candidate, current_mandatory, 0)
        recursive_execution_times.append(time.time() - start_time)
        if iterative_result != recursive_result:
            results_match = False
        # display progress bar
        progress_bar.progress((i+1) / total_steps)

    # ===================
    #       MAIN UI
    # ===================
    df = pd.DataFrame({
        'Jumlah Aktivitas': range(1, dataset_size + 1, simulation_step),
        'Waktu Eksekusi Algoritma Iteratif': iterative_execution_times,
        'Waktu Eksekusi Algoritma Rekursif': recursive_execution_times
    })
    col1, col2 = st.columns(2) 
    with col1:
        # time execution visualization
        st.subheader("Grafik Performa")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['Jumlah Aktivitas'], df['Waktu Eksekusi Algoritma Iteratif'], 'o', label="Algoritma Iteratif")
        ax.plot(df['Jumlah Aktivitas'], df['Waktu Eksekusi Algoritma Rekursif'], 'o', label="Algoritma Rekursif")
        if mandatory_schedule_choice == "Acak" and growth_mode == "Proporsional terhadap nC":
            title = f"nM {ratio}% dari nC" 
        else:
            title = f"nM = {len(current_mandatory_fixed)}"
        ax.set_title(f"Perbandingan Waktu Eksekusi ({title})", fontsize=12)
        ax.set_xlabel('Ukuran Aktivitas Kandidat (nC)')
        ax.set_ylabel('Waktu Eksekusi (Detik)')
        ax.set_ylim(0)
        ax.set_xlim(0)
        ax.legend()
        ax.grid(True, linestyle="--", linewidth=0.5)
        st.pyplot(fig)
        with st.expander("Analisis Kompleksitas Waktu"):
            st.markdown("""
            | Pendekatan | Kasus | Kompleksitas |
            | :--- | :--- | :--- |
            | **Iteratif** | Best | $\Theta(n_C)$ |
            | | Average | $\Theta(n_C \cdot n_M)$ |
            | | Worst | $\Theta(n_C \cdot n_M)$ |
            | **Rekursif** | Best | $\Theta(n_C)$ |
            | | Average | $\Theta(n_C \cdot n_M)$ |
            | | Worst | $\Theta(n_C \cdot n_M)$ |
            """)
    with col2:
        # display algorithms' correctnes
        st.subheader("Validasi Algoritma")
        if results_match:
            st.success("Kedua algoritma mengembalikan list 'Result' yang ekivalen.")
        else:
            st.error("Kedua algoritma tidak mengembalikan list 'Result' yang ekivalen.")
        st.divider()
        # display time performance basic stats
        iterative_average_execution_time = df['Waktu Eksekusi Algoritma Iteratif'].mean()
        recursive_average_execution_time = df['Waktu Eksekusi Algoritma Rekursif'].mean()
        if iterative_average_execution_time > 0:
            diff_factor = (recursive_average_execution_time / iterative_average_execution_time)
        else:
            diff_factor = 0
        st.metric(label="Pendekatan Iteratif", value=f"{iterative_average_execution_time:.6f}s")
        st.metric(label="Pendekatan Rekursif", value=f"{recursive_average_execution_time:.6f}s", delta=f"{diff_factor:.6f}x lebih lambat", delta_color="inverse")
    # display result returned by the algorithms
    if results_match:
        st.divider()
        st.subheader("Daftar Hasil Aktivitas Bebas Konflik")
        if len(iterative_result) > 0:
            df_result = pd.DataFrame(iterative_result)
            st.write(f"Ditemukan {len(iterative_result)} aktivitas kandidat yang tidak bentrok:")
            st.dataframe(df_result, use_container_width=True, hide_index=True)
        else:
            st.warning("Semua aktivitas kandidat bentrok dengan jadwal mandatory.")
    