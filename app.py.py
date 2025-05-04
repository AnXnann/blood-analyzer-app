import streamlit as st
import pandas as pd
import datetime
import os

st.title("🩸 วิเคราะห์ผลเลือด (เลือดปลายนิ้ว)")

file_name = "data.csv"

# โหลดข้อมูลเก่า
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
else:
    df = pd.DataFrame(columns=["date", "glucose", "hemoglobin", "cholesterol"])
    df.to_csv(file_name, index=False)

with st.form("input_form"):
    date = st.date_input("วันที่ตรวจ", datetime.date.today())
    glucose = st.number_input("ระดับน้ำตาลในเลือด (mg/dL)", min_value=0, max_value=500)
    hemoglobin = st.number_input("ค่า Hemoglobin (g/dL)", min_value=0.0, max_value=20.0)
    cholesterol = st.number_input("ค่า Cholesterol (mg/dL)", min_value=0, max_value=400)


    submit_button = st.form_submit_button("✅ วิเคราะห์และบันทึก")

if submit_button:
    results = []

    # วิเคราะห์ glucose
    if glucose < 70:
        results.append("น้ำตาล: ❗ ต่ำเกินไป → ควรรับประทานอาหาร/น้ำหวาน")
    elif glucose <= 140:
        results.append("น้ำตาล: ✅ ปกติ")
    else:
        results.append("น้ำตาล: ⚠️ สูง → ควรตรวจซ้ำหรือปรึกษาแพทย์")

    # วิเคราะห์ hemoglobin
    if hemoglobin < 12:
        results.append("Hemoglobin: ❗ ต่ำ → อาจมีภาวะโลหิตจาง")
    elif hemoglobin <= 16:
        results.append("Hemoglobin: ✅ ปกติ")
    else:
        results.append("Hemoglobin: ⚠️ สูง → ควรตรวจเพิ่มเติม")

    # วิเคราะห์ cholesterol
    if cholesterol < 200:
        results.append("Cholesterol: ✅ ปกติ")
    elif cholesterol <= 239:
        results.append("Cholesterol: ⚠️ สูงเล็กน้อย → ควรปรับอาหาร")
    else:
        results.append("Cholesterol: ❗ สูง → ควรปรึกษาแพทย์")

    # แสดงผล
    st.subheader("ผลวิเคราะห์")
    for r in results:
        st.write(r)

    # บันทึกข้อมูล
    new_data = {
        "date": date,
        "glucose": glucose,
        "hemoglobin": hemoglobin,
        "cholesterol": cholesterol
    }
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(file_name, index=False)

    st.success("✅ บันทึกข้อมูลเรียบร้อยแล้ว")

# แสดงกราฟย้อนหลัง
st.subheader("📊 กราฟผลเลือดย้อนหลัง")
if df.empty or df["date"].isnull().all():
    st.info("ยังไม่มีข้อมูลย้อนหลัง")
else:
    df["date"] = pd.to_datetime(df["date"])
    df_sorted = df.sort_values("date")
    for col in ["glucose", "hemoglobin", "cholesterol"]:
        st.write(f"### {col}")
        st.line_chart(df_sorted.set_index("date")[col])

    with st.expander("📝 ดูข้อมูลย้อนหลัง"):
        st.dataframe(df_sorted.reset_index(drop=True))
