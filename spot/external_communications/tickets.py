import requests
from settings.settings import DEMO_API_URL

def get_tickets_by_customer(address):
    res = requests.get(DEMO_API_URL+ "/tickets", params={'customer': address})
    return res.json()

def spend_ticket(ticket_id):
    requests.post(DEMO_API_URL+ '/spendings', params={"ticket_id": ticket_id})