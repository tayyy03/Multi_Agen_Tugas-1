import json
import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from datetime import datetime
from logger import log_message

class ProviderAgent(Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.inventory = {
            "Pizza": 5,
            "Burger": 3,
            "Pasta": 0,   
        }

    class HandleOrderBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  
            if msg:
                try:
                    content = json.loads(msg.body)
                    performative = msg.metadata.get("performative", "inform")
                    conv_id = msg.metadata.get("conversation-id", "conv-unknown")

                    # log pesan masuk
                    log_message(msg.sender, self.agent.jid, performative, conv_id, content)

                    if performative == "request":
                        item = content.get("item")
                        qty = content.get("qty", 1)

                        if self.agent.inventory.get(item, 0) >= qty:
                            response = {
                                "available": True,
                                "eta": random.randint(15, 45),
                                "delivery_fee": 15000,
                            }
                            reply = Message(to=str(msg.sender))
                            reply.set_metadata("performative", "propose")
                            reply.set_metadata("conversation-id", conv_id)
                            reply.body = json.dumps(response)
                            await self.send(reply)

                            log_message(self.agent.jid, msg.sender, "propose", conv_id, response)

                        else:
                            substitute = "Burger" if item != "Burger" else "Pizza"
                            response = {
                                "available": False,
                                "substitute": substitute,
                                "eta": random.randint(20, 50),
                                "delivery_fee": 18000,
                            }
                            reply = Message(to=str(msg.sender))
                            reply.set_metadata("performative", "propose")
                            reply.set_metadata("conversation-id", conv_id)
                            reply.body = json.dumps(response)
                            await self.send(reply)

                            log_message(self.agent.jid, msg.sender, "propose", conv_id, response)

                    elif performative == "accept-proposal":
                        item = content.get("item")
                        qty = content.get("qty", 1)

                        if self.agent.inventory.get(item, 0) >= qty:
                            self.agent.inventory[item] -= qty
                            order_id = f"ORD{random.randint(1000,9999)}"
                            confirmation = {"order_id": order_id, "status": "confirmed"}
                            reply = Message(to=str(msg.sender))
                            reply.set_metadata("performative", "inform")
                            reply.set_metadata("conversation-id", conv_id)
                            reply.body = json.dumps(confirmation)
                            await self.send(reply)

                            log_message(self.agent.jid, msg.sender, "inform", conv_id, confirmation)
                        else:
                            fail_msg = {"status": "failed", "reason": "Out of stock (race condition)"}
                            reply = Message(to=str(msg.sender))
                            reply.set_metadata("performative", "failure")
                            reply.set_metadata("conversation-id", conv_id)
                            reply.body = json.dumps(fail_msg)
                            await self.send(reply)

                            log_message(self.agent.jid, msg.sender, "failure", conv_id, fail_msg)

                except Exception as e:
                    print(f"[Provider] Error parsing message: {e}")

    async def setup(self):
        print(f"[Provider] Agent {self.jid} started")
        self.add_behaviour(self.HandleOrderBehaviour())
