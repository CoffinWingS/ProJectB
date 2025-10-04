import streamlit as st
import math
from sympy import sympify, symbols, lambdify

# -----------------------------
# ตั้งค่า Streamlit Page
# -----------------------------
st.set_page_config(page_title="โปรแกรมแก้สมการโดยระเบียบวิธีแก้ตำแหน่งผิด", page_icon="🧮", layout="centered")
st.title("🔢 โปรแกรมระเบียบวิธีแก้ตำแหน่งผิด (False Position Method)")

col1= st.columns(1)
    with col1:
        st.image("./img/math.jpg", use_container_width=True)

st.write("ใส่สมการในรูปแบบที่ใช้ `x` เป็นตัวแปร เช่น `exp(x) - 3*x` หรือ `e**x - 3*x` นะครับ(~ o ​​¯▽¯) ~ o   " )

# -----------------------------
# รับข้อมูลจากผู้ใช้
# -----------------------------
expr_str = st.text_input("ใส่สมการ f(x) =", "exp(x) - 3*x")
a = st.number_input("ค่าเริ่มต้น A", value=0.6, step=0.05)
b = st.number_input("ค่าเริ่มต้น B", value=0.625, step=0.05)
tolerance = st.number_input("ค่าความคลาดเคลื่อน (Tolerance)", value=0.0001, step=0.0001, format="%.6f")

# -----------------------------
# สร้างฟังก์ชันจากข้อความสมการ
# -----------------------------
x = symbols('x')
try:
    expr = sympify(expr_str)
    f = lambdify(x, expr, modules=['math'])
except Exception as e:
    st.error("สมการไม่ถูกต้อง! (@ _ @ ;)  ตรวจสอบรูปแบบการเขียนอีกครั้ง เช่น exp(x)-3*x")
    st.stop()

# -----------------------------
# ระเบียบวิธีแก้ตำแหน่งผิด (False Position)
# -----------------------------
def false_position(f, a, b, tol=1e-6, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("ฟังก์ชันที่จุด A และ B ต้องมีเครื่องหมายต่างกัน (f(A)*f(B) < 0)")

    results = []
    for i in range(1, max_iter+1):
        # คำนวณจุด c ตามสูตร
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        results.append((i, a, b, c, fa, fb, fc))

        # ตรวจสอบการหยุด
        if abs(fc) < tol:
            break

        # ปรับช่วงใหม่
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return results

# -----------------------------
# ปุ่มรัน
# -----------------------------
if st.button("เริ่มคำนวณ"):
    try:
        data = false_position(f, a, b, tol=tolerance)
        st.success("คำนวณเสร็จสิ้น!(ﾉ◕ヮ◕)ﾉ  ✅")

        # แสดงตารางผลลัพธ์
        import pandas as pd
        df = pd.DataFrame(data, columns=["รอบ", "A", "B", "C", "f(A)", "f(B)", "f(C)"])
        st.dataframe(df.style.format(precision=6), use_container_width=True)

        # แสดงผลรอบสุดท้าย
        last = df.iloc[-1]
        st.write(f"**คำตอบสุดท้าย:** c = {last['C']:.6f}")
        st.write(f"**f(c) = {last['f(C)']:.6f}**")
        if abs(last['f(C)']) < tolerance:
            st.success("✅ ใกล้ศูนย์เพียงพอแล้ว ถือเป็นคำตอบที่ดีมากๆๆ(╯3╰)╭♡")
        else:
            st.warning("⚠ ยังไม่ถึงเกณฑ์ tolerance ที่กำหนด")

        # แสดงขั้นตอนละเอียด
        st.subheader("🧮 ขั้นตอนการคำนวณ")
        for i, row in df.iterrows():
            st.markdown(
                f"**รอบที่ {int(row['รอบ'])}:** "
                f"A = {row['A']:.6f}, B = {row['B']:.6f}, C = {row['C']:.6f}, "
                f"f(A) = {row['f(A)']:.6f}, f(B) = {row['f(B)']:.6f}, f(C) = {row['f(C)']:.6f}"
            )

        # กราฟฟังก์ชัน
        import numpy as np
        import matplotlib.pyplot as plt

        st.subheader("📈 กราฟแสดงฟังก์ชันและจุด C")

        X = np.linspace(a - 0.5, b + 0.5, 200)
        Y = [f(xi) for xi in X]

        plt.figure(figsize=(6,4))
        plt.axhline(0, color='gray', linestyle='--')
        plt.plot(X, Y, label='f(x)')
        plt.scatter(df["C"], df["f(C)"], color='red', label='Point C (each round)')
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title('Graph showing the finding of roots using the method of correcting the wrong position')
        st.pyplot(plt)

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
