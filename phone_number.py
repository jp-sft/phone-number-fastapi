"""
    Provide REST api to get all features of Google common lib phone_number
"""
from fastapi import FastAPI, HTTPException, Path
from starlette.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import phonenumbers as pn

origins = ["*"]


app = FastAPI(tags=["PhoneNumber"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PhoneNumberInfo(BaseModel):
    phone_number: str
    country_code: str
    national_number: str
    extension: str
    italian_leading_zero: str
    number_of_leading_zeros: str
    raw_input: str
    country_code_source: str
    preferred_domestic_carrier_code: str
    type: str
    is_possible_number: bool
    is_valid_number: bool
    region_code: str | None
    number_type: int

    @staticmethod
    def from_phonenumber(phone_number: pn.phonenumber.PhoneNumber):
        return PhoneNumberInfo(
            phone_number=pn.format_number(phone_number, pn.PhoneNumberFormat.E164),
            country_code=str(phone_number.country_code),
            national_number=str(phone_number.national_number),
            extension=str(phone_number.extension),
            italian_leading_zero=str(phone_number.italian_leading_zero),
            number_of_leading_zeros=str(phone_number.number_of_leading_zeros),
            raw_input=str(phone_number.raw_input),
            country_code_source=str(phone_number.country_code_source),
            preferred_domestic_carrier_code=str(
                phone_number.preferred_domestic_carrier_code
            ),
            type=str(pn.number_type(phone_number)),
            is_possible_number=pn.is_possible_number(phone_number),
            is_valid_number=pn.is_valid_number(phone_number),
            region_code=pn.region_code_for_number(phone_number),
            number_type=pn.number_type(phone_number),
        )


@app.get("/")
def info():
    return {"message": "This is a phone number validation service"}


@app.get(
    "/{number}", operation_id="get_phone_number_info", response_model=PhoneNumberInfo
)
def get_phone_number(
    number: str = Path(
        ..., title="Phone number", description="The phone number to validate"
    )
):
    try:
        phone_number = pn.parse(number)
    except pn.phonenumberutil.NumberParseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return PhoneNumberInfo.from_phonenumber(phone_number)


@app.get(
    "/{number}/validate", operation_id="validate_phone_number", response_model=bool
)
def validate_phone_number(
    number: str = Path(
        ..., title="Phone number", description="The phone number to validate"
    )
):
    try:
        phone_number = pn.parse(number)
    except pn.phonenumberutil.NumberParseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return pn.is_valid_number(phone_number)
