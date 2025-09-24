import asyncio
from provider_agent import ProviderAgent
from customer_agent import CustomerAgent

async def run_scenario():
    provider = ProviderAgent("providerbaru@xmpp.jp", "prov12345")

    customer = CustomerAgent("customerbaru@xmpp.jp", "cust12345", "providerbaru@xmpp.jp")

    orders = [
        {"item": "Pizza", "qty": 2},
        {"item": "Burger", "qty": 1},
        {"item": "Pasta", "qty": 3},  
    ]
    customer.orders = orders  

    # Start agent
    await provider.start(auto_register=False)
    await customer.start(auto_register=False)

    print("=== Scenario Start: Multi-Item Order ===")

    await asyncio.sleep(5)

    # Stop agent
    await customer.stop()
    await provider.stop()

    print("=== Scenario End ===\n")


if __name__ == "__main__":
    asyncio.run(run_scenario())
