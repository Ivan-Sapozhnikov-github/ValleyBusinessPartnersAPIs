import requests
import pandas as pd
from datetime import datetime
import json

def search_grants(keyword="", 
                  agencies="", 
                  opp_statuses="forecasted|posted", 
                  funding_categories="",
                  eligibilities="",
                  aln="",
                  rows=100):
    """
    Search for grants on grants.gov
    
    Parameters:
    - keyword: Search keyword (e.g., "technology", "education")
    - agencies: Agency codes separated by | (e.g., "HHS|DOE")
    - opp_statuses: Status of opportunities separated by | 
                    Options: "forecasted", "posted", "closed", "archived"
                    Default: "forecasted|posted"
    - funding_categories: Category codes (e.g., "HL" for Health, "ED" for Education)
    - eligibilities: Eligibility codes
    - aln: Assistance Listing Number
    - rows: Number of results to return (default 100)
    
    Returns:
    - DataFrame with grant opportunities
    """
    
    url = "https://api.grants.gov/v1/api/search2"
    
    # Prepare request body
    payload = {
        "rows": rows,
        "keyword": keyword,
        "oppNum": "",
        "eligibilities": eligibilities,
        "agencies": agencies,
        "oppStatuses": opp_statuses,
        "aln": aln,
        "fundingCategories": funding_categories
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print(f"Searching grants.gov with parameters:")
        print(f"  Keyword: {keyword if keyword else 'None'}")
        print(f"  Agencies: {agencies if agencies else 'All'}")
        print(f"  Status: {opp_statuses}")
        print(f"  Max results: {rows}\n")
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        # Check for errors
        if data.get('errorcode', 1) != 0:
            print(f"API Error: {data.get('msg', 'Unknown error')}")
            return pd.DataFrame()
        
        # Extract opportunities
        opportunities = data.get('data', {}).get('oppHits', [])
        hit_count = data.get('data', {}).get('hitCount', 0)
        
        print(f"Found {hit_count} total grants")
        print(f"Retrieved {len(opportunities)} grants\n")
        
        if not opportunities:
            print("No grants found matching criteria")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(opportunities)
        
        # Convert ALN list to string if present
        if 'alnist' in df.columns:
            df['aln_numbers'] = df['alnist'].apply(lambda x: ', '.join(x) if isinstance(x, list) else '')
            df = df.drop('alnist', axis=1)
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return pd.DataFrame()
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return pd.DataFrame()


def export_to_excel(df, filename=None):
    """
    Export DataFrame to Excel file
    
    Parameters:
    - df: DataFrame to export
    - filename: Output filename (default: grants_YYYYMMDD_HHMMSS.xlsx)
    """
    
    if df.empty:
        print("No data to export")
        return
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"grants_{timestamp}.xlsx"
    
    try:
        # Export to Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"✓ Successfully exported {len(df)} grants to {filename}")
        
    except Exception as e:
        print(f"Error exporting to Excel: {e}")


# Example usage
if __name__ == "__main__":
    
    # Example 1: Search for all open health-related grants
    print("=" * 60)
    print("EXAMPLE 1: Health grants")
    print("=" * 60)
    df = search_grants(
        keyword="health",
        opp_statuses="posted",
        rows=50
    )
    
    if not df.empty:
        print("\nSample results:")
        print(df[['number', 'title', 'agencyName', 'openDate', 'closeDate']].head())
        export_to_excel(df, "health_grants.xlsx")
    
    print("\n")
    
    # Example 2: Search by specific agency
    print("=" * 60)
    print("EXAMPLE 2: Department of Education grants")
    print("=" * 60)
    df = search_grants(
        agencies="ED",
        opp_statuses="forecasted|posted",
        rows=50
    )
    
    if not df.empty:
        print("\nSample results:")
        print(df[['number', 'title', 'agencyName', 'oppStatus']].head())
        export_to_excel(df, "education_grants.xlsx")
    
    print("\n")
    
    # Example 3: Search for technology grants
    print("=" * 60)
    print("EXAMPLE 3: Technology grants")
    print("=" * 60)
    df = search_grants(
        keyword="technology",
        opp_statuses="posted",
        rows=30
    )
    
    if not df.empty:
        export_to_excel(df, "technology_grants.xlsx")