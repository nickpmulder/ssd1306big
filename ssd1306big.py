import machine
import time

from micropython import const
import framebuf


# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,  # off
            # address setting
            SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            SET_CONTRAST,
            0xFF,  # maximum
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            # charge pump
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,
        ):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)



WIDTH = 128
HEIGHT = 64

i2c = machine.I2C(0)
address = 60
res_reg=8
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)



def clear():
    oled.fill(0)


#The Alphabet
def A(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+5,(p.y)+1,1)
    oled.line((p.x)+5,(p.y)+1,(p.x)+10,(p.y)+15,1)
    oled.line((p.x)+3,(p.y)+11,(p.x)+8,(p.y)+11,1)

    oled.show()
    
def B(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+6,(p.y)+1,1)
    oled.line((p.x)+6,(p.y)+1,(p.x)+8,(p.y)+3,1)
    oled.line((p.x)+8,(p.y)+3,(p.x)+8,(p.y)+4,1)
    oled.line((p.x)+8,(p.y)+4,(p.x)+6,(p.y)+7,1)
    oled.line((p.x)+5,(p.y)+7,(p.x)+1,(p.y)+7,1)
    oled.line((p.x)+6,(p.y)+7,(p.x)+9,(p.y)+10,1)
    oled.line((p.x)+9,(p.y)+10,(p.x)+9,(p.y)+12,1)
    oled.line((p.x)+9,(p.y)+12,(p.x)+6,(p.y)+15,1)
    oled.line((p.x)+6,(p.y)+15,(p.x)+1,(p.y)+15,1)
    oled.show()    
    
def C(p):
    oled.line((p.x)+10,(p.y)+2,(p.x)+9,(p.y)+1,1)
    oled.line((p.x)+9,(p.y)+1,(p.x)+4,(p.y)+1,1)
    oled.line((p.x)+4,(p.y)+1,(p.x)+2,(p.y)+3,1)
    oled.line((p.x)+2,(p.y)+3,(p.x)+1,(p.y)+7,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+1,(p.y)+12,1)
    oled.line((p.x)+1,(p.y)+12,(p.x)+4,(p.y)+15,1)
    oled.line((p.x)+4,(p.y)+15,(p.x)+8,(p.y)+15,1)
    oled.line((p.x)+8,(p.y)+15,(p.x)+10,(p.y)+13,1)
    oled.show()
    
def D(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+6,(p.y)+1,1)
    oled.line((p.x)+6,(p.y)+1,(p.x)+9,(p.y)+3,1)
    oled.line((p.x)+9,(p.y)+3,(p.x)+9,(p.y)+12,1)
    oled.line((p.x)+9,(p.y)+12,(p.x)+6,(p.y)+15,1)
    oled.line((p.x)+6,(p.y)+15,(p.x)+1,(p.y)+15,1)
    oled.show()
    
def E(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+9,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+7,(p.y)+7,1)
    oled.line((p.x)+1,(p.y)+15,(p.x)+9,(p.y)+15,1)
    oled.show()
    
def F(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+9,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+6,(p.y)+7,1)
    oled.show()
    
def G(p):
    oled.line((p.x)+9,(p.y)+2,(p.x)+8,(p.y)+1,1)
    oled.line((p.x)+8,(p.y)+1,(p.x)+4,(p.y)+1,1)
    oled.line((p.x)+4,(p.y)+1,(p.x)+2,(p.y)+3,1)
    oled.line((p.x)+2,(p.y)+3,(p.x)+1,(p.y)+7,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+1,(p.y)+12,1)
    oled.line((p.x)+1,(p.y)+12,(p.x)+4,(p.y)+15,1)
    oled.line((p.x)+4,(p.y)+15,(p.x)+8,(p.y)+15,1)
    oled.line((p.x)+8,(p.y)+15,(p.x)+10,(p.y)+13,1)
    oled.line((p.x)+10,(p.y)+13,(p.x)+10,(p.y)+9,1)
    oled.line((p.x)+10,(p.y)+9,(p.x)+6,(p.y)+9,1)    
    oled.show()

def H(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+9,(p.y)+7,1)
    oled.line((p.x)+9,(p.y)+15,(p.x)+9,(p.y)+1,1)
    oled.show()

def I(p):
    oled.line((p.x)+1,(p.y)+1,(p.x)+9,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+15,(p.x)+9,(p.y)+15,1)
    oled.line((p.x)+5,(p.y)+15,(p.x)+5,(p.y)+1,1)
    oled.show()

def J(p):
    oled.line((p.x)+9,(p.y)+1,(p.x)+9,(p.y)+10,1)
    oled.line((p.x)+9,(p.y)+10,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+3,(p.y)+15,1)
    oled.line((p.x)+3,(p.y)+15,(p.x)+1,(p.y)+10,1)
    oled.show()
    
def K(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+9,(p.x)+8,(p.y)+1,1)
    oled.line((p.x)+4,(p.y)+7,(p.x)+9,(p.y)+15,1)
    oled.show()

def L(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+15,(p.x)+9,(p.y)+15,1)
    oled.show()
    
def M(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+5,(p.y)+7,1)
    oled.line((p.x)+9,(p.y)+1,(p.x)+5,(p.y)+7,1)
    oled.line((p.x)+9,(p.y)+15,(p.x)+9,(p.y)+1,1)
    oled.show()

def N(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+9,(p.y)+15,1)
    oled.line((p.x)+9,(p.y)+15,(p.x)+9,(p.y)+1,1)
    oled.show()

def O(p):
    oled.line((p.x)+10,(p.y)+5,(p.x)+8,(p.y)+1,1)
    oled.line((p.x)+8,(p.y)+1,(p.x)+4,(p.y)+1,1)
    oled.line((p.x)+4,(p.y)+1,(p.x)+2,(p.y)+3,1)
    oled.line((p.x)+2,(p.y)+3,(p.x)+1,(p.y)+7,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+1,(p.y)+12,1)
    oled.line((p.x)+1,(p.y)+12,(p.x)+4,(p.y)+15,1)
    oled.line((p.x)+4,(p.y)+15,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+10,(p.y)+12,1)
    oled.line((p.x)+10,(p.y)+12,(p.x)+10,(p.y)+5,1)
    oled.show()


def P(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+7,(p.y)+1,1)
    oled.line((p.x)+7,(p.y)+1,(p.x)+9,(p.y)+4,1)
    oled.line((p.x)+9,(p.y)+4,(p.x)+9,(p.y)+6,1)
    oled.line((p.x)+9,(p.y)+6, (p.x)+6,(p.y)+9,1)
    oled.line((p.x)+5,(p.y)+9,(p.x)+1,(p.y)+9,1)
    oled.show() 

def Q(p):
    oled.line((p.x)+10,(p.y)+5,(p.x)+8,(p.y)+1,1)
    oled.line((p.x)+8,(p.y)+1,(p.x)+4,(p.y)+1,1)
    oled.line((p.x)+4,(p.y)+1,(p.x)+2,(p.y)+3,1)
    oled.line((p.x)+2,(p.y)+3,(p.x)+1,(p.y)+7,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+1,(p.y)+12,1)
    oled.line((p.x)+1,(p.y)+12,(p.x)+4,(p.y)+15,1)
    oled.line((p.x)+4,(p.y)+15,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+10,(p.y)+12,1)
    oled.line((p.x)+10,(p.y)+12,(p.x)+10,(p.y)+5,1)
    oled.line((p.x)+6,(p.y)+10,(p.x)+10,(p.y)+15,1)
    oled.show()

def R(p):
    oled.line((p.x)+1,(p.y)+15,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+7,(p.y)+1,1)
    oled.line((p.x)+7,(p.y)+1,(p.x)+9,(p.y)+4,1)
    oled.line((p.x)+9,(p.y)+4,(p.x)+9,(p.y)+6,1)
    oled.line((p.x)+9,(p.y)+6, (p.x)+6,(p.y)+9,1)
    oled.line((p.x)+5,(p.y)+9,(p.x)+1,(p.y)+9,1)
    oled.line((p.x)+5,(p.y)+9,(p.x)+9,(p.y)+15,1)
    oled.show()
    
def S(p):
    oled.line((p.x)+9,(p.y)+2,(p.x)+7,(p.y)+1,1)
    oled.line((p.x)+7,(p.y)+1,(p.x)+3,(p.y)+1,1)
    oled.line((p.x)+3,(p.y)+1,(p.x)+2,(p.y)+2,1)
    oled.line((p.x)+3,(p.y)+1,(p.x)+2,(p.y)+2,1)    
    oled.line((p.x)+2,(p.y)+2,(p.x)+1,(p.y)+5,1)
    oled.line((p.x)+1,(p.y)+5,(p.x)+5,(p.y)+7,1)
    oled.line((p.x)+5,(p.y)+7,(p.x)+9,(p.y)+8,1)
    oled.line((p.x)+9,(p.y)+8,(p.x)+10,(p.y)+11,1)
    oled.line((p.x)+10,(p.y)+11,(p.x)+10,(p.y)+13,1)
    oled.line((p.x)+10,(p.y)+13,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+4,(p.y)+15,1)
    oled.line((p.x)+4,(p.y)+15,(p.x)+1,(p.y)+13,1)
    #oled.line((p.x)+10,(p.y)+13,(p.x)+7,(p.y)+15,1)
    oled.show()

def T(p):
    oled.line((p.x)+5,(p.y)+15,(p.x)+5,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+9,(p.y)+1,1)
    oled.show()
    
def U(p):
    oled.line((p.x)+1,(p.y)+1,(p.x)+1,(p.y)+13,1)
    oled.line((p.x)+1,(p.y)+13,(p.x)+3,(p.y)+15,1)
    oled.line((p.x)+3,(p.y)+15,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+9,(p.y)+13,1)
    oled.line((p.x)+9,(p.y)+13,(p.x)+9,(p.y)+1,1)
    oled.show()

def V(p):
    oled.line((p.x)+1,(p.y)+1,(p.x)+5,(p.y)+15,1)
    oled.line((p.x)+5,(p.y)+15,(p.x)+9,(p.y)+1,1)
    oled.show()

def W(p):
    oled.line((p.x)+1,(p.y)+1,(p.x)+3,(p.y)+15,1)
    oled.line((p.x)+3,(p.y)+15,(p.x)+5,(p.y)+8,1)
    oled.line((p.x)+5,(p.y)+8,(p.x)+8,(p.y)+15,1)
    oled.line((p.x)+8,(p.y)+15,(p.x)+10,(p.y)+1,1)
    oled.show()

def X(p):
    oled.line((p.x)+1,(p.y)+1,(p.x)+9,(p.y)+15,1)
    oled.line((p.x)+9,(p.y)+1,(p.x)+1,(p.y)+15,1)
    oled.show()

def Y(p):
    oled.line((p.x)+5,(p.y)+15,(p.x)+5,(p.y)+7,1)
    oled.line((p.x)+5,(p.y)+7,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+5,(p.y)+7,(p.x)+10,(p.y)+1,1)
    oled.show()

def Z(p):
    oled.line((p.x)+1,(p.y)+1,(p.x)+9,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+15,(p.x)+9,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+15,(p.x)+9,(p.y)+15,1)
    oled.show()

def period(p):
    oled.line((p.x)+1,(p.y)+14,(p.x)+2,(p.y)+14,1)
    oled.line((p.x)+1,(p.y)+15,(p.x)+2,(p.y)+15,1)
    oled.show()

def exclam(p):
    oled.line((p.x)+1,(p.y)+14,(p.x)+1,(p.y)+15,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+1,(p.y)+10,1)
    oled.show()

def plus(p):
    oled.line((p.x)+5,(p.y)+5,(p.x)+5,(p.y)+11,1)
    oled.line((p.x)+2,(p.y)+8,(p.x)+8,(p.y)+8,1)
    oled.show()
    
def minus(p):
    oled.line((p.x)+2,(p.y)+8,(p.x)+8,(p.y)+8,1)
    oled.show()
    
def equal(p):
    oled.line((p.x)+2,(p.y)+6,(p.x)+8,(p.y)+6,1)
    oled.line((p.x)+2,(p.y)+9,(p.x)+8,(p.y)+9,1)
    oled.show()

def comma(p):
    oled.line((p.x)+1,(p.y)+13,(p.x)+1,(p.y)+14,1)
    oled.line((p.x)+2,(p.y)+13,(p.x)+2,(p.y)+17,1)
    oled.line((p.x)+1,(p.y)+17,(p.x)+2,(p.y)+17,1)
    oled.show()

def colon(p):
    oled.line((p.x)+1,(p.y)+14,(p.x)+2,(p.y)+14,1)
    oled.line((p.x)+1,(p.y)+15,(p.x)+2,(p.y)+15,1)
    oled.line((p.x)+1,(p.y)+6,(p.x)+2,(p.y)+6,1)
    oled.line((p.x)+1,(p.y)+5,(p.x)+2,(p.y)+5,1)
    oled.show()


def slash(p):
    oled.line((p.x)+9,(p.y)+1,(p.x)+1,(p.y)+15,1)
    oled.show()
    
def question(p):
    oled.line((p.x)+5,(p.y)+14,(p.x)+6,(p.y)+14,1)
    oled.line((p.x)+5,(p.y)+15,(p.x)+6,(p.y)+15,1)
    oled.line((p.x)+5,(p.y)+10,(p.x)+5,(p.y)+8,1)
    oled.line((p.x)+5,(p.y)+8,(p.x)+8,(p.y)+6,1)
    oled.line((p.x)+8,(p.y)+6,(p.x)+9,(p.y)+2,1)
    oled.line((p.x)+8,(p.y)+1,(p.x)+4,(p.y)+1,1)

    oled.show()


def amp(p):
    #&
    oled.line((p.x)+4,(p.y)+7,(p.x)+2,(p.y)+5,1)
    oled.line((p.x)+2,(p.y)+5,(p.x)+2,(p.y)+3,1)
    oled.line((p.x)+2,(p.y)+3,(p.x)+3,(p.y)+2,1)
    oled.line((p.x)+3,(p.y)+2,(p.x)+4,(p.y)+1,1)
    oled.line((p.x)+4,(p.y)+1,(p.x)+6,(p.y)+1,1)
    oled.line((p.x)+6,(p.y)+1,(p.x)+7,(p.y)+2,1)
    oled.line((p.x)+7,(p.y)+2,(p.x)+8,(p.y)+3,1)
    oled.line((p.x)+8,(p.y)+3,(p.x)+8,(p.y)+4,1)
    oled.line((p.x)+8,(p.y)+4,(p.x)+6,(p.y)+6,1)
    oled.line((p.x)+6,(p.y)+6,(p.x)+1,(p.y)+10,1)
    oled.line((p.x)+1,(p.y)+10,(p.x)+1,(p.y)+13,1)
    oled.line((p.x)+1,(p.y)+13,(p.x)+3,(p.y)+15,1)
    oled.line((p.x)+3,(p.y)+15,(p.x)+6,(p.y)+15,1)
    oled.line((p.x)+6,(p.y)+15,(p.x)+9,(p.y)+9,1)
    oled.line((p.x)+4,(p.y)+8,(p.x)+10,(p.y)+15,1)
    
    oled.show()


def zero(p):
    oled.line((p.x)+10,(p.y)+5,(p.x)+8,(p.y)+1,1)
    oled.line((p.x)+8,(p.y)+1,(p.x)+4,(p.y)+1,1)
    oled.line((p.x)+4,(p.y)+1,(p.x)+2,(p.y)+3,1)
    oled.line((p.x)+2,(p.y)+3,(p.x)+1,(p.y)+7,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+1,(p.y)+12,1)
    oled.line((p.x)+1,(p.y)+12,(p.x)+4,(p.y)+15,1)
    oled.line((p.x)+4,(p.y)+15,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+10,(p.y)+12,1)
    oled.line((p.x)+10,(p.y)+12,(p.x)+10,(p.y)+5,1)
    oled.line((p.x)+9,(p.y)+4,(p.x)+2,(p.y)+12,1)
    oled.show()

def one(p):
    oled.line((p.x)+5,(p.y)+15,(p.x)+5,(p.y)+1,1)
    oled.line((p.x)+5,(p.y)+1,(p.x)+2,(p.y)+3,1)
    oled.show()

def two(p):
    oled.line((p.x)+1,(p.y)+3,(p.x)+2,(p.y)+1,1)
    oled.line((p.x)+2,(p.y)+1,(p.x)+7,(p.y)+1,1)    
    oled.line((p.x)+7,(p.y)+1,(p.x)+9,(p.y)+3,1)
    oled.line((p.x)+9,(p.y)+3,(p.x)+9,(p.y)+6,1)
    oled.line((p.x)+9,(p.y)+6,(p.x)+2,(p.y)+13,1)
    oled.line((p.x)+2,(p.y)+13,(p.x)+1,(p.y)+15,1)
    oled.line((p.x)+1,(p.y)+15,(p.x)+10,(p.y)+15,1)
    oled.show()
    

def three(p):
    oled.line((p.x)+1,(p.y)+3,(p.x)+2,(p.y)+1,1)
    oled.line((p.x)+2,(p.y)+1,(p.x)+7,(p.y)+1,1)    
    oled.line((p.x)+7,(p.y)+1,(p.x)+9,(p.y)+3,1)
    oled.line((p.x)+9,(p.y)+3,(p.x)+9,(p.y)+5,1)
    oled.line((p.x)+9,(p.y)+5,(p.x)+7,(p.y)+7,1)
    oled.line((p.x)+7,(p.y)+7,(p.x)+4,(p.y)+7,1)    
    oled.line((p.x)+7,(p.y)+8,(p.x)+9,(p.y)+9,1)
    oled.line((p.x)+9,(p.y)+9,(p.x)+9,(p.y)+12,1)
    oled.line((p.x)+9,(p.y)+12,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+3,(p.y)+15,1)
    oled.line((p.x)+3,(p.y)+15,(p.x)+1,(p.y)+13,1)    

    oled.show()

def four(p):
    oled.line((p.x)+8,(p.y)+1,(p.x)+8,(p.y)+15,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+1,(p.y)+7,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+9,(p.y)+7,1)
    oled.show()

def five(p):
    oled.line((p.x)+9,(p.y)+1,(p.x)+1,(p.y)+1,1)
    oled.line((p.x)+1,(p.y)+1,(p.x)+1,(p.y)+7,1)
    oled.line((p.x)+7,(p.y)+7,(p.x)+1,(p.y)+7,1)    
    oled.line((p.x)+7,(p.y)+8,(p.x)+9,(p.y)+9,1)
    oled.line((p.x)+9,(p.y)+9,(p.x)+9,(p.y)+12,1)
    oled.line((p.x)+9,(p.y)+12,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+3,(p.y)+15,1)
    oled.line((p.x)+3,(p.y)+15,(p.x)+1,(p.y)+13,1)
    oled.show()

def six(p):
    oled.line((p.x)+10,(p.y)+3,(p.x)+8,(p.y)+1,1)
    oled.line((p.x)+8,(p.y)+1,(p.x)+4,(p.y)+1,1)
    oled.line((p.x)+4,(p.y)+1,(p.x)+2,(p.y)+3,1)
    oled.line((p.x)+2,(p.y)+3,(p.x)+1,(p.y)+7,1)
    oled.line((p.x)+1,(p.y)+7,(p.x)+1,(p.y)+12,1)
    oled.line((p.x)+1,(p.y)+12,(p.x)+4,(p.y)+15,1)
    oled.line((p.x)+4,(p.y)+15,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+10,(p.y)+13,1)
    oled.line((p.x)+10,(p.y)+13,(p.x)+10,(p.y)+9,1)
    oled.line((p.x)+10,(p.y)+9,(p.x)+8,(p.y)+7,1)
    oled.line((p.x)+8,(p.y)+7,(p.x)+4,(p.y)+7,1)
    oled.line((p.x)+4,(p.y)+7,(p.x)+2,(p.y)+9,1)
    oled.show()
    

def seven(p):
    oled.line((p.x)+1,(p.y)+1,(p.x)+10,(p.y)+1,1)
    oled.line((p.x)+10,(p.y)+1,(p.x)+3,(p.y)+15,1)
    oled.show()
    
def eight(p):
    oled.line((p.x)+4,(p.y)+7,(p.x)+2,(p.y)+5,1)
    oled.line((p.x)+2,(p.y)+5,(p.x)+2,(p.y)+3,1)
    oled.line((p.x)+2,(p.y)+3,(p.x)+3,(p.y)+2,1)
    oled.line((p.x)+3,(p.y)+2,(p.x)+4,(p.y)+1,1)
    oled.line((p.x)+4,(p.y)+1,(p.x)+6,(p.y)+1,1)
    oled.line((p.x)+6,(p.y)+1,(p.x)+7,(p.y)+2,1)
    oled.line((p.x)+7,(p.y)+2,(p.x)+8,(p.y)+3,1)
    oled.line((p.x)+8,(p.y)+3,(p.x)+8,(p.y)+5,1)
    oled.line((p.x)+8,(p.y)+5,(p.x)+6,(p.y)+7,1)
    oled.line((p.x)+1,(p.y)+10,(p.x)+1,(p.y)+13,1)
    oled.line((p.x)+1,(p.y)+13,(p.x)+3,(p.y)+15,1)
    oled.line((p.x)+3,(p.y)+15,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+9,(p.y)+13,1)
    oled.line((p.x)+9,(p.y)+13,(p.x)+9,(p.y)+10,1)
    oled.line((p.x)+9,(p.y)+10,(p.x)+6,(p.y)+7,1)
    oled.line((p.x)+6,(p.y)+7,(p.x)+4,(p.y)+7,1)
    oled.line((p.x)+4,(p.y)+7,(p.x)+2,(p.y)+9,1)
    oled.show()

def nine(p):
    oled.line((p.x)+10,(p.y)+6,(p.x)+8,(p.y)+8,1)
    oled.line((p.x)+8,(p.y)+8,(p.x)+3,(p.y)+8,1)
    oled.line((p.x)+3,(p.y)+8,(p.x)+1,(p.y)+5,1)
    oled.line((p.x)+1,(p.y)+5,(p.x)+1,(p.y)+3,1)
    oled.line((p.x)+1,(p.y)+3,(p.x)+3,(p.y)+1,1)
    oled.line((p.x)+3,(p.y)+1,(p.x)+8,(p.y)+1,1)
    oled.line((p.x)+8,(p.y)+1,(p.x)+10,(p.y)+3,1)
    oled.line((p.x)+10,(p.y)+3,(p.x)+10,(p.y)+10,1)
    oled.line((p.x)+10,(p.y)+10,(p.x)+9,(p.y)+13,1)
    oled.line((p.x)+9,(p.y)+13,(p.x)+7,(p.y)+15,1)
    oled.line((p.x)+7,(p.y)+15,(p.x)+3,(p.y)+15,1)
    oled.line((p.x)+3,(p.y)+15,(p.x)+1,(p.y)+13,1)
    oled.show()

def space(p):
    oled.show()
    
    
#positon object 

class Pos:
    def __init__(self, x, y):
        self.x=x
        self.y=y
       
#define position x and y   
p0=Pos(0,0)
p1=Pos(15,0)
p2=Pos(30,0)
p3=Pos(45,0)
p4=Pos(60,0)
p5=Pos(75,0)
p6=Pos(90,0)
p7=Pos(105,0)
p8=Pos(0,22)
p9=Pos(15,22)
p10=Pos(30,22)
p11=Pos(45,22)
p12=Pos(60,22)
p13=Pos(75,22)
p14=Pos(90,22)
p15=Pos(105,22)
p16=Pos(0,44)
p17=Pos(15,44)
p18=Pos(30,44)
p19=Pos(45,44)
p20=Pos(60,44)
p21=Pos(75,44)
p22=Pos(90,44)
p23=Pos(105,44)

line1Array=[p0,p1,p2,p3,p4,p5,p6,p7]
line2Array=[p8,p9,p10,p11,p12,p13,p14,p15]
line3Array=[p16,p17,p18,p19,p20,p21,p22,p23]
displayArray=[p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23]



def display(text, posArray):
    for i in range (len(text)):
        if text[i]=="A" or text[i]=="a":
            A(posArray[i])
        if text[i]=="B" or text[i]=="b":
            B(posArray[i])
        if text[i]=="C" or text[i]=="c":
            C(posArray[i])
        if text[i]=="D" or text[i]=="d":
            D(posArray[i])
        if text[i]=="E" or text[i]=="e":
            E(posArray[i])
        if text[i]=="F" or text[i]=="f":
            F(posArray[i])
        if text[i]=="G" or text[i]=="g":
            G(posArray[i])
        if text[i]=="H" or text[i]=="h":
            H(posArray[i])
        if text[i]=="I" or text[i]=="i":
            I(posArray[i])
        if text[i]=="J" or text[i]=="j":
            J(posArray[i])
        if text[i]=="K" or text[i]=="k":
            K(posArray[i])
        if text[i]=="L" or text[i]=="l":
            L(posArray[i])
        if text[i]=="M" or text[i]=="m":
            M(posArray[i])
        if text[i]=="N" or text[i]=="n":
            N(posArray[i])
        if text[i]=="O" or text[i]=="o":
            O(posArray[i])
        if text[i]=="P" or text[i]=="p":
            P(posArray[i])
        if text[i]=="Q" or text[i]=="q":
            Q(posArray[i])
        if text[i]=="R" or text[i]=="r":
            R(posArray[i])
        if text[i]=="S" or text[i]=="s":
            S(posArray[i])
        if text[i]=="T" or text[i]=="t":
            T(posArray[i])
        if text[i]=="U" or text[i]=="u":
            U(posArray[i])
        if text[i]=="V" or text[i]=="v":
            V(posArray[i])
        if text[i]=="W" or text[i]=="w":
            W(posArray[i])
        if text[i]=="X" or text[i]=="x":
            X(posArray[i])
        if text[i]=="Y" or text[i]=="y":
            Y(posArray[i])
        if text[i]=="Z" or text[i]=="z":
            Z(posArray[i])
        if text[i]=="0":
            zero(posArray[i])
        if text[i]=="1":
            one(posArray[i])
        if text[i]=="2":
            two(posArray[i])
        if text[i]=="3":
            three(posArray[i])
        if text[i]=="4":
            four(posArray[i])
        if text[i]=="5":
            five(posArray[i])
        if text[i]=="6":
            six(posArray[i])
        if text[i]=="7":
            seven(posArray[i])
        if text[i]=="8":
            eight(posArray[i])
        if text[i]=="9":
            nine(posArray[i])
        if text[i]==".":
            period(posArray[i])
        if text[i]=="!":
            exclam(posArray[i])
        if text[i]=="?":
            question(posArray[i])
        if text[i]=="/":
            slash(posArray[i])
        if text[i]==":":
            colon(posArray[i])
        if text[i]==",":
            comma(posArray[i])
        if text[i]=="&":
            amp(posArray[i])
        if text[i]=="+":
            plus(posArray[i])
        if text[i]=="-":
            minus(posArray[i])
        if text[i]=="=":
            equal(posArray[i])
        if text[i]==" ":
            space(posArray[i])



def line1(line1text):
    display(line1text, line1Array)

def line2(line2text):
    display(line2text, line2Array)

def line3(line3text):
    display(line3text, line3Array)
    
def flow(string):
    display(string, displayArray)
    
def wrap(string):
    if len(string)> 8:
        spaceArray = []
        cut1 = 23
        cut2 = 23
        cut3 = 23
        for character in range (len(string)):
            if string[character] == " ":
                spaceArray.append(character)
        for i in range (len(spaceArray)):    
            if spaceArray[i] < 8 :
                cut1= spaceArray[i]
                #cut[0]=space
            
            if 8 < spaceArray[i] < 16 :
                cut2=spaceArray[i]
               
            if 16 < spaceArray[i] < 24 :
                cut3=spaceArray[i]
              
        line1(string[0:(cut1)])
        line2(string[(cut1+1):(cut2)])
        line3(string[(cut2+1):(cut3)])
        
    else:
        line1(string)
    #line2(line2text)
    #line3(line3text)
    
