import uvicorn
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    # Load environment variables
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    
    # Get port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # We pass the import string instead of the object so reload works
    uvicorn.run(
        "api.app:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True
    )
