import hashlib
import random
import struct
import time
import json


class Gorgon:
    digits   = {c: i for i, c in enumerate("0123456789abcdefghijklmnopqrstuvwxyz")}
    HEX_STRS = [[30 ,0 ,224 ,220 ,147 ,69 ,1 ,200 ],[30 ,0 ,224 ,236 ,147 ,69 ,1 ,200 ],[30 ,0 ,224 ,228 ,147 ,69 ,1 ,208 ],[30 ,60 ,224 ,244 ,147 ,69 ,0 ,216 ],[30 ,64 ,224 ,228 ,147 ,69 ,0 ,216 ],[30 ,0 ,224 ,227 ,147 ,69 ,1 ,213 ],[30 ,64 ,224 ,210 ,147 ,69 ,0 ,160 ],[30 ,64 ,224 ,203 ,147 ,69 ,0 ,150 ],[30 ,64 ,224 ,211 ,147 ,69 ,0 ,167 ],[30 ,64 ,224 ,228 ,147 ,69 ,0 ,156 ],[30 ,64 ,224 ,216 ,147 ,69 ,0 ,216 ],[30 ,64 ,224 ,226 ,147 ,69 ,0 ,205 ],[30 ,64 ,224 ,214 ,147 ,69 ,0 ,176 ],[30 ,64 ,224 ,217 ,147 ,69 ,0 ,180 ],[30 ,64 ,224 ,240 ,147 ,69 ,0 ,213 ],[30 ,64 ,224 ,210 ,147 ,69 ,0 ,216 ],[30 ,64 ,224 ,235 ,147 ,69 ,0 ,192 ],[30 ,64 ,224 ,234 ,147 ,69 ,0 ,193 ],[30 ,64 ,224 ,234 ,147 ,69 ,0 ,186 ],[30 ,64 ,224 ,171 ,147 ,69 ,0 ,136 ],[30 ,64 ,224 ,103 ,147 ,69 ,0 ,166 ],[30 ,64 ,224 ,167 ,147 ,69 ,0 ,15 ],[30 ,64 ,224 ,139 ,147 ,69 ,0 ,182 ],[30 ,64 ,224 ,194 ,147 ,69 ,0 ,84 ],[30 ,64 ,224 ,183 ,147 ,69 ,0 ,170 ],[30 ,64 ,224 ,205 ,147 ,69 ,0 ,125 ],[30 ,64 ,224 ,138 ,147 ,69 ,0 ,175 ],[30 ,64 ,224 ,229 ,147 ,69 ,0 ,12 ],[30 ,64 ,224 ,163 ,147 ,69 ,0 ,26 ],[30 ,64 ,224 ,105 ,147 ,69 ,0 ,35 ],[30 ,64 ,224 ,167 ,147 ,69 ,0 ,24 ],]
    LEN      = 20

    def calculate(self, params, cookie, body):

        self.hex_str = random.choice(self.HEX_STRS)
        hash = self.getGorgonHash(params, body, cookie)
        hexEncryption = self.encryption()
        gorgonHash = self.initGorgonHash(hash, hexEncryption)

        result = ""
        handle = self.handle(gorgonHash["gorgon"])

        for item in handle:
            result += self.hex2str(item)

        hash_1 = self.hex2str(self.hex_str[7])
        hash_2 = self.hex2str(self.hex_str[3])
        hash_3 = self.hex2str(self.hex_str[1])
        hash_4 = self.hex2str(self.hex_str[6])

        return {
            "X-Gorgon": "0404{}{}{}{}{}".format(hash_1, hash_2, hash_3, hash_4, result),
            "X-Khronos": str(hash["time"]),
        }

    def charCodeAt(self, str, i):
        return self.get_bianma((str[i:1]))

    def encryption(self):
        tmp = A = B = C = D = None
        hexs = []
        for i in range(256):
            hexs.append(i)

        for i in range(256):
            if i == 0:
                A = 0
            elif tmp is not None:
                A = tmp
            else:
                A = hexs[i - 1]
            B = self.hex_str[i % 8]
            if (A == 85) & (i != 1) & (tmp != 85):
                A = 0
            C = self.ensureMax(A + i + B)
            tmp = C if C < i else None
            D = hexs[C]
            hexs[i] = D
        return hexs

    def ensureMax(self, val, max=256):
        while val >= 256:
            val = val - 256
        return val

    def epoch(self):
        return int(round(time.time()))

    def convert_base(self, hex, base):
        return sum(
            self.digits[digit] * (base**i)
            for i, digit in enumerate(reversed(hex.lower()))
        )

    def fromHex(self, hex):
        return self.convert_base(hex, int(16))

    def getGorgonHash(self, url, data=None, cookie=None, encoding="UTF-8"):
        gorgon = []
        times = int(round(time.time()))
        hexTime = self.toHex(times)
        urlmd5 = hashlib.md5(url.encode("UTF-8")).hexdigest()

        rang = self.ranges(start=4)
        for i in rang:
            gorgon.append(self.fromHex(urlmd5[i * 2 : 2 * i + 2]))

        gorgon = gorgon + self.xGorgon_data(data, encoding)
        gorgon = gorgon + self.xGorgon_cookie(cookie, encoding)

        for i in rang:
            gorgon.append(0)

        for i in rang:
            gorgon.append(self.fromHex(hexTime[i * 2 : 2 * i + 2]))

        return {"gorgon": gorgon, "time": times}

    def get_bianma(self, str):
        result = []

    def handle(self, gorgonHash):
        rang = self.ranges(self.LEN)
        for i in rang:
            A = gorgonHash[i]
            B = self.reverse(A)
            C = int(gorgonHash[(i + 1) % self.LEN])
            D = B ^ C
            E = self.rbit(D)
            F = E ^ self.LEN
            G = ~F
            while G < 0:
                G += 4294967296

            a = self.toHex(G)
            offset = len(a) - 2

            H = self.fromHex(self.toHex(G)[offset:])
            gorgonHash[i] = H

        return gorgonHash

    def hex2str(self, num):
        tmp = self.toHex(num)
        if len(tmp) < 2:
            tmp = "0" + tmp
        return tmp

    def initGorgonHash(self, gorgonHash, hexEncryption):
        tmp_add = []
        tmp_hex = [] + hexEncryption
        A = B = C = D = E = F = G = None
        rang = self.ranges(self.LEN)
        for i in rang:
            A = gorgonHash["gorgon"][i]
            B = 0 if len(tmp_add) == 0 else tmp_add[-1]
            C = self.ensureMax(hexEncryption[i + 1] + int(B))
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = self.ensureMax(D + D)
            F = tmp_hex[E]
            G = A ^ F
            gorgonHash["gorgon"][i] = G

        return gorgonHash

    def ranges(self, start=0, stop=None, step=1):
        if stop is None:
            stop = start
            start = 0

        if ((step > 0) & (start >= stop)) or (step < 0) & (start <= stop):
            return []

        result = []

        for x in range(start, stop, step):
            result.append(x)

        return result

    def rbit(self, num):
        result = ""
        tmp = format(num, "b")

        while len(tmp) < 8:
            tmp = "0" + tmp

        rang = self.ranges(8)
        for i in rang:
            result += tmp[7 - i]
        return int(result, 2)

    def reverse(self, num):
        tmp = self.toHex(num)
        if len(tmp) < 2:
            tmp = "0" + tmp

        return self.fromHex(tmp[1:10] + tmp[0:1])

    def toHex(self, num):
        return format(int(num), "x")

    def uniord(self, str, from_encoding=False):
        if len(str == 1):
            return ord(str)
        str = str.encode("UCS-4BE")
        tmp = struct.pack("N", str)
        return tmp[1]

    def xGorgon_cookie(self, cookie, encoding="utf-8"):
        gorgon = []
        rang = self.ranges(4)
        if (cookie is None) or (len(cookie) == 0):
            for i in rang:
                gorgon.append(0)
        else:
            hashstr = hashlib.md5(cookie.encode()).hexdigest()
            for i in rang:
                gorgon.append(self.fromHex(hashstr[i * 2 : 2 * i + 2]))

        return gorgon

    def xGorgon_data(self, data: (bytes or None or str), encoding="utf-8"):
        gorgon = []
        data_md5 = None

        if (data is None) or (len(data) == 0):
            rang = self.ranges(4)
            for i in rang:
                gorgon.append(0)
        else:
            try:
                data_md5 = hashlib.md5(data).hexdigest()
            except Exception:
                data_md5 = hashlib.md5(data.encode('utf-8')).hexdigest()

            if encoding == "octet":
                try:
                    data_md5 = hashlib.md5(data).hexdigest()
                except Exception:
                    data_md5 = hashlib.md5(data.encode('utf-8')).hexdigest()
            rang = self.ranges(4)

            for i in rang:
                gorgon.append(self.fromHex(data_md5[i * 2 : 2 * i + 2]))

        return gorgon

class StableGorgon:
    def __init__(self, params: str, data: str, cookies: str, unix: int) -> None:
        self.unix = unix;self.params = params;self.data = data;self.cookies = cookies

    def hash(self, data: str) -> str:
        try:
            _hash = str(hashlib.md5(data.encode()).hexdigest())
        except Exception:
            _hash = str(hashlib.md5(data).hexdigest())
        return _hash

    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str = base_str + self.hash(self.data) if self.data else base_str + str('0' * 32)
        base_str = base_str + self.hash(self.cookies) if self.cookies else base_str + str('0' * 32)
        return base_str

    def get_value(self) -> json:
        base_str = self.get_base_string()
        return self.encrypt(base_str)

    def encrypt(self, data: str) -> json:
        unix = self.unix;
        len = 20;
        key = [223, 119, 185, 64, 185, 155, 132, 131, 209, 185, 203, 209, 247, 194, 185, 133, 195, 208, 251, 195];
        param_list = []
        for i in range(0, 12, 4):
            temp = data[8 * i:8 * (i + 1)]
            for j in range(4): H = int(temp[j * 2:(j + 1) * 2], 16);param_list.append(H)
        param_list.extend([0, 6, 11, 28]);
        H = int(hex(unix), 16);
        param_list.append((H & 4278190080) >> 24);
        param_list.append((H & 16711680) >> 16);
        param_list.append((H & 65280) >> 8);
        param_list.append((H & 255) >> 0);
        eor_result_list = []
        for (A, B) in zip(param_list, key): eor_result_list.append(A ^ B)
        for i in range(len): C = self.reverse(eor_result_list[i]);D = eor_result_list[
            (i + 1) % len];E = C ^ D;F = self.rbit_algorithm(E);H = (F ^ 4294967295 ^ len) & 255;eor_result_list[i] = H
        result = ''
        for param in eor_result_list: result += self.hex_string(param)
        return {'X-Gorgon': '0404b0d30000' + result, 'X-Khronos': str(unix)}

    def rbit_algorithm(self, num):
        result = '';
        tmp_string = bin(num)[2:]
        while len(tmp_string) < 8: tmp_string = '0' + tmp_string
        for i in range(0, 8): result = result + tmp_string[7 - i]
        return int(result, 2)

    def hex_string(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2: tmp_string = '0' + tmp_string
        return tmp_string

    def reverse(self, num):
        tmp_string = self.hex_string(num);return int(tmp_string[1:] + tmp_string[:1], 16)
