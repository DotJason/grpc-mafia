from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

ALIVE: Status
CIVILIAN: Role
CIVILIAN_WIN: GameStatus
DAY: GameStatus
DESCRIPTOR: _descriptor.FileDescriptor
GHOST: Status
MAFIA: Role
MAFIA_WIN: GameStatus
NIGHT: GameStatus
NONE: Role
SHERIFF: Role

class DisconnectResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetGameStatusResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: GameStatus
    def __init__(self, status: _Optional[_Union[GameStatus, str]] = ...) -> None: ...

class GetLastRevealedResponse(_message.Message):
    __slots__ = ["has_been_revealed", "player_id"]
    HAS_BEEN_REVEALED_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    has_been_revealed: bool
    player_id: int
    def __init__(self, player_id: _Optional[int] = ..., has_been_revealed: bool = ...) -> None: ...

class GetSessionResponse(_message.Message):
    __slots__ = ["is_session_present", "player_id", "role", "session_id"]
    IS_SESSION_PRESENT_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    is_session_present: bool
    player_id: int
    role: Role
    session_id: int
    def __init__(self, session_id: _Optional[int] = ..., is_session_present: bool = ..., player_id: _Optional[int] = ..., role: _Optional[_Union[Role, str]] = ...) -> None: ...

class MafiaActionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Player(_message.Message):
    __slots__ = ["is_role_revealed", "role", "status", "username"]
    IS_ROLE_REVEALED_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    is_role_revealed: bool
    role: Role
    status: Status
    username: str
    def __init__(self, username: _Optional[str] = ..., role: _Optional[_Union[Role, str]] = ..., status: _Optional[_Union[Status, str]] = ..., is_role_revealed: bool = ...) -> None: ...

class SheriffActionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SheriffRevealResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TargetRequest(_message.Message):
    __slots__ = ["source_user_id", "target_player_id"]
    SOURCE_USER_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    source_user_id: int
    target_player_id: int
    def __init__(self, source_user_id: _Optional[int] = ..., target_player_id: _Optional[int] = ...) -> None: ...

class UserId(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class UserName(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class VoteEndDayResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class VoteResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class GameStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
