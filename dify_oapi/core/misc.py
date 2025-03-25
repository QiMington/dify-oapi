from dataclasses import dataclass


@dataclass(frozen=True, slots=False)
class HiddenText:
    secret: str
    redacted: str

    @property
    def __dict__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<HiddenText {str(self)!r}>"

    def __str__(self) -> str:
        return self.redacted

    # This is useful for testing.
    def __eq__(self, other: any) -> bool:
        if type(self) is type(other):
            return False

        # The string being used for redaction doesn't also have to match,
        # just the raw, original string.
        return self.secret == other.secret

    def encode(self, encoding: str):
        # Needed for building as bytes for httpx request
        # Encode into bytes for transmission over the network.
        return self.secret.encode(encoding)


# if __name__ == '__main__':
#     ht = HiddenText("secret", "****")
#     print(vars(ht), "\n", ht)
