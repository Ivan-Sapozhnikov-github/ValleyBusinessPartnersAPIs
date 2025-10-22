# Valley Business Partners API Tools

Comprehensive data extraction tools for private equity financial modeling and due diligence. Built specifically for Valley Business Partners to analyze potential acquisition targets in Western Massachusetts.

## Overview

This toolkit provides four powerful data extraction tools designed to streamline financial modeling and due diligence processes:

1. **Google Reviews Tool** - Extract customer reviews and ratings for any business
2. **Competitors Tool** - Identify and analyze competitors in the same region
3. **OpenAI Deep Research Tool** - Generate comprehensive business analysis reports using AI
4. **SBA Loans Tool** - Access SBA loan rates, historical data, and eligibility analysis

All data can be exported to Excel (.xlsx) and CSV formats for easy integration into financial models.

## Features

- 🔍 **Comprehensive Business Analysis** - Run all tools at once for complete due diligence
- 📊 **Excel/CSV Export** - All data exports to spreadsheet formats
- 🤖 **AI-Powered Insights** - Leverage OpenAI for deep market research
- 💰 **SBA Loan Intelligence** - Access loan rates and eligibility information
- 🏢 **Competitive Intelligence** - Identify and analyze market competitors
- ⭐ **Customer Sentiment** - Analyze Google reviews and ratings

## Installation

### Prerequisites

- Python 3.8 or higher
- API Keys:
  - Google Places API key (for Reviews and Competitors tools)
  - OpenAI API key (for Research tool)
  - SBA API key (optional, for enhanced SBA data)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Ivan-Sapozhnikov-github/ValleyBusinessPartnersAPIs.git
cd ValleyBusinessPartnersAPIs
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys:
```bash
cp config.example.env .env
```

Edit `.env` and add your API keys:
```
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SBA_API_KEY=your_sba_api_key_here_if_required
```

## Getting API Keys

### Google Places API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable "Places API" and "Geocoding API"
4. Create credentials (API Key)
5. Copy the API key to your `.env` file

### OpenAI API
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key to your `.env` file

### SBA API
Most SBA public data does not require an API key. If you need enhanced access, visit [data.sba.gov](https://data.sba.gov/) for more information.

## Usage

### Interactive Mode

Run the main application:
```bash
python main.py
```

This launches an interactive menu where you can:
- Run comprehensive business analysis (all tools)
- Use individual tools separately
- Export data in your preferred format

### Programmatic Usage

You can also import and use the tools in your own Python scripts:

#### Google Reviews Tool
```python
from src.tools.google_reviews import GoogleReviewsTool

tool = GoogleReviewsTool()
reviews_df = tool.get_reviews("Big Y World Class Market", "Springfield MA")
tool.export_to_excel(reviews_df, "reviews.xlsx")
```

#### Competitors Tool
```python
from src.tools.competitors import CompetitorsTool

tool = CompetitorsTool()
competitors_df = tool.get_competitors_dataframe(
    business_type="grocery store",
    location="Springfield, MA",
    radius=25000  # 25km radius
)
tool.export_to_excel(competitors_df, "competitors.xlsx")
```

#### OpenAI Research Tool
```python
from src.tools.openai_research import OpenAIResearchTool

tool = OpenAIResearchTool()
analysis = tool.analyze_business(
    business_name="Big Y World Class Market",
    business_type="Grocery Store Chain",
    location="Western Massachusetts",
    additional_context="PE acquisition target"
)
tool.export_to_file(analysis['analysis'], "analysis", format="md")
```

#### SBA Loans Tool
```python
from src.tools.sba_loans import SBALoansTool

tool = SBALoansTool()

# Get current rates
rates_df = tool.get_loan_rates()

# Search loans by state
loans_df = tool.search_loans_by_state("MA", limit=50)

# Get historical rates
historical_df = tool.get_historical_rates(years=5)

# Analyze eligibility
eligibility = tool.analyze_loan_eligibility({
    'annual_revenue': 5_000_000,
    'employees': 25,
    'years_in_business': 5,
    'credit_score': 720
})

# Export all data
tool.export_to_excel({
    'Current Rates': rates_df,
    'Loans in MA': loans_df,
    'Historical Rates': historical_df
}, "sba_data.xlsx")
```

## Output

All exported files are saved to the `output/` directory with descriptive filenames including timestamps.

Example outputs:
- `Big_Y_World_Class_Market_20241022_120000_reviews.xlsx` - Customer reviews
- `Big_Y_World_Class_Market_20241022_120000_competitors.xlsx` - Competitor analysis
- `Big_Y_World_Class_Market_20241022_120000_analysis.md` - AI research report
- `Big_Y_World_Class_Market_20241022_120000_sba_loans.xlsx` - SBA loan data

## Project Structure

```
ValleyBusinessPartnersAPIs/
├── main.py                    # Main orchestrator and interactive CLI
├── requirements.txt           # Python dependencies
├── config.example.env        # Example configuration file
├── .env                      # Your API keys (not in git)
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── src/
│   └── tools/
│       ├── __init__.py
│       ├── google_reviews.py    # Google Reviews API tool
│       ├── competitors.py       # Competitors search tool
│       ├── openai_research.py   # OpenAI deep research tool
│       └── sba_loans.py         # SBA loans data tool
└── output/                   # Generated reports (not in git)
```

## Tool Details

### 1. Google Reviews Tool
Fetches Google reviews and business information using Google Places API.

**Features:**
- Search businesses by name and location
- Retrieve customer reviews with ratings
- Get business summary (overall rating, total reviews, contact info)
- Export to Excel with summary sheet

### 2. Competitors Tool
Identifies competitors in a specified region using Google Places API.

**Features:**
- Search by business type and location
- Configurable search radius
- Get competitor ratings and review counts
- Generate competitive landscape analysis
- Sort by rating and popularity

### 3. OpenAI Deep Research Tool
Generates comprehensive business analysis using OpenAI's GPT-4.

**Features:**
- Market overview and trends analysis
- Competitive landscape assessment
- Growth opportunities identification
- Risk factor analysis
- Financial considerations
- Strategic recommendations for PE investment

### 4. SBA Loans Tool
Provides SBA loan information and analysis.

**Features:**
- Current SBA loan rates (7(a), 504, Microloan, Express)
- Historical rate trends
- State-specific loan search
- Loan eligibility analysis
- Multiple program comparison

## Best Practices

1. **API Rate Limits**: Be mindful of API rate limits, especially with Google Places API
2. **Cost Management**: OpenAI API usage incurs costs based on tokens used
3. **Data Privacy**: Don't commit your `.env` file with API keys
4. **Regular Updates**: API endpoints and requirements may change; keep dependencies updated
5. **Batch Processing**: For multiple businesses, consider rate limiting and batch processing

## Troubleshooting

### "API key is required" error
- Ensure your `.env` file exists and contains valid API keys
- Check that environment variables are loaded (use `python-dotenv`)

### "No reviews found" or "No competitors found"
- Verify the business name and location are correct
- Try broader search terms
- Check that your Google API key has the necessary APIs enabled

### OpenAI API errors
- Verify your OpenAI API key is valid and has credits
- Check your usage limits on the OpenAI platform

### Empty or sample SBA data
- The SBA API structure may have changed; tool provides sample data as fallback
- Check `data.sba.gov` for current API documentation

## Contributing

This is a private tool for Valley Business Partners. For issues or feature requests, contact the development team.

## License

Proprietary - Valley Business Partners

## Support

For support or questions, please contact the Valley Business Partners technical team.

---

**Note**: This tool is designed for financial modeling and due diligence purposes. Always verify data from multiple sources and consult with professional advisors for investment decisions.
