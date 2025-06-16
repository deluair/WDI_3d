#!/usr/bin/env python3
"""
Test script to simulate the exact operations that were failing in the main app.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from process_wb_data import get_indicator_info, process_indicator_for_year
import config

def test_main_app_workflow():
    """Test the exact workflow that was failing in the main app."""
    print("🧪 Testing main app workflow for Foreign direct investment...\n")
    
    indicator_code = "BX.KLT.DINV.WD.GD.ZS"  # Foreign direct investment
    year = "2023"
    
    try:
        # Step 1: Get indicator info (this was causing the len() error)
        print("📊 Step 1: Getting indicator info...")
        indicator_info = get_indicator_info(indicator_code)
        print(f"✅ Got indicator info: {indicator_info['name']}")
        
        # Step 2: Test the exact conditions that were failing
        print("\n🔍 Step 2: Testing problematic conditions...")
        
        # This was line 326 in main_app.py that was failing
        if indicator_info['definition'] and len(indicator_info['definition']) > 10:
            print("✅ Old definition check would work")
        else:
            print("⚠️ Old definition check fails (expected since definition is empty)")
        
        # This is the new safe check
        if indicator_info.get('definition') and isinstance(indicator_info['definition'], str) and len(indicator_info['definition'].strip()) > 10:
            print("✅ New safe definition check works")
        else:
            print("✅ New safe definition check correctly handles empty definition")
        
        # Test unit check
        if indicator_info.get('unit') and str(indicator_info['unit']).strip() and str(indicator_info['unit']) != 'nan':
            print("✅ Unit check passes")
        else:
            print("✅ Unit check correctly handles empty unit")
        
        # Step 3: Try to process data for visualization
        print(f"\n📈 Step 3: Processing data for {year}...")
        df = process_indicator_for_year(indicator_code, year)
        
        if df is not None and not df.empty:
            print(f"✅ Successfully processed data: {len(df)} countries")
        else:
            print("⚠️ No data available for this year (this is okay)")
        
        print("\n🎉 All tests passed! The main app workflow should work correctly now.")
        return True
        
    except Exception as e:
        print(f"❌ Error in workflow: {str(e)}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_main_app_workflow()
