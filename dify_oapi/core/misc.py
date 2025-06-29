from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=False)
class HiddenText(str):
    secret: str
    redacted: str

    def __new__(cls, secret: str, redacted: str):
        obj = super().__new__(cls, redacted)
        return obj

    @property
    def __dict__(self):  # type: ignore[override]
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<HiddenText {str(self)!r}>"

    def __str__(self) -> str:
        return self.redacted

    # This is useful for testing.
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False

        # The string being used for redaction doesn't also have to match,
        # just the raw, original string.
        return self.secret == other.secret

    def encode(self, encoding="utf-8", errors="strict"):
        # Needed for building as bytes for httpx request
        # Encode into bytes for transmission over the network.
        return self.secret.encode(encoding, errors)


# if __name__ == '__main__':
#     ht = HiddenText("secret", "****")
#     print(vars(ht), "\n", ht)
