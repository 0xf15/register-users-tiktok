# This is how easy it is to solve TikTok captchas

import cv2
import base64
import numpy as np
import requests
import time
import random
from urllib.parse import urlencode


class PuzzleSolver:
    def __init__(self, base64puzzle, base64piece):
        self.puzzle = base64puzzle
        self.piece = base64piece

    def get_position(self):
        puzzle = self.__background_preprocessing()
        piece = self.__piece_preprocessing()
        matched = cv2.matchTemplate(
            puzzle,
            piece,
            cv2.TM_CCOEFF_NORMED
        )
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matched)
        return max_loc[0]

    def __background_preprocessing(self):
        img = self.__img_to_grayscale(self.piece)
        background = self.__sobel_operator(img)
        return background

    def __piece_preprocessing(self):
        img = self.__img_to_grayscale(self.puzzle)
        template = self.__sobel_operator(img)
        return template

    def __sobel_operator(self, img):
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S

        img = cv2.GaussianBlur(img, (3, 3), 0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(
            gray,
            ddepth,
            1,
            0,
            ksize=3,
            scale=scale,
            delta=delta,
            borderType=cv2.BORDER_DEFAULT,
        )
        grad_y = cv2.Sobel(
            gray,
            ddepth,
            0,
            1,
            ksize=3,
            scale=scale,
            delta=delta,
            borderType=cv2.BORDER_DEFAULT,
        )
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad

    def __img_to_grayscale(self, img):
        return cv2.imdecode(
            self.__string_to_image(img),
            cv2.IMREAD_COLOR
        )

    def __string_to_image(self, base64_string):

        return np.frombuffer(
            base64.b64decode(base64_string),
            dtype="uint8"
        )


class Captcha:
    def __init__(self, did, iid):
        self.__host = "verification-va.tiktokv.com"
        self.__device_id = did
        self.__install_id = iid
        self.__cookies = ""
        self.__client = requests.Session()

    def __params(self):
        params = {
            'lang': 'en',
            'app_name': 'musically_ly',
            'h5_sdk_version': '2.23.4',
            'sdk_version': '1.2.1',
            'iid': self.__install_id,
            'did': self.__device_id,
            'device_id': self.__device_id,
            'ch': 'googleplay',
            'aid': '1340',
            'os_type': '0',
            'tmp': f"{int(time.time())}{random.randint(111, 999)}",
            'platform': 'app',
            'webdriver': 'undefined',
            'locale': 'en',
            'vc': '16.9.4',
            'os_name': 'Android',
            'os_version': '25',
            'user_id': '0',
            'orientation': '1',
            'resolution': '575*994',
            'region': 'va',
            'device_brand': 'google',
            'device_model': 'G011A',
            'verify_host': 'https://www-useast1a.tiktok.com/',
            'challenge_code': '1105',
            'channel': 'googleplay',
            'app_version': '16.9.4'
        }

        return urlencode(params)

    def __headers(self) -> dict:
        headers = {
            "sdk-version": "2",
            "x-ss-req-ticket": str(int(time.time() * 1000)),
            "cookie": self.__cookies,
            "content-type": "application/json; charset=utf-8",
            "host": self.__host,
            "connection": "Keep-Alive",
            "user-agent": "okhttp/3.10.0.1",
            "passport-sdk-version": "19",
        }

        return headers

    def __get_challenge(self) -> dict:
        params = self.__params()

        req = self.__client.get(
            url=(
                "https://"
                + self.__host
                + "/captcha/get?"
                + params
            ),
            headers=self.__headers()
        )

        return req.json()

    def __solve_captcha(self, url_1: str, url_2: str) -> dict:
        puzzle = base64.b64encode(
            self.__client.get(
                url_1,
            ).content
        )
        piece = base64.b64encode(
            self.__client.get(
                url_2,
            ).content
        )

        solver = PuzzleSolver(puzzle, piece)
        maxloc = solver.get_position()
        randlength = round(
            random.random() * (100 - 50) + 50
        )
        time.sleep(1)
        return {
            "maxloc": maxloc,
            "randlenght": randlength
        }

    def __post_captcha(self, solve: dict) -> dict:
        params = self.__params()

        body = {
            "modified_img_width": 552,
            "id": solve["id"],
            "mode": "slide",
            "reply": list(
                {
                    "relative_time": i * solve["randlenght"],
                    "x": round(
                        solve["maxloc"] / (solve["randlenght"] / (i + 1))
                    ),
                    "y": solve["tip"],
                }
                for i in range(
                    solve["randlenght"]
                )
            ),
        }

        headers = self.__headers()

        req = self.__client.post(
            url=(
                "https://"
                + self.__host
                + "/captcha/verify?"
                + params
            ),
            headers=headers.update(
                {
                    "content-type": "application/json"
                }
            ),
            json=body
        )

        return req.json()

    def solve_captcha(self):
        __captcha_challenge = self.__get_challenge()

        __captcha_id = __captcha_challenge["data"]["id"]
        __tip_y = __captcha_challenge["data"]["question"]["tip_y"]

        solve = self.__solve_captcha(
            __captcha_challenge["data"]["question"]["url1"],
            __captcha_challenge["data"]["question"]["url2"],
        )

        solve.update(
            {
                "id": __captcha_id,
                "tip": __tip_y
            }
        )

        return self.__post_captcha(solve)
