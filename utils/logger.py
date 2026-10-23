"""
utils/logger.py
Standardized console logger with ANSI color coding and no emojis.
"""

from colorama import init, Fore, Style

init(autoreset=True)


class ConsoleLogger:
    @staticmethod
    def success(message: str) -> None:
        """Prints a success message in green."""
        print(f"{Fore.GREEN}{Style.BRIGHT}[+]{Style.RESET_ALL} {message}")

    @staticmethod
    def failure(message: str) -> None:
        """Prints a failure/alert message in red."""
        print(f"{Fore.RED}{Style.BRIGHT}[-]{Style.RESET_ALL} {message}")

    @staticmethod
    def info(message: str) -> None:
        """Prints an informational status in cyan."""
        print(f"{Fore.CYAN}{Style.BRIGHT}[*]{Style.RESET_ALL} {message}")

    @staticmethod
    def warning(message: str) -> None:
        """Prints a warning message in yellow."""
        print(f"{Fore.YELLOW}{Style.BRIGHT}[!]{Style.RESET_ALL} {message}")

    @staticmethod
    def header(title: str) -> None:
        """Prints a structured section banner."""
        border = "=" * 70
        print(f"\n{Fore.LIGHTBLACK_EX}{border}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{Style.BRIGHT}{title.center(70)}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{border}{Style.RESET_ALL}\n")