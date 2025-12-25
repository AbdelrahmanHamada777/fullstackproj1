from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Chat
from e_commerce.models import Product
import os

import requests

# Hugging Face API - using a simpler, faster model
HF_API_TOKEN = os.getenv('HF_API_TOKEN', '')
# Using a text generation model that's faster and more reliable
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

def ask_chatbot(message):
    """
    Use Hugging Face's free API with a conversational model.
    Falls back to simple responses if API fails.
    """
    headers = {"Content-Type": "application/json"}
    if HF_API_TOKEN:
        headers["Authorization"] = f"Bearer {HF_API_TOKEN}"
    
    try:
        # Try Hugging Face API first
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json={
                "inputs": message,
                "parameters": {
                    "max_length": 100,
                    "temperature": 0.7
                }
            },
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated = result[0].get('generated_text', '')
                if generated and generated != message:
                    return generated
        
        # Fallback to simple responses if API fails
        return get_simple_response(message)
        
    except Exception as e:
        # Fallback to simple responses on error
        return get_simple_response(message)

def get_simple_response(message):
    """Fallback responses when API is unavailable"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['hi', 'hello', 'hey']):
        return "Hello! 👋 Welcome to PC Planet! How can I help you today?"
    
    if 'monitor' in message_lower:
        return "We have great monitors! Check our Monitors category for the best deals."
    
    if 'graphic' in message_lower or 'gpu' in message_lower:
        return "Looking for a graphics card? Browse our Graphics Cards section!"
    
    if 'processor' in message_lower or 'cpu' in message_lower:
        return "We offer Intel and AMD processors. Visit our Processors category!"
    
    if 'budget' in message_lower:
        return "Tell me your budget and I'll help you find the best components!"
    
    return "I'm here to help! Ask me about monitors, graphics cards, processors, or your budget."

@login_required
def bot(request):
    chats = Chat.objects.filter(user=request.user).order_by('created_at')

    if request.method == 'POST':
        message = request.POST.get('message')

        budget = None
        if "budget" in message.lower():
            import re
            m = re.search(r'\d+', message)
            if m:
                budget = int(m.group())

        suggested_build = ""
        if budget:
            categories = Product.objects.values_list('category', flat=True).distinct()
            build = []
            total = 0
            for cat in categories:
                prod = Product.objects.filter(category=cat).order_by('price').first()
                if prod:
                    total += prod.price
                    if total <= budget:
                        build.append(f"{prod.name} (${prod.price})")
            if build:
                suggested_build = "Suggested build within your budget:\n" + "\n".join(build)

        final_message = message
        if suggested_build:
            final_message += "\n" + suggested_build

        response = ask_chatbot(final_message)

        chat = Chat.objects.create(user=request.user, message=message, response=response)
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html', {'chats': chats})
