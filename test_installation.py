"""
Installation Test Script

Tests that all dependencies are correctly installed and
the basic structure works without requiring API keys.
"""
import sys
import os

print("="*60)
print("VALLEY BUSINESS PARTNERS API TOOLS")
print("Installation Test")
print("="*60)

# Test 1: Python version
print("\n1. Checking Python version...")
version = sys.version_info
print(f"   Python {version.major}.{version.minor}.{version.micro}")
if version.major >= 3 and version.minor >= 8:
    print("   ✓ Python version is compatible (3.8+)")
else:
    print("   ✗ Python 3.8+ required")
    sys.exit(1)

# Test 2: Required modules
print("\n2. Checking required modules...")
required_modules = [
    'requests',
    'pandas',
    'openpyxl',
    'dotenv',
    'openai'
]

missing_modules = []
for module in required_modules:
    try:
        if module == 'dotenv':
            __import__('dotenv')
        else:
            __import__(module)
        print(f"   ✓ {module}")
    except ImportError:
        print(f"   ✗ {module} (missing)")
        missing_modules.append(module)

if missing_modules:
    print(f"\n   Missing modules: {', '.join(missing_modules)}")
    print("   Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 3: Project structure
print("\n3. Checking project structure...")
required_files = [
    'main.py',
    'requirements.txt',
    'config.example.env',
    'README.md',
    'src/tools/google_reviews.py',
    'src/tools/competitors.py',
    'src/tools/openai_research.py',
    'src/tools/sba_loans.py'
]

missing_files = []
for file_path in required_files:
    if os.path.exists(file_path):
        print(f"   ✓ {file_path}")
    else:
        print(f"   ✗ {file_path} (missing)")
        missing_files.append(file_path)

if missing_files:
    print(f"\n   Missing files: {', '.join(missing_files)}")
    sys.exit(1)

# Test 4: Import tools
print("\n4. Testing tool imports...")
sys.path.insert(0, 'src')

try:
    from tools.sba_loans import SBALoansTool
    print("   ✓ SBA Loans Tool")
except Exception as e:
    print(f"   ✗ SBA Loans Tool: {e}")

try:
    from tools.google_reviews import GoogleReviewsTool
    print("   ✓ Google Reviews Tool")
except Exception as e:
    print(f"   ✗ Google Reviews Tool: {e}")

try:
    from tools.competitors import CompetitorsTool
    print("   ✓ Competitors Tool")
except Exception as e:
    print(f"   ✗ Competitors Tool: {e}")

try:
    from tools.openai_research import OpenAIResearchTool
    print("   ✓ OpenAI Research Tool")
except Exception as e:
    print(f"   ✗ OpenAI Research Tool: {e}")

# Test 5: SBA Tool (no API key needed)
print("\n5. Testing SBA Loans Tool (no API key required)...")
try:
    from tools.sba_loans import SBALoansTool
    tool = SBALoansTool()
    
    # Test get_loan_rates
    rates_df = tool.get_loan_rates()
    if len(rates_df) > 0:
        print(f"   ✓ get_loan_rates() - Found {len(rates_df)} loan programs")
    else:
        print("   ✗ get_loan_rates() - No data returned")
    
    # Test analyze_loan_eligibility
    business_info = {
        'annual_revenue': 1_000_000,
        'employees': 10,
        'years_in_business': 3,
        'credit_score': 700
    }
    eligibility = tool.analyze_loan_eligibility(business_info)
    if 'recommended_programs' in eligibility:
        print(f"   ✓ analyze_loan_eligibility() - {len(eligibility['recommended_programs'])} programs recommended")
    else:
        print("   ✗ analyze_loan_eligibility() - No recommendations")
    
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Check for .env file
print("\n6. Checking configuration...")
if os.path.exists('.env'):
    print("   ✓ .env file exists")
    print("   Note: Verify API keys are set for Google and OpenAI tools")
else:
    print("   ⚠ .env file not found")
    print("   Copy config.example.env to .env and add your API keys")
    print("   Some tools will not work without API keys")

# Test 7: Output directory
print("\n7. Checking output directory...")
if not os.path.exists('output'):
    os.makedirs('output')
    print("   ✓ Created output/ directory")
else:
    print("   ✓ output/ directory exists")

# Summary
print("\n" + "="*60)
print("INSTALLATION TEST COMPLETE")
print("="*60)

if missing_modules or missing_files:
    print("\n⚠ Some checks failed. Please address the issues above.")
    sys.exit(1)
else:
    print("\n✓ All checks passed!")
    print("\nYou're ready to use the Valley Business Partners API Tools!")
    print("\nNext steps:")
    print("  1. Copy config.example.env to .env")
    print("  2. Add your API keys to .env")
    print("  3. Run: python main.py")
    print("\nOr check out:")
    print("  • QUICKSTART.md for a quick start guide")
    print("  • examples/example_usage.py for code examples")
    print("  • README.md for full documentation")
    print("\n" + "="*60)
