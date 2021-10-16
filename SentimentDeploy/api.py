from typing import Dict

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from .sentiment-analyzer import SentimentAnalyzer, getSA

app = FastAPI()

class SentimentRequest(BaseModel):
	text: str

class SentimentResponse(BaseModel):
	# probabilities: Dict[str, float]
	# sentiment: str
	output: list[Dict]


@app.post("/sentiment_analyze", response_model=SentimentResponse)
def classify(request: SentimentRequest, model: SentimentAnalyzer = Depends(getSA())):
	output = model.sentiment_analysis(request.text)
	return SentimentResponse(
		output=output
	)