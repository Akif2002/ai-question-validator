from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load Pretrained GPT-2 Model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Function to generate AI-related questions
def generate_question():
    prompt = "Create a question related to artificial intelligence. Example: 'How does AI improve healthcare?' \nQuestion:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs, 
        max_length=50, 
        num_return_sequences=1, 
        temperature=0.7,  
        top_k=50,        
        top_p=0.95,       
        do_sample=True    
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Generate and print a question
if __name__ == "__main__":
    question = generate_question()
    print("Generated Question:", question)
