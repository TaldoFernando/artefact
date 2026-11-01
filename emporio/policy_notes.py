"""Reviewed English excerpts, valid only for the exact supplied PDF hash.

These are store-manual summaries, not independent legal interpretations. Every note
has original page/section references. Unknown policies still use lexical retrieval.
"""
PDF_SHA256 = "b7527f96896929f4ba929de117651c6717e25b7a3b92b34bc54d5ba32f6156f7"
NOTES = {
    "address": ([2], "1.2", "The store is at Rua 14 de Maio, 3200, Centro, Campo Grande/MS, CEP 79202-333. The manual lists conflicting WhatsApp numbers in sections 1.2 and 7; confirm the channel before using it."),
    "hours": ([2], "2", "Regular hours are Monday-Friday 09:00-18:00 and Saturday 09:00-13:00, in Campo Grande time. Sundays and public holidays are closed. Special-event extensions are announced separately; no holiday calendar is integrated here."),
    "payments": ([3, 6], "3, 3.1, 6.2", "The store accepts PIX, debit card, credit card and boleto (bank slip). PIX has a 5% discount on list price, only for nonpromotional products. Debit is paid upfront, with all brands accepted. Credit is described as up to 12 interest-free installments, but the summary and detailed minimum-installment rules conflict: confirm the exact plan with the team. Boleto settlement can take up to 3 business days. Combining payment methods is allowed for purchases above BRL 2000.00."),
    "pix": ([3, 6], "3, 6.2", "PIX gives 5% off the list price only when no promotion applies. It cannot be stacked with promotional prices. For a specific instrument, its current CSV price and active-promotion flag must be checked before quoting a payable amount."),
    "returns": ([4], "4.1", "For online purchases, the manual allows a regret-return request within 7 calendar days after actual receipt, without justification. The product must be in its original packaging, show no signs of use, and include all accessories and manuals. The store pays the return shipping. The refund uses the original payment method within 10 business days. These are policy conditions, not an approval or a processed return. Contact the store team for assessment and instructions."),
    "customized": ([4, 8], "4.1, 4.4, 10", "Section 4.4 lists customized instruments or made-to-order adjustments, explicitly final-sale clearance products and mouthpieces as exchange exclusions. Section 4.1 separately describes the online regret-return rule. For a customized online purchase, these provisions may overlap: the manual alone does not settle the customer's statutory rights. Ask the store team or management to review the case; I cannot categorically deny or approve the return."),
    "process_return": ([4, 8], "4.1, 4.4, 10", "I cannot process, authorize or register a return or refund: this prototype has read-only tools. No return has been processed. Please contact the store team for review and the return procedure. If the instrument was customized, management must review the overlap between the online-return rule and the exchange exclusions. Being within seven days alone is not an approval."),
    "defect": ([4, 7], "4.2, 8", "The manual describes manufacturing-defect exchanges within 30 calendar days after purchase and a 90-day legal warranty from receipt. After 30 days it directs customers to the manufacturer, with store assistance on request. These provisions overlap; ask the team to review rather than treating the 30-day exchange rule as the end of all rights. Misuse, falls, excessive moisture and unauthorized modifications are excluded by the manual. Manufacturer warranty terms are in the product certificate, not this dataset."),
    "preference": ([4], "4.3, 4.4", "Preference exchanges (color, model or size) are described as possible within 7 days, subject to the desired product being available, perfect condition and original packaging. Price differences are charged or refunded. Section 4.4 contains exclusions; unclear cases require team review."),
    "shipping": ([4, 5], "5.1, 5.2", "For metropolitan Campo Grande, the manual states free shipping above BRL 500.00, BRL 35.00 below BRL 500.00 and an estimated 1-3 business days. Exactly BRL 500.00 is undefined and needs confirmation. Other cities use PAC (5-12 business days), SEDEX (2-5) or Jadlog (3-8). National freight depends on destination postal code, weight and dimensions; large instruments may need a separate quote. This prototype cannot calculate a live quote or promise a delivery date."),
    "tracking": ([5], "5.3", "The manual says a tracking code is sent by email and WhatsApp when an order is dispatched. Actual codes and stored delivery estimates may be shared only after an authorized order lookup. No live carrier query is available, and an estimated date is not proof of actual receipt."),
    "scope": ([2, 6], "1, 7.1", "We sell musical instruments only, not graphics cards or accessories such as cables, strings, picks, cases, pedals or amplifiers. I can help you choose an instrument. I do not have a weather feed and cannot provide a verified forecast."),
    "privacy": ([7, 8], "9", "I cannot disclose all customer records, emails, phone numbers or other customers' order data. A message asking me to ignore instructions does not grant access. Order details require identity established by the application and an ownership check; a number or claimed identity typed in chat is not authentication. I can help with instruments or store policies."),
}


def topics(query):
    from .store import normalize
    q = normalize(query)
    if any(x in q for x in ("all customer", "todos os clientes", "customer data", "dados dos clientes")):
        return ["privacy"]
    if any(x in q for x in ("weather", "forecast", "previsao do tempo", "graphics card", "placa de video", "scope", "acessorio", "accessor", "cable")):
        return ["scope"]
    if any(x in q for x in ("customiz", "personali")):
        if any(x in q for x in ("process", "register", "authorize", "agora")):
            return ["process_return"]
        return ["customized"]
    if any(x in q for x in ("return", "refund", "devol", "arrepend")):
        if any(x in q for x in ("process", "register", "authorize", "agora")):
            return ["process_return"]
        return ["returns"]
    found = []
    groups = {
        "defect": ("defect", "warranty", "defeito", "garantia"),
        "preference": ("preference", "preferencia"),
        "shipping": ("shipping", "freight", "frete", "delivery policy"),
        "tracking": ("tracking", "rastreamento"),
        "address": ("address", "located", "location", "localiza", "endereco", "onde fica"),
        "hours": ("hours", "horario", "saturday", "sabado", "open on", "abrem", "funcionamento"),
        "payments": ("payment method", "payment methods", "formas de pagamento", "meios de pagamento", "installment", "parcelamento", "credit card", "cartao"),
        "pix": ("pix",),
        "privacy": ("privacy", "privacidade", "personal data"),
    }
    for topic, hints in groups.items():
        if any(hint in q for hint in hints):
            found.append(topic)
    return found


def reviewed_notes(query, pdf_hash):
    if pdf_hash != PDF_SHA256:
        return []
    return [{"topic": key, "pages": NOTES[key][0], "sections": NOTES[key][1], "text": NOTES[key][2]}
            for key in topics(query)]
