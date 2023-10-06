Example 3: Subscribing to Orderbook Accounts (Advanced)
-------------------------------------------------------

This is a more advanced version of :doc:`subscribing to an account <subscribe_account>`. Here we handle the websocket connection ourselves and open 2 account subscriptions to both the bid and ask accounts of the orderbook, streaming updates over the single websocket connection.
Based on the subscription id, we can then determine which updates are bid and ask data.

.. literalinclude:: ../../../examples/subscribe_orderbook.py
   :language: python
   :caption: subscribe_orderbook.py