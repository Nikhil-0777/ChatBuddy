import google.generativeai as genai

genai.configure(api_key="AIzaSyDqIC-zXGH1U1vjSOoL2YZ5XQggCLVPZGo")  # Replace with your actual key

models = genai.list_models()
for model in models:
    print(model.name)
