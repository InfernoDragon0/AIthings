#TODO AI stuff in another thread, before the ClientEncoder. AI to tell ClientEncoder to encode (probably with a variable) when ready
class ClientProcessor():
    def __init__(self):
        pass
    
    def asInferenceObject(self): #can remove if not needed
        return {"x": 123, "y": 234, "confidence": 1, "inferred": "Person"}