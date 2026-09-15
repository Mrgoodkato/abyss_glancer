# System-safe status dictionary with ANSI coloring
STATUS = {
    # Core Operations
    "success": {"symbol": "\u2713", "color": "\033[92m", "label": "OK"},    # Green  ✓
    "error":   {"symbol": "\u2717", "color": "\033[91m", "label": "FAIL"},  # Red    ✗
    "waiting": {"symbol": "\u29D6", "color": "\033[93m", "label": "WAIT"},  # Yellow ⧖
    "skipped": {"symbol": "\u229D", "color": "\033[90m", "label": "SKIP"},  # Gray   ⊝
    
    # Extended Operations
    "info":    {"symbol": "\u2139", "color": "\033[94m", "label": "INFO"},  # Blue   ℹ
    "warn":    {"symbol": "\u26A0", "color": "\033[93m", "label": "WARN"},  # Yellow ⚠
    "debug":   {"symbol": "\u2699", "color": "\033[95m", "label": "DBUG"},  # Magenta ⚙
    "pending": {"symbol": "\u25CB", "color": "\033[96m", "label": "PEND"},  # Cyan   ○
    "bullet":  {"symbol": "\u2022", "color": "\033[37m", "label": "ITEM"},  # White  •
    "arrow":   {"symbol": "\u279C", "color": "\033[94m", "label": "MOVE"},  # Blue   ➜
}

RESET = "\033[0m"

def logstat(key: str, use_symbols: bool = True) -> None:
    """Prints formatted log lines using symbols or label fallback."""
    item = STATUS.get(key, STATUS["info"])
    
    if use_symbols:
        stat_symbol = f"{item['color']}{item['symbol']}{RESET}"
    else:
        # Fallback for plain text files or raw logs
        stat_symbol = f"{item['color']}[{item['label']:^4}]{RESET}"
        
    return f"{stat_symbol}"