"""
Google Reviews API Tool
Pulls Google Reviews for a specific business using Google Places API
"""
import os
import requests
from typing import List, Dict, Optional
import pandas as pd


class GoogleReviewsTool:
    """Tool for fetching Google Reviews of a business"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Google Reviews Tool
        
        Args:
            api_key: Google Places API key. If not provided, will use GOOGLE_API_KEY env var
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def search_place(self, business_name: str, location: str = "Western Massachusetts") -> Optional[str]:
        """
        Search for a place by name and location
        
        Args:
            business_name: Name of the business
            location: Location to search in (default: Western Massachusetts)
            
        Returns:
            Place ID if found, None otherwise
        """
        search_url = f"{self.base_url}/findplacefromtext/json"
        params = {
            'input': f"{business_name} {location}",
            'inputtype': 'textquery',
            'fields': 'place_id,name,formatted_address',
            'key': self.api_key
        }
        
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK' and data.get('candidates'):
                return data['candidates'][0]['place_id']
            else:
                print(f"No place found for '{business_name}' in {location}")
                return None
        except Exception as e:
            print(f"Error searching for place: {e}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information about a place including reviews
        
        Args:
            place_id: Google Place ID
            
        Returns:
            Dictionary with place details and reviews
        """
        details_url = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,formatted_address,rating,user_ratings_total,reviews,price_level,website,formatted_phone_number',
            'key': self.api_key
        }
        
        try:
            response = requests.get(details_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                return data.get('result', {})
            else:
                print(f"Error getting place details: {data.get('status')}")
                return None
        except Exception as e:
            print(f"Error fetching place details: {e}")
            return None
    
    def get_reviews(self, business_name: str, location: str = "Western Massachusetts") -> pd.DataFrame:
        """
        Get reviews for a business
        
        Args:
            business_name: Name of the business
            location: Location to search in
            
        Returns:
            DataFrame with review data
        """
        place_id = self.search_place(business_name, location)
        if not place_id:
            return pd.DataFrame()
        
        details = self.get_place_details(place_id)
        if not details:
            return pd.DataFrame()
        
        reviews = details.get('reviews', [])
        if not reviews:
            print(f"No reviews found for {business_name}")
            return pd.DataFrame()
        
        # Format reviews into a structured format
        review_data = []
        for review in reviews:
            review_data.append({
                'business_name': details.get('name', business_name),
                'author': review.get('author_name', 'Anonymous'),
                'rating': review.get('rating', 0),
                'text': review.get('text', ''),
                'time': review.get('time', ''),
                'relative_time': review.get('relative_time_description', '')
            })
        
        df = pd.DataFrame(review_data)
        
        # Add business summary info
        summary_info = {
            'business_address': details.get('formatted_address', ''),
            'overall_rating': details.get('rating', 0),
            'total_ratings': details.get('user_ratings_total', 0),
            'website': details.get('website', ''),
            'phone': details.get('formatted_phone_number', '')
        }
        
        # Add summary as attributes to the DataFrame
        for key, value in summary_info.items():
            df.attrs[key] = value
        
        return df
    
    def export_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        """
        Export reviews to CSV
        
        Args:
            df: DataFrame with review data
            filename: Output filename
            
        Returns:
            Path to the saved file
        """
        output_path = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        
        # Create a copy with summary info as first row
        if df.attrs:
            summary_df = pd.DataFrame([{
                'business_name': '=== BUSINESS SUMMARY ===',
                'author': df.attrs.get('business_address', ''),
                'rating': df.attrs.get('overall_rating', ''),
                'text': f"Total Ratings: {df.attrs.get('total_ratings', '')}",
                'time': df.attrs.get('website', ''),
                'relative_time': df.attrs.get('phone', '')
            }])
            export_df = pd.concat([summary_df, df], ignore_index=True)
        else:
            export_df = df
        
        export_df.to_csv(output_path, index=False)
        print(f"Reviews exported to {output_path}")
        return output_path
    
    def export_to_excel(self, df: pd.DataFrame, filename: str) -> str:
        """
        Export reviews to Excel
        
        Args:
            df: DataFrame with review data
            filename: Output filename
            
        Returns:
            Path to the saved file
        """
        output_path = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Write reviews
            df.to_excel(writer, sheet_name='Reviews', index=False)
            
            # Write summary on a separate sheet if attributes exist
            if df.attrs:
                summary_data = {
                    'Metric': list(df.attrs.keys()),
                    'Value': list(df.attrs.values())
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"Reviews exported to {output_path}")
        return output_path


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    
    tool = GoogleReviewsTool()
    
    # Example: Get reviews for a business
    reviews_df = tool.get_reviews("Big Y World Class Market", "Springfield MA")
    
    if not reviews_df.empty:
        print(f"\nFound {len(reviews_df)} reviews")
        print(reviews_df.head())
        
        # Export to CSV and Excel
        tool.export_to_csv(reviews_df, "google_reviews.csv")
        tool.export_to_excel(reviews_df, "google_reviews.xlsx")
