#!/usr/bin/env python
"""
Simple Flask app runner without auto-reload to avoid terminal issues
"""
from website import create_app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*80)
    print("🚀 SSIS Flask App Starting...")
    print("="*80)
    print(f"📍 Visit: http://127.0.0.1:5000")
    print(f"📍 Alternative: http://localhost:5000")
    print("="*80 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Disable auto-reload to prevent abortion issues
    )
