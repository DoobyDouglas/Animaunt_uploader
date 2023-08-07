class Anime:
    def __init__(
            self,
            name,
            number,
            animaunt_link=None,
            findanime_link=None,
            anime_365_link=None,
            path=None,
            ) -> None:
        self.name = name
        self.number = number
        self.animaunt_link = animaunt_link
        self.findanime_link = findanime_link
        self.anime_365_link = anime_365_link
        self.path = path
        self.link = None
        self.file = None
        self.resilt_link = None

    def __str__(self) -> str:
        return self.name


class Dorama:
    def __init__(
            self,
            name,
            number,
            malfurik_link=None,
            ) -> None:
        self.name = name
        self.number = number
        self.malfurik_link = malfurik_link
        self.doramatv_link = None
        self.link = None
        self.resilt_link = None

    def __str__(self) -> str:
        return self.name
