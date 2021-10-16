from typing import Dict

from fastapi import Depends, FastAPI
from pydantic import BaseModel

import SentimentAnalyzer, getSA

app = FastAPI()

class SentimentRequest(BaseModel):
	text: str

class SentimentResponse(BaseModel):
	# probabilities: Dict[str, float]
	# sentiment: str
	output: list[Dict]


@app.post("/sentiiment_analyze", response_model=SentimentResponse)
def classify(request: SentimentRequest, model: SentimentAnalyzer = Depends(getSA())):
	output = model.sentiment_analysis(request.text)
	return SentimentResponse(
		output=output
	)