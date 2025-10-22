"""
Example usage of Valley Business Partners API Tools

This script demonstrates how to use each tool programmatically.
Customize this for your specific needs.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
from src.tools.google_reviews import GoogleReviewsTool
from src.tools.competitors import CompetitorsTool
from src.tools.openai_research import OpenAIResearchTool
from src.tools.sba_loans import SBALoansTool

# Load environment variables
load_dotenv()


def example_google_reviews():
    """Example: Fetch Google reviews for a business"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Google Reviews")
    print("="*60)
    
    try:
        tool = GoogleReviewsTool()
        
        # Get reviews for a business
        reviews_df = tool.get_reviews(
            business_name="Big Y World Class Market",
            location="Springfield MA"
        )
        
        if not reviews_df.empty:
            print(f"\n✓ Found {len(reviews_df)} reviews")
            print(f"Average Rating: {reviews_df.attrs.get('overall_rating', 'N/A')}")
            print(f"Total Ratings: {reviews_df.attrs.get('total_ratings', 'N/A')}")
            print(f"\nSample Reviews:")
            print(reviews_df[['author', 'rating', 'text']].head(3).to_string())
            
            # Export
            tool.export_to_excel(reviews_df, "example_reviews.xlsx")
            print(f"\n✓ Exported to output/example_reviews.xlsx")
        else:
            print("No reviews found")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Tip: Make sure GOOGLE_API_KEY is set in .env file")


def example_competitors():
    """Example: Find competitors in a region"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Competitor Analysis")
    print("="*60)
    
    try:
        tool = CompetitorsTool()
        
        # Find competitors
        competitors_df = tool.get_competitors_dataframe(
            business_type="grocery store",
            location="Springfield, MA",
            radius=25000  # 25km
        )
        
        if not competitors_df.empty:
            print(f"\n✓ Found {len(competitors_df)} competitors")
            print(f"\nTop 5 Competitors by Rating:")
            print(competitors_df[['name', 'rating', 'user_ratings_total', 'address']].head(5).to_string())
            
            # Export
            tool.export_to_excel(competitors_df, "example_competitors.xlsx")
            print(f"\n✓ Exported to output/example_competitors.xlsx")
        else:
            print("No competitors found")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Tip: Make sure GOOGLE_API_KEY is set in .env file")


def example_openai_research():
    """Example: Generate AI-powered business analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 3: OpenAI Deep Research")
    print("="*60)
    
    try:
        tool = OpenAIResearchTool()
        
        # Conduct business analysis
        analysis = tool.analyze_business(
            business_name="Big Y World Class Market",
            business_type="Grocery Store Chain",
            location="Western Massachusetts",
            additional_context="Regional grocery chain, potential PE acquisition target"
        )
        
        if 'analysis' in analysis:
            print(f"\n✓ Analysis completed")
            print(f"Model: {analysis.get('model_used', 'N/A')}")
            print(f"Tokens: {analysis.get('tokens_used', 0)}")
            print(f"\nAnalysis Preview (first 500 chars):")
            print("-" * 60)
            print(analysis['analysis'][:500] + "...")
            print("-" * 60)
            
            # Export
            tool.export_to_file(analysis['analysis'], "example_analysis", format="md")
            tool.export_analysis_to_excel(analysis, "example_analysis.xlsx")
            print(f"\n✓ Exported to output/example_analysis.md and .xlsx")
        else:
            print(f"Error: {analysis.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Tip: Make sure OPENAI_API_KEY is set in .env file")


def example_sba_loans():
    """Example: Get SBA loan information"""
    print("\n" + "="*60)
    print("EXAMPLE 4: SBA Loans Information")
    print("="*60)
    
    tool = SBALoansTool()
    
    # Get current rates
    print("\nCurrent SBA Loan Rates:")
    rates_df = tool.get_loan_rates()
    print(rates_df[['program', 'max_loan_amount', 'typical_spread', 'use_case']].to_string())
    
    # Get historical rates
    print("\n\nHistorical Rates (last 12 months):")
    historical_df = tool.get_historical_rates(years=1)
    print(historical_df.head(4).to_string())
    
    # Analyze eligibility
    print("\n\nLoan Eligibility Analysis:")
    business_info = {
        'annual_revenue': 5_000_000,
        'employees': 25,
        'years_in_business': 5,
        'credit_score': 720
    }
    
    eligibility = tool.analyze_loan_eligibility(business_info)
    print(f"Business Revenue: ${eligibility['business_revenue']:,.0f}")
    print(f"Employees: {eligibility['employee_count']}")
    print(f"\nRecommended Programs:")
    for program in eligibility['recommended_programs']:
        print(f"  • {program['program']}: {program['max_amount']}")
    
    # Export all
    tool.export_to_excel({
        'Current Rates': rates_df,
        'Historical Rates': historical_df
    }, "example_sba_loans.xlsx")
    print(f"\n✓ Exported to output/example_sba_loans.xlsx")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("VALLEY BUSINESS PARTNERS API TOOLS")
    print("Example Usage Demonstrations")
    print("="*60)
    
    print("\nThese examples show how to use each tool programmatically.")
    print("Customize this script for your specific needs.\n")
    
    # Run examples that don't require API keys first
    example_sba_loans()
    
    # Then try the ones that need API keys
    example_google_reviews()
    example_competitors()
    example_openai_research()
    
    print("\n" + "="*60)
    print("EXAMPLES COMPLETED")
    print("="*60)
    print("\nCheck the output/ directory for generated files.")
    print("Review the code above to see how to use each tool.")


if __name__ == "__main__":
    # Check for .env file
    if not os.path.exists('.env'):
        print("\n⚠ WARNING: .env file not found!")
        print("Some examples may fail without API keys.")
        print("Copy config.example.env to .env and add your API keys.\n")
    
    main()
