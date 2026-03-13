# run.py
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check for API key
if not os.getenv('GEMINI_API_KEY'):
    print("⚠️  Warning: GEMINI_API_KEY not found in .env file")
    print("Please add your API key to .env file")
    sys.exit(1)

# Run Streamlit app
os.system('streamlit run app.py')