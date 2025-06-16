import pandas as pd

# Load the series data
df = pd.read_csv('WDISeries.csv')

# Search for CO2 indicators
print("Searching for CO2-related indicators...")
co2_indicators = df[df['Indicator Name'].str.contains('CO2', case=False, na=False)]

print(f"\nFound {len(co2_indicators)} CO2-related indicators:")
print("="*80)

for _, row in co2_indicators.iterrows():
    print(f"{row['Series Code']}: {row['Indicator Name']}")

print("\n" + "="*80)

# Also search for emission indicators
print("\nSearching for emission-related indicators...")
emission_indicators = df[df['Indicator Name'].str.contains('emission', case=False, na=False)]

print(f"\nFound {len(emission_indicators)} emission-related indicators:")
print("="*80)

for _, row in emission_indicators.head(10).iterrows():  # Show first 10
    print(f"{row['Series Code']}: {row['Indicator Name']}")

if len(emission_indicators) > 10:
    print(f"... and {len(emission_indicators) - 10} more")
