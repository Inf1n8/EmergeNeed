import google.cloud.dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from config import (DIALOGFLOW_LANGUAGE_CODE)
from google.protobuf.json_format import MessageToJson
import google.protobuf  as pf


def get_entities(txt, session_client, session):
    text_input = dialogflow.types.TextInput(text=txt, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    sentiment_config = dialogflow.SentimentAnalysisRequestConfig(
        analyze_query_text_sentiment=True
    )
    query_params = dialogflow.QueryParameters(
        sentiment_analysis_request_config=sentiment_config
    )
    try:
        response = session_client.detect_intent(request={
            "session": session,
            "query_input": query_input,
            "query_params": query_params
        })
    except InvalidArgument:
        raise
    res = { 
            'entities': list(set(dict(response.query_result.parameters)['symptoms'])),
            'text': response.query_result.query_text,
            'intent': response.query_result.intent.display_name,
            'intent_conf': response.query_result.intent_detection_confidence,
            'sentiment_score': response.query_result.sentiment_analysis_result.query_text_sentiment.score,
            'sentiment_magnitude': response.query_result.sentiment_analysis_result.query_text_sentiment.magnitude
        }
    return res