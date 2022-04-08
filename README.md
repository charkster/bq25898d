# bq25898d
![picture](https://www.ti.com/content/dam/ticom/images/products/legacy-boards/b/bq25910evm-854_bq25910evm-854-image-board-1.jpg)

Python Class for controlling the BQ25898D

BQ25898D.py was created from the TI datasheet and verified on the BQ25910EVM-854 board (which also has a BQ25910 slave charger). test_bq25898d.py is an example of controlling both the bq25898d and bq25910 with a raspberry pi and custom relay board.

I hope to upload thermal images of the BQ25898D charging at 3, 4 and 5A.

I am planning to add routines for Quick Charge 3.0 and Pump Express wall adapter support (to negotiate new voltages from the wall adapter). QC 3.0 support requires a modification to the BQ25910EVM-854 board to get access to D+ and D-. I have a Pump Express adapter on order (Sony UCH12), and will checkout how reliably the BQ25898D is able to get 9V from that adapter.
