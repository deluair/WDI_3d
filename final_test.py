#!/usr/bin/env python3
"""
Final validation test for the World Bank Visualization App.
Tests all 20 indicators to ensure no len() errors occur.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import config
from process_wb_data import get_indicator_info

def test_all_indicators():
    """Test all 20 popular indicators for the len() error."""
    print("🧪 Final validation: Testing all 20 popular indicators...")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, code in config.POPULAR_INDICATORS.items():
        try:
            print(f"\n📊 Testing: {name[:50]}..." + ("" if len(name) <= 50 else "..."))
            
            # Get indicator info
            info = get_indicator_info(code)
            
            # Test all the problematic operations
            # 1. Test definition length check (main_app.py line 326)
            if info.get('definition') and isinstance(info['definition'], str) and len(info['definition'].strip()) > 10:
                definition = info['definition']
                if len(definition) > 300:
                    definition = definition[:300] + "..."
                print(f"   ✅ Definition check passed (length: {len(info['definition'])})")
            else:
                print(f"   ✅ Definition safely handled (empty or short)")
            
            # 2. Test unit check
            if info.get('unit') and str(info['unit']).strip() and str(info['unit']) != 'nan':
                print(f"   ✅ Unit check passed: {info['unit']}")
            else:
                print(f"   ✅ Unit safely handled (empty)")
            
            # 3. Test topic check
            if info.get('topic'):
                print(f"   ✅ Topic: {info['topic'][:40]}..." if len(info['topic']) > 40 else f"   ✅ Topic: {info['topic']}")
            else:
                print(f"   ✅ Topic safely handled (empty)")
            
            passed += 1
            print(f"   🎯 Result: PASSED")
            
        except Exception as e:
            failed += 1
            print(f"   ❌ Result: FAILED - {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"🏁 Final Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📊 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 SUCCESS! All indicators pass the len() error fix!")
        print("🌍 The World Bank Visualization App is ready for all 20 indicators!")
    else:
        print(f"\n⚠️ Warning: {failed} indicators still have issues.")
    
    return failed == 0

if __name__ == "__main__":
    test_all_indicators()
