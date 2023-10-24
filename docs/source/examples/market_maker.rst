Example 6: Simple Market Maker Bot
--------------------------------------------

This example shows how to create a simple market maker bot that will quote on both sides of the orderbook for a given market. 
It references the Binance USD-M futures market midpoint as the fair price, and dynamically adjusts quotes as the market moves.

You can market-make on the SOL-PERP market with 20bps edge by running:

.. code-block:: python
   
   python market_maker.py --asset SOL --edge 20

.. note::

   This bot can run using the public RPCs (default option), but if you're quoting aggressively you may want to run it 
   using your own RPC using the `-u` option as you'll likely get rate-limited.

.. literalinclude:: ../../../examples/market_maker.py
   :language: python
   :caption: market_maker.py