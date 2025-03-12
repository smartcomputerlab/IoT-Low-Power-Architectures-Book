from machine import I2C
from time import sleep_ms

class _Subscriptable():
    def __getitem__(self, item):
        return None

_subscriptable = _Subscriptable()

List = _subscriptable
Optional = _subscriptable
Union = _subscriptable

class EEPROM(object):

    def __init__(self,
                 addr: int = 0x50,
                 pages: int = 128,
                 bpp: int = 32,
                 i2c: Optional[I2C] = None,
                 at24x: int = 0) -> None:
        
        self._addr = addr
        standard_eeproms = {
            32: [128, 32],      # 4KiB 32Kbits, 128 pages, 32 bytes/page
            64: [256, 32],      # 8KiB 64Kbits, 256 pages, 32 bytes/page
            128: [256, 64],     # 16KiB 128Kbits, 256 pages, 64 bytes/page
            256: [512, 64],     # 32KiB 256Kbits, 512 pages, 64 bytes/page
            512: [512, 128],    # 64KiB 512Kbits, 512 pages, 128 bytes/page
        }
        if at24x in standard_eeproms:
            self._pages, self._bpp = standard_eeproms[at24x]
        else:
            self._pages = pages
            self._bpp = bpp
        if i2c is None:
            # default assignment, check the docs
            self._i2c = I2C(0)
        else:
            self._i2c = i2c

    @property
    def addr(self) -> int:
        return self._addr
    @property
    def capacity(self) -> int:
        return self._pages * self._bpp
    @property
    def pages(self) -> int:
        return self._pages
    @property
    def bpp(self) -> int:
        return self._bpp

    def length(self) -> int:
        return self.capacity

    def read(self, addr: int, nbytes: int = 1) -> bytes:
        if addr > self.capacity or addr < 0:
            raise ValueError(
                "Read address {} outside of device address range {}".
                format(addr, self.capacity)
            )
        if addr + nbytes > self.capacity:
            raise ValueError(
                "Last read address {} outside of device address range {}".
                format(addr + nbytes, self.capacity)
            )
        return self._i2c.readfrom_mem(self._addr, addr, nbytes, addrsize=16)

    def write(self, addr: int, buf: Union[bytes, List[int], str]) -> None:
        offset = addr % self._bpp
        partial = 0
        if addr > self.capacity or addr < 0:
            raise ValueError(
                "Write address {} outside of device address range {}".
                format(addr, self.capacity)
            )
        if addr + len(buf) > self.capacity:
            raise ValueError(
                "Last data at {} does not fit into device address range {}".
                format(addr + len(buf), self.capacity)
            )
        # partial page write
        if offset > 0:
            partial = self._bpp - offset
            self._i2c.writeto_mem(
                self._addr, addr, buf[0:partial], addrsize=16
            )
            sleep_ms(5)
            addr += partial
        # full page write
        for i in range(partial, len(buf), self._bpp):
            self._i2c.writeto_mem(
                self._addr,
                addr + i - partial,
                buf[i:i + self._bpp],
                addrsize=16
            )
            sleep_ms(5)

    def update(self, addr: int, buf: Union[bytes, List[int], str]) -> None:
        for idx, ele in enumerate(buf):
            this_addr = addr + idx
            if isinstance(ele, int):
                this_val = ele.to_bytes(1, 'big')
            else:
                this_val = str(ele).encode()
            current_value = self.read(addr=this_addr)   # returns bytes
            if current_value != this_val:
                self.write(addr=this_addr, buf=this_val)

    def wipe(self) -> None:
        page_buff = b'\xff' * self.bpp
        for i in range(self.pages):
            self.write(i * self.bpp, page_buff)

    def print_pages(self, addr: int, nbytes: int) -> None:
        unknown_data_first_page = addr % self.bpp
        unknown_data_last_page = self.bpp - (addr + nbytes) % self.bpp
        if unknown_data_last_page % self.bpp == 0:
            unknown_data_last_page = 0
        data = self.read(addr=addr, nbytes=nbytes)
        extended_data = (
            b'?' * unknown_data_first_page +
            data +
            b'?' * unknown_data_last_page
        )
        sliced_data = [
            extended_data[i: i + self.bpp] for i in range(0,
                                                          len(extended_data),
                                                          self.bpp)
        ]
        print('Page {:->4}: 0 {} {}'.
              format('x', '-' * (self.bpp - len(str(self.bpp))), self.bpp))
        for idx, a_slice in enumerate(sliced_data):
            print('Page {:->4}: {}'.format(idx, a_slice))




























