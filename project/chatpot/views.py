from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Chat
from e_commerce.models import Product
import os

import requests
import os

# Hugging Face API (free tier)
HF_API_TOKEN = os.getenv('HF_API_TOKEN', '')  # Optional - works without token but with rate limits
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"

def ask_huggingface(message):
    """
    Use Hugging Face's free Inference API for chatbot responses.
    No API key required (but rate limited). Can add HF_API_TOKEN for higher limits.
    """
    headers = {}
    if HF_API_TOKEN:
        headers["Authorization"] = f"Bearer {HF_API_TOKEN}"
    
    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": message},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'Sorry, I could not generate a response.')
            return "I'm here to help! Ask me about PC components or your budget."
        else:
            return "I'm currently busy. Please try again in a moment!"
    except Exception as e:
        return f"I'm having trouble connecting. Please ask about our products instead!"

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

        response = ask_huggingface(final_message)

        chat = Chat.objects.create(user=request.user, message=message, response=response)
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html', {'chats': chats})
