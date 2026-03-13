
import streamlit as st
from PIL import Image
from datetime import datetime

# Import modules
from image_processor import ImageProcessor
from ocr import OCRExtractor
from gemini_client import GeminiClient
from equation_solver import EquationSolver
from mistake_detector import MistakeDetector
from export_utils import ExportUtils


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Math Tutor",
    page_icon="👩‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- CREATIVE CSS DESIGN ----------------
def load_css():
    st.markdown("""
    <style>

    .main-title{
        font-size:50px;
        text-align:center;
        font-weight:700;
        background: linear-gradient(90deg,#1e3c72,#2a5298);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        margin-bottom:10px;
    }

    .subtitle{
        text-align:center;
        font-size:20px;
        color:gray;
        margin-bottom:40px;
    }

    .feature-card{
        background:#f7f9fc;
        padding:25px;
        border-radius:15px;
        text-align:center;
        box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    }

    .step-card{
        background:#f0f4ff;
        padding:18px;
        border-radius:12px;
        margin-top:12px;
        border-left:5px solid #1e3c72;
    }

    .answer-box{
        background:#e6f3ff;
        padding:25px;
        border-radius:15px;
        border:2px solid #1e3c72;
        text-align:center;
        margin-top:20px;
    }

    .stButton>button{
        background:#1e3c72;
        color:white;
        border-radius:8px;
        font-weight:bold;
    }

    </style>
    """, unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
def init_session():

    if "history" not in st.session_state:
        st.session_state.history = []

    if "latex_equation" not in st.session_state:
        st.session_state.latex_equation = None

    if "solution" not in st.session_state:
        st.session_state.solution = None


# ---------------- MODULE INIT ----------------
@st.cache_resource
def init_modules():

    return {
        "image_processor": ImageProcessor(),
        "ocr": OCRExtractor(),
        "gemini": GeminiClient(),
        "solver": EquationSolver(),
        "mistake": MistakeDetector(),
        "export": ExportUtils()
    }


# ---------------- SIDEBAR ----------------
def sidebar():

    with st.sidebar:

        st.title("👩‍🏫 AI Math Tutor")

        page = st.radio(
            "Navigation",
            ["🏠 Home", "📝 Solve Problem", "📚 History", "❓ Help"]
        )

        st.markdown("---")

        st.info("""
Tips for best results

• Use good lighting  
• Keep equation centered  
• Write clearly  
• Avoid shadows
""")

    return page


# ---------------- HOME PAGE ----------------
def home():

    st.markdown('<div class="main-title">AI Math Tutor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Smart Algebra Learning Assistant</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="feature-card"><h3>📸 Image OCR</h3>Upload handwritten or printed equations</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="feature-card"><h3>🧮 Step Solver</h3>Understand each solving step clearly</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="feature-card"><h3>🎯 Mistake Finder</h3>Detect common student mistakes</div>', unsafe_allow_html=True)


# ---------------- SOLVE PAGE ----------------
def solve_page(modules):

    st.title("Solve Algebra Problem")

    col1, col2 = st.columns(2)

    with col1:

        uploaded_file = st.file_uploader(
            "Upload equation image",
            type=["png", "jpg", "jpeg","webp"]
        )

        if uploaded_file:

            image = Image.open(uploaded_file)

            st.image(image, caption="Uploaded Image")

            if st.button("🔍 Process Equation"):

                with st.spinner("Reading equation..."):

                    processed = modules["image_processor"].preprocess(image)

                    ocr_result = modules["ocr"].extract_text(processed)

                    # -------- FIXED ERROR HANDLING --------
                    if isinstance(ocr_result, dict):
                        text = ocr_result.get("text", "")
                        confidence = ocr_result.get("confidence", 0)

                    elif isinstance(ocr_result, str):
                        text = ocr_result
                        confidence = 1.0

                    else:
                        text = ""
                        confidence = 0
                    # -------------------------------------

                    if text:

                        latex = modules["gemini"].image_to_latex(image)

                        st.session_state.latex_equation = latex

                        st.success(f"Equation detected (confidence {confidence:.2%})")

                    else:

                        st.error("Equation could not be detected")


    with col2:

        if st.session_state.latex_equation:

            st.subheader("Detected Equation")

            st.latex(st.session_state.latex_equation)

            edited = st.text_area(
                "Edit equation if needed",
                value=st.session_state.latex_equation
            )

            st.session_state.latex_equation = edited

            if st.button("🧮 Solve Equation"):

                with st.spinner("Solving..."):

                    solution = modules["solver"].solve_equation(edited)

                    if "error" not in solution:

                        st.session_state.solution = solution

                        st.session_state.history.append({
                            "time": datetime.now(),
                            "equation": edited,
                            "solution": solution
                        })

                    else:

                        st.error(solution["error"])


    # ---------------- SHOW SOLUTION ----------------

    if st.session_state.solution:

        st.markdown("---")

        sol = st.session_state.solution

        st.subheader("Step-by-Step Solution")

        for step in sol.get("steps", []):

            st.markdown(
                f"""
<div class="step-card">
<b>Step {step.get('step')}</b><br>
{step.get('description')}
</div>
""",
                unsafe_allow_html=True
            )

        if sol.get("solutions"):

            st.markdown('<div class="answer-box">', unsafe_allow_html=True)

            st.subheader("Final Answer")

            for s in sol["solutions"]:
                st.latex(f"x = {s}")

            st.markdown("</div>", unsafe_allow_html=True)


# ---------------- HISTORY PAGE ----------------
def history_page():

    st.title("Solution History")

    if not st.session_state.history:

        st.info("No solved problems yet")

    else:

        for item in reversed(st.session_state.history):

            st.write(item["time"])

            st.latex(item["equation"])


# ---------------- HELP PAGE ----------------
def help_page():

    st.title("Help")

    st.write("""
Tips for taking equation photos

• Use bright lighting  
• Keep equation centered  
• Avoid shadows  
• Write clearly
""")


# ---------------- MAIN ----------------
def main():

    load_css()

    init_session()

    modules = init_modules()

    page = sidebar()

    if "Home" in page:
        home()

    elif "Solve" in page:
        solve_page(modules)

    elif "History" in page:
        history_page()

    elif "Help" in page:
        help_page()


if __name__ == "__main__":
    main()

