#!/usr/bin/python

import time
import smbus
from rpi_i2c_new  import rpi_i2c

# ===========================================================================
# INA219 Class
# ===========================================================================

class BQ25898D:
	i2c = None

# ===========================================================================
#   I2C DEVICE ADDRESS
# ==========================================================================
	__BQ25898D_DEV_ID                           = 0x6A
# ===========================================================================

# ===========================================================================
#    INPUT CURRENT LIMIT CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG00                                = 0x00 # ADDRESS
# ===========================================================================
	__BQ25898D_REG00_INPUT_CURRENT_LIMIT_LSB        = 0.05 # Amps
	__BQ25898D_REG00_INPUT_CURRENT_LIMIT_MAX        = 3.15 # Amps
	__BQ25898D_REG00_INPUT_CURRENT_LIMIT_NUM_SHIFTS = 0
	__BQ25898D_REG00_INPUT_CURRENT_LIMIT_BIT_MASK   = 0x3F
	__BQ25898D_REG00_INPUT_CURRENT_LIMIT_PIN_ENABLE = 0x40
	__BQ25898D_REG00_HIZ_MODE_ENABLE                = 0x80
	
# ===========================================================================
#    WALL ADAPTER COMMUNICATION CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG01                            = 0x01 # ADDRESS
# ===========================================================================
	__BQ25898D_REG01_DPLUS_BIT_MASK             = 0xE0
	__BQ25898D_REG01_DPLUS_HIZ                  = 0x00
	__BQ25898D_REG01_DPLUS_0V                   = 0x20
	__BQ25898D_REG01_DPLUS_0P6V                 = 0x40
	__BQ25898D_REG01_DPLUS_1P2V                 = 0x60
	__BQ25898D_REG01_DPLUS_2P0V                 = 0x80
	__BQ25898D_REG01_DPLUS_2P7V                 = 0xA0
	__BQ25898D_REG01_DPLUS_3P3V                 = 0xC0
	__BQ25898D_REG01_DPLUS_SHORT                = 0xE0
	__BQ25898D_REG01_DMINUS_BIT_MASK            = 0x1C
	__BQ25898D_REG01_DMINUS_HIZ                 = 0x00
	__BQ25898D_REG01_DMINUS_0V                  = 0x04
	__BQ25898D_REG01_DMINUS_0P6V                = 0x08
	__BQ25898D_REG01_DMINUS_1P2V                = 0x0C
	__BQ25898D_REG01_DMINUS_2P0V                = 0x10
	__BQ25898D_REG01_DMINUS_2P7V                = 0x14
	__BQ25898D_REG01_DMINUS_3P3V                = 0x18
	__BQ25898D_REG01_MAXC_12V                   = 0x02
	__BQ25898D_REG01_VDPM_OS_BIT_MASK           = 0x01
	__BQ25898D_REG01_VDPM_OS_0P6A               = 0x01
	__BQ25898D_REG01_VDPM_OS_0P4A               = 0x00
	
# ===========================================================================
#    WALL ADAPTER COMMUNICATION AND ADC CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG02                            = 0x02 # ADDRESS
# ===========================================================================
	__BQ25898D_REG02_AUTO_DPDM_ENABLE           = 0x01
	__BQ25898D_REG02_FORCE_DPDM_ENABLE          = 0x02
	__BQ25898D_REG02_MAXC_ENABLE                = 0x04
	__BQ25898D_REG02_HVDCP_ENABLE               = 0x08
	__BQ25898D_REG02_ICO_ENABLE                 = 0x10
	__BQ25898D_REG02_BST_FREQ_BIT_MASK          = 0x20
	__BQ25898D_REG02_BST_FREQ_1P5M              = 0x20
	__BQ25898D_REG02_BST_FREQ_0P5M              = 0x00
	__BQ25898D_REG02_ADC_CONV_RATE_BIT_MASK     = 0x40
	__BQ25898D_REG02_ADC_CONV_RATE_CONTINUOUS   = 0x40
	__BQ25898D_REG02_ADC_CONV_RATE_1_SHOT       = 0x00
	__BQ25898D_REG02_ADC_CONV_START             = 0x80
	
# ===========================================================================
#    VSYS_MIN AND CHARGE CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG03                            = 0x03 # ADDRESS
# ===========================================================================
	__BQ25898D_REG03_MIN_VBAT_2P5_FALLING       = 0x01
	__BQ25898D_REG03_MIN_VBAT_2P9_FALLING       = 0x00
	__BQ25898D_REG03_MIN_VBAT_BIT_MASK          = 0x01
	__BQ25898D_REG03_VSYS_MIN_OFFSET            = 3.0
	__BQ25898D_REG03_VSYS_MIN_LSB               = 0.1
	__BQ25898D_REG03_VSYS_MIN_MAX               = 3.7
	__BQ25898D_REG03_VSYS_MIN_NUM_SHIFTS        = 1
	__BQ25898D_REG03_VSYS_MIN_BIT_MASK          = 0x0E
	__BQ25898D_REG03_CHG_CONFIG_ENABLE          = 0x10
	__BQ25898D_REG03_OTG_CONFIG_ENABLE          = 0x20
	__BQ25898D_REG03_WD_RST                     = 0x40
	__BQ25898D_REG03_FORCE_DSEL                 = 0x80

# ===========================================================================
#    CHARGE CURRENT CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG04                            = 0x04 # ADDRESS
# ===========================================================================
	__BQ25898D_REG04_CHARGE_CURRENT_LSB         = 0.064
	__BQ25898D_REG04_CHARGE_CURRENT_MAX         = 4.032
	__BQ25898D_REG04_CHARGE_CURRENT_NUM_SHIFTS  = 0
	__BQ25898D_REG04_CHARGE_CURRENT_BIT_MASK    = 0x7F
	__BQ25898D_REG04_EN_PUMPX                   = 0x80
	
# ===========================================================================
#    PRE AND TERMINATION CHARGE CURRENT CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG05                            = 0x05 # ADDRESS
# ===========================================================================
	__BQ25898D_REG05_ITERM_LSB                  = 0.064
	__BQ25898D_REG05_ITERM_MAX                  = 1.024
	__BQ25898D_REG05_ITERM_NUM_SHIFTS           = 0
	__BQ25898D_REG05_ITERM_BIT_MASK             = 0x0F
	__BQ25898D_REG05_IPRE_LSB                   = 0.064
	__BQ25898D_REG05_IPRE_MAX                   = 1.024
	__BQ25898D_REG05_IPRE_BIT_NUM_SHIFTS        = 4
	__BQ25898D_REG05_IPRE_BIT_MASK              = 0xF0

# ===========================================================================
#    CHARGE VOLTAGE LIMIT CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG06                            = 0x06 # ADDRESS
# ===========================================================================
	__BQ25898D_REG06_VREG_OFFSET                = 3.84
	__BQ25898D_REG06_VREG_LSB                   = 0.016
	__BQ25898D_REG06_VREG_MAX                   = 4.608
	__BQ25898D_REG06_VREG_NUM_SHIFTS            = 2
	__BQ25898D_REG06_VREG_BIT_MASK              = 0xFC
	__BQ25898D_REG06_BATLOWV_BIT_MASK           = 0x02
	__BQ25898D_REG06_BATLOWV_3P0                = 0x02
	__BQ25898D_REG06_BATLOWV_2P8                = 0x00
	__BQ25898D_REG06_VCHGREG_BIT_MASK           = 0x01
	__BQ25898D_REG06_VCHGREG_0P2                = 0x01
	__BQ25898D_REG06_VCHGREG_0P1                = 0x00
	
# ===========================================================================
#    CHARGE TIMER CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG07                            = 0x07 # ADDRESS
# ===========================================================================
	__BQ25898D_REG07_JEITA_BIT_MASK             = 0x01
	__BQ25898D_REG07_JEITA_20PER_ICHG           = 0x01
	__BQ25898D_REG07_JEITA_50PER_ICHG           = 0x00
	__BQ25898D_REG07_FAST_CHG_TIMER_BIT_MASK    = 0x06
	__BQ25898D_REG07_FAST_CHG_TIMER_5HR         = 0x00
	__BQ25898D_REG07_FAST_CHG_TIMER_8HR         = 0x02
	__BQ25898D_REG07_FAST_CHG_TIMER_12HR        = 0x04
	__BQ25898D_REG07_FAST_CHG_TIMER_20HR        = 0x06
	__BQ25898D_REG07_EN_TIMER_SAFETY            = 0x08
	__BQ25898D_REG07_WATCHDOG_BIT_MASK          = 0x30
	__BQ25898D_REG07_WATCHDOG_DISABLE           = 0x00
	__BQ25898D_REG07_WATCHDOG_40S               = 0x10
	__BQ25898D_REG07_WATCHDOG_80S               = 0x20
	__BQ25898D_REG07_WATCHDOG_160S              = 0x30
	__BQ25898D_REG07_STAT_DISABLE               = 0x40
	__BQ25898D_REG07_EN_TERM                    = 0x80
	
# ===========================================================================
#    IR COMPENSATION CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG08                            = 0x08 # ADDRESS
# ===========================================================================
	__BQ25898D_REG08_TREG_BIT_MASK              = 0x03
	__BQ25898D_REG08_TREG_60C                   = 0x00
	__BQ25898D_REG08_TREG_80C                   = 0x01
	__BQ25898D_REG08_TREG_100C                  = 0x02
	__BQ25898D_REG08_TREG_120C                  = 0x03
	__BQ25898D_REG08_IR_VCLAMP_LSB              = 0.032
	__BQ25898D_REG08_IR_VCLAMP_MAX              = 0.224
	__BQ25898D_REG08_IR_VCLAMP_NUM_SHIFTS       = 2
	__BQ25898D_REG08_IR_VCLAMP_BIT_MASK         = 0x1C
	__BQ25898D_REG08_IR_BAT_COMP_LSB            = 0.02
	__BQ25898D_REG08_IR_BAT_COMP_MAX            = 0.140
	__BQ25898D_REG08_IR_BAT_COMP_NUM_SHIFTS     = 5
	__BQ25898D_REG08_IR_BAT_COMP_BIT_MASK       = 0xE0

# ===========================================================================
#    PUMP EXPRESS AND BATFET CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG09                            = 0x09 # ADDRESS
# ===========================================================================
	__BQ25898D_REG09_PUMPX_DOWN_ENABLE          = 0x01
	__BQ25898D_REG09_PUMPX_UP_ENABLE            = 0x02
	__BQ25898D_REG09_BATFET_RST_N               = 0x04
	__BQ25898D_REG09_BATFET_DLY                 = 0x08
	__BQ25898D_REG09_JIETA_VSET                 = 0x10
	__BQ25898D_REG09_BATFET_DISABLE             = 0x20
	__BQ25898D_REG09_TIMER2X_ENABLE             = 0x40
	__BQ25898D_REG09_FORCE_ICO                  = 0x80
	
# ===========================================================================
#     OTG BOOST CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG0A                            = 0x0A # ADDRESS
# ===========================================================================
	__BQ25898D_REG0A_BOOST_LIM_BIT_MASK         = 0x07
	__BQ25898D_REG0A_BOOST_LIM_0P5              = 0x00
	__BQ25898D_REG0A_BOOST_LIM_0P8              = 0x01
	__BQ25898D_REG0A_BOOST_LIM_1P0              = 0x02
	__BQ25898D_REG0A_BOOST_LIM_1P2              = 0x03
	__BQ25898D_REG0A_BOOST_LIM_1P5              = 0x04
	__BQ25898D_REG0A_BOOST_LIM_1P8              = 0x05
	__BQ25898D_REG0A_BOOST_LIM_2P1              = 0x06
	__BQ25898D_REG0A_BOOST_LIM_2P4              = 0x07
	__BQ25898D_REG0A_PFM_OTG_DIS                = 0x80
	__BQ25898D_REG0A_BOOSTV_OFFSET              = 4.55
	__BQ25898D_REG0A_BOOSTV_LSB                 = 0.064
	__BQ25898D_REG0A_BOOSTV_MAX                 = 5.51
	__BQ25898D_REG0A_BOOSTV_NUM_SHIFTS          = 4
	__BQ25898D_REG0A_BOOSTV_BIT_MASK            = 0xF0
	
# ===========================================================================
#     VBUS AND CHARGER STATUS REGISTER (RO)
# ===========================================================================
	__BQ25898D_REG0B                            = 0x0B # ADDRESS
# ===========================================================================
	__BQ25898D_REG0B_VSYS_STAT                  = 0x01
	__BQ25898D_REG0B_PG_STAT                    = 0x04
	__BQ25898D_REG0B_CHGR_STAT_BIT_MASK         = 0x18
	__BQ25898D_REG0B_CHGR_STAT_NOT_CHARGING     = 0x00
	__BQ25898D_REG0B_CHGR_STAT_PRE_CHG          = 0x08
	__BQ25898D_REG0B_CHGR_STAT_FAST_CHARGING    = 0x10
	__BQ25898D_REG0B_CHGR_STAT_CHG_TERM_DONE    = 0x18
	__BQ25898D_REG0B_VBUS_STAT_BIT_MASK         = 0xE0
	__BQ25898D_REG0B_VBUS_STAT_NO_INPUT         = 0x00
	__BQ25898D_REG0B_VBUS_STAT_USB_CDP_1P5A     = 0x40
	__BQ25898D_REG0B_VBUS_STAT_USB_DCP_3P25A    = 0x60
	__BQ25898D_REG0B_VBUS_STAT_MAXCHARGE_1P5A   = 0x80
	__BQ25898D_REG0B_VBUS_STAT_UNKNOWN          = 0xA0
	__BQ25898D_REG0B_VBUS_STAT_NON_STANDARD     = 0xC0
	__BQ25898D_REG0B_VBUS_STAT_OTG              = 0xE0

# ===========================================================================
#     FAULT STATUS REGISTER (RO)
# ===========================================================================
	__BQ25898D_REG0C                            = 0x0C # ADDRESS
# ===========================================================================
	__BQ25898D_REG0C_NTC_FAULT_TS_WARM          = 0x02
	__BQ25898D_REG0C_NTC_FAULT_TS_COOL          = 0x03
	__BQ25898D_REG0C_NTC_FAULT_TS_COLD          = 0x05
	__BQ25898D_REG0C_NTC_FAULT_TS_HOT           = 0x06
	__BQ25898D_REG0C_BAT_FAULT                  = 0x08
	__BQ25898D_REG0C_CHGR_FAULT_INPUT           = 0x10
	__BQ25898D_REG0C_CHGR_FAULT_THERMAL_SHTDWN  = 0x20 
	__BQ25898D_REG0C_CHGR_FAULT_CHG_TIMER_EXP   = 0x30
	__BQ25898D_REG0C_BOOST_FAULT                = 0x40
	__BQ25898D_REG0C_WATCHDOG_FAULT             = 0x80
	
# ===========================================================================
#     VIN DPM CONFIG REGISTER (R/W)
# ===========================================================================
	__BQ25898D_REG0D                            = 0x0D # ADDRESS
# ===========================================================================
	__BQ25898D_REG0D_VINDPM_OFFSET              = 2.6
	__BQ25898D_REG0D_VINDPM_LSB                 = 0.1
	__BQ25898D_REG0D_VINDPM_MAX                 = 15.3
	__BQ25898D_REG0D_VINDPM_NUM_SHIFTS          = 0
	__BQ25898D_REG0D_VINDPM_BIT_MASK            = 0x7F
	__BQ25898D_REG0D_FORCE_VINDPM               = 0x80
	
# ===========================================================================
#     ADC BATTERY VOLTAGE VALUE REGISTER (RO)
# ===========================================================================
	__BQ25898D_REG0E                            = 0x0E # ADDRESS
# ===========================================================================
	__BQ25898D_REG0E_ADC_BATV_OFFSET            = 2.304
	__BQ25898D_REG0E_ADC_BATV_LSB               = 0.02
	__BQ25898D_REG0E_ADC_BATV_BIT_MASK          = 0x7F
	__BQ25898D_REG0E_THERM_STAT                 = 0x80
	
# ===========================================================================
#     ADC VSYS VOLTAGE VALUE REGISTER (RO)
# ===========================================================================
	__BQ25898D_REG0F                            = 0x0F # ADDRESS
# ===========================================================================
	__BQ25898D_REG0F_ADC_SYSV_OFFSET            = 2.304
	__BQ25898D_REG0F_ADC_SYSV_LSB               = 0.02
	__BQ25898D_REG0F_ADC_SYSV_BIT_MASK          = 0x7F
	
# ===========================================================================
#     ADC TS VOLTAGE PERCENT OF REGN VALUE REGISTER (RO) 
# ===========================================================================
	__BQ25898D_REG10                            = 0x10 # ADDRESS
# ===========================================================================
	__BQ25898D_REG10_TSPCT_OFFSET               = 0.21
	__BQ25898D_REG10_TSPCT_LSB                  = 0.00465
	__BQ25898D_REG10_TSPCT_MAX                  = 0.8
	
# ===========================================================================
#     ADC VBUS VOLTAGE VALUE REGISTER (RO) 
# ===========================================================================
	__BQ25898D_REG11                            = 0x11 # ADDRESS
# ===========================================================================
	__BQ25898D_REG11_ADC_VBUS_OFFSET            = 2.6
	__BQ25898D_REG11_ADC_VBUS_LSB               = 0.1
	__BQ25898D_REG11_ADC_VBUS_MAX               = 15.6
	__BQ25898D_REG11_ADC_VBUS_BIT_MASK          = 0x7F
	__BQ25898D_REG11_VBUS_GD                    = 0x80
	
# ===========================================================================
#     ADC CHARGE CURRENT VALUE REGISTER (RO) 
# ===========================================================================
	__BQ25898D_REG12                            = 0x12 # ADDRESS
# ===========================================================================
	__BQ25898D_REG12_ICHGR_LSB                  = 0.05
	__BQ25898D_REG12_ICHGR_MAX                  = 6.35
	
# ===========================================================================
#     EFFECTIVE IDPM CURRENT LIMIT VALUE REGISTER (RO) 
# ===========================================================================
	__BQ25898D_REG13                            = 0x13 # ADDRESS
# ===========================================================================
	__BQ25898D_REG13_IDPM_LIM_OFFSET            = 0.1
	__BQ25898D_REG13_IDPM_LIM_LSB               = 0.05
	__BQ25898D_REG13_IDPM_LIM_MAX               = 3.25
	__BQ25898D_REG13_IDPM_LIM_BIT_MASK          = 0x3F
	__BQ25898D_REG13_IDPM_STAT                  = 0x40
	__BQ25898D_REG13_VDPM_STAT                  = 0x80
	
# ===========================================================================
#     DEVICE INFO AND REGISTER RESET CONTROL REGISTER (RW) 
# ===========================================================================
	__BQ25898D_REG14                            = 0x14 # ADDRESS
# ===========================================================================
	__BQ25898D_REG14_DEVICE_REVISION_BIT_MASK   = 0x03
	__BQ25898D_REG14_TS_PROFILE_BIT_MASK        = 0x04
	__BQ25898D_REG14_DEVICE_PART_NUM_BIT_MASK   = 0x38
	__BQ25898D_REG14_ICO_OPTIMIZED_STATUS       = 0x40
	__BQ25898D_REG14_REG_RESET                  = 0x80


	# Constructor
	def __init__(self, address=__BQ25898D_DEV_ID, debug=False):
		self.i2c = rpi_i2c(address, debug=debug, name="bq25898d")
		self.address = address
		self.debug = debug
		
	# this routine will read the address register, set the bits high specified by the value and preserve all other bits
	def read_modify_write(self, address, value):
		present_reg_val = self.i2c.readU8(address)
		modified_reg_val = (present_reg_val | value) & 0xFF
		self.i2c.write8(address,modified_reg_val)
		if (self.debug == True):
			print "CALLED: read_modify_write, Address 0x%02x, Read value 0x%02x, Modified it to be 0x%02x, and wrote it" % (address,present_reg_val,modified_reg_val)
	
	# this routine will read the address register, set the bits low specified by the value and preserve all other bits
	def read_clear_write(self, address, value):
		present_reg_val = self.i2c.readU8(address)
		modified_reg_val = (present_reg_val & (~value)) & 0xFF
		self.i2c.write8(address,modified_reg_val)
		if (self.debug == True):
			print "CALLED: read_clear_write, Address 0x%02x, Read value 0x%02x, Modified it to be 0x%02x, and wrote it" % (address,present_reg_val,modified_reg_val)

	def write_bit_field(self, address, bit_mask, value): # value must be within the bit_mask
		present_reg_val = self.i2c.readU8(address)
		modified_reg_val = ((present_reg_val & (~bit_mask & 0xFF)) + (value & bit_mask & 0xFF)) & 0xFF
		self.i2c.write8(address,modified_reg_val)
		if (self.debug == True):
			print "CALLED: write_bit_field, Address 0x%02x, Read value 0x%02x, Modified it to be 0x%02x, and wrote it" % (address,present_reg_val,modified_reg_val)

	def trigger_adc_1_shot_conversion(self):
		self.read_clear_write(self.__BQ25898D_REG02, self.__BQ25898D_REG02_ADC_CONV_RATE_CONTINUOUS)
		self.read_modify_write(self.__BQ25898D_REG02, self.__BQ25898D_REG02_ADC_CONV_START)
		if (self.debug == True):
			print "CALLED: trigger_adc_1_shot_conversion"

	def read_adc_battery_voltage(self):
		self.trigger_adc_1_shot_conversion()
		reg_val = self.i2c.readU8(self.__BQ25898D_REG0E)
		battery_voltage = (reg_val & self.__BQ25898D_REG0E_ADC_BATV_BIT_MASK) * \
		                  self.__BQ25898D_REG0E_ADC_BATV_LSB + self.__BQ25898D_REG0E_ADC_BATV_OFFSET
		if (self.debug == True):
			print "CALLED read_adc_battery_voltage, raw register is 0x%02x real value is %f volts" % (reg_val,battery_voltage)
		return battery_voltage

	def read_adc_vsys_voltage(self):
		self.trigger_adc_1_shot_conversion()
		reg_val = self.i2c.readU8(self.__BQ25898D_REG0F)
		vsys_voltage = (reg_val & self.__BQ25898D_REG0F_ADC_SYSV_BIT_MASK) * \
		              self.__BQ25898D_REG0F_ADC_SYSV_LSB + self.__BQ25898D_REG0F_ADC_SYSV_OFFSET
		if (self.debug == True):
			print "CALLED: read_adc_vsys_voltage, raw register is 0x%02x real value is %f volts" % (reg_val,vsys_voltage)
		return vsys_voltage
		
	def read_adc_vbus_voltage(self):
		self.trigger_adc_1_shot_conversion()
		reg_val = self.i2c.readU8(self.__BQ25898D_REG11)
		vbus_voltage = (reg_val & self.__BQ25898D_REG11_ADC_VBUS_BIT_MASK) * \
		              self.__BQ25898D_REG11_ADC_VBUS_LSB + self.__BQ25898D_REG11_ADC_VBUS_OFFSET
		if (self.debug == True):
			print "CALLED: read_adc_vbus_voltage, raw register is 0x%02x real value is %f volts" % (reg_val,vbus_voltage)
		return vbus_voltage
		
	def read_adc_charge_current(self):
		self.trigger_adc_1_shot_conversion()
		reg_val = self.i2c.readU8(self.__BQ25898D_REG12)
		charge_current = (reg_val * self.__BQ25898D_REG12_ICHGR_LSB)
		if (self.debug == True):
			print "CALLED: read_adc_charge_current, raw register is 0x%02x real value is %f amps" % (reg_val,charge_current)
		return charge_current
		
	def read_charge_status(self):
		reg_val = self.i2c.readU8(self.__BQ25898D_REG0B)
		status = reg_val & self.__BQ25898D_REG0B_CHGR_STAT_BIT_MASK
		if (status == self.__BQ25898D_REG0B_CHGR_STAT_NOT_CHARGING):
			print "CHARGE STATUS: NOT CHARGING"
		elif (status == self.__BQ25898D_REG0B_CHGR_STAT_PRE_CHG):
			print "CHARGE STATUS: PRE CHARGE"
		elif (status == self.__BQ25898D_REG0B_CHGR_STAT_FAST_CHARGING):
			print "CHARGE STATUS: FAST CHARGING"
		elif (status == self.__BQ25898D_REG0B_CHGR_STAT_CHG_TERM_DONE):
			print "CHARGE STATUS: CHARGE TERMINATION COMPLETE"
		else:
			print "CHARGE STATUS: *** ERROR, UNKNOWN ***"
		
	def read_vsys_status(self):
		reg_val = self.i2c.readU8(self.__BQ25898D_REG0B)
		if (reg_val & self.__BQ25898D_REG0B_VSYS_STAT == self.__BQ25898D_REG0B_VSYS_STAT):
			vsys_stat = 1
			if (self.debug == True):
				print "CALLED: read_vsys_status, VSYS is in VSYS regulation (VBAT < VSYS_MIN)"
		else:
			vsys_stat = 0
			if (self.debug == True):
				print "CALLED: read_vsys_status, VSYS is not in regulation (VBAT > VSYS_MIN)"
		return vsys_stat
	
	def read_power_good_status(self):
		reg_val = self.i2c.readU8(self.__BQ25898D_REG0B)
		if (reg_val & self.__BQ25898D_REG0B_PG_STAT == self.__BQ25898D_REG0B_PG_STAT):
			pg_stat = 1
			if (self.debug == True):
				print "CALLED: read_power_good_status, Power is Good"
		else:
			pg_stat = 0
			if (self.debug == True):
				print "CALLED: read_power_good_status, Power is not Good"
		return pg_stat
	
	def read_faults(self):
		reg_val = self.i2c.readU8(self.__BQ25898D_REG0C)
		if (reg_val & self.__BQ25898D_REG0C_NTC_FAULT_TS_WARM == self.__BQ25898D_REG0C_NTC_FAULT_TS_WARM):
			print "NTC TS WARM is set"
		if (reg_val & self.__BQ25898D_REG0C_NTC_FAULT_TS_COOL == self.__BQ25898D_REG0C_NTC_FAULT_TS_COOL):
			print "NTC TS COOL is set"
		if (reg_val & self.__BQ25898D_REG0C_NTC_FAULT_TS_COLD == self.__BQ25898D_REG0C_NTC_FAULT_TS_COLD):
			print "NTC TS COLD is set"
		if (reg_val & self.__BQ25898D_REG0C_NTC_FAULT_TS_HOT == self.__BQ25898D_REG0C_NTC_FAULT_TS_HOT):
			print "NTC TS HOT is set"
		if (reg_val & self.__BQ25898D_REG0C_BAT_FAULT == self.__BQ25898D_REG0C_BAT_FAULT):
			print "BAT FAULT is set"
		if (reg_val & self.__BQ25898D_REG0C_CHGR_FAULT_INPUT == self.__BQ25898D_REG0C_CHGR_FAULT_INPUT):
			print "CHARGER INPUT FAULT is set"
		if (reg_val & self.__BQ25898D_REG0C_CHGR_FAULT_THERMAL_SHTDWN == self.__BQ25898D_REG0C_CHGR_FAULT_THERMAL_SHTDWN):
			print "CHARGER THERMAL SHUTDOWN FAULT is set"
		if (reg_val & self.__BQ25898D_REG0C_CHGR_FAULT_CHG_TIMER_EXP == self.__BQ25898D_REG0C_CHGR_FAULT_CHG_TIMER_EXP):
			print "CHARGER SAFETY TIMER EXPIRATION FAULT"
		if (reg_val & self.__BQ25898D_REG0C_BOOST_FAULT == self.__BQ25898D_REG0C_BOOST_FAULT):
			print "OTG BOOST FAULT is set"
		if (reg_val & self.__BQ25898D_REG0C_WATCHDOG_FAULT == self.__BQ25898D_REG0C_WATCHDOG_FAULT):
			print "WATCHDOG FAULT is set"
		
	def reset_all_registers(self):
		self.read_modify_write(self.__BQ25898D_REG14, self.__BQ25898D_REG14_REG_RESET)
		if (self.debug == True):
			print "BQ25898D RESET ALL REGISTERS"
		
	def enable_charging(self):
		self.read_modify_write(self.__BQ25898D_REG03, self.__BQ25898D_REG03_CHG_CONFIG_ENABLE)
		if (self.debug == True):
			print "BQ25898D ENABLED CHARGING"
		
	def disable_charging(self):
		self.read_clear_write(self.__BQ25898D_REG03, self.__BQ25898D_REG03_CHG_CONFIG_ENABLE)
		if (self.debug == True):
			print "BQ25898D DISABLED CHARGING"
		
	def enable_otg(self):
		self.read_modify_write(self.__BQ25898D_REG03, self.__BQ25898D_REG03_OTG_CONFIG_ENABLE)
		if (self.debug == True):
			print "ENABLED OTG BOOST"
		
	def disable_otg(self):
		self.read_clear_write(self.__BQ25898D_REG03, self.__BQ25898D_REG03_OTG_CONFIG_ENABLE)
		if (self.debug == True):
			print "DISABLED OTG BOOST"
	
	def set_ilim_current(self,input_current_limit):
		if (input_current_limit > self.__BQ25898D_REG00_INPUT_CURRENT_LIMIT_MAX):
			print "*** ERROR: given input_current_limit of %f is larger than allowed %f" % (input_current_limit,self.__BQ25898D_REG00_INPUT_CURRENT_LIMIT_MAX)
		else:
			self.read_clear_write(self.__BQ25898D_REG00, self.__BQ25898D_REG00_INPUT_CURRENT_LIMIT_PIN_ENABLE)
			ilim_val = ( int(input_current_limit / self.__BQ25898D_REG00_INPUT_CURRENT_LIMIT_LSB) << self.__BQ25898D_REG00_INPUT_CURRENT_LIMIT_NUM_SHIFTS ) & 0xFF
			self.write_bit_field(self.__BQ25898D_REG00, self.__BQ25898D_REG00_INPUT_CURRENT_LIMIT_BIT_MASK, ilim_val)
			if (self.debug == True):
				print "CALLED: set_ilim_current, given limit %f, dac_value is 0x%02x" % (input_current_limit,ilim_val)
	
	def set_charge_current(self, charge_current):
		if (charge_current > self.__BQ25898D_REG04_CHARGE_CURRENT_MAX):
			print "*** ERROR: given charge current of %f is larger than allowed %f" % (charge_current,self.__BQ25898D_REG04_CHARGE_CURRENT_MAX)
		else:
			ichgr_val = ( int(charge_current / self.__BQ25898D_REG04_CHARGE_CURRENT_LSB) << self.__BQ25898D_REG04_CHARGE_CURRENT_NUM_SHIFTS ) & 0xFF
			self.write_bit_field(self.__BQ25898D_REG04, self.__BQ25898D_REG04_CHARGE_CURRENT_BIT_MASK ,ichgr_val)
			if (self.debug == True):
				print "CALLED: set_charge_current, given limit %f, dac_value is 0x%02x" % (charge_current,ichgr_val)

	def set_vsys_min_voltage(self, vsys_voltage):
		if (vsys_voltage > self.__BQ25898D_REG03_VSYS_MIN_MAX):
			print "*** ERROR: given vsys_voltage of %f is larger than allowed %f" % (vsys_voltage,self.__BQ25898D_REG03_VSYS_MIN_MAX)
		else:
			vsys_val = (int( (vsys_voltage - self.__BQ25898D_REG03_VSYS_MIN_OFFSET) / self.__BQ25898D_REG03_VSYS_MIN_LSB ) << self.__BQ25898D_REG03_VSYS_MIN_NUM_SHIFTS ) % 0xFF
			self.write_bit_field(self.__BQ25898D_REG03, self.__BQ25898D_REG03_VSYS_MIN_BIT_MASK, vsys_val)
			if (self.debug == True):
				print "CALLED: set_vsys_min, given vsys_voltage of %f, dac_value is 0x%02x" % (vsys_voltage,vsys_val)


	def set_charge_voltage_limit(self, vreg_voltage):
		if (vreg_voltage > self.__BQ25898D_REG06_VREG_MAX):
			print "*** ERROR: given vreg_voltage of %f is larger than allowed %f" % (vreg_voltage,self.__BQ25898D_REG06_VREG_MAX)
		else:
			vreg_val = (int((vreg_voltage - self.__BQ25898D_REG06_VREG_OFFSET) / self.__BQ25898D_REG06_VREG_LSB) << self.__BQ25898D_REG06_VREG_NUM_SHIFTS ) & 0xFF
			self.write_bit_field(self.__BQ25898D_REG06, self.__BQ25898D_REG06_VREG_BIT_MASK, vreg_val)
			if (self.debug == True):
				print "CALLED: set_charge_voltage, given vreg_voltage of %f, dac_value is 0x%02x" % (vreg_voltage,vreg_val)


	def read_idpm_vdpm_status(self):
		reg_val = self.i2c.readU8(self.__BQ25898D_REG13)
		if (reg_val & self.__BQ25898D_REG13_IDPM_STAT == self.__BQ25898D_REG13_IDPM_STAT):
			print "IDPM STATUS BIT is SET (in current regulation)"
		if (reg_val & self.__BQ25898D_REG13_VDPM_STAT == self.__BQ25898D_REG13_VDPM_STAT):
			print "VDPM STATUS BIT is SET (in voltage regulation)"

	def set_hiz_mode(self):
		self.read_modify_write(self.__BQ25898D_REG00, self.__BQ25898D_REG00_HIZ_MODE_ENABLE)
		print "Enabled BQ25898D HIZ Mode"
	
	
