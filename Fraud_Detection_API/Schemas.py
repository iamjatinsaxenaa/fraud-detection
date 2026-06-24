from pydantic import BaseModel, Field
from typing import Literal

class Transaction(BaseModel):

    amount: float = Field(
        ...,
        example=1500.00,
        description="Transaction kitne rupees ka tha? (1 se 50,000 ke beech)"
    )

    transaction_hour: int = Field(
        ...,
        example=14,
        description="Transaction kis time hua? (0=midnight, 6=subah, 12=dopahar, 18=shaam, 23=raat)"
    )

    merchant_category: Literal["grocery", "restaurant", "online", "atm", "travel", "other"] = Field(
        ...,
        example="online",
        description="Transaction kahan hua? grocery/restaurant/online/atm/travel/other"
    )

    transaction_type: Literal["purchase", "withdrawal", "transfer"] = Field(
        ...,
        example="purchase",
        description="Transaction ka type kya tha? purchase/withdrawal/transfer"
    )

    location_match: bool = Field(
        ...,
        example=True,
        description="Kya transaction aapke registered location se hua? (true=haan, false=nahi)"
    )

    is_foreign_transaction: bool = Field(
        ...,
        example=False,
        description="Kya ye transaction foreign country se hua? (true=haan, false=nahi)"
    )

    previous_fraud_count: int = Field(
        ...,
        example=0,
        description="Is card pe pehle kitni baar fraud hua? (0 matlab kabhi nahi)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 1500.00,
                "transaction_hour": 14,
                "merchant_category": "online",
                "transaction_type": "purchase",
                "location_match": True,
                "is_foreign_transaction": False,
                "previous_fraud_count": 0
            }
        }