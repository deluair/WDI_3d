#!/usr/bin/env python3
"""
Test script to verify the float/len() error fix.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from process_wb_data import get_indicator_info
import config

def test_indicator_info(indicator_code, indicator_name):
    """Test getting indicator info for a specific indicator."""
    print(f"\n🧪 Testing {indicator_name} ({indicator_code})...")
    
    try:
        info = get_indicator_info(indicator_code)
        print(f"✅ Successfully retrieved info:")
        print(f"   Name: {info['name']}")
        print(f"   Unit: {info['unit']}")
        print(f"   Topic: {info['topic']}")
        print(f"   Definition length: {len(info['definition']) if info['definition'] else 0}")
        print(f"   Definition type: {type(info['definition'])}")
        
        # Test the len() operations that were causing issues
        if info.get('definition') and isinstance(info['definition'], str) and len(info['definition'].strip()) > 10:
            print(f"   ✅ Definition passes length check")
            definition = info['definition']
            if len(definition) > 300:
                definition = definition[:300] + "..."
            print(f"   ✅ Definition truncation works")
        else:
            print(f"   ⚠️ Definition does not pass length check or is empty")
            
        if info.get('unit') and str(info['unit']).strip() and str(info['unit']) != 'nan':
            print(f"   ✅ Unit check passes")
        else:
            print(f"   ⚠️ Unit check fails or is empty")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"❌ Error type: {type(e)}")
        return False

def main():
    """Test the problematic indicators."""
    print("🔧 Testing indicator info retrieval after float/len() fix...\n")
    
    # Test the Foreign direct investment indicator that was causing issues
    problem_indicators = [
        ("BX.KLT.DINV.WD.GD.ZS", "Foreign direct investment"),
        ("NY.GDP.PCAP.CD", "GDP per capita"),
        ("SP.POP.TOTL", "Population"),
        ("EN.ATM.CO2E.PC", "CO2 emissions"),
        ("SL.UEM.TOTL.ZS", "Unemployment rate")
    ]
    
    passed = 0
    total = len(problem_indicators)
    
    for code, name in problem_indicators:
        if test_indicator_info(code, name):
            passed += 1
    
    print(f"\n🏁 Test Results: {passed}/{total} indicators passed")
    
    if passed == total:
        print("✅ All tests passed! The float/len() error has been fixed.")
    else:
        print("❌ Some tests failed. Further investigation needed.")

if __name__ == "__main__":
    main()
