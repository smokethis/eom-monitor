# Centralised UI tokens

class Theme:
    # Colours
    BG = "bg-slate-950"
    SURFACE = "bg-slate-900"
    SURFACE_ALT = "bg-slate-800"

    TEXT = "text-slate-100"
    TEXT_MUTED = "text-slate-400"
    TEXT_SUBTLE = "text-slate-500"

    BORDER = "border border-slate-700"

    PRIMARY = "text-blue-400"
    SUCCESS = "text-emerald-400"
    WARNING = "text-amber-400"
    ERROR = "text-red-400"

    # Typography
    TITLE = "text-2xl font-semibold"
    HEADING = "text-lg font-medium"
    LABEL = "text-sm font-medium"
    BODY = "text-base"
    SMALL = "text-sm"

    # Layout
    CARD = (
        "rounded-xl "
        "p-4 "
        "shadow-md "
        "bg-slate-900 "
        "border border-slate-700"
    )

    CARD_HOVER = (
        "hover:border-slate-500 "
        "transition-colors"
    )

    INPUT = (
        "bg-slate-800 "
        "border border-slate-700 "
        "rounded-lg"
    )

    BUTTON = (
        "rounded-lg "
        "px-4 py-2 "
        "font-medium"
    )

    TITLE_BAR = (
        "w-full "
        "bg-slate-800 "
        "border-b border-slate-700 "
        "px-6 py-4"
    )