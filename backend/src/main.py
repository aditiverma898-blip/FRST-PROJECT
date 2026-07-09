import uvicorn
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    
    # We pass the import string instead of the object so reload works
    uvicorn.run(
        "api.app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
