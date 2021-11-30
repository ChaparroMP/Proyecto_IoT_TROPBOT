
from smbus import SMBus

ADS1015_ADDRESS            = 0x48 # 100 1000
ADS1015_POINTER_CONVERSION = 0x00
ADS1015_POINTER_CONFIG     = 0x01 # REG_CFG = 0x01


ADS1015_CONFIG_COMP_QUE_DISABLE = 0x0003 # bit [1:0]
ADS1015_CONFIG_COMP_LAT         = 0x0000 # bit [2] default, to put in 1 0x0004
ADS1015_CONFIG_COMP_POL         = 0x0000 # bit [3] default, to put in 1 0x0008
ADS1015_CONFIG_COMP_MODE        = 0x0000 # bit [4] default, to put in 1 0x0010
ADS1015_CONFIG_DATA_RATE        = 0x0000 # bit [7:5] "100" 0 0000 (0x080) : 1600 SPS (default), 
ADS1015_CONFIG_MODE             = 0x0000 # bit [8] "1" 0000 0000 Single-shot mode or power-down state (default)
# ADS1015_CONFIG_PGA            = 0x0000 # bit [11:9] "010"0 0000 0000: FSR = ±2.048 V (default)
# ADS1015_CONFIG_MUX            = 0x0000 # bit [14:12] 0"000" 0000 00000000 : AINP = AIN0 and AINN = AIN1 (default)
ADS1015_CONFIG_OS               = 0x0000 # bit [15] 0x8000 # 1000000000000000 operation status

i2c_ch = 1

samples_per_second_map = {128: 0x0000, 250: 0x0020, 490: 0x0040, 920: 0x0060, 1600: 0x0080, 2400: 0x00A0, 3300: 0x00C0}
channel_map = {0: 0x4000, 1: 0x5000, 2: 0x6000, 3: 0x7000}
programmable_gain_map = {6144: 0x0000, 4096: 0x0200, 2048: 0x0400, 1024: 0x0600, 512: 0x0800, 256: 0x0A00}

PGA_6_144V = 6144
PGA_4_096V = 4096
PGA_2_048V = 2048
PGA_1_024V = 1024
PGA_0_512V = 512
PGA_0_256V = 256

def Read_ADC(AnalogIn, PGA, DataRate):
    
    # open i2c bus
    i2c = SMBus(i2c_ch)
    
    # sane defaults
    config = 0x0003 | 0x0100

    config |= samples_per_second_map[DataRate]
    config |= channel_map[AnalogIn]
    config |= programmable_gain_map[PGA]

    # set "single shot" mode
    config |= 0x8000

    # write single conversion flag
    i2c.write_i2c_block_data(ADS1015_ADDRESS, ADS1015_POINTER_CONFIG, [(config >> 8) & 0xFF, config & 0xFF])       

    data = i2c.read_i2c_block_data(ADS1015_ADDRESS, ADS1015_POINTER_CONVERSION)

        # 16-bit
    value = (data[0] << 8) | data[1]

    if value & 0x8000:  # Check and apply sign bit
        value -= 1 << 16

    value /= 32767.0  # Divide by full scale rane

    value *= float(PGA)  # Multiply by gain
    value /= 1000.0  # Scale from mV to V
    value = max(0, value)  # Sweep negative voltages under the rug

    return value


#while (True):
#    dataADC = Read_ADC(0, PGA_6_144V, 250)
#    print(dataADC)