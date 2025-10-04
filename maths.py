import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


x = symbols("x")

# ฟังก์ชันสำหรับ parse สมการ
def parse_function(expr_str):
    expr = sympify(expr_str)
    f = lambdify(x, expr, modules=['numpy'])
    df = lambdify(x, expr.diff(x), modules=['numpy'])
    return f, df

def bisection(f, a, b, tol=1e-6, max_iter=100):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return None, "f(a) และ f(b) ต้องมีเครื่องหมายต่างกัน", []
    history = []
    for i in range(max_iter):
        c = (a+b)/2
        fc = f(c)
        history.append((i+1, c, fc))
        if abs(fc) < tol or (b-a)/2 < tol:
            return c, None, history
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return c, "ไม่คอนเวอร์จ์ใน {} รอบ".format(max_iter), history

def newton(f, df, x0, tol=1e-6, max_iter=100):
    history = []
    xn = x0
    for i in range(max_iter):
        fx = f(xn)
        dfx = df(xn)
        history.append((i+1, xn, fx))
        if abs(fx) < tol:
            return xn, None, history
        if abs(dfx) < 1e-12:
            return None, "อนุพันธ์ใกล้ศูนย์ Newton ล้มเหลว", history
        xn = xn - fx/dfx
    return xn, "ไม่คอนเวอร์จ์ใน {} รอบ".format(max_iter), history

# ---------------- Streamlit UI -----------------
st.title("🔢 Root Finder Web App")
st.write("ใส่สมการที่มี x แล้วเลือกวิธีแก้")

expr_str = st.text_input("สมการ (เช่น exp(x) - 3*x)", "exp(x) - 3*x")
method = st.selectbox("เลือกวิธีแก้", ["Bisection", "Newton-Raphson"])

f, df = parse_function(expr_str)

if method == "Bisection":
    a = st.number_input("ค่าเริ่มต้น a", value=0.0)
    b = st.number_input("ค่าเริ่มต้น b", value=1.0)
    if st.button("คำนวณ"):
        root, err, hist = bisection(f, a, b)
        if err:
            st.error(err)
        else:
            st.success(f"Root ≈ {root:.6f}, f(root) ≈ {f(root):.2e}")
            st.write("ตาราง Iterations:")
            st.dataframe(hist, use_container_width=True)
elif method == "Newton-Raphson":
    x0 = st.number_input("ค่าเริ่มต้น x0", value=0.6)
    if st.button("คำนวณ"):
        root, err, hist = newton(f, df, x0)
        if err:
            st.error(err)
        else:
            st.success(f"Root ≈ {root:.6f}, f(root) ≈ {f(root):.2e}")
            st.write("ตาราง Iterations:")
            st.dataframe(hist, use_container_width=True)

# Plot function
st.write("### กราฟฟังก์ชัน")
X = np.linspace(-2, 2, 400)
Y = f(X)
fig, ax = plt.subplots()
ax.axhline(0, color='black', lw=1)
ax.plot(X, Y, label=expr_str)
ax.legend()
st.pyplot(fig)
