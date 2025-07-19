#!/usr/bin/env python3
"""
Simple script to call all Ollama models
Requires: pip install ollama
"""

import ollama

def test_all_models():
    """Simple function to test all available Ollama models"""
    try:
        # Get list of all models
        models = ollama.list()
        
        if not models['models']:
            print("No models found! Install models with: ollama pull <model-name>")
            return
        
        print(f"Found {len(models['models'])} models:")
        for model in models['models']:
            print(f"  - {model['name']}")
        
        print("\nTesting all models...")
        print("-" * 50)
        
        test_prompt = "Hello! Please tell me your name and what you can do in one sentence."
        
        for model in models['models']:
            model_name = model['name']
            print(f"\n🤖 Testing: {model_name}")
            
            try:
                response = ollama.generate(
                    model=model_name,
                    prompt=test_prompt
                )
                
                print(f"✅ Response: {response['response']}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Ollama is running: ollama serve")

if __name__ == "__main__":
    test_all_models()