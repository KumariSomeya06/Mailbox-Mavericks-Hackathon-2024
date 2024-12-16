import logging
from fastapi import  APIRouter
from .model import EmailPriorityRequest

from .service import EmailService

logger = logging.getLogger()
router = APIRouter()

@router.get("/emailresponse/{clientid}/{emailid}",tags=["Email"])
async def Email_Response(clientid:int,emailid:int):
    result = await EmailService.email_response(clientid=clientid, emailid=emailid)
    return result

@router.get("/email/{clientid}",tags=["Email"])
async def Specific_Email(clientid:int):
    result =  await EmailService.specific_email(clientid)
    return result
 

@router.get("/emaillist",tags=["Email"])
async def Email_List():
    result =  await EmailService.email_list()
    return result


@router.get("/priorityanalyze", tags=["Email Analysis"])
async def Email_List_With_Analysis(request: EmailPriorityRequest):
    priority  = await EmailService.email_with_priorityanalysis(request.email_body)
    return {"priority": priority}


@router.get("/sentimentanalyze", tags=["Email Analysis"])
async def Email_List_With_Analysis(request: EmailPriorityRequest):
    sentiment = await EmailService.email_with_sentimentanalysis(request.email_body)
    return {"sentiment": sentiment}


@router.get("/emaillist/analyze", tags=["Email Analysis"])
async def Email_List_With_Analysis():
    result = await EmailService.email_list_with_analysis()
    return result.to_dict()

