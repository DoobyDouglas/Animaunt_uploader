class Episode:

    __slots__ = ('__name', '__number', '__link', '__result_link')

    def __init__(self, name, number) -> None:
        self.__name = name
        self.__number = number
        self.__link = None
        self.__result_link = None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def number(self) -> str:
        return self.__number

    @property
    def link(self) -> str:
        return self.__link

    @link.setter
    def link(self, link: str) -> None:
        self.__link = link

    @property
    def result_link(self) -> str:
        return self.__result_link

    @result_link.setter
    def result_link(self, result_link) -> None:
        self.__result_link = result_link

    def __str__(self) -> str:
        return f'{self.name} --> {self.number}'

    def __repr__(self) -> str:
        return self.__str__()


class Anime(Episode):

    __slots__ = (
        'animaunt_link',
        'findanime_link',
        'anime_365_link',
        'path',
        '__file',
    )

    def __init__(
            self,
            name,
            number,
            animaunt_link=None,
            findanime_link=None,
            anime_365_link=None,
            path=None,
            ) -> None:
        super().__init__(name, number)
        self.animaunt_link = animaunt_link
        self.findanime_link = findanime_link
        self.anime_365_link = anime_365_link
        self.path = path
        self.__file = None

    @property
    def file(self) -> str:
        return self.__file

    @file.setter
    def file(self, file: str) -> None:
        self.__file = file


class Dorama(Episode):

    __slots__ = (
        'malfurik_link',
        'doramatv_link',
    )

    def __init__(
            self,
            name,
            number,
            malfurik_link=None,
            doramatv_link=None,
            ) -> None:
        super().__init__(name, number)
        self.malfurik_link = malfurik_link
        self.doramatv_link = doramatv_link
