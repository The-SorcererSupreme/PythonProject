# backend/src/app/run.py
from app import create_app

app = create_app()

def print_registered_routes():
    print("\n--- Registered Routes ---")
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, Rule: {rule.rule}, Methods: {', '.join(rule.methods)}")
    print("-------------------------\n")

print_registered_routes()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
