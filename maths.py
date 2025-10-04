# maths.py
import streamlit as st
from sympy import symbols, sympify, lambdify
import mpmath as mp

st.set_page_config(page_title="Math Solver", page_icon="🧮", layout="centered")

st.title("🧮 Root Finder Web App")
st.write("ใส่สมการ เช่น `exp(x) - 3*x` หรือ `x**2 - 4` แล้วเลือกวิธีที่ต้องการ")

x = symbols('x')

def parse_function(expr_str):
    expr = sympify(expr_str)
    f = lambdify(x, expr, modules=['mpmath', 'math'])
    df = lambdify(x, expr.diff(x), modules=['mpmath', 'math'])
    return f, df

method = st.selectbox("เลือกวิธี", ["Bisection", "Newton-Raphson"])
expr_str = st.text_input("สมการ f(x) =", "exp(x) - 3*x")
tol = st.number_input("Tolerance (ค่าความคลาดเคลื่อน)", value=1e-6, format="%.1e")

f, df = parse_function(expr_str)

if method == "Bisection":
    a = st.number_input("ค่าเริ่มต้น a", value=0.0)
    b = st.number_input("ค่าเริ่มต้น b", value=1.0)
elif method == "Newton-Raphson":
    x0 = st.number_input("ค่าเริ่มต้น x0", value=0.5)

if st.button("คำนวณ"):
    try:
        if method == "Bisection":
            fa, fb = f(a), f(b)
            if fa*fb > 0:
                st.error("f(a) และ f(b) ต้องมีเครื่องหมายตรงข้าม!")
            else:
                for i in range(100):
                    c = (a + b) / 2
                    fc = f(c)
                    if abs(fc) < tol or abs(b - a)/2 < tol:
                        break
                    if fa * fc < 0:
                        b, fb = c, fc
                    else:
                        a, fa = c, fc
                st.success(f"Root ≈ {c:.6f}  |  f(c) = {fc:.6e}  |  Iterations = {i}")
        else:  # Newton
            xn = x0
            for i in range(100):
                fx = f(xn)
                dfx = df(xn)
                if abs(dfx) < 1e-12:
                    st.error("Derivative = 0, Newton หยุดการคำนวณ")
                    break
                xn1 = xn - fx/dfx
                if abs(fx) < tol or abs(xn1 - xn) < tol:
                    xn = xn1
                    break
                xn = xn1
            st.success(f"Root ≈ {xn:.6f}  |  f(x) = {f(xn):.6e}  |  Iterations = {i}")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
