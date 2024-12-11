import logging
from fastapi import  APIRouter

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
