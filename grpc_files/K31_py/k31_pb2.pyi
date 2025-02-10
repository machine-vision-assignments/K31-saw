from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProductionData(_message.Message):
    __slots__ = ("WD", "P1", "P2", "DropOffRampPos")
    class EOperation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OP_NOOP: _ClassVar[ProductionData.EOperation]
        OP_BLINDDETECT: _ClassVar[ProductionData.EOperation]
        OP_ROLLIN: _ClassVar[ProductionData.EOperation]
        OP_POS_DIV: _ClassVar[ProductionData.EOperation]
        OP_POS_FRONT_FORW: _ClassVar[ProductionData.EOperation]
        OP_POS_FRONT_BACKW: _ClassVar[ProductionData.EOperation]
        OP_POS_BACK: _ClassVar[ProductionData.EOperation]
        OP_CUT_DIV: _ClassVar[ProductionData.EOperation]
        OP_CUT_FRONT: _ClassVar[ProductionData.EOperation]
        OP_CUT_BACK: _ClassVar[ProductionData.EOperation]
    OP_NOOP: ProductionData.EOperation
    OP_BLINDDETECT: ProductionData.EOperation
    OP_ROLLIN: ProductionData.EOperation
    OP_POS_DIV: ProductionData.EOperation
    OP_POS_FRONT_FORW: ProductionData.EOperation
    OP_POS_FRONT_BACKW: ProductionData.EOperation
    OP_POS_BACK: ProductionData.EOperation
    OP_CUT_DIV: ProductionData.EOperation
    OP_CUT_FRONT: ProductionData.EOperation
    OP_CUT_BACK: ProductionData.EOperation
    class PilaData(_message.Message):
        __slots__ = ("Production", "RoundProfile", "Size", "Position", "Speed", "Operation", "SawDown", "SawUp", "AutoMode")
        PRODUCTION_FIELD_NUMBER: _ClassVar[int]
        ROUNDPROFILE_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        SPEED_FIELD_NUMBER: _ClassVar[int]
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        SAWDOWN_FIELD_NUMBER: _ClassVar[int]
        SAWUP_FIELD_NUMBER: _ClassVar[int]
        AUTOMODE_FIELD_NUMBER: _ClassVar[int]
        Production: bool
        RoundProfile: bool
        Size: float
        Position: float
        Speed: float
        Operation: ProductionData.EOperation
        SawDown: bool
        SawUp: bool
        AutoMode: bool
        def __init__(self, Production: bool = ..., RoundProfile: bool = ..., Size: _Optional[float] = ..., Position: _Optional[float] = ..., Speed: _Optional[float] = ..., Operation: _Optional[_Union[ProductionData.EOperation, str]] = ..., SawDown: bool = ..., SawUp: bool = ..., AutoMode: bool = ...) -> None: ...
    WD_FIELD_NUMBER: _ClassVar[int]
    P1_FIELD_NUMBER: _ClassVar[int]
    P2_FIELD_NUMBER: _ClassVar[int]
    DROPOFFRAMPPOS_FIELD_NUMBER: _ClassVar[int]
    WD: int
    P1: ProductionData.PilaData
    P2: ProductionData.PilaData
    DropOffRampPos: float
    def __init__(self, WD: _Optional[int] = ..., P1: _Optional[_Union[ProductionData.PilaData, _Mapping]] = ..., P2: _Optional[_Union[ProductionData.PilaData, _Mapping]] = ..., DropOffRampPos: _Optional[float] = ...) -> None: ...

class SituationData(_message.Message):
    __slots__ = ("WD", "P1", "P2")
    class EStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STAT_NODETECT: _ClassVar[SituationData.EStatus]
        STAT_PARTIAL_FRONT: _ClassVar[SituationData.EStatus]
        STAT_PARTIAL_BACK: _ClassVar[SituationData.EStatus]
        STAT_FULL: _ClassVar[SituationData.EStatus]
        STAT_FULL_2SPLIT: _ClassVar[SituationData.EStatus]
    STAT_NODETECT: SituationData.EStatus
    STAT_PARTIAL_FRONT: SituationData.EStatus
    STAT_PARTIAL_BACK: SituationData.EStatus
    STAT_FULL: SituationData.EStatus
    STAT_FULL_2SPLIT: SituationData.EStatus
    class DetData(_message.Message):
        __slots__ = ("PosFront", "PosBack", "Status", "DropOff", "Certainty", "DetInFront", "DetInBack")
        POSFRONT_FIELD_NUMBER: _ClassVar[int]
        POSBACK_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        DROPOFF_FIELD_NUMBER: _ClassVar[int]
        CERTAINTY_FIELD_NUMBER: _ClassVar[int]
        DETINFRONT_FIELD_NUMBER: _ClassVar[int]
        DETINBACK_FIELD_NUMBER: _ClassVar[int]
        PosFront: float
        PosBack: float
        Status: SituationData.EStatus
        DropOff: bool
        Certainty: float
        DetInFront: bool
        DetInBack: bool
        def __init__(self, PosFront: _Optional[float] = ..., PosBack: _Optional[float] = ..., Status: _Optional[_Union[SituationData.EStatus, str]] = ..., DropOff: bool = ..., Certainty: _Optional[float] = ..., DetInFront: bool = ..., DetInBack: bool = ...) -> None: ...
    WD_FIELD_NUMBER: _ClassVar[int]
    P1_FIELD_NUMBER: _ClassVar[int]
    P2_FIELD_NUMBER: _ClassVar[int]
    WD: int
    P1: SituationData.DetData
    P2: SituationData.DetData
    def __init__(self, WD: _Optional[int] = ..., P1: _Optional[_Union[SituationData.DetData, _Mapping]] = ..., P2: _Optional[_Union[SituationData.DetData, _Mapping]] = ...) -> None: ...

class CaptureFilter(_message.Message):
    __slots__ = ("Filter",)
    class ECaptureFilter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CF_ALL: _ClassVar[CaptureFilter.ECaptureFilter]
        CF_Z1: _ClassVar[CaptureFilter.ECaptureFilter]
        CF_Z2: _ClassVar[CaptureFilter.ECaptureFilter]
        CF_Z3: _ClassVar[CaptureFilter.ECaptureFilter]
    CF_ALL: CaptureFilter.ECaptureFilter
    CF_Z1: CaptureFilter.ECaptureFilter
    CF_Z2: CaptureFilter.ECaptureFilter
    CF_Z3: CaptureFilter.ECaptureFilter
    FILTER_FIELD_NUMBER: _ClassVar[int]
    Filter: CaptureFilter.ECaptureFilter
    def __init__(self, Filter: _Optional[_Union[CaptureFilter.ECaptureFilter, str]] = ...) -> None: ...

class CaptureSignal(_message.Message):
    __slots__ = ("IdCapture", "IdKus", "Marker", "RefLine1", "RefLine2")
    IDCAPTURE_FIELD_NUMBER: _ClassVar[int]
    IDKUS_FIELD_NUMBER: _ClassVar[int]
    MARKER_FIELD_NUMBER: _ClassVar[int]
    REFLINE1_FIELD_NUMBER: _ClassVar[int]
    REFLINE2_FIELD_NUMBER: _ClassVar[int]
    IdCapture: int
    IdKus: int
    Marker: int
    RefLine1: str
    RefLine2: str
    def __init__(self, IdCapture: _Optional[int] = ..., IdKus: _Optional[int] = ..., Marker: _Optional[int] = ..., RefLine1: _Optional[str] = ..., RefLine2: _Optional[str] = ...) -> None: ...

class OcrResult(_message.Message):
    __slots__ = ("IdCapture", "IdKus", "ResultLine1", "ResultLine2", "Result", "ResultStr", "LogoStatus")
    class EMarkingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MRK_NONE: _ClassVar[OcrResult.EMarkingStatus]
        MRK_OK: _ClassVar[OcrResult.EMarkingStatus]
        MRK_WRONG: _ClassVar[OcrResult.EMarkingStatus]
        MRK_PART: _ClassVar[OcrResult.EMarkingStatus]
        MRK_DEFORMED: _ClassVar[OcrResult.EMarkingStatus]
        MRK_CAM: _ClassVar[OcrResult.EMarkingStatus]
        MRK_BLUR: _ClassVar[OcrResult.EMarkingStatus]
        MRK_ERROR: _ClassVar[OcrResult.EMarkingStatus]
    MRK_NONE: OcrResult.EMarkingStatus
    MRK_OK: OcrResult.EMarkingStatus
    MRK_WRONG: OcrResult.EMarkingStatus
    MRK_PART: OcrResult.EMarkingStatus
    MRK_DEFORMED: OcrResult.EMarkingStatus
    MRK_CAM: OcrResult.EMarkingStatus
    MRK_BLUR: OcrResult.EMarkingStatus
    MRK_ERROR: OcrResult.EMarkingStatus
    class ELogoStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LG_NONE: _ClassVar[OcrResult.ELogoStatus]
        LG_Part: _ClassVar[OcrResult.ELogoStatus]
        LG_FULL: _ClassVar[OcrResult.ELogoStatus]
    LG_NONE: OcrResult.ELogoStatus
    LG_Part: OcrResult.ELogoStatus
    LG_FULL: OcrResult.ELogoStatus
    IDCAPTURE_FIELD_NUMBER: _ClassVar[int]
    IDKUS_FIELD_NUMBER: _ClassVar[int]
    RESULTLINE1_FIELD_NUMBER: _ClassVar[int]
    RESULTLINE2_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RESULTSTR_FIELD_NUMBER: _ClassVar[int]
    LOGOSTATUS_FIELD_NUMBER: _ClassVar[int]
    IdCapture: int
    IdKus: int
    ResultLine1: str
    ResultLine2: str
    Result: OcrResult.EMarkingStatus
    ResultStr: str
    LogoStatus: OcrResult.ELogoStatus
    def __init__(self, IdCapture: _Optional[int] = ..., IdKus: _Optional[int] = ..., ResultLine1: _Optional[str] = ..., ResultLine2: _Optional[str] = ..., Result: _Optional[_Union[OcrResult.EMarkingStatus, str]] = ..., ResultStr: _Optional[str] = ..., LogoStatus: _Optional[_Union[OcrResult.ELogoStatus, str]] = ...) -> None: ...
