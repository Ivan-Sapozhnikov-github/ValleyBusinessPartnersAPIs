"""
Competitors API Tool
Finds competitors in the same region using Google Places API
"""
import os
import requests
from typing import List, Dict, Optional
import pandas as pd


class CompetitorsTool:
    """Tool for finding competitors in a specific region"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Competitors Tool
        
        Args:
            api_key: Google Places API key. If not provided, will use GOOGLE_API_KEY env var
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def geocode_location(self, location: str) -> Optional[Dict]:
        """
        Get coordinates for a location
        
        Args:
            location: Location string (e.g., "Springfield, MA")
            
        Returns:
            Dictionary with lat/lng coordinates
        """
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': location,
            'key': self.api_key
        }
        
        try:
            response = requests.get(geocode_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK' and data.get('results'):
                location_data = data['results'][0]['geometry']['location']
                return {
                    'lat': location_data['lat'],
                    'lng': location_data['lng']
                }
            else:
                print(f"Could not geocode location: {location}")
                return None
        except Exception as e:
            print(f"Error geocoding location: {e}")
            return None
    
    def search_competitors(self, business_type: str, location: str, radius: int = 25000) -> List[Dict]:
        """
        Search for competitors in a specific area
        
        Args:
            business_type: Type of business (e.g., "restaurant", "retail store")
            location: Location to search around
            radius: Search radius in meters (default: 25km)
            
        Returns:
            List of competitor businesses
        """
        coords = self.geocode_location(location)
        if not coords:
            return []
        
        # Use nearby search
        search_url = f"{self.base_url}/nearbysearch/json"
        params = {
            'location': f"{coords['lat']},{coords['lng']}",
            'radius': radius,
            'keyword': business_type,
            'key': self.api_key
        }
        
        competitors = []
        
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                for place in data.get('results', []):
                    competitor = {
                        'name': place.get('name', ''),
                        'address': place.get('vicinity', ''),
                        'rating': place.get('rating', 0),
                        'user_ratings_total': place.get('user_ratings_total', 0),
                        'place_id': place.get('place_id', ''),
                        'types': ', '.join(place.get('types', [])),
                        'price_level': place.get('price_level', 'N/A'),
                        'business_status': place.get('business_status', 'UNKNOWN')
                    }
                    competitors.append(competitor)
                
                # Handle pagination if there's a next_page_token
                next_page_token = data.get('next_page_token')
                if next_page_token:
                    import time
                    time.sleep(2)  # Required delay before using next_page_token
                    
                    next_params = {
                        'pagetoken': next_page_token,
                        'key': self.api_key
                    }
                    next_response = requests.get(search_url, params=next_params)
                    next_data = next_response.json()
                    
                    if next_data.get('status') == 'OK':
                        for place in next_data.get('results', []):
                            competitor = {
                                'name': place.get('name', ''),
                                'address': place.get('vicinity', ''),
                                'rating': place.get('rating', 0),
                                'user_ratings_total': place.get('user_ratings_total', 0),
                                'place_id': place.get('place_id', ''),
                                'types': ', '.join(place.get('types', [])),
                                'price_level': place.get('price_level', 'N/A'),
                                'business_status': place.get('business_status', 'UNKNOWN')
                            }
                            competitors.append(competitor)
            
            return competitors
            
        except Exception as e:
            print(f"Error searching for competitors: {e}")
            return []
    
    def get_competitors_dataframe(self, business_type: str, location: str, radius: int = 25000) -> pd.DataFrame:
        """
        Get competitors as a pandas DataFrame
        
        Args:
            business_type: Type of business
            location: Location to search around
            radius: Search radius in meters
            
        Returns:
            DataFrame with competitor data
        """
        competitors = self.search_competitors(business_type, location, radius)
        
        if not competitors:
            print(f"No competitors found for '{business_type}' near {location}")
            return pd.DataFrame()
        
        df = pd.DataFrame(competitors)
        
        # Sort by rating and number of reviews
        if not df.empty:
            df = df.sort_values(by=['rating', 'user_ratings_total'], ascending=False)
        
        return df
    
    def export_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        """
        Export competitors to CSV
        
        Args:
            df: DataFrame with competitor data
            filename: Output filename
            
        Returns:
            Path to the saved file
        """
        output_path = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        
        df.to_csv(output_path, index=False)
        print(f"Competitors exported to {output_path}")
        return output_path
    
    def export_to_excel(self, df: pd.DataFrame, filename: str) -> str:
        """
        Export competitors to Excel
        
        Args:
            df: DataFrame with competitor data
            filename: Output filename
            
        Returns:
            Path to the saved file
        """
        output_path = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Competitors', index=False)
            
            # Add summary statistics
            if not df.empty:
                summary_data = {
                    'Metric': [
                        'Total Competitors',
                        'Average Rating',
                        'Median Rating',
                        'Total Reviews',
                        'Average Reviews per Business'
                    ],
                    'Value': [
                        len(df),
                        df['rating'].mean() if 'rating' in df.columns else 0,
                        df['rating'].median() if 'rating' in df.columns else 0,
                        df['user_ratings_total'].sum() if 'user_ratings_total' in df.columns else 0,
                        df['user_ratings_total'].mean() if 'user_ratings_total' in df.columns else 0
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        print(f"Competitors exported to {output_path}")
        return output_path


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    
    tool = CompetitorsTool()
    
    # Example: Find competitors for a grocery store in Western Massachusetts
    competitors_df = tool.get_competitors_dataframe(
        business_type="grocery store",
        location="Springfield, MA",
        radius=25000  # 25km radius
    )
    
    if not competitors_df.empty:
        print(f"\nFound {len(competitors_df)} competitors")
        print(competitors_df.head(10))
        
        # Export to CSV and Excel
        tool.export_to_csv(competitors_df, "competitors.csv")
        tool.export_to_excel(competitors_df, "competitors.xlsx")
