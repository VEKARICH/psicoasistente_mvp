from dataclasses import dataclass
from typing import Protocol

from app.config import get_settings

settings = get_settings()

CRISIS_KEYWORDS = {
    "suicidio", "suicidarme", "matarme", "quitarme la vida", "autolesión", "autolesion", "cortarme",
    "hacerme daño", "hacerme dano", "no quiero vivir", "me quiero morir", "lastimar a alguien",
    "dañar a alguien", "dano a otros", "daño a otros",
}

INTENT_KEYWORDS = {
        "soledad": {
        "soledad",
        "me siento solo",
        "me siento sola",
        "miedo a la soledad",
        "temor a la soledad",
        "miedo al abandono",
        "abandono",
        "rechazo",
        "quedarme solo",
        "quedarme sola",
    },
    "ansiedad": {
        "ansiedad",
        "ansioso",
        "ansiosa",
        "nervios",
        "angustia",
        "pánico",
        "panico",
        "preocupado",
        "preocupada",
        "taquicardia",
    },
    "tristeza": {    "triste", "tristeza", "llorar", "vacío", "vacio", "desanimado", "desanimada"
    },
    "estres": {"estrés", "estres", "agotado", "agotada", "abrumado", "abrumada", "presión", "presion", "burnout"
    },
    "problemas_personales": {"pareja", "familia", "discusión", "discusion", "amigo", "amiga", "conflicto", "problema"
    },
    "depresion_sin_diagnostico": {"depresión", "depresion", "sin ganas", "no tengo energía", "no tengo energia", "apatía", "apatia"
    },
}


class FutureLLMAdapter(Protocol):
    def generate(self, message: str, context: list[dict]) -> str:  # pragma: no cover
        ...


@dataclass
class AssistantReply:
    reply_text: str
    safety_flag: str | None
    intent: str | None


def _normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def detect_crisis(message: str) -> bool:
    text = _normalize(message)
    return any(k in text for k in CRISIS_KEYWORDS)


import re
import unicodedata


def _normalize_text(text: str) -> str:
    text = (text or "").lower().strip()
    # Quitar tildes
    text = "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )
    # Espacios normales
    text = re.sub(r"\s+", " ", text)
    return text


def detect_intent(user_text: str) -> str:
    text = _normalize_text(user_text)

    # 1) Crisis primero (si ya tienes esta lógica, mantenla)
    crisis_terms = [
        "me quiero morir", "quiero matarme", "suicid", "autolesion",
        "hacerme dano", "hacerme daño", "matar a alguien", "hacer dano a alguien"
    ]
    if any(term in text for term in crisis_terms):
        return "crisis"

    # 2) Elegir la coincidencia más específica (keyword más larga)
    best_intent = None
    best_keyword_len = -1

    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            nkw = _normalize_text(kw)
            if nkw in text:
                # Priorizar keyword más larga (más específica)
                if len(nkw) > best_keyword_len:
                    best_intent = intent
                    best_keyword_len = len(nkw)

    return best_intent or "general"


def _base_prefix() -> str:
    return (
        "Gracias por escribir. Lo que sientes importa, y podemos pensar en pasos pequeños y seguros. "
        "No puedo diagnosticar ni reemplazar atención profesional, pero sí darte orientación general."
    )


def _follow_up() -> str:
    return "Si quieres, cuéntame qué parte te está pesando más ahora mismo (pensamientos, cuerpo, sueño o situación)."


def crisis_response() -> AssistantReply:
    text = (
        "Siento que estés pasando por esto. Tu seguridad es lo más importante en este momento. "
        "Por favor busca ayuda inmediata con una persona adulta/de confianza cercana ahora mismo y contacta servicios de emergencia de tu país si estás en peligro o podrías hacerte daño o dañar a alguien. "
        "Si puedes, evita quedarte a solas y aléjate de objetos con los que puedas lastimarte. "
        "También puedes decirme si estás con alguien de confianza en este momento para orientarte en pasos de apoyo generales.\n\n"
        f"{settings.disclaimer_text}"
    )
    return AssistantReply(reply_text=text, safety_flag="CRISIS", intent="crisis")


def _resp_ansiedad() -> str:
    return (
        f"{_base_prefix()}\n\n"
        "Cuando hay ansiedad, suele ayudar bajar la activación del cuerpo primero. Prueba esta respiración guiada simple:\n"
        "- Inhala por la nariz 4 segundos\n"
        "- Exhala lento 6 segundos\n"
        "- Repite 5 veces sin forzarte\n\n"
        "También puede servir: notar 5 cosas que ves, 4 que sientes y 3 que oyes (anclaje al presente). "
        "Si esto te pasa seguido, buscar apoyo profesional puede darte herramientas más personalizadas.\n\n"
        f"{_follow_up()}\n\n{settings.disclaimer_text}"
    )


def _resp_tristeza() -> str:
    return (
        f"{_base_prefix()}\n\n"
        "Con tristeza, a veces funciona enfocarse en cuidados básicos antes de resolver todo:\n"
        "- Comer algo simple e hidratarte\n"
        "- Dar una caminata corta o moverte 5–10 minutos\n"
        "- Escribir en un journal: qué siento, qué lo activó, qué necesito hoy\n"
        "- Hablar con alguien de confianza aunque sea por mensaje\n\n"
        "No tienes que cargarlo solo/a. Pedir apoyo es una fortaleza.\n\n"
        f"{_follow_up()}\n\n{settings.disclaimer_text}"
    )

def _resp_soledad() -> str:
    return (
        f"{_base_prefix()}\n\n"
        "Tener miedo a la soledad puede sentirse muy intenso, y no significa que estés haciendo algo mal. "
        "A veces ayuda trabajar en dos frentes: calmar el momento y construir apoyo poco a poco.\n\n"
        "Puedes probar esto hoy:\n"
        "- Haz una pausa de respiración (inhala 4 segundos, exhala 6 segundos, 5 repeticiones)\n"
        "- Escribe en una nota o journal: qué pensamiento aparece (ej. ‘me voy a quedar solo/a’) y qué evidencia real tengo ahora\n"
        "- Contacta a una persona de confianza con un mensaje simple (ej. ‘¿tienes 10 minutos para hablar?’)\n"
        "- Planea una actividad breve con conexión (caminar con alguien, llamada, estudiar acompañado/a, grupo/club)\n"
        "- Mantén una rutina básica (sueño, comida, movimiento), porque cuando estamos agotados la sensación de soledad pesa más\n\n"
        "Si este miedo te está afectando mucho o se repite seguido, buscar apoyo profesional puede ayudarte a trabajarlo con herramientas más personalizadas.\n\n"
        "Si quieres, puedo ayudarte a convertir eso en un plan concreto para hoy (por ejemplo: a quién escribir, qué decir y qué hacer si no responden de inmediato).\n\n"
        f"{settings.disclaimer_text}"
    )
    
def _resp_estres() -> str:
    return (
        f"{_base_prefix()}\n\n"
        "Cuando hay estrés/agotamiento, ayuda bajar la exigencia y ordenar por prioridad mínima:\n"
        "1) Elige una sola tarea pequeña (5–15 min)\n"
        "2) Haz una pausa breve sin pantalla\n"
        "3) Revisa sueño, comida e hidratación\n"
        "4) Si puedes, pide ayuda concreta (ej. acompañamiento, dividir tareas)\n\n"
        "Si quieres, puedo ayudarte a convertir lo que tienes encima en un plan de pasos pequeños.\n\n"
        f"{settings.disclaimer_text}"
    )


def _resp_problemas_personales() -> str:
    return (
        f"{_base_prefix()}\n\n"
        "En problemas personales (familia, amistades, pareja), suele ayudar separar: hechos, emociones y necesidades.\n"
        "Una forma breve de expresarlo es: ‘Cuando pasó X, me sentí Y, y necesito Z’.\n"
        "También puedes escribirlo primero antes de hablar para ordenar ideas.\n\n"
        "Si hay una situación de riesgo, violencia o miedo, busca apoyo inmediato de una persona adulta/de confianza o servicios de emergencia de tu país.\n\n"
        f"{_follow_up()}\n\n{settings.disclaimer_text}"
    )


def _resp_depresion() -> str:
    return (
        f"{_base_prefix()}\n\n"
        "Lo que describes puede sentirse muy pesado. Sin hacer diagnóstico, sí es importante tomarlo en serio y buscar apoyo profesional si esto dura varios días o afecta sueño, energía, estudio/trabajo o relaciones.\n\n"
        "Mientras tanto, prueba objetivos muy pequeños y realistas hoy:\n"
        "- ducharte o lavarte la cara\n"
        "- comer algo\n"
        "- salir a la luz del día unos minutos\n"
        "- escribir cómo te sientes del 0 al 10\n"
        "- avisarle a alguien de confianza que no la estás pasando bien\n\n"
        f"{_follow_up()}\n\n{settings.disclaimer_text}"
    )


def _resp_general() -> str:
    return (
        f"{_base_prefix()}\n\n"
        "Puedo acompañarte con orientación general y herramientas seguras como respiración, journaling, organización de pasos pequeños, hábitos de sueño y cómo pedir apoyo.\n\n"
        f"{_follow_up()}\n\n{settings.disclaimer_text}"
    )


def generate_safe_reply(message: str, history: list[dict] | None = None, llm_adapter: FutureLLMAdapter | None = None) -> AssistantReply:
    # Punto de extensión futuro (LLM): se mantiene apagado en este MVP por seguridad/costo/configuración.
    _ = history, llm_adapter

    if detect_crisis(message):
        return crisis_response()

    intent = detect_intent(message)
    if intent == "ansiedad":
        return AssistantReply(_resp_ansiedad(), None, intent)
    if intent == "tristeza":
        return AssistantReply(_resp_tristeza(), None, intent)
    if intent == "soledad":
        return AssistantReply(_resp_soledad(), None, intent)
    if intent == "estres":
        return AssistantReply(_resp_estres(), None, intent)
    if intent == "problemas_personales":
        return AssistantReply(_resp_problemas_personales(), None, intent)
    if intent == "depresion_sin_diagnostico":
        return AssistantReply(_resp_depresion(), None, intent)
    return AssistantReply(_resp_general(), None, "general")
