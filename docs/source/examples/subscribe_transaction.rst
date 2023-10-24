Example 5: Subscribing to Transactions (Advanced)
-------------------------------------------------

This is a more advanced version of :doc:`subscribing to events <subscribe_event>` that shows how to subscribe to transactions.
Transactions are a superset of the event logs, they contain both event data as well as the transaction arguments. Hence the returned data is more verbose.

.. note::
   
   The :meth:`subscribe_transaction <zetamarkets_py.client.Client.subscribe_transactions>` method is not supported by the public Solana RPC interface (until RPC 2.0 is released). You will need to pass in a Triton RPC URL to run this example.
   More info can be found in `Triton's documentation <https://docs.triton.one/project-yellowstone/whirligig-websockets#transactionsubscribe>`_.

.. literalinclude:: ../../../examples/subscribe_transaction.py
   :language: python
   :caption: subscribe_transaction.py