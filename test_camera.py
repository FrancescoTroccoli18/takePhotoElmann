import streamlit as st
from PIL import Image
import io
import base64
from write_on_db import *

st.title("Acquisizione foto via QR")

# Recupero i parametri dall'URL
query_params = st.query_params()
token = query_params.get("token", [None])[0]
codice_test = query_params.get("test", [None])[0]
current_user = query_params.get("ut", [None])[0]

if token is None or codice_test is None:
    st.error("Token o Codice Test non presenti nell'URL!")
else:
    st.write(f"Token: {token}, Codice Test: {codice_test}")

    # Stato per mantenere l'immagine tra i rerun
    if "foto" not in st.session_state:
        st.session_state.foto = None
    if "base64_img" not in st.session_state:
        st.session_state.base64_img = None

    # Se non c'è immagine o si clicca "Riscatta", riapri fotocamera
    if st.session_state.foto is None:
        st.session_state.foto = st.camera_input("Scatta la foto")

    if st.session_state.foto is not None:
        # Converto in Base64
        img = Image.open(st.session_state.foto)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_img = buf.getvalue()
        st.session_state.base64_img = base64.b64encode(byte_img).decode("utf-8")

        st.image(img, caption="Immagine pronta per il salvataggio", use_column_width=True)

        # Pulsante per salvare
        if st.button("Conferma e Salva"):
            insert_photo(token, codice_test, st.session_state.base64_img, current_user)
            st.success("Salvata con successo!")
            # Resetta l'immagine dopo il salvataggio
            st.session_state.foto = None
            st.session_state.base64_img = None

    # Pulsante per riscattare (riaprire la fotocamera)
    if st.button("Riscatta"):
        st.session_state.foto = None
        st.rerun()
