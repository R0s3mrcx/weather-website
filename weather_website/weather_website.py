import reflex as rx
import os
from dotenv import load_dotenv
import asyncio
import aiohttp

load_dotenv()

API_KEY: str = os.getenv("API_KEY")

css: dict = {
    "app": {"_dark": {"bg": "#1f2028"}},
    "main": {
        "width": "100%",
        "height": "100vh",
        "display": "flex",
        "flex_direction": "column",
        "align_items": "center",
        "justify_content": "center",
        "padding_top": "60px",
        "box_sizing": "border-box",
        "background_image": "url('/path_to_background_image.jpg')",
        "background_size": "cover",
        "background_position": "center",
    },
    "header": {
        "align_items": "center",
        "width": "100%",
        "height": "50px",
        "box_shadow": "0px 8px 16px 0px rgba(0,0,0,0.25)",
        "padding": "0 1rem",
        "position": "fixed",
        "top": "0",
        "_dark": {"bg": "#000000"},
        "_light": {"bg": "#ffffff"},
        "transition": "all 300ms ease",
    },
    "input": {
        "width": "82%",
        "height": "50px",
        "text_align": "center",
        "text_color": "white",
        "font_size": "20px",
        "transition": "all 600ms ease",
        "margin_bottom": "10px",
        "border_radius": "20px",
        "border_width": "0px",
        "background": "rgba(0, 0, 0, 0.5)",
    },
    "stack": {
        "width": "90%",
        "max_width": "600px",
        "align_items": "center",
        "justify_content": "center",
        "display": "flex",
        "flex_direction": "column",
        "padding_top": "4em",
        "border_radius": "10px",
        "padding": "20px",
    },
    "content": {
        "width": "100%",
        "max_width": "460px",
        "transition": "all 300ms ease",
        "border_radius": "10px",
        "justify_content": "center",
        "display": "flex",
        "overflow": "hidden",
        "box_shadow": "0px 10px 20px 0px rgba(0,0,0,0.5)",
        "height": "auto",
        "padding": "0",
        "flex_direction": "column",
        "align_items": "center",
        "color": "white",
    },
    "stat_container": {
        "display": "flex",
        "flex_direction": "column",
        "align_items": "center",
        "justify_content": "center",
        "flex": "1",
        "background": "transparent",
    },
    "stat_heading": {
        "font_size": "20px",
        "margin": "0",
    },
    "stat_text": {
        "font_size": "12px",
        "font_weight": "bold",
        "opacity": "0.6",
        "margin": "0",
    },
    "media_queries": {
        "@media screen and (max-width: 768px)": {
            "content": {
                "flex_direction": "column",
                "height": "auto",
            },
            "input": {
                "width": "100%",
                "height": "40px",
                "font_size": "20px",
                "text_align": "center",
                "align_items": "center",
                "margin_bottom": "10px",
            },
            "stat_heading": {
                "font_size": "18px",
            },
            "stat_text": {
                "font_size": "10px",
            },
        },
        "@media screen and (max-width: 480px)": {
            "header": {
                "font_size": "16px",
            },
            "input": {
                "height": "35px",
                "font_size": "20px",
            },
            "stat_heading": {
                "font_size": "16px",
            },
            "stat_text": {
                "font_size": "9px",
            },
        },
    },
}


class State(rx.State):
    location: str = ""
    city: str = ""
    country: str = ""
    temp: str = ""
    speed: str = ""
    humidity: str = ""
    image_src: str = "/search-icon-png-5.png"
    user_input: str = ""
    content_height: str = "0px"
    content_bg: str = "rgba(0, 0, 0, 0.5)"

    def get_input_value(self, user_input: str) -> None:
        self.user_input = user_input
        if self.user_input:
            self.expand_content_height()
            self.image_src = "/search-icon-png-5.png"
        else:
            self.collapse_content_height()

    async def route_after_key_press(self, key: str) -> None:
        if key == "Enter" and self.user_input:
            self.expand_content_height()
            await self.give_content_bg()
            await self.get_weather_data()
            self.content_bg = "rgba(0, 0, 0, 0.5)"

    async def give_content_bg(self) -> None:
        await asyncio.sleep(0.75)
        if self.content_bg != "rgba(0, 0, 0, 0.5)":
            self.content_bg = "rgba(0, 0, 0, 0.5)"

    def expand_content_height(self) -> None:
        if self.content_height != "auto":
            self.content_height = "auto"

    def collapse_content_height(self) -> None:
        if self.content_height != "0px":
            self.content_height = "0px"
            self.content_bg = "rgba(0, 0, 0, 0.5)"

    async def get_weather_data(self):
        __city__: str = self.user_input
        async with aiohttp.ClientSession() as session:
            async with session.get(get_weather_request(__city__)) as response:
                if response.status == 200:
                    data = await response.json()
                    self.content_bg = "rgba(0, 0, 0, 0.75)"
                    self.city = __city__
                    self.country = data["sys"]["country"]
                    self.temp = f"{int(data['main']['temp'])}°C"
                    self.humidity = f"{int(data['main']['humidity'])}%"
                    self.speed = f"{int(data['wind']['speed'])} km/h"

                    self.location = f"{self.city.capitalize()}, {self.country}"

                    weather_main = data["weather"][0]["main"].lower()
                    if weather_main in ["clear", "sun"]:
                        self.image_src = "/sun.png"
                    elif weather_main in ["cloud", "clouds"]:
                        self.image_src = "/cloud.png"
                    else:
                        self.image_src = "/rain.png"

                    self.user_input = ""


def get_weather_request(city: str) -> str:
    return f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"


def Header() -> rx.Component:
    return rx.hstack(
        rx.heading("Weather Online", size="md"),
        rx.spacer(),
        rx.button(
            rx.color_mode_cond(
                rx.icon("moon", color="black", stroke_width=2.5),
                rx.icon("sun", color="white", stroke_width=2.5)
            ),
            on_click=rx.toggle_color_mode,
            style={"background": "none", "border": "none"}
        ),
        style=css.get("header")
    )


def index() -> rx.Component:
    header: rx.Component = Header()

    return rx.vstack(
        header,
        rx.vstack(
            rx.input(
                placeholder="Enter a city name to get the weather",
                on_change=State.get_input_value,
                on_key_down=State.route_after_key_press,
                background="rgba(0, 0, 0, 0.5)",
                style=css.get("input"),
                value=State.user_input,
                variant="soft",
            ),
            style=css.get("stack"),
        ),
        rx.vstack(
            rx.container(
                rx.vstack(
                    rx.image(
                        src=State.image_src,
                        height="80px",
                        width="80px"
                    ),
                    rx.heading(State.location, size="md"),
                    spacing="0",
                    width="100%",
                    height="inherit",
                    display="flex",
                    align_items="center",
                    justify_content="center"
                ),
                style=css.get("left_container"),
            ),
            rx.container(
                rx.stack(
                    rx.container(
                        rx.heading(State.temp, style=css.get("stat_heading")),
                        rx.text("TEMP", style=css.get("stat_text")),
                        style=css.get("stat_container")
                    ),
                    rx.container(
                        rx.heading(State.speed, style=css.get("stat_heading")),
                        rx.text("SPEED", style=css.get("stat_text")),
                        style=css.get("stat_container")
                    ),
                    rx.container(
                        rx.heading(State.humidity, style=css.get("stat_heading")),
                        rx.text("HUMIDITY", style=css.get("stat_text")),
                        style=css.get("stat_container")
                    ),
                    style=css.get("right_container"),
                ),
                style=css.get("content"),
            ),
            style={**css.get("content"), "height": State.content_height, "background": State.content_bg},
        ),
        style=css.get("main"),
    )


app = rx.App()
app.add_page(index)
app._compile()