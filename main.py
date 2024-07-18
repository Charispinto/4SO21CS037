from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
import requests
app = FastAPI()

win_size = 10

arr = {
    "p": [],
    "f": [],
    "e": [],
    "r": []
}

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIxMjk2NjMyLCJpYXQiOjE3MjEyOTYzMzIsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjVhYTgxOWFmLWViZDYtNDI0Mi1iOTgzLWI3ODMwMzllMzhkZiIsInN1YiI6IjIxaDE2LmNoYXJpc0BzamVjLmFjLmluIn0sImNvbXBhbnlOYW1lIjoiZ29NYXJ0IiwiY2xpZW50SUQiOiI1YWE4MTlhZi1lYmQ2LTQyNDItYjk4My1iNzgzMDM5ZTM4ZGYiLCJjbGllbnRTZWNyZXQiOiJUc254eUlTQmtOd0V2YlhzIiwib3duZXJOYW1lIjoiQ2hhcmlzIiwib3duZXJFbWFpbCI6IjIxaDE2LmNoYXJpc0BzamVjLmFjLmluIiwicm9sbE5vIjoiNFNPMjFDUzAzNyJ9.gMSwoecJ3-Qzaug4xVbnWOM2YSTYiEMp-EZH1HEUiOo"

headers = {
    "Authorization": f"Bearer {access_token}"
}

class ResponseModel(BaseModel):
    windowPrevState: List[int]
    windowCurrState: List[int]
    numbers: List[int]
    avg: float

async def fetch_numbers(number_type: str):
        response = requests.get(f"http://20.244.56.144/test/{number_type}", headers=headers)
        response.raise_for_status()
        numbers = response.json().get('numbers', [])
        print(numbers)
        return numbers

def num_type(uid):
    match uid:
        case 'e':
            return 'even'
        case 'p':
            return 'primes'
        case 'f':
            return 'fibo'
        case 'r':
            return 'rand'
        
def calc_avg(numbers: List[int]):
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

@app.get("/numbers/{number_type}", response_model=ResponseModel)
async def get_numbers(number_type: str):
    prev_state = arr[number_type].copy()
    print(number_type)

    numbers = await fetch_numbers(num_type(number_type))
    
    for number in numbers:
        if number not in arr[number_type]:
            if len(arr[number_type]) >= win_size:
                arr[number_type].pop(0)
            arr[number_type].append(number)

    curr_state = arr[number_type]
    avg = calc_avg(curr_state)

    return ResponseModel(
        windowPrevState=prev_state,
        windowCurrState=curr_state,
        numbers=numbers,
        avg=avg
    )
