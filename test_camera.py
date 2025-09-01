import streamlit as st
import pandas as pd
from PIL import Image
import io
import qrcode

st.title("Acquisizione foto via QR")

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["image_bytes"])

# URL pubblico della tua app
url_pubblico = "https://tuo_url_pubblico"

# Genero il QR code
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(url_pubblico)
qr.make(fit=True)
img_qr = qr.make_image(fill_color="black", back_color="white")

# --- FIX: converto PIL.Image in bytes ---
buf = io.BytesIO()
img_qr.save(buf, format="PNG")
qr_bytes = buf.getvalue()

# Mostro il QR code
st.image(qr_bytes, caption="Scansiona il QR per aprire la pagina sul telefono")

# Input fotocamera
foto = st.camera_input("Scatta la foto")

if foto is not None:
    img = Image.open(foto)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_img = buf.getvalue()

    new_row = pd.DataFrame({"image_bytes": [byte_img]})
    st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

    st.image(img, caption="Immagine salvata", use_column_width=True)
    st.success("Immagine salvata nel DataFrame!")
    st.write(st.session_state.df)
