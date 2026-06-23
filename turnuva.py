# --- GRUP VE MAÇ EKRANLARI (GÜNCELLENMİŞ YAPI) ---
for i in range(4):
    grup_id = f"Grup {i+1}"
    with tabs[i]:
        st.subheader(f"{grup_id} Takımları")
        for t_idx in range(4):
            st.session_state.takimlar[grup_id][t_idx] = st.text_input(f"{t_idx+1}. Takım", value=st.session_state.takimlar[grup_id][t_idx], key=f"inp_{grup_id}_{t_idx}")
        
        t = st.session_state.takimlar[grup_id]
        program = {"1. Gün": [(t[0], t[3]), (t[1], t[2])], "2. Gün": [(t[0], t[1]), (t[2], t[3])], "3. Gün": [(t[0], t[2]), (t[1], t[3])]}
        
        for gun, maclar in program.items():
            with st.expander(f"📅 {gun} Maçları"):
                for m1, m2 in maclar:
                    st.markdown(f"#### {m1} vs {m2}")
                    # 3 maç tipi için döngü
                    for tur in ["Tekler 1", "Tekler 2", "Çiftler"]:
                        st.write(f"**{tur}**")
                        key = f"{grup_id}_{gun}_{m1}_{m2}_{tur}"
                        if key not in st.session_state.skorlar: st.session_state.skorlar[key] = ["0","0","0","0","0","0"]
                        
                        # 3 Set (2şerli giriş)
                        cols = st.columns(6)
                        cols[0].text_input("1.Set (K)", value=st.session_state.skorlar[key][0], key=f"{key}_0")
                        cols[1].text_input("1.Set (V)", value=st.session_state.skorlar[key][1], key=f"{key}_1")
                        cols[2].text_input("2.Set (K)", value=st.session_state.skorlar[key][2], key=f"{key}_2")
                        cols[3].text_input("2.Set (V)", value=st.session_state.skorlar[key][3], key=f"{key}_3")
                        cols[4].text_input("3.Set (K)", value=st.session_state.skorlar[key][4], key=f"{key}_4")
                        cols[5].text_input("3.Set (V)", value=st.session_state.skorlar[key][5], key=f"{key}_5")
