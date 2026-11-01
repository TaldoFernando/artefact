# 04 promotion

Actual local model transcript. Model: `qwen3:8b`.

**Customer:** What is the current price of the Kalani KAL-700T? Can I stack a PIX discount with its promotion?

**Mel:** Here's what I found in the supplied catalog snapshot (prices in BRL):

- **Kalani KAL-700T Tenor Natural**: BRL 323.10. Stock: 11; status: active.
  List price: BRL 359.00; active promotion: 10% off. The extra 5% PIX discount does not apply.

These are source-file records, not a live stock guarantee. Would you like to compare specific models?

<details><summary>Tool evidence</summary>

```json
[
  {
    "tool": "search_products",
    "arguments": {
      "available_only": true,
      "query": "Kalani KAL-700T"
    },
    "result": {
      "source": "products.csv + promotions.csv (provided snapshot, not a live ERP)",
      "queried_at_utc": "2026-11-01T19:38:26.328278+00:00",
      "total_matches": 1,
      "products": [
        {
          "product_id": 127,
          "name": "Kalani KAL-700T Tenor Natural",
          "status": "active",
          "stock_quantity": 11,
          "available": true,
          "list_price_brl": "359.00",
          "discount_percent": "10",
          "price_brl": "323.10",
          "promotion_active": true,
          "pix_price_brl": "323.10",
          "pix_discount_applied": false,
          "payment_rule": "PIX discount does not apply to promotional prices.",
          "description": "Ukulele tenor Kalani com corpo em Sapele e tampo em Spruce. Boa relação custo-benefício para quem busca um instrumento maior."
        }
      ],
      "truncated": false
    }
  }
]
```

</details>
