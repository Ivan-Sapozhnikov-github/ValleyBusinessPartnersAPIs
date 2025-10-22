"""
Valley Business Partners API Tools - Main Orchestrator
Comprehensive data extraction tool for private equity financial modeling
"""
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools.google_reviews import GoogleReviewsTool
from tools.competitors import CompetitorsTool
from tools.openai_research import OpenAIResearchTool
from tools.sba_loans import SBALoansTool


class ValleyBusinessPartnersAPI:
    """Main orchestrator for all API tools"""
    
    def __init__(self):
        """Initialize all API tools"""
        load_dotenv()
        
        print("Initializing Valley Business Partners API Tools...")
        
        try:
            self.google_reviews = GoogleReviewsTool()
            print("✓ Google Reviews Tool initialized")
        except Exception as e:
            print(f"⚠ Google Reviews Tool not initialized: {e}")
            self.google_reviews = None
        
        try:
            self.competitors = CompetitorsTool()
            print("✓ Competitors Tool initialized")
        except Exception as e:
            print(f"⚠ Competitors Tool not initialized: {e}")
            self.competitors = None
        
        try:
            self.openai_research = OpenAIResearchTool()
            print("✓ OpenAI Research Tool initialized")
        except Exception as e:
            print(f"⚠ OpenAI Research Tool not initialized: {e}")
            self.openai_research = None
        
        self.sba_loans = SBALoansTool()
        print("✓ SBA Loans Tool initialized")
        
        print("\nAll tools ready!\n")
    
    def comprehensive_business_analysis(self, business_name: str, business_type: str, 
                                       location: str = "Western Massachusetts"):
        """
        Perform comprehensive analysis of a business using all available tools
        
        Args:
            business_name: Name of the business
            business_type: Type/industry of the business
            location: Location of the business
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{business_name.replace(' ', '_')}_{timestamp}"
        
        print(f"\n{'='*60}")
        print(f"COMPREHENSIVE BUSINESS ANALYSIS")
        print(f"Business: {business_name}")
        print(f"Type: {business_type}")
        print(f"Location: {location}")
        print(f"{'='*60}\n")
        
        # 1. Get Google Reviews
        if self.google_reviews:
            print("1. Fetching Google Reviews...")
            try:
                reviews_df = self.google_reviews.get_reviews(business_name, location)
                if not reviews_df.empty:
                    print(f"   Found {len(reviews_df)} reviews")
                    self.google_reviews.export_to_excel(reviews_df, f"{base_filename}_reviews.xlsx")
                    print(f"   ✓ Reviews exported")
                else:
                    print("   No reviews found")
            except Exception as e:
                print(f"   Error: {e}")
        else:
            print("1. Google Reviews Tool not available (missing API key)")
        
        # 2. Find Competitors
        if self.competitors:
            print("\n2. Finding Competitors...")
            try:
                competitors_df = self.competitors.get_competitors_dataframe(
                    business_type=business_type,
                    location=location,
                    radius=25000
                )
                if not competitors_df.empty:
                    print(f"   Found {len(competitors_df)} competitors")
                    self.competitors.export_to_excel(competitors_df, f"{base_filename}_competitors.xlsx")
                    print(f"   ✓ Competitors exported")
                else:
                    print("   No competitors found")
            except Exception as e:
                print(f"   Error: {e}")
        else:
            print("\n2. Competitors Tool not available (missing API key)")
        
        # 3. OpenAI Deep Research
        if self.openai_research:
            print("\n3. Conducting OpenAI Deep Research...")
            try:
                analysis = self.openai_research.analyze_business(
                    business_name=business_name,
                    business_type=business_type,
                    location=location,
                    additional_context="Private equity acquisition target in Western Massachusetts"
                )
                if 'analysis' in analysis:
                    print(f"   ✓ Analysis complete (used {analysis.get('tokens_used', 0)} tokens)")
                    self.openai_research.export_to_file(
                        analysis['analysis'], 
                        f"{base_filename}_analysis",
                        format="md"
                    )
                    self.openai_research.export_analysis_to_excel(
                        analysis,
                        f"{base_filename}_analysis.xlsx"
                    )
                    print(f"   ✓ Analysis exported")
                else:
                    print(f"   Error in analysis: {analysis.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"   Error: {e}")
        else:
            print("\n3. OpenAI Research Tool not available (missing API key)")
        
        # 4. SBA Loan Information
        print("\n4. Fetching SBA Loan Information...")
        try:
            # Get current rates
            rates_df = self.sba_loans.get_loan_rates()
            print(f"   ✓ Current SBA loan rates retrieved")
            
            # Get state-specific loans
            state_code = self._get_state_code(location)
            loans_df = self.sba_loans.search_loans_by_state(state_code, limit=50)
            print(f"   ✓ SBA loans in {state_code} retrieved")
            
            # Get historical rates
            historical_df = self.sba_loans.get_historical_rates(years=3)
            print(f"   ✓ Historical rates retrieved")
            
            # Export all SBA data
            self.sba_loans.export_to_excel({
                'Current Rates': rates_df,
                f'Loans in {state_code}': loans_df,
                'Historical Rates': historical_df
            }, f"{base_filename}_sba_loans.xlsx")
            print(f"   ✓ SBA data exported")
        except Exception as e:
            print(f"   Error: {e}")
        
        print(f"\n{'='*60}")
        print(f"ANALYSIS COMPLETE")
        print(f"All files saved to: output/")
        print(f"{'='*60}\n")
    
    def _get_state_code(self, location: str) -> str:
        """Extract state code from location string"""
        state_mapping = {
            'massachusetts': 'MA',
            'ma': 'MA',
            'new york': 'NY',
            'ny': 'NY',
            'connecticut': 'CT',
            'ct': 'CT',
            'vermont': 'VT',
            'vt': 'VT',
            'new hampshire': 'NH',
            'nh': 'NH',
            'rhode island': 'RI',
            'ri': 'RI'
        }
        
        location_lower = location.lower()
        for key, code in state_mapping.items():
            if key in location_lower:
                return code
        
        return 'MA'  # Default to MA


def print_menu():
    """Print the main menu"""
    print("\n" + "="*60)
    print("VALLEY BUSINESS PARTNERS API TOOLS")
    print("Data Extraction for Financial Modeling")
    print("="*60)
    print("\nAvailable Tools:")
    print("  1. Comprehensive Business Analysis (All Tools)")
    print("  2. Google Reviews Only")
    print("  3. Competitors Analysis Only")
    print("  4. OpenAI Deep Research Only")
    print("  5. SBA Loans Information Only")
    print("  6. Exit")
    print("="*60)


def main():
    """Main entry point"""
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n⚠ WARNING: .env file not found!")
        print("Please copy config.example.env to .env and add your API keys.")
        print("Some tools may not work without API keys.\n")
    
    api = ValleyBusinessPartnersAPI()
    
    while True:
        print_menu()
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '6':
            print("\nThank you for using Valley Business Partners API Tools!")
            break
        
        if choice == '1':
            # Comprehensive Analysis
            business_name = input("\nEnter business name: ").strip()
            business_type = input("Enter business type/industry: ").strip()
            location = input("Enter location (default: Western Massachusetts): ").strip() or "Western Massachusetts"
            
            api.comprehensive_business_analysis(business_name, business_type, location)
        
        elif choice == '2':
            # Google Reviews Only
            if not api.google_reviews:
                print("\n⚠ Google Reviews Tool not available. Check API key.")
                continue
            
            business_name = input("\nEnter business name: ").strip()
            location = input("Enter location (default: Western Massachusetts): ").strip() or "Western Massachusetts"
            
            print(f"\nFetching reviews for {business_name}...")
            reviews_df = api.google_reviews.get_reviews(business_name, location)
            
            if not reviews_df.empty:
                print(f"\nFound {len(reviews_df)} reviews")
                print(reviews_df.head())
                
                filename = input("\nEnter output filename (without extension): ").strip() or "google_reviews"
                api.google_reviews.export_to_excel(reviews_df, f"{filename}.xlsx")
                print(f"✓ Exported to output/{filename}.xlsx")
            else:
                print("No reviews found")
        
        elif choice == '3':
            # Competitors Only
            if not api.competitors:
                print("\n⚠ Competitors Tool not available. Check API key.")
                continue
            
            business_type = input("\nEnter business type to search: ").strip()
            location = input("Enter location (default: Western Massachusetts): ").strip() or "Western Massachusetts"
            radius = input("Enter search radius in meters (default: 25000): ").strip()
            radius = int(radius) if radius.isdigit() else 25000
            
            print(f"\nSearching for competitors...")
            competitors_df = api.competitors.get_competitors_dataframe(business_type, location, radius)
            
            if not competitors_df.empty:
                print(f"\nFound {len(competitors_df)} competitors")
                print(competitors_df.head(10))
                
                filename = input("\nEnter output filename (without extension): ").strip() or "competitors"
                api.competitors.export_to_excel(competitors_df, f"{filename}.xlsx")
                print(f"✓ Exported to output/{filename}.xlsx")
            else:
                print("No competitors found")
        
        elif choice == '4':
            # OpenAI Research Only
            if not api.openai_research:
                print("\n⚠ OpenAI Research Tool not available. Check API key.")
                continue
            
            business_name = input("\nEnter business name: ").strip()
            business_type = input("Enter business type/industry: ").strip()
            location = input("Enter location (default: Western Massachusetts): ").strip() or "Western Massachusetts"
            
            print(f"\nConducting deep research analysis...")
            analysis = api.openai_research.analyze_business(business_name, business_type, location)
            
            if 'analysis' in analysis:
                print(f"\n{analysis['analysis'][:500]}...")
                print(f"\n(Full analysis saved to file)")
                
                filename = input("\nEnter output filename (without extension): ").strip() or "openai_analysis"
                api.openai_research.export_to_file(analysis['analysis'], filename, format="md")
                api.openai_research.export_analysis_to_excel(analysis, f"{filename}.xlsx")
                print(f"✓ Exported to output/{filename}.md and output/{filename}.xlsx")
            else:
                print(f"Error: {analysis.get('error', 'Unknown error')}")
        
        elif choice == '5':
            # SBA Loans Only
            print("\nSBA Loans Information")
            print("  a. Current loan rates")
            print("  b. Search loans by state")
            print("  c. Historical rates")
            print("  d. Analyze loan eligibility")
            
            sub_choice = input("Select option (a-d): ").strip().lower()
            
            if sub_choice == 'a':
                rates_df = api.sba_loans.get_loan_rates()
                print("\nCurrent SBA Loan Rates:")
                print(rates_df.to_string())
                
                save = input("\nExport to Excel? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Enter filename (without extension): ").strip() or "sba_rates"
                    api.sba_loans.export_to_excel({'Current Rates': rates_df}, f"{filename}.xlsx")
                    print(f"✓ Exported to output/{filename}.xlsx")
            
            elif sub_choice == 'b':
                state_code = input("Enter state code (default: MA): ").strip().upper() or "MA"
                limit = input("Enter max results (default: 50): ").strip()
                limit = int(limit) if limit.isdigit() else 50
                
                loans_df = api.sba_loans.search_loans_by_state(state_code, limit)
                print(f"\nSBA Loans in {state_code}:")
                print(loans_df.head(10).to_string())
                
                save = input("\nExport to Excel? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Enter filename (without extension): ").strip() or f"sba_loans_{state_code}"
                    api.sba_loans.export_to_excel({f'Loans in {state_code}': loans_df}, f"{filename}.xlsx")
                    print(f"✓ Exported to output/{filename}.xlsx")
            
            elif sub_choice == 'c':
                years = input("Enter years of history (default: 5): ").strip()
                years = int(years) if years.isdigit() else 5
                
                historical_df = api.sba_loans.get_historical_rates(years)
                print(f"\nHistorical SBA Loan Rates (last {years} years):")
                print(historical_df.head(10).to_string())
                
                save = input("\nExport to Excel? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Enter filename (without extension): ").strip() or "sba_historical_rates"
                    api.sba_loans.export_to_excel({'Historical Rates': historical_df}, f"{filename}.xlsx")
                    print(f"✓ Exported to output/{filename}.xlsx")
            
            elif sub_choice == 'd':
                print("\nEnter business information:")
                revenue = float(input("Annual revenue ($): ").strip() or 0)
                employees = int(input("Number of employees: ").strip() or 0)
                years = int(input("Years in business: ").strip() or 0)
                credit = int(input("Credit score: ").strip() or 0)
                
                business_info = {
                    'annual_revenue': revenue,
                    'employees': employees,
                    'years_in_business': years,
                    'credit_score': credit
                }
                
                eligibility = api.sba_loans.analyze_loan_eligibility(business_info)
                
                print("\n" + "="*60)
                print("LOAN ELIGIBILITY ANALYSIS")
                print("="*60)
                print(f"Annual Revenue: ${eligibility['business_revenue']:,.2f}")
                print(f"Employees: {eligibility['employee_count']}")
                print(f"Years in Business: {eligibility['years_in_business']}")
                print(f"Credit Score: {eligibility['credit_score']}")
                print("\nRecommended Programs:")
                for program in eligibility['recommended_programs']:
                    print(f"\n  • {program['program']}")
                    print(f"    Status: {program['eligible']}")
                    print(f"    Max Amount: {program['max_amount']}")
                    print(f"    Notes: {program['notes']}")
                print("\n" + eligibility['general_notes'])
                print("="*60)
        
        else:
            print("\nInvalid option. Please select 1-6.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
