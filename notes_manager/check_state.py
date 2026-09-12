from app.state import AppState


state = AppState()

print("Notes count:", len(state.notes))

state.storage.close()

print("State check completed")