Example 6: Simple Market Maker Bot
--------------------------------------------

This example shows how to create a simple market maker bot that will quote on both sides of the orderbook for a given market. 
It references the Binance USD-M futures market midpoint as the fair price, and dynamically adjust quotes as the market moves.

You can market make on the SOL-PERP market with 20bps edge by running: `python market_maker.py -asset SOL -edge 20 -offset 0`

.. literalinclude:: ../../../examples/market_maker.py
   :language: python
   :caption: market_maker.py