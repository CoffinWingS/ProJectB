# maths.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, symbols, lambdify, diff

# ---------------------------
# Helper Functions
# ---------------------------
x = symbols('x')

def parse_function(expr_str):
    try:
        expr = sympify(expr_str)
        f = lambdify(x, expr, modules=['numpy'])
        df = lambdify(x, diff(expr, x), modules=['numpy'])
        return f, df, None
    except Exception as e:
        return None, None, str(e)

def bisection(f, a, b, tol=1e-6, max_iter=100):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) และ f(b) ต้องมีค่าต่างเครื่องหมายกัน")

    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c, fc, i + 1
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c, fc, max_iter

def newton(f, df, x0, tol=1e-6, max_iter=100):
    x_curr = x0
    for i in range(max_iter):
        fx = f(x_curr)
        dfx = df(x_curr)
        if abs(dfx) < 1e-12:
            raise ZeroDivisionError("ค่าลูกอนุพันธ์เป็นศูนย์ ทำให้ Newton-Raphson ล้มเหลว")
        x_next = x_curr - fx / dfx
        if abs(fx) < tol or abs(x_next - x_curr) < tol:
            return x_next, f(x_next), i + 1
        x_curr = x_next
    return x_curr, f(x_curr), max_iter

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🧮 โปรแกรมระเบียบวิธีแก้สมการ (Root Finding Methods)")
st.markdown("ระบุสมการ เช่น `exp(x) - 3*x` หรือ `x**3 - x - 2`")

expr_str = st.text_input("สมการ f(x) =", "exp(x) - 3*x")

method = st.selectbox(
    "เลือกวิธีการแก้สมการ",
    ["Bisection", "Newton-Raphson"]
)

f, df, error = parse_function(expr_str)
if error:
    st.error(f"เกิดข้อผิดพลาดในการอ่านสมการ: {error}")
    st.stop()

if method == "Bisection":
    a = st.number_input("ค่า a (เริ่มต้นช่วง)", value=0.0)
    b = st.number_input("ค่า b (สิ้นสุดช่วง)", value=1.0)
else:
    x0 = st.number_input("ค่าตั้งต้น x₀", value=0.6)

tol = st.number_input("ค่า tolerance (ความแม่นยำ)", value=1e-6, format="%.1e")
max_iter = st.number_input("จำนวนรอบสูงสุด", value=100, step=10)

if st.button("คำนวณ"):
    try:
        if method == "Bisection":
            root, fval, iters = bisection(f, a, b, tol, max_iter)
        else:
            root, fval, iters = newton(f, df, x0, tol, max_iter)

        st.success(f"ผลลัพธ์: x ≈ {root:.6f}, f(x) = {fval:.6e}, รอบ = {iters}")

        # กราฟ
        x_vals = np.linspace(root - 2, root + 2, 400)
        y_vals = f(x_vals)
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label='f(x)')
        ax.axhline(0, color='black', linestyle='--')
        ax.axvline(root, color='red', linestyle='--', label=f'Root ≈ {root:.6f}')
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
