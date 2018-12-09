#!/usr/bin/python

from rpi_hat_eval_board  import rpi_hat_eval_board
from rpi_i2c             import rpi_i2c
from BQ25898D            import BQ25898D
from BQ25910             import BQ25910
import time

bq25910      = BQ25910(debug=False)
bq25898d     = BQ25898D(debug=False)
eb           = rpi_hat_eval_board(debug=False)

print "\n-> Ensure all relays are off <-"
eb.relay_vin.relay_off()
eb.relay_otg.relay_off()
eb.relay_vsys.relay_off()

print "\n-> Read Internal ADC Vbat and Vsys <-"
bq25898d.read_adc_battery_voltage()
bq25898d.read_adc_vsys_voltage()

print "Enable Vsys Load of 500mA"
eb.relay_vsys.relay_off()
print "VSYS Bus voltage is %02f" % eb.ina233_u7_vsys.getBusVoltage_V()
print "VSYS Current is %02f mA"  % eb.ina233_u7_vsys.getCurrent_mA()
eb.load_vsys.set_current_load_ma(load=500.0)
print "VSYS Bus voltage is %02f" % eb.ina233_u7_vsys.getBusVoltage_V()
print "VSYS Current is %02f mA"  % eb.ina233_u7_vsys.getCurrent_mA()
time.sleep(5)
eb.relay_vsys.relay_off()

print "\n-> Enable Charging on Master Only<-"
bq25898d.disable_charging()
eb.qc3.set_adapter_voltage(voltage=5.0)
time.sleep(1)
#eb.qc3.set_adapter_voltage(voltage=9.0)
#time.sleep(1)
eb.relay_vin.relay_on()
bq25898d.set_ilim_current(input_current_limit=2.0)
bq25898d.set_charge_current(charge_current=0.5)
bq25898d.set_vsys_min_voltage(vsys_voltage=3.7)
bq25898d.set_charge_voltage_limit(vreg_voltage=4.2)
bq25898d.enable_charging()
time.sleep(2)
bq25898d.read_faults()
bq25898d.read_charge_status()
bq25898d.read_idpm_vdpm_status()
print "Internal ADC VBUS value is %f volts" % (bq25898d.read_adc_vbus_voltage())
print "Internal ADC Charge current is %f amps" % (bq25898d.read_adc_charge_current())
print "VIN Bus voltage is %02f" % eb.ina233_u6_vin.getBusVoltage_V()
print "VIN Current is %02f mA"  % eb.ina233_u6_vin.getCurrent_mA()
bq25898d.disable_charging()
#bq25898d.set_hiz_mode()
time.sleep(2)

print "\n-> Enable Charging on Slave Only, VBUS less than INPUT VOLTAGE LIMIT<-"
bq25910.disable_watchdog()
bq25910.set_input_voltage_limit(input_voltage_limit=7.2)
bq25910.set_battery_voltage_limit(battery_voltage_limit=4.2)
bq25910.set_charge_current_limit(charge_current_limit=0.5)
bq25910.set_input_current_limit(input_current_limit=2.0)
bq25910.enable_charging()
time.sleep(2)
bq25910.read_charge_status()
bq25910.read_all_int_status()
bq25910.read_all_fault_status()
bq25910.read_all_int_flags()
bq25910.read_all_fault_flags()
print "VIN Bus voltage is %02f" % eb.ina233_u6_vin.getBusVoltage_V()
print "VIN Current is %02f mA"  % eb.ina233_u6_vin.getCurrent_mA()
print "\n-> Enable Charging on Slave Only, VBUS now greater than INPUT VOLTAGE LIMIT<-"
eb.qc3.set_adapter_voltage(voltage=9.0)
time.sleep(1)
bq25910.read_charge_status()
bq25910.read_all_int_status()
bq25910.read_all_fault_status()
bq25910.read_all_int_flags()
bq25910.read_all_fault_flags()
print "VIN Bus voltage is %02f" % eb.ina233_u6_vin.getBusVoltage_V()
print "VIN Current is %02f mA"  % eb.ina233_u6_vin.getCurrent_mA()
bq25910.disable_charging()
eb.relay_vin.relay_off()

print "\n-> Enable OTG with 500mA load using defaults <-"
eb.load_otg.set_current_load_ma(load=500.0)
bq25898d.enable_otg()
time.sleep(2)
bq25898d.read_faults()
eb.relay_otg.relay_off()
print "VIN Bus voltage is %02f" % eb.ina233_u6_vin.getBusVoltage_V()
print "VIN Current is %02f mA"  % eb.ina233_u6_vin.getCurrent_mA()
eb.relay_otg.relay_on()
print "VIN Bus voltage is %02f" % eb.ina233_u6_vin.getBusVoltage_V()
print "VIN Current is %02f mA"  % eb.ina233_u6_vin.getCurrent_mA()
bq25898d.read_adc_vbus_voltage()
time.sleep(5)
eb.load_otg.set_current_load_off()
print "VIN Bus voltage is %02f" % eb.ina233_u6_vin.getBusVoltage_V()
print "VIN Current is %02f mA"  % eb.ina233_u6_vin.getCurrent_mA()
bq25898d.disable_otg()

print "\n-> Ensure all relays are off <-"
eb.relay_vin.relay_off()
eb.relay_otg.relay_off()
eb.relay_vsys.relay_off()

print "\n-> Reset all registers <-"
bq25898d.reset_all_registers()
bq25910.reset_all_registers()

