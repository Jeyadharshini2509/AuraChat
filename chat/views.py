from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .groq_client import generate_reply
from .models import ChatThread, Message


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("chat_home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def chat_home(request):
    return _render_chat(request, active_thread=None)


@login_required
def chat_thread(request, thread_id):
    active_thread = get_object_or_404(ChatThread, id=thread_id, user=request.user)
    return _render_chat(request, active_thread=active_thread)


def _render_chat(request, active_thread):
    threads = ChatThread.objects.filter(user=request.user)
    messages = active_thread.messages.all() if active_thread else []
    return render(
        request,
        "chat/chat.html",
        {
            "threads": threads,
            "active_thread": active_thread,
            "messages": messages,
        },
    )


@login_required
@require_POST
def send_message(request):
    content = request.POST.get("content", "").strip()
    thread_id = request.POST.get("thread_id")
    is_htmx = request.headers.get("HX-Request")

    if not content:
        return redirect("chat_home")

    if thread_id:
        thread = get_object_or_404(ChatThread, id=thread_id, user=request.user)
    else:
        title = content[:40] + ("..." if len(content) > 40 else "")
        thread = ChatThread.objects.create(user=request.user, title=title)

    Message.objects.create(thread=thread, role="user", content=content)

    history = [{"role": m.role, "content": m.content} for m in thread.messages.all()]

    try:
        reply_text = generate_reply(history)
    except Exception as exc:
        err = str(exc)
        if "503" in err:
            reply_text = "⚠️ Gemini is currently overloaded. Please try again in a moment."
        elif "API_KEY" in err or "api_key" in err.lower():
            reply_text = "⚠️ Your Gemini API key is missing or invalid. Check your .env file."
        else:
            reply_text = f"⚠️ Something went wrong. Please try again.\n\n_{err}_"

    Message.objects.create(thread=thread, role="assistant", content=reply_text)
    thread.save()  # bumps updated_at so thread rises to the top of the sidebar

    if is_htmx:
        if not thread_id:
            # Brand-new thread — redirect so the URL and sidebar update
            response = HttpResponse()
            response["HX-Redirect"] = reverse("chat_thread", kwargs={"thread_id": thread.id})
            return response
        # Existing thread — return ONLY the assistant bubble.
        # The user bubble is already shown immediately by JS before the request fires.
        return render(
            request,
            "chat/_assistant_bubble.html",
            {"reply": reply_text},
        )

    return redirect("chat_thread", thread_id=thread.id)


@login_required
@require_POST
def delete_thread(request, thread_id):
    thread = get_object_or_404(ChatThread, id=thread_id, user=request.user)
    thread.delete()
    return redirect("chat_home")
