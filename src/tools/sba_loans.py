"""
SBA Loans API Tool
Connects to US Government SBA API to pull loan rates and data
"""
import os
import requests
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime


class SBALoansTool:
    """Tool for fetching SBA loan data and rates"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the SBA Loans Tool
        
        Args:
            api_key: SBA API key (if required). If not provided, will use SBA_API_KEY env var
        """
        self.api_key = api_key or os.getenv('SBA_API_KEY')
        # SBA.gov data is often available through data.sba.gov
        self.base_url = "https://data.sba.gov/api/sba"
    
    def get_loan_rates(self) -> pd.DataFrame:
        """
        Get current SBA loan rates
        
        Returns:
            DataFrame with loan rate information
        """
        # Note: This is a mock implementation as the actual SBA API structure
        # may vary. You'll need to adjust based on the actual API endpoints.
        
        # Common SBA loan programs
        loan_programs = [
            {
                'program': 'SBA 7(a) Loan',
                'max_loan_amount': '$5,000,000',
                'rate_type': 'Variable',
                'base_rate': 'Prime Rate + spread',
                'typical_spread': '2.25% - 2.75%',
                'guarantee': '75-85%',
                'use_case': 'Working capital, equipment, real estate'
            },
            {
                'program': 'SBA 504 Loan',
                'max_loan_amount': '$5,500,000',
                'rate_type': 'Fixed',
                'base_rate': '10-year Treasury + spread',
                'typical_spread': '~2.0%',
                'guarantee': 'Up to 40%',
                'use_case': 'Real estate, equipment (long-term fixed assets)'
            },
            {
                'program': 'SBA Microloan',
                'max_loan_amount': '$50,000',
                'rate_type': 'Variable',
                'base_rate': 'Varies by intermediary',
                'typical_spread': '8% - 13%',
                'guarantee': 'N/A',
                'use_case': 'Working capital, inventory, supplies'
            },
            {
                'program': 'SBA Express Loan',
                'max_loan_amount': '$500,000',
                'rate_type': 'Variable or Fixed',
                'base_rate': 'Prime Rate + spread',
                'typical_spread': '4.5% - 6.5%',
                'guarantee': '50%',
                'use_case': 'Quick funding, working capital'
            }
        ]
        
        df = pd.DataFrame(loan_programs)
        df['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        
        return df
    
    def search_loans_by_state(self, state_code: str = "MA", limit: int = 100) -> pd.DataFrame:
        """
        Search for SBA loans by state
        
        Args:
            state_code: Two-letter state code (default: MA for Massachusetts)
            limit: Maximum number of records to return
            
        Returns:
            DataFrame with loan data
        """
        # This endpoint structure is based on data.sba.gov open data
        # The actual endpoint may need adjustment based on current API
        endpoint = f"{self.base_url}/loans"
        
        params = {
            'state': state_code,
            'limit': limit
        }
        
        if self.api_key:
            params['api_key'] = self.api_key
        
        try:
            # Try to fetch real data
            response = requests.get(endpoint, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict) and 'results' in data:
                    return pd.DataFrame(data['results'])
            
            # If API call fails, return mock data for demonstration
            print(f"Note: Unable to fetch live SBA data (status: {response.status_code}). Returning sample structure.")
            return self._get_sample_loan_data(state_code)
            
        except Exception as e:
            print(f"Error fetching SBA loan data: {e}")
            print("Returning sample loan data structure.")
            return self._get_sample_loan_data(state_code)
    
    def _get_sample_loan_data(self, state_code: str) -> pd.DataFrame:
        """
        Generate sample loan data for demonstration
        
        Args:
            state_code: State code
            
        Returns:
            DataFrame with sample data
        """
        sample_data = [
            {
                'loan_number': 'SBA-2024-001',
                'borrower_name': 'Sample Business 1',
                'borrower_state': state_code,
                'approval_date': '2024-01-15',
                'loan_amount': 250000,
                'program': '7(a)',
                'term_months': 120,
                'jobs_supported': 5,
                'business_type': 'Retail'
            },
            {
                'loan_number': 'SBA-2024-002',
                'borrower_name': 'Sample Business 2',
                'borrower_state': state_code,
                'approval_date': '2024-02-20',
                'loan_amount': 500000,
                'program': '504',
                'term_months': 240,
                'jobs_supported': 12,
                'business_type': 'Manufacturing'
            },
            {
                'loan_number': 'SBA-2024-003',
                'borrower_name': 'Sample Business 3',
                'borrower_state': state_code,
                'approval_date': '2024-03-10',
                'loan_amount': 35000,
                'program': 'Microloan',
                'term_months': 72,
                'jobs_supported': 2,
                'business_type': 'Service'
            }
        ]
        
        df = pd.DataFrame(sample_data)
        df.attrs['note'] = "This is sample data. Connect to actual SBA API for real data."
        return df
    
    def get_historical_rates(self, years: int = 5) -> pd.DataFrame:
        """
        Get historical SBA loan rate trends
        
        Args:
            years: Number of years of historical data
            
        Returns:
            DataFrame with historical rate data
        """
        # Note: This would need to be connected to actual historical data source
        # For now, returning a sample structure
        
        from datetime import timedelta
        
        historical_data = []
        base_date = datetime.now()
        
        for i in range(years * 4):  # Quarterly data
            quarter_date = base_date - timedelta(days=i*90)
            historical_data.append({
                'date': quarter_date.strftime('%Y-%m-%d'),
                'quarter': f"Q{((quarter_date.month-1)//3)+1} {quarter_date.year}",
                'prime_rate': 8.5 - (i * 0.05),  # Sample declining trend
                'sba_7a_rate': 10.75 - (i * 0.05),
                'sba_504_rate': 6.5 - (i * 0.03),
                'treasury_10yr': 4.2 - (i * 0.04)
            })
        
        df = pd.DataFrame(historical_data)
        df = df.sort_values('date')
        df.attrs['note'] = "Sample historical data. Connect to actual data source for real rates."
        return df
    
    def analyze_loan_eligibility(self, business_info: Dict[str, any]) -> Dict[str, any]:
        """
        Analyze loan eligibility based on business information
        
        Args:
            business_info: Dictionary with business details
            
        Returns:
            Dictionary with eligibility analysis
        """
        revenue = business_info.get('annual_revenue', 0)
        employees = business_info.get('employees', 0)
        years_in_business = business_info.get('years_in_business', 0)
        credit_score = business_info.get('credit_score', 0)
        
        recommendations = []
        
        # 7(a) Loan eligibility
        if revenue <= 30_000_000 and employees <= 500:
            recommendations.append({
                'program': 'SBA 7(a) Loan',
                'eligible': 'Likely Eligible',
                'max_amount': '$5,000,000',
                'notes': 'Good for working capital, equipment, and real estate'
            })
        
        # 504 Loan eligibility
        if revenue <= 30_000_000 and employees <= 500 and years_in_business >= 2:
            recommendations.append({
                'program': 'SBA 504 Loan',
                'eligible': 'Likely Eligible',
                'max_amount': '$5,500,000',
                'notes': 'Best for purchasing real estate or equipment'
            })
        
        # Microloan
        if revenue <= 5_000_000:
            recommendations.append({
                'program': 'SBA Microloan',
                'eligible': 'Likely Eligible',
                'max_amount': '$50,000',
                'notes': 'Good for small capital needs'
            })
        
        # Express loan
        if credit_score >= 680 and years_in_business >= 1:
            recommendations.append({
                'program': 'SBA Express Loan',
                'eligible': 'Likely Eligible',
                'max_amount': '$500,000',
                'notes': 'Fast approval process'
            })
        
        return {
            'business_revenue': revenue,
            'employee_count': employees,
            'years_in_business': years_in_business,
            'credit_score': credit_score,
            'recommended_programs': recommendations,
            'general_notes': 'These are preliminary assessments. Consult with an SBA lender for detailed eligibility.'
        }
    
    def export_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        """
        Export data to CSV
        
        Args:
            df: DataFrame to export
            filename: Output filename
            
        Returns:
            Path to the saved file
        """
        output_path = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        
        df.to_csv(output_path, index=False)
        print(f"SBA data exported to {output_path}")
        return output_path
    
    def export_to_excel(self, data_dict: Dict[str, pd.DataFrame], filename: str) -> str:
        """
        Export multiple datasets to Excel with multiple sheets
        
        Args:
            data_dict: Dictionary mapping sheet names to DataFrames
            filename: Output filename
            
        Returns:
            Path to the saved file
        """
        output_path = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"SBA data exported to {output_path}")
        return output_path


if __name__ == "__main__":
    # Example usage
    from dotenv import load_dotenv
    load_dotenv()
    
    tool = SBALoansTool()
    
    # Get current loan rates
    print("\n=== Current SBA Loan Rates ===")
    rates_df = tool.get_loan_rates()
    print(rates_df)
    
    # Search loans in Massachusetts
    print("\n=== SBA Loans in Massachusetts ===")
    loans_df = tool.search_loans_by_state("MA", limit=10)
    print(loans_df.head())
    
    # Get historical rates
    print("\n=== Historical Rate Trends ===")
    historical_df = tool.get_historical_rates(years=3)
    print(historical_df.head())
    
    # Analyze eligibility
    print("\n=== Loan Eligibility Analysis ===")
    business_info = {
        'annual_revenue': 5_000_000,
        'employees': 25,
        'years_in_business': 5,
        'credit_score': 720
    }
    eligibility = tool.analyze_loan_eligibility(business_info)
    print(f"Revenue: ${eligibility['business_revenue']:,}")
    print(f"Employees: {eligibility['employee_count']}")
    print(f"\nRecommended Programs:")
    for program in eligibility['recommended_programs']:
        print(f"  - {program['program']}: {program['eligible']} (up to {program['max_amount']})")
    
    # Export all data
    tool.export_to_excel({
        'Current Rates': rates_df,
        'Loans in MA': loans_df,
        'Historical Rates': historical_df
    }, "sba_loans_data.xlsx")
