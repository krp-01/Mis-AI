def generate_local_response(question, profile):
    question_lower = question.lower()

    if "bursa" in question_lower or "invest" in question_lower:
        if profile["risc"] == "prudent":
            return (
                "Pentru profilul tau, ar fi mai bine sa incepi cu sume mici, "
                "investitii mai stabile si o strategie prudenta."
            )
        else:
            return (
                "Pentru profilul tau, poti analiza optiuni cu potential mai mare, "
                "dar cu reguli clare de control al riscului."
            )

    if "organiz" in question_lower or "program" in question_lower or "plan" in question_lower:
        if profile["disciplina"] == "disciplinat":
            return "Pentru tine ar functiona bine un plan clar, impartit pe pasi si obiective."
        else:
            return "Pentru tine ar fi mai bine un plan simplu, flexibil, usor de urmat."

    if profile["emotie"] == "emotional":
        return "Iti raspund intr-un mod calm, echilibrat si atent la partea emotionala."
    else:
        return "Iti raspund direct, logic si orientat spre eficienta."
