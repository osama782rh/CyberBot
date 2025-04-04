from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import sys

# Modèle anglais DialoGPT utilisé pour répondre en français via prompt
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

chat_history_ids = None

def generate_response(user_input):
    global chat_history_ids

    prompt = f"Tu es un robot intelligent qui parle uniquement en français. {user_input}"

    new_input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=300,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=50,
        top_p=0.9,
        temperature=0.7
    )

    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[Erreur] Aucun message fourni.")
    else:
        message = " ".join(sys.argv[1:])
        print(generate_response(message))
