
import streamlit as st
import pandas as pd
import os
from PIL import Image

st.set_page_config(page_title="Intersectional Analysis Dashboard", layout="wide")

st.title("📊 Mentor & Mentee Intersectional Analysis Dashboard")
st.markdown("Explore 1-way to 4-way intersectional analyses with interpretations and visuals.")

# Utility functions
def display_image_with_caption(img_path, caption):
    st.image(img_path, use_column_width=True, caption=caption)

def read_text(file_path):
    with open(file_path, "r") as file:
        return file.read()

def try_read_table(file_path):
    try:
        delim = "\t" if "\t" in open(file_path).read(200) else ","
        return pd.read_csv(file_path, delimiter=delim)
    except:
        return None

# Root folders
root_dirs = {
    "Mentor": "mentor_IA_final",
    "Mentee": "mentee_IA_final"
}

group = st.sidebar.radio("Select Group", list(root_dirs.keys()))
level = st.sidebar.radio("Analysis Level", ["1-way", "2-way", "3-way", "4-way"])

base_path = os.path.join(root_dirs[group], level)

# === 1-WAY SPECIAL HANDLING ===
if level == "1-way":
    st.header(f"🔍 1-Way Analysis for {group}")
    tab_names = ["Gender", "Race", "Career Stage", "Parent Education"]
    file_keys = {
        "Gender": "Gender_Category",
        "Race": "Race_Categories",
        "Career Stage": "CareerStage_NRMNCC_4",
        "Parent Education": "ParentGuardianEducation"
    }

    tabs = st.tabs(tab_names)
    for i, key in enumerate(file_keys):
        with tabs[i]:
            file_root = file_keys[key]
            image_dir = os.path.join(base_path, "images")
            txt_dir = os.path.join(base_path, "txt")
            csv_dir = os.path.join(base_path, "csv")

            boxplot_file = f"{file_root}_boxplot.png"
            txt_file = f"{file_root}_counts.txt"
            csv_file = f"{file_root}_counts.csv"

            # Image
            img_path = os.path.join(image_dir, boxplot_file)
            if os.path.exists(img_path):
                st.subheader(f"{key} Boxplot")
                display_image_with_caption(img_path, f"Distribution by {key}")

            # Table
            csv_path = os.path.join(csv_dir, csv_file)
            if os.path.exists(csv_path):
                df = try_read_table(csv_path)
                if df is not None:
                    st.subheader(f"{key} Summary Table")
                    st.dataframe(df)

            # Interpretation
            txt_path = os.path.join(txt_dir, txt_file)
            if os.path.exists(txt_path):
                st.subheader(f"Interpretation for {key}")
                st.markdown("```text\n" + read_text(txt_path) + "\n```")
            else:
                st.info("No interpretation available.")

# === 4-WAY SPECIAL HANDLING ===
elif level == "4-way":
    st.header(f"📊 4-Way Comprehensive Analysis for {group}")

    files = sorted(os.listdir(base_path))
    csvs = [f for f in files if f.endswith(".csv")]
    images = [f for f in files if f.endswith((".png", ".jpg", ".jpeg"))]

    for img in images:
        img_path = os.path.join(base_path, img)
        display_image_with_caption(img_path, img)

    for csv_file in csvs:
        csv_path = os.path.join(base_path, csv_file)
        st.subheader(f"📄 Data: {csv_file}")
        try:
            df = pd.read_csv(csv_path)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading {csv_file}: {e}")

# === 2- AND 3-WAY ===
else:
    st.header(f"{level.upper()} Intersectional Analysis for {group}")
    if os.path.exists(base_path):
        folders = sorted([f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))])
        if folders:
            selected_folder = st.selectbox("Select an Intersection", folders)
            folder_path = os.path.join(base_path, selected_folder)
            images_path = os.path.join(folder_path, "images")
            analysis_path = os.path.join(folder_path, "analysis.txt")

            if os.path.exists(images_path):
                images = sorted([img for img in os.listdir(images_path) if img.endswith((".png", ".jpg", ".jpeg"))])
                for img in images:
                    display_image_with_caption(os.path.join(images_path, img), img)
            else:
                st.warning("No images folder found.")

            if os.path.exists(analysis_path):
                st.subheader("📄 Interpretation")
                st.markdown("```text\n" + read_text(analysis_path) + "\n```")
            else:
                st.info("No analysis summary found.")
        else:
            st.warning("No intersection folders found.")
    else:
        st.error("Selected analysis level directory not found.")
