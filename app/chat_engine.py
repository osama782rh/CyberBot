import sys
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-base"

def load_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        device = "cpu"
        model.to(device)
        return tokenizer, model, device
    except Exception as e:
        print("Erreur lors du chargement du modèle :", e)
        sys.exit(1)

def generate_response(user_input, tokenizer, model, device):
    # On traite 'user_input' comme instruction
    try:
        # Encoder l'instruction
        inputs = tokenizer.encode(user_input, return_tensors="pt").to(device)
        # Génération
        outputs = model.generate(
            inputs,
            max_length=150,
            do_sample=True,
            top_k=50,
            top_p=0.9,
            temperature=0.7,
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.strip()
    except Exception as e:
        print("Erreur lors de la génération :", e)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[Erreur] Aucun message fourni.")
        sys.exit(1)
    user_input = " ".join(sys.argv[1:])
    tokenizer, model, device = load_model()
    response = generate_response(user_input, tokenizer, model, device)
    if response:
        print(response)
    else:
        print("[Erreur] Aucune réponse générée.")
