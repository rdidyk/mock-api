import attr


@attr.s
class Route:
    uri = attr.ib()
    view = attr.ib()
    methods = attr.ib(default=None)
    name = attr.ib(default=None)
