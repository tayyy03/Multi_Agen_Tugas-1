import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from logger import log_message


class CustomerAgent(Agent):
    def __init__(self, jid, password, provider_jid):
        super().__init__(jid, password)
        self.provider_jid = provider_jid
        self.orders = [
            {"item": "Pizza", "qty": 2},
            {"item": "Burger", "qty": 1},
            {"item": "Pasta", "qty": 3},
        ]

    class OrderBehaviour(CyclicBehaviour):
        async def on_start(self):
            # kirim semua order di awal
            for order in self.agent.orders:
                msg = Message(
                    to=self.agent.provider_jid,
                    body=json.dumps(order),
                    metadata={
                        "performative": "request",
                        "conversation_id": str(id(self.agent)),
                    },
                )
                await self.send(msg)
                print(f"[Customer] Kirim order: {order}")
                log_message(
                    self.agent.jid, self.agent.provider_jid,
                    "request", msg.metadata["conversation_id"], order
                )

        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                try:
                    content = json.loads(msg.body)
                except json.JSONDecodeError:
                    print("[Customer] Error: gagal decode isi pesan")
                    return

                performative = msg.metadata.get("performative", "")

                if performative == "propose":
                    if content.get("available", False):
                        print("[Customer] Terima proposal:", content)
                    else:
                        print("[Customer] Item habis. Substitusi ditawarkan:", content.get("substitute"))
                else:
                    print("[Customer] Pesan lain:", content)

    async def setup(self):
        self.add_behaviour(self.OrderBehaviour())
