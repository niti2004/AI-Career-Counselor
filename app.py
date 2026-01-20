import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the Flask app from backend
from backend.app import app

# Get environment variables for API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure environment variables are set (for production)
if not OPENAI_API_KEY and not GOOGLE_API_KEY:
    print("⚠️ Warning: No API keys found. Some features may not work.")
    print("Set OPENAI_API_KEY or GOOGLE_API_KEY environment variables.")

if __name__ == "__main__":
    # Run on 0.0.0.0 to be accessible from outside (required for Render)
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
