import streamlit as st
import pandas as pd
import pdfplumber
import json
import os
import time

# 🎨 Page Config
st.set_page_config(page_title="Smart File Converter", page_icon="📂", layout="wide")

# 📌 Sidebar Section
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📂 Upload File", "ℹ️ About"])

# 📌 Sidebar Extra Features
st.sidebar.markdown("---")
st.sidebar.subheader("🌟 More Features Coming Soon!")
st.sidebar.info("- AI-based File Insights\n- OCR for Image-to-Text\n- Secure File Storage")

# 📌 Page Routing
if page == "🏠 Home":
    st.title("📂 Smart File Converter & Analyzer")
    st.markdown("<h4 style='text-align:center;'>Easily convert and analyze your files (CSV, Excel, PDF, JSON, TXT)</h4><hr>", unsafe_allow_html=True)

elif page == "📂 Upload File":
    # 📌 **File Upload Section**
    st.subheader("📤 Upload Your File")
    uploaded_file = st.file_uploader("Drop your file here to convert (CSV, Excel, PDF, JSON, TXT)", type=["csv", "xlsx", "pdf", "json", "txt"])

    if uploaded_file:
        file_name = uploaded_file.name
        file_extension = file_name.split(".")[-1]

        # 📌 **Show File Name & Details**
        st.markdown(f"<p class='uploaded-file'>📄 Uploaded File: `{file_name}`</p>", unsafe_allow_html=True)

        # 📌 **Processing File Based on Type**
        with st.spinner("📂 Processing file..."):
            time.sleep(1.5)  # Simulate Loading

            if file_extension == "csv":
                df = pd.read_csv(uploaded_file)
            elif file_extension == "xlsx":
                df = pd.read_excel(uploaded_file)
            elif file_extension == "json":
                df = pd.DataFrame(json.load(uploaded_file))
            elif file_extension == "txt":
                df = pd.DataFrame({"Text": uploaded_file.read().decode("utf-8").splitlines()})
            elif file_extension == "pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                df = pd.DataFrame({"PDF Text": text.split("\n")})

            # 📌 **Basic File Summary**
            st.success(f"✅ Successfully processed `{file_name}`")
            st.subheader("📊 File Summary:")
            st.write(f"🔹 **Rows:** {df.shape[0]}  |  🔹 **Columns:** {df.shape[1]}")
            st.dataframe(df.head(10))  # Show first 10 rows

            # 📌 **Conversion Options**
            st.subheader("🔄 Convert File To:")
            convert_to = st.selectbox("Select format:", ["CSV", "Excel", "JSON", "TXT"])

            # 📌 **Convert & Download Button**
            if st.button("🚀 Convert & Download"):
                with st.spinner("🔄 Converting file..."):
                    time.sleep(2)  # Simulate processing
                    converted_file = f"converted_file.{convert_to.lower()}"

                    if convert_to == "CSV":
                        df.to_csv(converted_file, index=False)
                    elif convert_to == "Excel":
                        df.to_excel(converted_file, index=False)
                    elif convert_to == "JSON":
                        df.to_json(converted_file, orient="records", indent=4)
                    elif convert_to == "TXT":
                        df.to_csv(converted_file, index=False, sep="\t")
                
                # ✅ **Download Section**
                st.success(f"🎉 File converted successfully to `{convert_to}`!")
                with open(converted_file, "rb") as f:
                    st.download_button("📥 Download Converted File", f, file_name=converted_file)

                os.remove(converted_file)  # Cleanup temporary file

elif page == "ℹ️ About":
    st.title("ℹ️ About Smart File Converter")
    st.markdown("""
    - **Version:** 1.0.0
    - **Developed By:** Iqra Khan
    - **Features:** Convert and analyze files easily.
    - **Upcoming Features:** AI-based document processing.
    """)

# 📌 Footer
st.markdown("<p class='footer'>🔹 Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
