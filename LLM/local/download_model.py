from transformers import AutoTokenizer, AutoModelForCausalLM

# model_id = "Qwen/Qwen1.5-1.8B"
# local_dir = "./qwen_model(2.5-3B)"
# local_dir = "./qwen_model(2.5-7B)"
# local_dir = "./qwen_model(1.5-1.8B)"

# model_id = "Qwen/Qwen1.5-0.5B"
# local_dir = "./qwen_model(1.5-0.5B)"

model_id = "google/gemma-2b"
local_dir = "gemma_model_2b"

# Загружаем
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)


# Сохраняем как обычную модель
tokenizer.save_pretrained(local_dir)
model.save_pretrained(local_dir)



