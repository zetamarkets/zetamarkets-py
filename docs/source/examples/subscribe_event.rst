Example 4: Subscribing to Events
--------------------------------

In this example we subscribe to all on-chain events related to our margin account (PlaceOrder, Trade, OrderComplete, Liquidate).
This is helpful to keep track of when your orders go through, when you get filled on trades etc.

.. literalinclude:: ../../../examples/subscribe_event.py
   :language: python
   :caption: subscribe_event.py