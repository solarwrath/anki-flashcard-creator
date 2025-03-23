from typing import Optional, List
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class ImageSearchService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.cse_id = os.getenv('GOOGLE_CSE_ID')
        if not self.api_key or not self.cse_id:
            raise ValueError("Google API credentials not found in environment variables")
        
        self.service = build("customsearch", "v1", developerKey=self.api_key)

    def search_image(self, query: str, num_results: int = 5) -> List[str]:
        """
        Search for images using Google Custom Search API
        Returns a list of image URLs, or empty list if no results found
        """
        try:
            result = self.service.cse().list(
                q=query,
                cx=self.cse_id,
                searchType='image',
                num=num_results
            ).execute()

            if 'items' in result:
                return [item['link'] for item in result['items']]
            return []
            
        except Exception as e:
            print(f"Error searching for images: {e}")
            return [] 